import type { Card, Pile, DragState } from './types.js'
import { createDeck, shuffle, isRed, clonePiles } from './deck.js'
import { audio } from './audio.js'
import {
  CARD_WIDTH,
  CARD_HEIGHT,
  CARD_OFFSET_Y,
  PILE_GAP_X,
  PILE_GAP_Y,
  resizeCanvas,
  drawPile,
  drawDrag,
} from './render.js'

const NUM_TABLEAUS = 7
const NUM_FOUNDATIONS = 4

export class SolitaireGame {
  canvas: HTMLCanvasElement
  ctx: CanvasRenderingContext2D
  piles: Pile[] = []
  history: Pile[][] = []
  drag: DragState = {
    active: false,
    cards: [],
    sourcePileIndex: -1,
    offsetX: 0,
    offsetY: 0,
    x: 0,
    y: 0,
  }
  lastTapTime = 0
  lastTapX = 0
  lastTapY = 0

  constructor(canvas: HTMLCanvasElement) {
    this.canvas = canvas
    this.ctx = resizeCanvas()
    this.newGame()
    this.bindInput()
    window.addEventListener('resize', () => this.render())
  }

  newGame(): void {
    this.hideVictory()
    this.history = []
    const deck = shuffle(createDeck())
    const stockCards: Card[] = []

    // Tableau piles: indices 0-6
    this.piles = []
    for (let i = 0; i < NUM_TABLEAUS; i++) {
      const cards: Card[] = []
      for (let j = 0; j <= i; j++) {
        const card = deck.pop()!
        card.faceUp = j === i
        cards.push(card)
      }
      this.piles.push({
        cards,
        type: 'tableau',
        index: i,
        x: 0,
        y: 0,
      })
    }

    // Stock: index 7
    while (deck.length > 0) {
      const card = deck.pop()!
      card.faceUp = false
      stockCards.push(card)
    }
    this.piles.push({
      cards: stockCards,
      type: 'stock',
      index: NUM_TABLEAUS,
      x: 0,
      y: 0,
    })

    // Waste: index 8
    this.piles.push({
      cards: [],
      type: 'waste',
      index: NUM_TABLEAUS + 1,
      x: 0,
      y: 0,
    })

    // Foundations: indices 9-12
    for (let i = 0; i < NUM_FOUNDATIONS; i++) {
      this.piles.push({
        cards: [],
        type: 'foundation',
        index: i,
        x: 0,
        y: 0,
      })
    }

    audio.playDeal()
    this.layout()
    this.render()
  }

  layout(): void {
    const margin = PILE_GAP_X
    const startX = margin
    const startY = PILE_GAP_Y

    for (let i = 0; i < NUM_TABLEAUS; i++) {
      this.piles[i].x = startX + i * (CARD_WIDTH + PILE_GAP_X)
      this.piles[i].y = startY + CARD_HEIGHT + PILE_GAP_Y
    }

    this.piles[NUM_TABLEAUS].x = startX
    this.piles[NUM_TABLEAUS].y = startY
    this.piles[NUM_TABLEAUS + 1].x = startX + CARD_WIDTH + PILE_GAP_X
    this.piles[NUM_TABLEAUS + 1].y = startY

    for (let i = 0; i < NUM_FOUNDATIONS; i++) {
      this.piles[NUM_TABLEAUS + 2 + i].x =
        startX + (3 + i) * (CARD_WIDTH + PILE_GAP_X)
      this.piles[NUM_TABLEAUS + 2 + i].y = startY
    }
  }

