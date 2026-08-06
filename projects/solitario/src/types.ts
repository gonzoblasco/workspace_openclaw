export type Suit = 'hearts' | 'diamonds' | 'clubs' | 'spades'
export type Rank = 'A' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '10' | 'J' | 'Q' | 'K'

export interface Card {
  suit: Suit
  rank: Rank
  value: number
  faceUp: boolean
  id: string
}

export interface Pile {
  cards: Card[]
  type: 'stock' | 'waste' | 'foundation' | 'tableau'
  index: number
  x: number
  y: number
}

export interface DragState {
  active: boolean
  cards: Card[]
  sourcePileIndex: number
  offsetX: number
  offsetY: number
  x: number
  y: number
}

export interface HistoryState {
  piles: Pile[]
}
