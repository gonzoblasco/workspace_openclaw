import { describe, it, expect } from 'vitest'
import { buildDialecticPrompt, parseEmotionalTone, generateDivergencePaths } from './dialectic-engine'

describe('Divergence Engine', () => {
   describe('Prompt Generation', () => {
      it('should generate proper dialectic prompt structure', () => {
         const input = {
            beatFile: {
              path: 'beats/capitulo-03.md',
              content: '',
              metadata: {}
            },
            userAlteration: 'What if this moment was a turning point?'
         }

         const result = buildDialecticPrompt(input)

         expect(result).toHaveProperty('role')
         expect(result).toHaveProperty('outputFormat')
         expect(result.role === 'Umbra Literary Critic').toBe(true)
      })

      it('should calibrate emotional tones correctly', () => {
         const sublimeContent = `This isn't just about losing the memory card. It's about everything we've lost and the emptiness of what used to fill these walls.`

         const comicContent = `He was fumbling with the door handle for the tenth time, each click echoing like a hammer blow against the hollow sound of their apartment.`

         expect(parseEmotionalTone(sublimeContent)).toBe('sublime')
         expect(parseEmotionalTone(comicContent)).toBe('comic')
      })
   })

   describe('Divergence Paths', () => {
     it('should generate exactly 3 paths', () => {
       const input = {
         beatFile: {
           path: 'beats/capitulo-01.md',
           content: '',
           metadata: { emotionalTone: 'sublime' }
         },
         userAlteration: ''
       }

       const paths = generateDivergencePaths(input)

       expect(paths.length).toBe(3)
       paths.forEach((p, idx) => {
         expect(['sublime', 'comic', 'tragic']).includes(p.emotionalWeight as any)
       })
     })
   })
})