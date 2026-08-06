import type { Card, Pile } from './types.js'
import { isRed } from './deck.js'

export const CARD_WIDTH = 80
export const CARD_HEIGHT = 120
export const CARD_RADIUS = 6
export const CARD_OFFSET_Y = 28
export const PILE_GAP_X = 16
export const PILE_GAP_Y = 16

function getCanvas(): HTMLCanvasElement {
  const canvas = document.getElementById('game') as HTMLCanvasElement
  if (!canvas) throw new Error('Canvas not found')
  return canvas
}

export function resizeCanvas(): CanvasRenderingContext2D {
  const canvas = getCanvas()
  const ctx = canvas.getContext('2d')!
  const dpr = window.devicePixelRatio || 1
  const rect = canvas.getBoundingClientRect()
  canvas.width = rect.width * dpr
  canvas.height = rect.height * dpr
  ctx.scale(dpr, dpr)
  return ctx
}

export function drawRoundedRect(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  w: number,
  h: number,
  r: number,
): void {
  ctx.beginPath()
  ctx.moveTo(x + r, y)
  ctx.lineTo(x + w - r, y)
  ctx.quadraticCurveTo(x + w, y, x + w, y + r)
  ctx.lineTo(x + w, y + h - r)
  ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h)
  ctx.lineTo(x + r, y + h)
  ctx.quadraticCurveTo(x, y + h, x, y + h - r)
  ctx.lineTo(x, y + r)
  ctx.quadraticCurveTo(x, y, x + r, y)
  ctx.closePath()
}

export function drawEmptySlot(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  label?: string,
): void {
  ctx.save()
  ctx.strokeStyle = 'rgba(255,255,255,0.2)'
  ctx.lineWidth = 2
  drawRoundedRect(ctx, x, y, CARD_WIDTH, CARD_HEIGHT, CARD_RADIUS)
  ctx.stroke()
  if (label) {
    ctx.fillStyle = 'rgba(255,255,255,0.2)'
    ctx.font = 'bold 24px sans-serif'
    ctx.textAlign = 'center'
    ctx.textBaseline = 'middle'
    ctx.fillText(label, x + CARD_WIDTH / 2, y + CARD_HEIGHT / 2)
  }
  ctx.restore()
}

export function drawCard(
  ctx: CanvasRenderingContext2D,
  card: Card,
  x: number,
  y: number,
): void {
  ctx.save()
  drawRoundedRect(ctx, x, y, CARD_WIDTH, CARD_HEIGHT, CARD_RADIUS)
  ctx.fillStyle = card.faceUp ? '#f8f8f8' : '#2a4a36'
  ctx.fill()
  ctx.strokeStyle = '#1a2e22'
  ctx.lineWidth = 1
  ctx.stroke()

  if (card.faceUp) {
    ctx.fillStyle = isRed(card) ? '#b91c1c' : '#111827'
    ctx.font = 'bold 20px sans-serif'
    ctx.textAlign = 'left'
    ctx.textBaseline = 'top'
    ctx.fillText(card.rank, x + 6, y + 6)

    const suitSymbol = getSuitSymbol(card.suit)
    ctx.font = '24px sans-serif'
    ctx.fillText(suitSymbol, x + 6, y + 28)

    // Bottom-right inverted
    ctx.save()
    ctx.translate(x + CARD_WIDTH - 6, y + CARD_HEIGHT - 6)
    ctx.rotate(Math.PI)
    ctx.fillText(card.rank, 0, 0)
    ctx.fillText(suitSymbol, 0, 22)
    ctx.restore()
  } else {
    // Back pattern
    ctx.fillStyle = '#1e3d2a'
    drawRoundedRect(ctx, x + 3, y + 3, CARD_WIDTH - 6, CARD_HEIGHT - 6, 4)
    ctx.fill()
    ctx.strokeStyle = 'rgba(255,255,255,0.25)'
    ctx.lineWidth = 2
    ctx.stroke()

    // Cross-hatch pattern
    ctx.strokeStyle = 'rgba(255,255,255,0.08)'
    ctx.lineWidth = 1
    ctx.beginPath()
    for (let i = 10; i < CARD_WIDTH; i += 12) {
      ctx.moveTo(x + i, y + 4)
      ctx.lineTo(x + i, y + CARD_HEIGHT - 4)
    }
    for (let i = 10; i < CARD_HEIGHT; i += 12) {
      ctx.moveTo(x + 4, y + i)
      ctx.lineTo(x + CARD_WIDTH - 4, y + i)
    }
    ctx.stroke()
  }

  ctx.restore()
}

function getSuitSymbol(suit: string): string {
  switch (suit) {
    case 'hearts': return '♥'
    case 'diamonds': return '♦'
    case 'clubs': return '♣'
    case 'spades': return '♠'
    default: return '?'
  }
}

export function drawPile(
  ctx: CanvasRenderingContext2D,
  pile: Pile,
  dragSourceIndex: number | null,
): void {
  if (pile.cards.length === 0) {
    const label = getPileLabel(pile)
    drawEmptySlot(ctx, pile.x, pile.y, label)
    return
  }

  for (let i = 0; i < pile.cards.length; i++) {
    const card = pile.cards[i]
    const isDragged = dragSourceIndex === pile.index && i >= pile.cards.length - 1
    if (isDragged) continue

    const offsetY = pile.type === 'tableau' ? i * CARD_OFFSET_Y : 0
    drawCard(ctx, card, pile.x, pile.y + offsetY)
  }
}

function getPileLabel(pile: Pile): string | undefined {
  if (pile.type === 'stock') return '↻'
  if (pile.type === 'foundation') {
    const symbols: Record<string, string> = {
      hearts: '♥',
      diamonds: '♦',
      clubs: '♣',
      spades: '♠',
    }
    const suits = ['hearts', 'diamonds', 'clubs', 'spades']
    return symbols[suits[pile.index]] ?? '?'
  }
  return undefined
}

export function drawDrag(
  ctx: CanvasRenderingContext2D,
  cards: Card[],
  x: number,
  y: number,
): void {
  for (let i = 0; i < cards.length; i++) {
    drawCard(ctx, cards[i], x, y + i * CARD_OFFSET_Y)
  }
}
