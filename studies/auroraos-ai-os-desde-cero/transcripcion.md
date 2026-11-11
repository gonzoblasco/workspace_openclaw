# AuroraOS: forzar a la IA a escribir un sistema operativo — transcript

**Video:** [I Forced AI to Build a Custom Operating System (It Actually Worked)](https://www.youtube.com/watch?v=s6FNslOI5ac)
**Canal:** The Render Guy · **Publicado:** 2026-10-07 · **Duración:** 7:32 (452 s)
**Fuente del texto:** subtítulos automáticos de YouTube (`en-orig`, 150 cues tras deduplicar; 865 palabras). No se editó ningún cue.

## Glosario de correcciones del ASR

| ASR | Real |
|---|---|
| "GRUB, and BIOS S boot" | GRUB y boot por BIOS |
| "Aurora OS" / "AuroraOS" | AuroraOS (el video dice ambas) |
| "Opus 5.5" | Claude Opus 5.5 (versión que anuncia el video; no verificada fuera de él) |
| "S boot" | chainload del sector de arranque |

> El audio no siempre distingue lo que el video muestra; donde el ponente dice un número (líneas, archivos, minutos), se cita tal cual y se marca como **claim del video**, no como hecho verificado.

---

[00:00] Let's find out.
[00:01] >> [music]
[00:03] >> Okay, I'm in Claude. The trick
[00:06] I'm letting Claude write the prompt for
[00:07] Claude code. Build a custom operating
[00:09] system from scratch
[00:12] in C and assembly, like real operating
[00:14] systems. [music]
[00:18] Runs in VirtualBox
[00:21] with a Mac OS style interface.
[00:26] And it has to make [music] an ISO file.
[00:28] That's the boot disk.
[00:31] Opus 5.5, [music]
[00:33] effort medium, and send.
[00:38] It went [music] with x86, GRUB, and BIOS
[00:41] S boot. Fair enough. Name Aurora OS.
[00:44] >> [music]
[00:44] >> I like that. Seven phases. Boot, kernel,
[00:48] input, graphics, window manager, apps,
[00:51] and polish. [music] Copy and let's go.
[00:53] Real quick though, before I paste it,
[00:56] this is way harder than it sounds.
[00:57] [music] When you press power, a boot
[00:59] loader wakes up. In our case, that's
[01:02] GRUB, and it loads the kernel. The
[01:04] kernel [music] is the boss. It talks to
[01:06] the CPU, the memory, the keyboard, and
[01:08] the mouse. On top [music] of that, you
[01:10] need drivers, graphics, a window
[01:12] manager, and then finally apps. And
[01:14] Claude has [music] to write every single
[01:16] one of these. No Linux, no libraries,
[01:19] nothing.
[01:21] Claude code. Paste the prompt plus some
[01:24] Mac OS screenshots so it gets the vibe.
[01:26] Google Mac OS, copy, paste.
[01:30] One more.
[01:35] And send.
[01:37] First, it checks my tools. VirtualBox,
[01:39] Homebrew, compilers. Then it plans
[01:42] everything before writing a single line.
[01:47] The plan. Seven phases, and after each
[01:50] one it boots the OS in QEMU to check it.
[01:52] Design.
[01:53] My screenshots as inspiration, but
[01:55] everything original. No Apple stuff. And
[01:58] two questions. Where do I put it? And I
[02:01] picked the wrong folder. Classic. And
[02:04] VirtualBox probably won't run X86 on my
[02:07] ARM Mac.
[02:09] Ignoring that.
[02:15] Yes, Claude. New folder. Go.
[02:19] And now, we wait.
[02:23] >> [music]
[02:26] >> And it's done. About 50 minutes.
[02:29] Honestly, that's fine.
[02:30] >> [music]
[02:30] >> I've had Claude grind for hours before.
[02:34] Almost 6,000 lines of C [music] and
[02:37] assembly. 88 files and one ISO.
[02:41] Okay, let's boot it. Wait. Claude says
[02:43] VirtualBox can't run it on my Mac.
[02:46] Remember that warning I ignored? Yeah,
[02:49] it was right. My Mac has an ARM chip,
[02:52] and this OS is built for X86. Basically,
[02:55] a different language. So, Claude just
[02:57] launches it in QEMU instead. That's an
[03:00] emulator that pretends to be an X86 PC.
[03:03] Fine by me.
[03:05] Okay, it's booting.
[03:08] Oh, wow. Okay, this actually looks good.
[03:14] About this computer. [music]
[03:15] Aurora OS version 0.1. It even reads my
[03:20] CPU and the memory. And I can drag the
[03:22] window around. Look at the dock. It
[03:25] magnifies when I hover, just like on a
[03:27] Mac. A clock app. Analog, [music]
[03:30] digital, and a calendar. And I can even
[03:32] maximize it.
[03:42] >> [music]
[03:43] >> Files. A little file viewer with a
[03:45] change log and a read me.
[03:49] >> [music]
[03:49] >> The system menu up here. about settings,
[03:53] restart, shut down.
[03:55] And a terminal. Let's type help.
[03:59] >> [music]
[04:03] >> Echo, ls, cat, memory, uptime,
[04:06] processes. It even has the primes
[04:08] benchmark.
[04:12] >> [music]
[04:13] >> Let's try echo. Hello from OS.
[04:26] And it prints it. Okay, plus one for
[04:28] that.
[04:30] Now let's turn it off. Power off. Nope,
[04:33] command not found. Okay, it's shut down.
[04:41] And it's off. It actually powered itself
[04:44] off.
[04:46] For a first try, that's honestly really
[04:48] good. So yeah, I call this an OS, but
[04:51] let's push it. Round two. Let's ask for
[04:54] a web browser. Quickly add a web browser
[04:57] so I can search. Opus 5.5 again and it
[05:00] barely touches my limits. Big plus.
[05:05] >> [music]
[05:05] >> It's thinking for a while on this one.
[05:10] Claude says a full browser quickly isn't
[05:13] possible. [music]
[05:14] Every search engine needs HTTPS. That's
[05:17] tens of thousands of lines, but it can
[05:20] do a text browser. [music]
[05:21] Network driver, a small network stack,
[05:24] HTTP, and it'll try DuckDuckGo. [music]
[05:27] Come on, Claude. So here's what it's
[05:30] building. A driver for the virtual
[05:32] network card, then ethernet, IP, [music]
[05:35] DNS, TCP, and HTTP on top. And for
[05:40] HTTPS, it wrote a tiny helper on my Mac
[05:43] that handles the encryption.
[05:46] And it's way faster this time,
[05:48] >> [music]
[05:48] >> about 18 minutes.
[05:58] >> [music]
[05:59] >> There's a new icon in the dock, a
[06:01] browser start page. Welcome to the web.
[06:04] Let's [music] search for Wiki.
[06:09] And those are DuckDuckGo results from
[06:12] the real internet in an OS that didn't
[06:14] exist an hour ago. Wikipedia, no styling
[06:17] at all, but it loads.
[06:22] Now Google, and that's Google's page.
[06:25] Plain HTML, but it works.
[06:40] Oh, and there's settings, too. Light
[06:42] mode, dark mode, wallpapers.
[06:48] Dark mode. Okay, that's clean. Another
[06:50] plus point.
[06:53] So, what do I think? In two prompts,
[06:56] Claude built a real bootable OS. Its own
[06:59] kernel, a macOS-style desktop, apps, a
[07:01] terminal, and a web browser. And it
[07:03] barely lags. It's not perfect. [music]
[07:06] It doesn't run in VirtualBox on my Mac,
[07:09] and websites have zero styling. So,
[07:11] [music] I'm giving it 6.5 out of 10.
[07:15] So, yeah, [music] Claude can actually
[07:17] build an operating system. And once
[07:20] again, it didn't disappoint.
[07:22] What should [music] I make Claude build
[07:23] next? Let me know in the comments, and
[07:26] subscribe so you don't miss it. See you.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
