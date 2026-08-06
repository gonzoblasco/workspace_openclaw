class AudioEngine {
  private ctx: AudioContext | null = null
  private enabled = false
  private unlocked = false

  private getContext(): AudioContext | null {
    if (!this.enabled) return null
    if (!this.ctx) {
      const Ctx =
        window.AudioContext ||
        (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext
      if (!Ctx) return null
      this.ctx = new Ctx()
    }
    return this.ctx
  }

  enable(): void {
    if (this.enabled) return
    this.enabled = true
    this.unlock()
  }

  private unlock(): void {
    if (this.unlocked) return
    const ctx = this.getContext()
    if (!ctx) return

    if (ctx.state === 'suspended') {
      void ctx.resume()
    }

    // iOS/Safari needs an oscillator started inside a gesture to unlock audio
    const osc = ctx.createOscillator()
    const gain = ctx.createGain()
    gain.gain.value = 0.001
    osc.connect(gain)
    gain.connect(ctx.destination)
    osc.start(0)
    osc.stop(ctx.currentTime + 0.001)

    this.unlocked = true
  }

  private tone(
    frequency: number,
    duration: number,
    type: OscillatorType = 'sine',
    volume = 0.3,
    when?: number,
  ): void {
    const ctx = this.getContext()
    if (!ctx) return

    this.unlock()

    const t = when ?? ctx.currentTime
    const osc = ctx.createOscillator()
    const gain = ctx.createGain()

    osc.type = type
    osc.frequency.setValueAtTime(frequency, t)

    gain.gain.setValueAtTime(0, t)
    gain.gain.linearRampToValueAtTime(volume, t + 0.01)
    gain.gain.exponentialRampToValueAtTime(0.001, t + duration)

    osc.connect(gain)
    gain.connect(ctx.destination)

    osc.start(t)
    osc.stop(t + duration + 0.05)
  }

  private noise(duration: number, volume = 0.15): void {
    const ctx = this.getContext()
    if (!ctx) return

    this.unlock()

    const bufferSize = Math.max(ctx.sampleRate * duration, 1)
    const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate)
    const data = buffer.getChannelData(0)
    for (let i = 0; i < bufferSize; i++) {
      data[i] = Math.random() * 2 - 1
    }

    const noise = ctx.createBufferSource()
    noise.buffer = buffer

    const filter = ctx.createBiquadFilter()
    filter.type = 'lowpass'
    filter.frequency.value = 1200

    const gain = ctx.createGain()
    gain.gain.setValueAtTime(volume, ctx.currentTime)
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + duration)

    noise.connect(filter)
    filter.connect(gain)
    gain.connect(ctx.destination)
    noise.start()
  }

  playFlip(): void {
    this.tone(800, 0.08, 'triangle', 0.25)
  }

  playPlace(): void {
    const ctx = this.getContext()
    const t = ctx?.currentTime ?? 0
    this.tone(400, 0.1, 'sine', 0.3, t)
    this.tone(600, 0.08, 'sine', 0.2, t + 0.05)
  }

  playError(): void {
    this.tone(200, 0.2, 'sawtooth', 0.25)
  }

  playWin(): void {
    const ctx = this.getContext()
    const t = ctx?.currentTime ?? 0
    this.tone(523, 0.2, 'sine', 0.3, t)
    this.tone(659, 0.2, 'sine', 0.3, t + 0.2)
    this.tone(784, 0.3, 'sine', 0.3, t + 0.4)
    this.tone(1047, 0.6, 'sine', 0.3, t + 0.7)
  }

  playDeal(): void {
    this.noise(0.08, 0.2)
  }
}

export const audio = new AudioEngine()
