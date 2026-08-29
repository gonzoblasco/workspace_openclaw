# BRIEF - Project Overview

## What

Match-3 game rebuild in Godot 4.7, replicating the Kenney Starter-Kit-Match-3 gameplay using the same CC0 assets but with our own architecture and code.

## Why

Replicate the match-3 starter kit "a nuestro propio modo" - same assets (CC0), but with clean architecture, separated responsibilities, and maintainable code. Not copying the original prompt or monolithic implementation.

## Stack

- Godot 4.7.2 (GDScript)
- Assets: Kenney CC0 (5 tiles, background, cursors, sounds, sparkle particles)

## Status

- [x] Discovery
- [x] Definition
- [x] In Development
- [ ] Live
- [ ] Archived

## Key Decisions

- Rebuild in Godot (not web port) - Option A from roadmap
- Separate logic: board, input, audio, effects in modules (not monolithic main.gd)
- State machine: IDLE → SWAPPING → RESOLVING → REFILLING
- Grid as data structure decoupled from visual nodes (model vs view)
- Features extra (score, timer, levels) deferred to Phase 5 (optional)