  bindInput(): void {
    const onDown = (e: PointerEvent) => {
      e.preventDefault()
      audio.enable()
      const { x, y } = this.getPointerPos(e)

      const now = performance.now()
      const timeSinceLastTap = now - this.lastTapTime
      const distance = Math.hypot(x - this.lastTapX, y - this.lastTapY)
      if (timeSinceLastTap < 300 && distance < 30) {
        // Double tap
        if (this.tryAutoMove(x, y)) {
          this.lastTapTime = 0
          return
        }
      }
      this.lastTapTime = now
      this.lastTapX = x
      this.lastTapY = y

      this.onPointerDown(x, y)
    }

    const onMove = (e: PointerEvent) => {
      e.preventDefault()
      const { x, y } = this.getPointerPos(e)
      this.onPointerMove(x, y)
    }

    const onUp = (e: PointerEvent) => {
      e.preventDefault()
      const { x, y } = this.getPointerPos(e)
      this.onPointerUp(x, y)
    }

    this.canvas.addEventListener('pointerdown', onDown)
    this.canvas.addEventListener('pointermove', onMove)
    this.canvas.addEventListener('pointerup', onUp)
    this.canvas.addEventListener('pointercancel', onUp)

    document.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'z') {
        e.preventDefault()
        this.undo()
      }
    })
  }

  getPointerPos(e: PointerEvent): { x: number; y: number } {
    const rect = this.canvas.getBoundingClientRect()
    return {
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
    }
  }

  onPointerDown(x: number, y: number): void {
    const hit = this.hitTest(x, y)
    if (!hit) {
      // Click on stock to draw
      const stock = this.piles[NUM_TABLEAUS]
      if (this.pointInPile(x, y, stock)) {
        this.drawFromStock()
        this.render()
      }
      return
    }

    const pile = this.piles[hit.pileIndex]
    const cardIndex = hit.cardIndex

    if (pile.type === 'stock') {
      this.drawFromStock()
      this.render()
      return
    }

    if (pile.type === 'waste') {
      const card = pile.cards[pile.cards.length - 1]
      this.startDrag(pile, [card], x, y, cardIndex)
      return
    }

    if (pile.type === 'foundation') {
      const card = pile.cards[pile.cards.length - 1]
      this.startDrag(pile, [card], x, y, cardIndex)
      return
    }

    if (pile.type === 'tableau') {
      // Can drag from any face-up card to the bottom
      const cards = pile.cards.slice(cardIndex)
      if (cards.length > 0 && cards[0].faceUp) {
        this.startDrag(pile, cards, x, y, cardIndex)
      }
    }
  }

  startDrag(
    pile: Pile,
    cards: Card[],
    x: number,
    y: number,
    cardIndex: number,
  ): void {
    const offsetY = pile.type === 'tableau' ? cardIndex * CARD_OFFSET_Y : 0
    this.drag = {
      active: true,
      cards,
      sourcePileIndex: pile.index,
      offsetX: x - pile.x,
      offsetY: y - (pile.y + offsetY),
      x: pile.x,
      y: pile.y + offsetY,
    }
    this.render()
  }

  onPointerMove(x: number, y: number): void {
    if (!this.drag.active) return
    this.drag.x = x - this.drag.offsetX
    this.drag.y = y - this.drag.offsetY
    this.render()
  }

  onPointerUp(x: number, y: number): void {
    if (!this.drag.active) return

    const sourcePile = this.piles[this.drag.sourcePileIndex]
    const targetPile = this.findDropTarget(x, y, sourcePile)

    if (targetPile && this.canDrop(this.drag.cards, targetPile)) {
      // Save state before move
      this.saveHistory()

      // Move cards
      const cardsToMove = this.drag.cards
      sourcePiles(sourcePile, cardsToMove.length)
      targetPile.cards.push(...cardsToMove)
      this.flipTableauTop(sourcePile)
      audio.playPlace()
    }

    this.drag.active = false
    this.drag.cards = []
    this.drag.sourcePileIndex = -1
    this.checkVictory()
    this.render()
  }

  findDropTarget(x: number, y: number, source: Pile): Pile | null {
    // Check foundations first (top row)
    for (let i = NUM_TABLEAUS + 2; i < this.piles.length; i++) {
      const pile = this.piles[i]
      if (this.pointInPile(x, y, pile)) {
        return pile
      }
    }

    // Then tableaus
    for (let i = 0; i < NUM_TABLEAUS; i++) {
      const pile = this.piles[i]
      if (this.pointInPile(x, y, pile)) {
        if (pile.index !== source.index) return pile
      }
    }

    return null
  }

  canDrop(cards: Card[], target: Pile): boolean {
    if (cards.length === 0) return false
    const movingCard = cards[0]

    if (target.type === 'foundation') {
      // Only single card allowed to foundation
      if (cards.length > 1) return false
      const top = target.cards[target.cards.length - 1]
      if (!top) return movingCard.value === 1
      return top.suit === movingCard.suit && top.value === movingCard.value - 1
    }

    if (target.type === 'tableau') {
      const top = target.cards[target.cards.length - 1]
      if (!top) return movingCard.value === 13
      return (
        isRed(top) !== isRed(movingCard) &&
        top.value === movingCard.value + 1
      )
    }

    return false
  }

  pointInPile(x: number, y: number, pile: Pile): boolean {
    let h = CARD_HEIGHT
    if (pile.type === 'tableau' && pile.cards.length > 1) {
      h = CARD_HEIGHT + (pile.cards.length - 1) * CARD_OFFSET_Y
    }
    return x >= pile.x && x <= pile.x + CARD_WIDTH && y >= pile.y && y <= pile.y + h
  }

  hitTest(x: number, y: number): { pileIndex: number; cardIndex: number } | null {
    // Iterate from top-most visual elements to bottom
    for (let i = this.piles.length - 1; i >= 0; i--) {
      const pile = this.piles[i]
      if (!this.pointInPile(x, y, pile)) continue

      if (pile.cards.length === 0) return { pileIndex: i, cardIndex: -1 }

      if (pile.type === 'tableau') {
        // Find deepest face-up card under pointer
        for (let j = pile.cards.length - 1; j >= 0; j--) {
          const cardY = pile.y + j * CARD_OFFSET_Y
          if (y >= cardY && y <= cardY + CARD_HEIGHT) {
            if (pile.cards[j].faceUp) {
              return { pileIndex: i, cardIndex: j }
            }
            return null // Face-down card under pointer
          }
        }
        return null
      }

      // Waste/foundation: only top card
      if (pile.type === 'waste' || pile.type === 'foundation') {
        return { pileIndex: i, cardIndex: pile.cards.length - 1 }
      }

      // Stock
      if (pile.type === 'stock') {
        return { pileIndex: i, cardIndex: pile.cards.length - 1 }
      }
    }
    return null
  }

  drawFromStock(): void {
    this.saveHistory()
    const stock = this.piles[NUM_TABLEAUS]
    const waste = this.piles[NUM_TABLEAUS + 1]

    if (stock.cards.length === 0) {
      // Recycle waste back to stock
      while (waste.cards.length > 0) {
        const card = waste.cards.pop()!
        card.faceUp = false
        stock.cards.push(card)
      }
      audio.playPlace()
    } else {
      const card = stock.cards.pop()!
      card.faceUp = true
      waste.cards.push(card)
      audio.playFlip()
    }
  }

  saveHistory(): void {
    this.history.push(clonePiles(this.piles))
    if (this.history.length > 50) {
      this.history.shift()
    }
  }

  tryAutoMove(x: number, y: number): boolean {
    const hit = this.hitTest(x, y)
    if (!hit) return false

    const pile = this.piles[hit.pileIndex]
    if (pile.cards.length === 0) return false

    const cardIndex = hit.cardIndex
    const card = pile.cards[cardIndex]
    if (!card || !card.faceUp) return false

    // Only auto-move the single card (or top card of tableau sequence)
    const cardsToMove = pile.cards.slice(cardIndex)
    if (cardsToMove.length > 1) return false

    // Try foundation first
    for (let i = NUM_TABLEAUS + 2; i < this.piles.length; i++) {
      const target = this.piles[i]
      if (this.canDrop(cardsToMove, target)) {
        this.saveHistory()
        sourcePiles(pile, cardsToMove.length)
        target.cards.push(...cardsToMove)
        this.flipTableauTop(pile)
        audio.playPlace()
        this.render()
        this.checkVictory()
        return true
      }
    }

    // Then tableau
    for (let i = 0; i < NUM_TABLEAUS; i++) {
      const target = this.piles[i]
      if (target.index !== pile.index && this.canDrop(cardsToMove, target)) {
        this.saveHistory()
        sourcePiles(pile, cardsToMove.length)
        target.cards.push(...cardsToMove)
        this.flipTableauTop(pile)
        audio.playPlace()
        this.render()
        this.checkVictory()
        return true
      }
    }

    return false
  }

  checkVictory(): void {
    const foundations = this.piles.slice(NUM_TABLEAUS + 2)
    const totalInFoundations = foundations.reduce((sum, pile) => sum + pile.cards.length, 0)
    if (totalInFoundations === 52) {
      audio.playWin()
      this.showVictory()
    }
  }

  showVictory(): void {
    const el = document.getElementById('victory')
    if (el) el.classList.add('show')
  }

  hideVictory(): void {
    const el = document.getElementById('victory')
    if (el) el.classList.remove('show')
  }

  flipTableauTop(pile: Pile): void {
    if (
      pile.type === 'tableau' &&
      pile.cards.length > 0 &&
      !pile.cards[pile.cards.length - 1].faceUp
    ) {
      pile.cards[pile.cards.length - 1].faceUp = true
    }
  }

  undo(): void {
    if (this.history.length === 0) return
    this.piles = this.history.pop()!
    this.drag.active = false
    this.drag.cards = []
    this.drag.sourcePileIndex = -1
    this.layout()
    this.render()
  }

  render(): void {
    this.ctx = resizeCanvas()
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height)
    this.layout()

    for (const pile of this.piles) {
      drawPile(this.ctx, pile, this.drag.active ? this.drag.sourcePileIndex : null)
    }

    if (this.drag.active) {
      drawDrag(this.ctx, this.drag.cards, this.drag.x, this.drag.y)
    }
  }
}

function sourcePiles(pile: Pile, count: number): void {
  for (let i = 0; i < count; i++) {
    pile.cards.pop()
  }
}
