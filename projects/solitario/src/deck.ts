import type { Card, Rank, Suit, Pile } from './types.js'

const SUITS: Suit[] = ['hearts', 'diamonds', 'clubs', 'spades']
const RANKS: Rank[] = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

export function createDeck(): Card[] {
  const deck: Card[] = []
  let id = 0
  for (const suit of SUITS) {
    for (let i = 0; i < RANKS.length; i++) {
      const rank = RANKS[i]
      deck.push({
        suit,
        rank,
        value: i + 1,
        faceUp: false,
        id: `${suit}-${rank}-${id++}`,
      })
    }
  }
  return deck
}

export function shuffle<T>(array: T[]): T[] {
  const copy = [...array]
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[copy[i], copy[j]] = [copy[j], copy[i]]
  }
  return copy
}

export function isRed(card: Card): boolean {
  return card.suit === 'hearts' || card.suit === 'diamonds'
}

export function cloneCard(card: Card): Card {
  return { ...card }
}

export function clonePile(pile: Pile): Pile {
  return {
    ...pile,
    cards: pile.cards.map(cloneCard),
  }
}

export function clonePiles(piles: Pile[]): Pile[] {
  return piles.map(clonePile)
}
