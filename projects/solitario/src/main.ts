import { SolitaireGame } from './game.js'
import { audio } from './audio.js'

function main(): void {
  const canvas = document.getElementById('game') as HTMLCanvasElement | null
  if (!canvas) {
    console.error('No se encontró el canvas #game')
    return
  }

  const game = new SolitaireGame(canvas)

  const undoBtn = document.getElementById('undo') as HTMLButtonElement | null
  if (undoBtn) {
    undoBtn.addEventListener('click', () => game.undo())
  }

  const newGameBtn = document.getElementById('new-game') as HTMLButtonElement | null
  if (newGameBtn) {
    newGameBtn.addEventListener('click', () => game.newGame())
  }

  const victoryBtn = document.getElementById('victory-new-game') as HTMLButtonElement | null
  if (victoryBtn) {
    victoryBtn.addEventListener('click', () => game.newGame())
  }

  const enableAudioBtn = document.getElementById('enable-audio') as HTMLButtonElement | null
  if (enableAudioBtn) {
    enableAudioBtn.addEventListener('click', () => {
      audio.enable()
      enableAudioBtn.style.display = 'none'
    })
  }
}

main()
