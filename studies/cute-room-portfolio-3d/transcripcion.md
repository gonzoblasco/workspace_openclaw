# Transcripción — Create a Cute Room Portfolio with Blender, Three.js, JavaScript

- Fuente: https://www.youtube.com/watch?v=tdsQwuyS6DQ
- Canal: freeCodeCamp.org (`@freecodecamp`)
- Expositor: **Andrew Woan** (@andrewwoan) — confirmado en la descripción oficial; el ASR lo escribe «Andrew Wan»
- Duración: 08:42:31
- Fecha de publicación: 2025-11-19
- Idioma del audio: inglés
- Subtítulos: automáticos (`en-orig`), descargados por `timedtext` con `fmt=json3`
- Cobertura: 14.576 cues → 108.922 palabras; el último cue cae en 08:42:29 sobre 08:42:31 de duración
- Capítulos oficiales: 42 en la descripción del video (fuente primaria del mapa temporal)
- Código del curso: https://github.com/andrewwoan/sooahkimsfolio · demo: http://sooahs-room-folio.com/
- Formato: un cue por línea, `[h:mm:ss] texto`. Los timestamps son el inicio real del cue.

## Glosario de errores del ASR

Los captions son automáticos y deforman nombres propios, APIs y atajos. Se listan acá para leer el cuerpo sin editar los cues:

| Dice | Es |
|---|---|
| 3.js, 3JS, 3GS, 3js | **Three.js** (`threejs.org`) |
| Andrew Wan | **Andrew Woan** (confirmado en la descripción oficial) |
| Mr. Whiskers / whiskers | el personaje gato del proyecto, correcto |
| EV (render engine) | **EEVEE** |
| D noiseis / de-noise | **Denoise** (denoising) |
| cycles | **Cycles** (motor de render de Blender) |
| principal BSDF / principled | **Principled BSDF** |
| engon / engones | **n-gon** (cara de más de cuatro vértices) |
| try / tries | **tri** (cara de tres vértices) |
| engon | **n-gon** |
| quads | **quads** (correcto) |
| loop tools | **LoopTools** (addon de Blender) |
| anzo piece / piece upward | **P → Separate by selection** |
| GB file / GB model | **GLB / glTF** |
| 3GS texture loader | **Three.js `TextureLoader`** |
| loaders | **GLTFLoader / DracoLoader / TextureLoader** |
| Draco | **Draco** (compresión de malla, correcto) |
| squish | **Squoosh** (`squoosh.app`, compresor de imágenes de Google) |
| WEBP / webp | **WebP** |
| Vit | **Vite** (`vitejs.dev`) |
| mpm / npmi | **npm** |
| How.js / howler | **Howler.js** |
| Verscell | **Vercel** |
| OrbitControls / orbit controls | **`OrbitControls`** (correcto) |
| raycaster / ray caster | **`Raycaster`** (correcto) |
| Gab | **GSAP** |
| UV squares | **UV Squares** (addon, correcto) |
| smart UV project | **Smart UV Project** (correcto) |
| Cycles | **Cycles** |
| 2040 / 204080 | **2048** (textura 2K) |
| Acadia trees | **Acacia** (árboles de Minecraft) |
| win sight of the day on awards | *Awwwards* Site of the Day |

[0:00:00] Learn how to use 3JS and Blender to
[0:00:02] design a stunning and interactive 3D
[0:00:04] portfolio. This course will take you
[0:00:06] from the foundational concepts of 3D
[0:00:09] modeling in Blender to creating a fully
[0:00:12] functional, award-worthy portfolio
[0:00:14] website using 3JS. You'll master
[0:00:17] essential techniques like proper quad
[0:00:19] topology for clean models and texture
[0:00:22] baking to optimize your scene for the
[0:00:25] web. By the end, you'll have a
[0:00:26] delightful, cute, and professionally
[0:00:29] deployed 3JS project featuring all your
[0:00:32] handmodeled creations, including the
[0:00:34] adorable Mr. Whiskers. Andrew Wan
[0:00:37] developed this course. Hey everyone,
[0:00:39] welcome back to another video. Thanks so
[0:00:41] much for stopping by. So, without
[0:00:43] further ado, let me just refresh the
[0:00:44] page and show you what we'll be creating
[0:00:46] today. So, small loading screen. Hover
[0:00:48] enter, hit enter. That just says hello.
[0:00:51] Changes a little bit. Small little
[0:00:52] animation there. And then we have these
[0:00:54] objects animating in to catch the user
[0:00:56] intention. Sorry, let me just move this
[0:00:58] for a second to catch the user's
[0:01:00] attention to so they know where to
[0:01:02] click. So that's why I animated these
[0:01:04] and these and these as well. And then
[0:01:06] when you click on one of these, it pops
[0:01:08] up a simple model like so. And you can
[0:01:10] style it however you want, like so, you
[0:01:13] know, very, very simple. And then you
[0:01:15] can also click outside of the thing as
[0:01:16] well. So, if you're familiar with 3JS, I
[0:01:18] just used orbit controls for navigation,
[0:01:20] except I limited the pan and the
[0:01:22] rotation so we don't see the back of it
[0:01:24] because I deleted a bunch of faces back
[0:01:26] there. If you don't know what I'm
[0:01:27] talking about, that's totally okay. So,
[0:01:28] now I just want to talk about the
[0:01:30] specifics of what you'll learn in this
[0:01:32] video cuz there's a few things that
[0:01:33] you're seeing that I won't explicitly
[0:01:35] teach. So, one of them is the light to
[0:01:38] dark mode toggle here where I switch
[0:01:40] from light theme to dark theme. This
[0:01:42] requires a shader, which I was planning
[0:01:44] to cover in this course, but I felt like
[0:01:46] it was getting a little too dense and a
[0:01:48] little too long, so I did not include
[0:01:50] that. Don't worry, my next video will,
[0:01:51] but the code is there if you want to
[0:01:53] take a look at it and take a stab at
[0:01:55] yourself. But mostly everything like
[0:01:56] this hover effect, you'll learn about
[0:01:58] it. You'll learn how to create your own
[0:01:59] materials in Blender. You'll learn how
[0:02:01] to model everything, unwrap things. You
[0:02:03] can take a look at the video chapter
[0:02:06] stamps. So, primarily the only two
[0:02:08] things that I'm not teaching is this
[0:02:10] coffee steam here and the light theme
[0:02:12] and dark theme toggle. But everything
[0:02:14] else you'll be able to know how to
[0:02:16] create by the end of this video. So,
[0:02:18] some segments are very very slow and
[0:02:20] step by step and then others are more
[0:02:22] just speed up walking through you code
[0:02:25] where I just have the code there and
[0:02:27] then I just talk about it through there
[0:02:28] and then everything in between, you
[0:02:30] know, half of writing code and talking
[0:02:32] and then also half step by step and
[0:02:34] drawing out explanations. So, I kind of
[0:02:37] just adapt it based on what I think that
[0:02:40] specific section needs. But by the end
[0:02:41] of this video, hopefully you can create
[0:02:43] some really awesome stuff. So, when it
[0:02:45] comes to prerequisites, you just need to
[0:02:47] know the basics of Blender and the
[0:02:49] basics of 3GS. I do have an intro to
[0:02:52] creative web development course where I
[0:02:54] cover a lot of concepts much slower than
[0:02:56] I do in this video. I kind of just
[0:02:58] assume like you already know how to set
[0:02:59] up a basic scene. You know how to do
[0:03:01] some basic models in 3GS. In this video,
[0:03:04] I assume you don't have any knowledge of
[0:03:06] 3JS and have no knowledge of Blender.
[0:03:08] So, if you want, you can skim through
[0:03:10] getting started with 3GS. And if you
[0:03:12] understand everything there, then you
[0:03:13] should be more than good enough to go.
[0:03:15] Same with Blender. If you can make like
[0:03:17] this tree and like this background here
[0:03:19] without any help, you know, you're
[0:03:20] definitely well prepared for what we're
[0:03:23] going to be doing. Yeah. So, definitely
[0:03:24] reach out if you have any questions.
[0:03:26] Feel free to reach me out on Discord.
[0:03:28] I'm most active there. You can find it
[0:03:30] probably in my YouTube description
[0:03:31] somewhere, but email is totally fine as
[0:03:34] well. Also, if you'd like to support me,
[0:03:35] you know, definitely consider checking
[0:03:37] me out on patreon.com. I would really
[0:03:40] appreciate it. Uh, you know, anything
[0:03:42] means a lot. Or alternatively, if you
[0:03:44] want to buy me a coffee, that's really
[0:03:46] awesome as well. And if you do ever, you
[0:03:49] know, financially support me in some
[0:03:51] way, you know, definitely reach out for
[0:03:52] a chat and a call and we can just set
[0:03:55] something up for sure. I would
[0:03:56] definitely love to chat with you. So
[0:03:58] without further ado, let's get straight
[0:03:59] into the video. Hope to see you on the
[0:04:01] other side and definitely share what you
[0:04:03] create. Okay, before we start modeling,
[0:04:04] I just want to talk about some terms
[0:04:06] that you'll hear me say a lot and I kind
[0:04:08] of want to explain them. So when I say a
[0:04:10] try, uh what I mean is a face with three
[0:04:13] vertices. 1 2 3. And if I say a quad,
[0:04:16] that's one with four vertices. And then
[0:04:19] you'll hear me say engon, which which
[0:04:22] you've probably heard of things before
[0:04:24] like pentagon, octagon, so on so forth.
[0:04:26] Those prefixes actually resemble
[0:04:28] numbers. So we just represent it with n,
[0:04:30] right? Some number of vertices gone or
[0:04:33] whatever. Um, so like let's say we have
[0:04:36] a pentagon, right? This has five
[0:04:38] vertices like so. So instead of calling
[0:04:41] a pentagon, I'll just call it an engon.
[0:04:43] And any face with you know more than
[0:04:45] four is going to be called an engon in
[0:04:48] my book. And obviously if you have just
[0:04:50] two vertices, this is like a line or
[0:04:52] something, right? So, it's generally
[0:04:54] best practice to try and make your
[0:04:56] model, your objects consist of quad
[0:04:59] faces and quad topology. And the reason
[0:05:02] for that is because 3D software handles
[0:05:04] the calculations that it does behind the
[0:05:06] scenes a lot better with these quad sort
[0:05:09] of faces rather than some of these other
[0:05:11] ones like engones and tries. It doesn't
[0:05:13] mean you always have to go for quads.
[0:05:14] It's just general best practice. Also,
[0:05:16] when you have quad topology, you kind of
[0:05:18] want them to be equal in size across
[0:05:21] your model, other than obviously areas
[0:05:23] that need more detail. Um, but for the
[0:05:25] most part, places with the same level of
[0:05:27] detail should have relatively similar
[0:05:29] quad sizes.
[0:05:31] Yeah. So, as I work through the
[0:05:33] tutorial, I'm going to be going into
[0:05:34] more detail and showing more examples so
[0:05:36] you know what I'm talking about, uh, and
[0:05:38] can visualize it a little bit better
[0:05:39] than what I'm doing here. All right. So,
[0:05:41] I'm in a new general Blender file here.
[0:05:43] Now, I'm going to say all the hot keys I
[0:05:45] use out loud, but in case I forget
[0:05:47] something, try and look down here to see
[0:05:49] if you can see it over here. Not
[0:05:51] everything will show up here. So, in the
[0:05:53] case that I don't mention anything and
[0:05:55] it doesn't show up here, you know, just
[0:05:57] post a timestamp below and I'll get back
[0:05:59] to you as soon as I can. So, the first
[0:06:01] thing I'm going to do is probably delete
[0:06:02] this point late. And then I'm going to
[0:06:04] hit M and move this into a new
[0:06:06] collection called lights, camera,
[0:06:08] action, and just disable it so we don't
[0:06:10] see it in the meantime. Now, to start
[0:06:13] and create a room, you can totally start
[0:06:15] with the default cube. So, let's just do
[0:06:17] that. So, I'm going to hit S to scale it
[0:06:19] up. Then, I'm going to go into edit
[0:06:21] mode. And if you want this pi menu thing
[0:06:23] here, you can go into edit preferences,
[0:06:26] go into keymap, and do tab for pi menu.
[0:06:29] That way, you can easily go between all
[0:06:31] different kinds of modes. By default, if
[0:06:34] you hit tab, you'll just go into between
[0:06:36] object and edit mode, but I like doing
[0:06:38] this because I use these other modes,
[0:06:40] too. not for this video, but you'll get
[0:06:43] used to it and it'll be just as fast as
[0:06:44] hitting tab eventually. Anyway, what I'm
[0:06:47] going to do is hit three to go into face
[0:06:49] select, which is right up here. I'm
[0:06:51] going to select these three, and I'm
[0:06:52] just going to hit X and delete the faces
[0:06:54] there. Now, instead of selecting these
[0:06:56] faces, well, I guess every single face,
[0:06:58] so you could just hit A to select
[0:07:00] everything and doing Alt E extrude along
[0:07:02] normals and then hitting S to scale
[0:07:04] evenly. Instead of doing that, I'm going
[0:07:06] to add a solidify modifier. This way we
[0:07:08] can just easily adjust it later if we
[0:07:10] want to. So now if I increase my
[0:07:14] thickness, you can see maybe I want to
[0:07:16] go that way instead. It's going to do
[0:07:18] the same thing. And we can just check
[0:07:20] even thickness here. Now generally
[0:07:22] before you apply a modifier, you should
[0:07:24] apply your scale. So I'm going to hit
[0:07:26] apply my scale. And you can see that's
[0:07:28] going to affect my solidify modifier,
[0:07:29] which is totally okay. For us, solidify
[0:07:32] modifier is not really a big issue
[0:07:33] whether you apply your scale or not. But
[0:07:35] for other modifiers, it will be. Anyway,
[0:07:37] we can always change it later. So,
[0:07:38] that's pretty good. And now I just want
[0:07:40] to move my cube up to above the grid
[0:07:43] just because the grid is a little bit
[0:07:45] distracting. You can hide the grid if
[0:07:46] you want, but I'm just going to move it
[0:07:48] above the grid. So, I'm going to go here
[0:07:50] into orthographic view and just bring it
[0:07:52] up just sitting right there. Cool. So,
[0:07:55] now we have a room that we can play
[0:07:57] with. And of course, if you want to
[0:07:59] adjust it, you can totally do that as
[0:08:00] well. I might be making slight scaling
[0:08:03] adjustments later
[0:08:06] and off camera, but I'll just show you
[0:08:08] now that I would go into wireframe view
[0:08:11] and probably just do something like
[0:08:12] this. Uh, GUI, select the vertices and
[0:08:16] things like that. Um, and and scaling
[0:08:19] and and so on so forth. So, just in case
[0:08:22] you see some slight changes, that's what
[0:08:24] I'll be doing. Now, I don't like how
[0:08:27] sharp these areas are. So, what I'm
[0:08:29] actually going to do is add a bevel
[0:08:31] modifier. And that'll just give it a
[0:08:33] more sty. And that'll just give it make
[0:08:35] it a little bit more stylistic and cute.
[0:08:37] So, we can increase the amount of
[0:08:39] segments to maybe like four. And you can
[0:08:41] see now it looks really really smooth.
[0:08:43] And then you can adjust how much you
[0:08:45] want to bevel. So, if you want it like
[0:08:47] more plumpy, you can totally increase
[0:08:49] the amount just like that. And then
[0:08:52] right now, what it's doing is flat
[0:08:53] shading the geometry that's being added.
[0:08:56] So, what you can do is right click and
[0:08:58] do shade smooth instead. Now, there's
[0:09:00] this other option called shade auto
[0:09:02] smooth, and it'll only take faces that
[0:09:05] are at certain angles and smooth those
[0:09:07] instead. So, you can see if I do shade
[0:09:09] auto smooth, we kind of get the same
[0:09:11] result. Um, this is not really a good
[0:09:13] model to show what that does. But, um,
[0:09:16] you can see we get the same result. So,
[0:09:17] we'll just leave that there for now. Now
[0:09:19] again, if you're a beginner to Blender,
[0:09:20] uh you'll know that bevel and solidify
[0:09:24] modifiers, these are operations you can
[0:09:25] actually do with Blender yourself. So
[0:09:27] again, if I just add a cube, just to
[0:09:30] show you, go into edit mode, select
[0:09:32] these faces, A to select everything, alt
[0:09:34] E, extrude along normals, S to scale,
[0:09:37] then I go into edit mode, hit A to
[0:09:39] select everything, then I apply my
[0:09:41] scale, go into edit mode, hit A to
[0:09:43] select everything, then do Ctrl +B,
[0:09:47] move my middle mouse button up to
[0:09:49] increase the amount of bevels. I have
[0:09:50] four cuts on my bevel modifier, and then
[0:09:52] I'm just going to left click and drag
[0:09:54] there. And then I'm going to rightclick
[0:09:56] and do shade auto smooth. And you can
[0:09:57] see we get the same thing here except
[0:09:59] one of them we did with modifiers.
[0:10:01] Whereas the other ones we use the actual
[0:10:03] operations. So you can see if we do uh
[0:10:06] shade flat you can see we're going to
[0:10:08] see all those phases. But if we do shade
[0:10:10] smooth we're going to get rid of all
[0:10:12] those. Super super cool. Okay. So, the
[0:10:14] next thing when it comes to creating a
[0:10:16] model and things like that, other than
[0:10:17] getting references, is to block out your
[0:10:20] scene and try and get a feel of what you
[0:10:22] want in your room, your composition, and
[0:10:24] things like that. You won't always do
[0:10:26] it. And for this tutorial, I don't think
[0:10:27] I'm going to be doing it, but I do want
[0:10:29] to touch on it because it's a ve very,
[0:10:31] very common practice when you starting a
[0:10:33] 3D art project. It's the same way how
[0:10:35] artists might have like guiding lines or
[0:10:37] sketches that start out before they
[0:10:39] start coloring and and things like that.
[0:10:41] So blocking out is kind of the same
[0:10:43] idea. So let's say you add like a plane
[0:10:45] here. And you're like, "Okay, I want my
[0:10:47] bed to maybe kind of look like this.
[0:10:50] Maybe about this shape. Go into edit
[0:10:51] mode. Hit A to select everything. E to
[0:10:54] extrude everything." And you're like,
[0:10:55] "Okay, my bed's going to be here." And
[0:10:57] then maybe you come over here, go to
[0:10:58] this add cube tool, and you're like,
[0:11:00] "Okay, I'm going to like put a desk over
[0:11:03] here. So maybe I want a desk over here."
[0:11:05] And then, okay, maybe I want some
[0:11:07] shelves over here. Like so forth. And
[0:11:10] then maybe you go into the annotate tool
[0:11:12] and you're like, "Okay, maybe I want
[0:11:13] like a clock over here." Uh, and then
[0:11:16] maybe like a lamp over here. Sorry,
[0:11:18] that's not a lamp. Um, that's a lamp.
[0:11:22] No, that's not a lamp either. And then
[0:11:23] you kind of just like, you know, get the
[0:11:25] get the general vibe of of what you
[0:11:26] want. So, that's totally an approach
[0:11:29] that you could go for if you want to.
[0:11:31] And it's a very very common practice,
[0:11:33] but for this video, I'm just going to be
[0:11:35] showing you how to model things rather
[0:11:36] than blocking out and and doing
[0:11:38] composition and all that kind of stuff.
[0:11:40] Okay, so I'm just going to select these
[0:11:41] and I'll just delete them. So, one thing
[0:11:43] I definitely want is a desk. So, I'm
[0:11:45] just going to shift right click
[0:11:46] somewhere to spawn a cube. So, shift A
[0:11:48] and just add a cube. Bring it up to any
[0:11:50] height. It doesn't really matter. You
[0:11:51] can always change it later. And kind of
[0:11:53] just like get it to a scale that you
[0:11:56] like. Doesn't really matter. And uh I'm
[0:11:58] just going to try and get a eye for the
[0:12:00] desk. It doesn't have to be
[0:12:01] proportional. Again, we're going for a
[0:12:03] more stylistic rather than realistic
[0:12:05] scene. So, if it's not proportional,
[0:12:07] that's totally okay. And of course, you
[0:12:08] can always change it later. Uh, and then
[0:12:10] I'm going to go for a standing desk. So,
[0:12:12] this is going to be a little bit
[0:12:14] non-traditional compared to regular
[0:12:15] desks. And I don't like seeing this
[0:12:17] here. So, what I can do is either go
[0:12:19] into local view with my numpad slash or
[0:12:22] come over to view local view and do
[0:12:24] toggle local view like so. Um, or you
[0:12:28] can just hit this and hit the eyeball
[0:12:29] here or hit H or Alt H to unhide. So, H
[0:12:33] or Alt H. So, I'm just going to go into
[0:12:36] local view here. And what I'm going to
[0:12:37] do is probably shift right click
[0:12:39] somewhere over here. And uh just add a
[0:12:42] plane. And I'm just going to scale that
[0:12:44] down like here or something like so,
[0:12:47] which will be the desk leg. And go into
[0:12:49] edit mode and just hit E and extrude it
[0:12:51] downwards. Then since this face is still
[0:12:54] selected, I'm actually going to hit P
[0:12:55] and separate by selection. So what that
[0:12:57] does is my selected thing now just
[0:13:00] became its own object. Now it still
[0:13:03] takes the origin point of the original
[0:13:05] thing that I separated it from. However,
[0:13:08] we can fix that if we do rightclick set
[0:13:10] origin origin to geometry. And now the
[0:13:13] origin's geometry is over here. And the
[0:13:15] scale and every operation will be around
[0:13:17] this origin point. Now, since the leg is
[0:13:19] going to be the same on the right and
[0:13:20] left, what I'm going to do is go into
[0:13:22] edit mode, add a loop cut to this plane
[0:13:24] right here. Right click to cancel the
[0:13:26] movement. And I'm just going to delete
[0:13:28] those vertices by selecting them. And
[0:13:30] I'm going to come over here and add a
[0:13:32] mirror modifier just like this. And now,
[0:13:34] if you're working in a different axis,
[0:13:36] you might have to change this, but I'm
[0:13:37] on the X. Then, I'm going to turn on
[0:13:38] clipping. This way, if I go into edit
[0:13:40] mode, you can see that they're not going
[0:13:42] to go through each other. If I turn it
[0:13:44] off, you can see they're going to go
[0:13:45] through each other and things like that.
[0:13:46] Now I can just select these, go into
[0:13:48] wireframe view, and just do GX,
[0:13:51] and then go into side view, and then
[0:13:53] just extrude it at like a small angle,
[0:13:56] kind of like this. And then I'm just
[0:13:58] going to hit E to extrude the the
[0:14:00] vertices again, and lock it on the
[0:14:02] X-axis. And probably go around here. And
[0:14:05] then I'll just hit E and just extrude
[0:14:06] again. Probably around here, just like
[0:14:08] this. And then I'll do E and lock it on
[0:14:11] the X-axis. But this time I want to turn
[0:14:13] on snapping. I'll turn on snapping here.
[0:14:16] go to vertex snapping. And now when I do
[0:14:18] G to move it, lock it on the X-axis and
[0:14:20] hover over this vertex here, you can see
[0:14:22] it's going to perfectly align just like
[0:14:24] that. And now if I go back into object
[0:14:27] view, I can turn off snapping here and
[0:14:28] go into solid view. You can see we kind
[0:14:30] of have a table like like this. And then
[0:14:33] we want to fill in these faces. So I'm
[0:14:34] going to select these two edges. Go into
[0:14:36] hit F to fill. Select these two, fill
[0:14:39] those as well. Select these two, hit
[0:14:41] fill. Select these two, and hit F to
[0:14:43] fill. Just like that. So now we kind of
[0:14:45] have like a table leg there. And then
[0:14:47] let's just scale it up just a little bit
[0:14:49] because I want it to be blocky and
[0:14:51] stylized. And then I might increase this
[0:14:54] just a little bit. Okay. When it comes
[0:14:56] to standing desks, uh usually there's
[0:14:58] like some sort of inset, right? And then
[0:14:59] the other there's like another overload
[0:15:02] thing that actually moves up and down
[0:15:04] the bar. What I'm probably going to do,
[0:15:05] well, first this is a little bit too
[0:15:07] thick. So I'm going to scale it first on
[0:15:09] the S and Y and then probably on the S
[0:15:11] and Z just like this. I'm going to apply
[0:15:13] my scale and then go into edit mode and
[0:15:16] whoops, I accidentally removed this
[0:15:18] face. But what we can do is just hold
[0:15:20] alt to select that entire edge loop
[0:15:21] there. Rather than clicking on all four
[0:15:23] of them, we can just hit alt and go near
[0:15:25] the edge. Hit fill just to fill that up.
[0:15:28] And then what we can do is hit I just to
[0:15:30] insert it a little bit like so. And then
[0:15:33] now we can just do E and extrude
[0:15:36] downwards. And since we have vertex
[0:15:37] snapping on, we can just snap it to a
[0:15:39] vertex like this. So, if you hold
[0:15:42] control, it'll turn it on automatically,
[0:15:44] even if it doesn't show it's on. You can
[0:15:45] also just come up here and click it, and
[0:15:46] you can see it'll snap there. Again,
[0:15:48] make sure you lock it on the axis, and
[0:15:50] you can snap it. Since these are all at
[0:15:51] the same level, it doesn't really matter
[0:15:53] which one you choose. Uh, so I'll just
[0:15:55] use this one here, but typically I
[0:15:56] usually just use control rather than
[0:15:59] come up here to toggle it on and off.
[0:16:01] You can also hover over it. And you can
[0:16:03] see shift tab is also another way to
[0:16:05] toggle it on and off, but usually I just
[0:16:07] use control, which is the hotkey for it.
[0:16:09] Okay, so now we kind of have our
[0:16:10] standing desk functionality. If you
[0:16:12] want, you can go into wireframe. Again,
[0:16:15] just select all these and kind of just
[0:16:16] adjust it here. And if you wanted
[0:16:18] multiple layers, you could just insert
[0:16:19] again and so on so forth. Okay, let's go
[0:16:21] out of local view. Um, and let's go back
[0:16:23] into solid view. That looks like a
[0:16:26] pretty cool desk. Obviously, it's not
[0:16:28] inside a room, which is fine. We can
[0:16:30] just adjust that very, very nicely. Just
[0:16:33] like that. Now, what we can do is use
[0:16:34] mirror modifiers for these. So, I'm
[0:16:36] going to come over here and add a mirror
[0:16:38] modifier. And then I'm just going to
[0:16:40] select this object to mirror over. And
[0:16:44] since I'm it's in the Y direction, we
[0:16:46] can switch this to Y. And now you can
[0:16:47] see it's over there. And get rid of the
[0:16:49] X value. Then same thing with here, but
[0:16:52] instead of adding the mirror and doing
[0:16:53] all that again, what we can do is select
[0:16:55] this, shift select, and select this one
[0:16:57] as well. Make it the active object. Come
[0:16:59] over here and do copy to selected. And
[0:17:01] that's a really easy way to copy a
[0:17:04] modifier from your selected object or
[0:17:06] your active object to your other
[0:17:09] selected objects. And you can see it's
[0:17:10] added right here. This is going to be
[0:17:12] the same thing we do with the bevel
[0:17:14] modifier. So our room right here, it has
[0:17:16] a bevel modifier, right? And we want to
[0:17:18] copy this to all of these as well. So
[0:17:21] what I'm going to do is select all
[0:17:23] these, hold shift, and make this the
[0:17:25] active object highlighted by orange.
[0:17:27] Then I'm just going to come over to the
[0:17:29] bevel modifier and do copy to selected.
[0:17:31] And now you can see the bevel modifier
[0:17:33] is also applied to our table stuff. And
[0:17:36] make sure to apply your scale so it
[0:17:38] works properly. And I'm going to
[0:17:39] rightclick and do shade smooth again.
[0:17:41] And you can see, okay, cool. We kind of
[0:17:43] have something more stylistic. And if
[0:17:45] the bevel is too much, you can come over
[0:17:47] here and with all three of them
[0:17:49] selected, you can see they all have
[0:17:51] 0.168 amount, right? With all of them
[0:17:54] selected, if you hold down Alt on your
[0:17:55] keyboard, you're going to you can adjust
[0:17:57] the bevel for all of them all at the
[0:17:59] same time. Just like that. So 0.78 looks
[0:18:03] good. And of course, if you want to
[0:18:05] adjust one of them's bevels and not the
[0:18:07] other, you can totally just do it
[0:18:09] individually as well. But if you want to
[0:18:10] group bevel, that's totally how you do
[0:18:12] it. And I feel like these are a little
[0:18:14] bit too uh far. So what I'm going to do
[0:18:16] is just do GX and kind of move it a
[0:18:18] little bit. S Y SX. And then maybe
[0:18:21] select this and kind of just scale that
[0:18:23] in a little bit. So there we kind of
[0:18:25] have like our cute little standing desk
[0:18:26] there. All right, let's create a
[0:18:28] tabletop thing. So I'm just going to go
[0:18:30] shift right click on top of my table. Um
[0:18:32] and probably add a plane. Then just
[0:18:34] scale it down. S Y probably scale it
[0:18:37] down a little bit. Uh S Y just like
[0:18:39] this. Go into edit mode. E to extrude
[0:18:41] that up a little bit. Go back into edit
[0:18:44] mode. Add a loop cut here. And then just
[0:18:46] give it an arbitrary size. and uh
[0:18:49] probably just E and extrude this out.
[0:18:51] And what I'm going to do is add a mirror
[0:18:53] modifier so I don't have to do it on the
[0:18:54] other side. So I'm just going to do
[0:18:56] that. Let's go into Y here. And since
[0:18:59] it's mirroring across this origin point,
[0:19:01] it's going to look like this. So what
[0:19:03] we're going to do is select everything
[0:19:05] in edit mode. Gy, and just pull
[0:19:07] everything over here. And then let's
[0:19:09] turn on clipping. And then let's just
[0:19:11] bring it back inside just like so until
[0:19:14] it snaps. Then let's go into edit mode
[0:19:17] still. Well, I was still in there.
[0:19:19] Select this face. Make sure that's
[0:19:21] selected and just delete that because
[0:19:22] we'll never see it. And uh cool. We kind
[0:19:24] of have a stand like this. And I just
[0:19:26] want to give it some style. So I'm going
[0:19:28] to select this E to extrude this out a
[0:19:30] little bit. Select this one and kind of
[0:19:32] just bring it in a little bit. Just like
[0:19:34] that. All right. And now let's apply our
[0:19:36] scale. And with this one as the active
[0:19:39] object, let's just come over here and do
[0:19:41] copy to selected. So now this has a
[0:19:43] bevel modifier. And I'll just do shade
[0:19:46] auto smooth here. Now, you will notice
[0:19:48] that there are some slight shading
[0:19:50] issues here. That's due to the way that
[0:19:52] we modeled the thing. Um the Hey, I'm
[0:19:55] Andrew from the future. I just want to
[0:19:57] talk about a quick fix to fix this
[0:19:59] corner here. Um, I did say it was a
[0:20:01] little bit too advanced because the
[0:20:03] professional way to fix it up is is a
[0:20:06] little bit too advanced for this course,
[0:20:08] but there's a really really quick way to
[0:20:10] fix it, at least visually good enough
[0:20:12] for us, and I show it later in the
[0:20:14] video, but I'm just going to do it now.
[0:20:16] So, in your bevel modifier, what you can
[0:20:19] do is come over to miter outer and
[0:20:22] change that to arc. And you can see that
[0:20:24] kind of already fixed some things. And
[0:20:25] then if you still have pinching here,
[0:20:27] you can try changing the amount of
[0:20:28] segments. And you can see going down to
[0:20:30] three actually made that a little bit
[0:20:32] better. And of course, you can also try
[0:20:34] and adjust the mount here as well. And
[0:20:36] then you also have this profile thing
[0:20:37] here in shape that can also adjust, you
[0:20:41] know, what kind of bevel you have. So I
[0:20:43] guess right now it's not a great example
[0:20:45] for using shape here, but when you use
[0:20:47] bevel in the future, you can play around
[0:20:49] with the shape to kind of help it out a
[0:20:51] little bit. Additionally, you'll see me
[0:20:53] add weighted normal modifiers to fix the
[0:20:56] shading of beveled things, which is
[0:20:58] totally fine. But you can also just come
[0:20:59] into the shading tab and click on harden
[0:21:01] normals here. I just by habit add
[0:21:03] weighted normal modifiers. So, just to
[0:21:05] show you the difference in geometry when
[0:21:07] I do arc versus sharp. I'll make this
[0:21:09] one sharp. I will apply both of the
[0:21:12] modifiers right like so. And you can see
[0:21:15] that this one is using sharp. This one
[0:21:18] is using arc. Typically, we go for quad
[0:21:21] geometries, which is what arc gives us.
[0:21:23] So, it's got a better edge flow here.
[0:21:25] Now, there's still an end gone here. So,
[0:21:26] there's still issues with the topology,
[0:21:28] but again, you know, that's like an
[0:21:31] advanced concept. So, this will be good
[0:21:33] enough. This will be better than uh what
[0:21:35] we see here. Yeah, I just wanted to
[0:21:37] point that out. And honestly, even if
[0:21:39] you leave it like this, it's really not
[0:21:40] a big deal either. Um, you know, just
[0:21:43] focus on having fun and and don't really
[0:21:45] worry about anything like that, right?
[0:21:47] So we can do the computer now. Let's
[0:21:49] just shift right click somewhere. Shift
[0:21:50] A. Add a plane. Just scale it down. Go
[0:21:53] into edit mode and just E extrude that
[0:21:55] up. Let's go out. Apply our scale. Go
[0:21:58] into edit mode again. Select this face.
[0:22:00] I to insert like so. Creates a face
[0:22:03] within the face. G. Shift Z and just
[0:22:06] move it. Uh, well, actually, let's just
[0:22:08] do GX and move it backward like here.
[0:22:10] And then just E extrude that up. Then we
[0:22:13] can go into face select and just hold
[0:22:15] alt to select the entire loop. Alt s to
[0:22:18] scale along normals and just make it a
[0:22:20] little bit thinner. Just like that. Then
[0:22:22] we can add like a loop cut. Um and uh
[0:22:26] kind of just extrude it inwards a little
[0:22:28] bit. Super super cool. Uh then we can do
[0:22:32] shift duplicate right click cancel p
[0:22:34] separate by selection. So this will
[0:22:36] become our computer. Right click set
[0:22:38] origin origin to geometry. And we can
[0:22:40] just scale that up a little bit. And
[0:22:42] then we can do a little bit sy like
[0:22:44] this. Uh then we can go into edit mode.
[0:22:46] Hit A to select everything. E extrude
[0:22:48] outward. Let's apply scale on this.
[0:22:50] Let's go back into edit mode. Hit I to
[0:22:52] insert a little bit. And then E to
[0:22:54] extrude it inwards. And there we kind of
[0:22:57] have a computer with a stand like so.
[0:23:01] And I think I just want to move this up
[0:23:03] uh just a little bit so we can see a
[0:23:04] little bit of the stand there. Um I feel
[0:23:08] like the stand is a little bit too big.
[0:23:09] So, I'm just going to select all those
[0:23:10] and do website proportional editing on
[0:23:13] uh we'll talk about that in a little
[0:23:14] bit. Um I must have hit a hotkey or
[0:23:17] something, but I'm just going to hit alt
[0:23:19] s and scale this along the normals just
[0:23:21] like that. Um this is also a little bit
[0:23:25] too thick. So, I'm just going to hold
[0:23:27] shift and alt to select both of those
[0:23:29] loops and just do sy and kind of scale
[0:23:32] it down a little bit like so. Um then we
[0:23:34] can just select these again. Uh, with
[0:23:37] this one selected, I guess we can just
[0:23:39] do copy to selected, just like so. And
[0:23:42] of course, make sure to apply our scale.
[0:23:44] Uh, one thing I'll say about this
[0:23:46] computer now is that it looks too thin
[0:23:49] compared to the rest of our scene. Uh,
[0:23:52] we want to go for more bulky and like
[0:23:56] full sort of vibe. So, what we're going
[0:23:58] to do is and go into edit mode and
[0:24:01] select the screen itself. Actually, we
[0:24:03] can turn this off temporarily so you can
[0:24:04] see what I'm doing.
[0:24:06] Um, and we're going to hit controll
[0:24:09] numpad plus to increase our selection.
[0:24:11] You can see it expanded our selection.
[0:24:13] So, we don't have to do that. Or you can
[0:24:14] just select this face, hold shift, alt,
[0:24:16] and try and get the loop, which also
[0:24:18] works as well. Or if you want the more
[0:24:20] hotkey, you can select a face, do select
[0:24:23] more or less, and you can see the hotkey
[0:24:25] is control numpad plus. You can just do
[0:24:26] more and it'll select everything. And
[0:24:28] then I'll do S, and then I'll scale it
[0:24:30] down. And then I don't want to do it on
[0:24:32] the X-axis. I don't think it is, but I'm
[0:24:34] just going to do S and then shift X and
[0:24:36] then just scale it a little bit here.
[0:24:38] And then I'm going to reactivate my
[0:24:39] bevel modifier so I can just kind of see
[0:24:41] how
[0:24:43] uh how thick it would be. Cool. And the
[0:24:46] computer itself is too thin. I like the
[0:24:48] frame. So, what I'm going to do is uh I
[0:24:51] think I'll just select everything and
[0:24:53] just do SX and just scale it up a little
[0:24:55] bit like that. Uh so, now you can tell
[0:24:56] that it's a little bit more full. And
[0:24:58] then I want the bottom a little bit
[0:25:00] higher than the rest of them. So, I'm
[0:25:01] just going to increase that a little
[0:25:03] bit. Just like that. So, the frame is a
[0:25:05] little bit bigger down here on the
[0:25:06] bottom. Right click, shade auto smooth.
[0:25:08] And there we have a computer. All right.
[0:25:10] For the mouse pad, uh, or table pad, I
[0:25:12] don't know what they call that. Uh, I'm
[0:25:14] just going to go into edit mode on this
[0:25:15] one. Shift duplicate. Right click,
[0:25:17] cancel, be separated by selection. Uh,
[0:25:19] make sure this one is selected. Right
[0:25:20] click, set origin, origin to geometry,
[0:25:23] like so. Just scale it down. Maybe go
[0:25:26] into top view. Um, maybe something like
[0:25:29] this size.
[0:25:31] Maybe a little bit smaller. Then go into
[0:25:33] edit mode. Hit A2 and E extrude
[0:25:35] everything. Apply our scale to make sure
[0:25:37] it works perfectly fine. Okay, cool. GZ.
[0:25:41] Move it a little bit down. Just like
[0:25:42] that. Um, maybe that's a little bit too
[0:25:46] big. So, we can tone that. And I don't
[0:25:48] think we need that many segments. Um, so
[0:25:50] maybe like three. Cool. Shade auto
[0:25:53] smooth. And there we kind of have like
[0:25:55] our little mouse pad thing. Uh so for
[0:25:58] keyboards generally the workflow is you
[0:26:01] go online and you look up keyboard plus
[0:26:04] cute um and then you find an image
[0:26:06] online and then right click and save the
[0:26:08] image to your desktop and then you go
[0:26:10] back into Blender shift A and add an
[0:26:13] image reference like so and then just
[0:26:15] navigate to that image. Nowadays you can
[0:26:17] just click and drag it into Blender and
[0:26:19] it'll autoimp import. If you don't like
[0:26:21] that rotation, you can quickly reset its
[0:26:23] rotation by doing alt R and it's
[0:26:25] positioned with alt g. And now you can
[0:26:27] see it's back at the world center. I
[0:26:29] don't want to do that. I'll just do alt
[0:26:30] r and then do rz90 just to rotate it a
[0:26:34] little bit. Come up here, scale it down
[0:26:35] a little bit and uh go into wireframe
[0:26:38] and just position it somewhere like
[0:26:40] here. And then since we have that, we
[0:26:42] can just shift right click to start a
[0:26:43] key. Add a plane. Scale it down to match
[0:26:47] the key a little bit like so. Go into
[0:26:49] edit mode. E to extrude that up. Scale
[0:26:51] that down a little bit. If you don't
[0:26:52] like wireframe here, um you can also go
[0:26:54] into X-ray mode, which is a very common
[0:26:57] thing. I use wireframe or X-ray. You
[0:26:59] know, I kind of switch between both of
[0:27:01] them. You can also adjust your reference
[0:27:02] image, which has a lot of properties
[0:27:04] like if you want it in front or change
[0:27:06] the visibility of it. So, if you come
[0:27:07] here, you can see you can see if you
[0:27:09] like the opacity level and things like
[0:27:11] that. So a lot of options you have um
[0:27:14] and and so let me just the typical
[0:27:16] workflow then is when you model a key
[0:27:18] you add like an array modifier and then
[0:27:20] maybe you add another array modifier but
[0:27:22] instead of in this way you go like this
[0:27:24] way or something and then you just
[0:27:26] increase the count and so on so forth
[0:27:28] and then when you're done you just apply
[0:27:30] them and then for and then since it
[0:27:33] becomes one object that's fine but maybe
[0:27:34] you want a separate object. So what you
[0:27:36] do instead is select one of the keys.
[0:27:38] Ctrl L and this will select all the
[0:27:40] linked things to your selection and then
[0:27:43] you just shift D D D D D D D D D D D D D
[0:27:44] D D D D D D D D D D D D D D D D D D D D
[0:27:44] D D D D D D D D to duplicate. Right
[0:27:45] click, cancel an P separate by selection
[0:27:46] and now you can see it becomes its own
[0:27:48] object. Then you just go back into
[0:27:50] wireframe, move this somewhere over here
[0:27:53] and of course you want to reset its
[0:27:55] origin. So right click, set origin
[0:27:56] origin to geometry. And now you can see
[0:27:58] that you kind of have a key like over
[0:28:00] here. Uh, and then you kind of just um
[0:28:04] and then you kind of just model the
[0:28:06] keyboard from that. There's another
[0:28:08] alternative where you use an SVG and
[0:28:10] just auto extrude a keyboard, which is
[0:28:13] fine, too, but there's a lot of topology
[0:28:15] issues there to clean up, and that's a
[0:28:17] little bit of an issue. If you're just
[0:28:19] going for a render, it's fine. But for
[0:28:21] us, there's kind of no reason to go with
[0:28:23] an SVG route. Uh, I'm not going to be
[0:28:25] using a reference at all because I'm
[0:28:26] just going to create something very,
[0:28:28] very basic. So, what I'm going to do,
[0:28:30] delete this one. and go into edit mode
[0:28:31] and select this one. Ctrl L. And this
[0:28:34] will select everything that is linked or
[0:28:37] connected to your selection. So if I
[0:28:40] select all these and do Ctrl L, you can
[0:28:42] see it's going to select the entire of
[0:28:43] these because all of them are connected.
[0:28:45] I'm just going to select one of them and
[0:28:47] P and separate by selection. So it
[0:28:49] becomes its own object. And then delete
[0:28:51] the rest because I want to read my array
[0:28:53] modifier that I applied. So now I'll
[0:28:55] just add my array modifier and then
[0:28:57] adjust it a little bit like this. Go
[0:28:59] into edit mode. SZZ just to scale this
[0:29:01] down a little bit. Um, a little bit nice
[0:29:04] key. Kind of like that. Then let's apply
[0:29:07] the B bevel modifier. So, select this
[0:29:10] one over here. Copy to selected. Super
[0:29:14] cool. Apply scale. Just make sure that
[0:29:16] works. Whoa, that looks a little bit too
[0:29:18] much. You can see applying scale is
[0:29:20] affecting the bevel here. So, this one
[0:29:23] I'm going to change down the amount a
[0:29:26] little bit. And if it's too fast, you
[0:29:28] can hold shift to make it a little bit
[0:29:30] smoother. So maybe about 08. Right
[0:29:33] click, shade auto smooth. Again, now we
[0:29:35] got some cute keys there. For the
[0:29:37] keyboard base, what I'm going to do is
[0:29:40] honestly probably just shift duplicate
[0:29:41] this one. Scale it down. Shift Z a
[0:29:44] little bit. Um, GZ, bring that up a
[0:29:47] little bit. Right on our keys. Super
[0:29:50] super cool. Go into edit mode. Probably
[0:29:53] bring up this edge a little bit so it's
[0:29:54] kind of a little bit stylized. Come over
[0:29:56] here. Go into side view. Just rotate it.
[0:29:59] Uh it doesn't have to be exact. You can
[0:30:02] match it with snapping if you wanted to.
[0:30:04] Uh there's like this align rotation to
[0:30:06] target property here, but I'm just going
[0:30:08] to eyeball it. Um and sometimes that's
[0:30:11] kind of all you need. And then here I
[0:30:14] want to add another ray modifier like
[0:30:16] so. And then instead of going this way,
[0:30:20] I just want to probably go in the Y
[0:30:22] direction this time. Super super cool.
[0:30:24] and just increase that like so. I don't
[0:30:27] want too many. And then probably select
[0:30:29] the whole thing and just GZ just to move
[0:30:32] it on the local Z-axis. GXX local
[0:30:37] X-axis.
[0:30:39] Then we can shift Duplicate. Right
[0:30:40] click, cancel this one. Get rid of the
[0:30:42] array modifier. Get rid of this array
[0:30:45] modifier. Go into top view. Just come
[0:30:48] over here somewhere. Um maybe scale this
[0:30:50] down a little bit. Uh, go into edit
[0:30:53] mode, wireframe, and maybe drag this out
[0:30:55] a little bit. GX.
[0:30:58] Then go back into solid view and just
[0:31:00] scale this up along the Y-axis. And now
[0:31:03] it looks a little bit too smooth. So we
[0:31:04] can just select the top face here, Sy,
[0:31:06] and bring that out a little bit. So
[0:31:08] there we have our spacebar. And then
[0:31:11] let's make sure to apply our scale. And
[0:31:13] then GZ just to bring it in a little
[0:31:16] bit. Just like that. So there we have
[0:31:18] our symbol symbol keyboard. Now, I don't
[0:31:21] like I don't like how this is so square.
[0:31:24] So, what we can do is go into edit mode,
[0:31:26] select these edges. You can actually
[0:31:29] just do shift G and select similar
[0:31:32] length in this case, and it'll select
[0:31:34] all the edges of that object that have a
[0:31:36] similar length, which is this one here.
[0:31:37] So, we don't have to go around and shift
[0:31:40] select all them. We can just select one,
[0:31:41] shift G, select similar length, and then
[0:31:44] we can do Ctrl +B to actually bevel it
[0:31:46] ourselves. And then just add a more
[0:31:48] rounded bevel. Kind of like that. If you
[0:31:50] want to increase the amount of segments,
[0:31:52] you can do controlB and use your mouse
[0:31:54] wheel to increase a little bit just so
[0:31:57] it looks a little bit smoother. And
[0:31:59] there we kind of have our keyboard just
[0:32:01] like that. Awesome. And there we kind of
[0:32:03] have our keyboard just like that. Um,
[0:32:06] and then maybe just scale it up a little
[0:32:08] bit just to make it a little bit more
[0:32:11] cute. But yeah, there we have our
[0:32:13] keyboard. Okay, let's create um probably
[0:32:15] a little plant. So, I'm just going to
[0:32:16] shift right click, add a plane, um,
[0:32:20] scale it down, go here, extrude upwards.
[0:32:23] And then I'm going to go and insert just
[0:32:25] like here, and E extrude downwards. Kind
[0:32:29] of like so. Again, same thing here. Ctrl
[0:32:32] L. This time I can just do copy
[0:32:33] modifiers. Apply my scale just to make
[0:32:36] sure that's fine. Cool. Shade auto
[0:32:38] smooth. Maybe too much here. So, maybe
[0:32:41] like three segments is okay from far
[0:32:43] away. Honestly, maybe even two. Yeah,
[0:32:46] like even two from far away. Again,
[0:32:47] there's shading issues, but not really a
[0:32:49] big deal. Um, I want to select all these
[0:32:52] and shift select all these. And I
[0:32:54] actually just want to scale that a
[0:32:55] little bit. Whoops. Let's turn off
[0:32:56] proportional editing. Let's do S. Uh,
[0:32:59] let's do alt. Let's do alt s and just
[0:33:02] squish it in a little bit. And the
[0:33:03] amount is too much for the amount of
[0:33:05] segments. So maybe we just add one more
[0:33:08] segment there. And increase the amount a
[0:33:10] little bit. Just like that.
[0:33:12] Um, so there we kind of have uh
[0:33:14] something like that. Uh, cute plant sort
[0:33:17] of thing. Or actually maybe this can be
[0:33:19] like a pen holder. So I'm going to
[0:33:20] select this face GZ and move it down
[0:33:21] there. And this can be like a pen holder
[0:33:24] rather than a plant. Okay. So for the
[0:33:27] pens or pencils, we can just shift right
[0:33:29] click somewhere, shift A, add a plane,
[0:33:32] scale it down. Go into edit mode, E and
[0:33:34] extrude upwards. And then we can e
[0:33:36] extrude upwards one more time. And just
[0:33:38] scale it down like so. And I kind of
[0:33:40] wanted to leave it a little bit just
[0:33:41] like that. Um, I'm not going to be
[0:33:43] giving this a bevel modifier primarily
[0:33:45] because it's so far away. I don't think
[0:33:47] anyone would be able to tell. And I'm
[0:33:48] just going to shift E duplicate. Shift
[0:33:51] Z. Move it around. R just to rotate a
[0:33:53] little bit. Have it leaning on this one.
[0:33:55] It doesn't matter if it's inside of the
[0:33:56] other one. Ideally, it shouldn't be
[0:33:58] inside of each other, but you know,
[0:34:01] you know, sometimes it's just you just
[0:34:04] uh got to save some time and uh just
[0:34:06] work with it. So there we kind of have
[0:34:08] like a cute little pencil holder there.
[0:34:11] Okay, now we can probably make like a
[0:34:13] flower plot or something. So I'm just
[0:34:14] just going to shift right click, add a
[0:34:16] plane, scale it down a little bit. Um,
[0:34:19] go into edit mode, E and extrude up a
[0:34:21] little bit like so. Um, probably inset
[0:34:25] here kind of like this. And just E and
[0:34:28] extrude downwards. This time I'm going
[0:34:30] to give it a subdivision surface
[0:34:32] modifier. Now instead of coming here to
[0:34:34] give a subdivision service modifier, you
[0:34:36] can just hit control or command two or
[0:34:38] three or one. And you can see it's going
[0:34:40] to adjust the amount of subdivision
[0:34:42] level it is. Um so you can do it like
[0:34:45] eight, you know, so on so forth. We
[0:34:47] don't need that many. I think three is
[0:34:48] going to be enough. Shade smooth. And
[0:34:50] you can see pretty pretty cool. We kind
[0:34:52] of have like a bowl sort of thing
[0:34:54] already. Uh and if this wants to be a
[0:34:57] little bit down, you can go down just a
[0:34:59] little bit. And if you don't like that
[0:35:02] the sides are too thin, of course you
[0:35:04] can always hold this alt s and just
[0:35:06] scale it in again. Uh, super cool. So we
[0:35:09] kind of have like a bowl there. Top is a
[0:35:11] little too thin for you. You can select
[0:35:12] the outer edge here. Um, and just do alt
[0:35:16] s and scale it up a little bit, which we
[0:35:17] can turn this off with o alt s and just
[0:35:20] make it a little bit thicker. Just like
[0:35:22] that. Scale down the whole thing. GZ.
[0:35:25] And now we kind of have like a cute
[0:35:27] little boulder. Three might be too much.
[0:35:29] So two is okay. It's starting to get a
[0:35:32] little bit weird at two, but from far
[0:35:34] away, no one's going to tell. So I'm
[0:35:35] just going to leave it at two. That'll
[0:35:36] save out on some memory there. So super
[0:35:40] cool. We have a ball there. Again, just
[0:35:42] to show that if I apply that, what that
[0:35:44] looks like. Um you can see kind of what
[0:35:47] it looks like here with the subdivision
[0:35:49] surface modifier. Also, I'm going to s
[0:35:51] shift Z. Maybe just make it a little bit
[0:35:53] smaller. For the stem, I'm going to
[0:35:54] shift right click somewhere and search
[0:35:56] for a basier curve and just add it over
[0:35:58] here. Then I'll just go into edit mode.
[0:36:01] And you can see as I edit these. Whoops.
[0:36:03] As I go here and edit these, you can
[0:36:05] kind of get a vibe like that. So with
[0:36:07] this one selected, I'm just going to
[0:36:09] shift S and selection to cursor, which
[0:36:11] will teleport it over there. And
[0:36:13] probably just scale this down a little
[0:36:15] bit here. And then for this verticy over
[0:36:17] here, I'm going to select that. And I
[0:36:19] want to lower the bar a little bit so I
[0:36:21] can see what I'm working with. I'm going
[0:36:22] to go into side view and I'm just going
[0:36:24] to bring it up kind of like this. Scale
[0:36:26] this. Scale this a little bit and kind
[0:36:29] of just make a shape like so. And with
[0:36:33] my curve selected, I'm going to come
[0:36:34] into the object, the curve data
[0:36:37] properties right here. And then I'm
[0:36:38] going to go for geometry and under bevel
[0:36:42] and round, I'm just going to hold shift
[0:36:44] and increase the resolution a little
[0:36:46] bit. So, we kind of get a stem like
[0:36:48] this. And I don't like how that bottom
[0:36:49] is kind of doing that. So, I'm just
[0:36:51] going to R Y. Change that a little bit.
[0:36:54] Maybe scale it down. Maybe grab this bar
[0:36:56] here and just bring it up a little bit.
[0:36:58] Boom. Yeah. Honestly, it doesn't really
[0:37:00] matter. Um, but there we kind of have
[0:37:03] our thing there. Okay. So, for the
[0:37:04] flower, what I'm going to do is probably
[0:37:06] shift right click somewhere. It doesn't
[0:37:07] really matter where. And just add a
[0:37:09] cube. Scale it down a little bit.
[0:37:10] Control 1 to add that subdivision
[0:37:12] surface modifier. Shade smooth. S just
[0:37:15] to scale it down. Yeah, it doesn't look
[0:37:17] great. We could crank this up if we
[0:37:18] wanted to to make it look nicer, but
[0:37:20] it'll be far away. Uh, so there we have
[0:37:22] the center of our flower. Then for the
[0:37:25] leaf itself, we can just actually just
[0:37:26] duplicate this and just gy move it over
[0:37:29] here. Sy, scale it up a little bit. Um,
[0:37:33] like so. Maybe we want to turn this one
[0:37:35] to two so we have a little bit more
[0:37:37] geometry to work with. Then I'll add a
[0:37:38] loop cut here and probably just do sx.
[0:37:41] Scale up a little bit and scale this in
[0:37:44] kind of like so. Uh, and then let's go
[0:37:47] into wireframe to make sure I select the
[0:37:48] bottom vertices as well. And kind of
[0:37:50] just scale this down here. Maybe make
[0:37:52] this taper off a little bit. Maybe add
[0:37:54] another loop cut here to bring that up.
[0:37:57] And then maybe something over here. Kind
[0:37:59] of just plump it up here. Whereas this
[0:38:01] kind of goes down just like that. Or we
[0:38:03] can turn off proportional editing if you
[0:38:05] think that helps. You can turn on
[0:38:07] proportional editing like so. Um, but
[0:38:11] anyway, there's kind of like our fly
[0:38:13] right there. Uh, that's seems like a
[0:38:16] little bit too big there. And uh, this I
[0:38:19] kind of want to Whoops. Let's go into
[0:38:20] wireframe. Um, this I kind of want to
[0:38:23] taper just a little bit more.
[0:38:26] But again, it's really up to you. And if
[0:38:28] you want extra detail cuz you're getting
[0:38:30] close, you can add like a loop cut here
[0:38:32] and like bring it down sort of thing.
[0:38:34] Uh, and then if you want more detail,
[0:38:36] you can like add a bevel. Um, and then
[0:38:38] you get a small line. Mess with it more
[0:38:40] if you want to. Uh, I'm just going to
[0:38:42] keep it really simple. Uh, kind of just
[0:38:44] like this. Okay. So, now what I want to
[0:38:46] do is create a lot of these around this
[0:38:50] sort of this object right here. So, what
[0:38:52] I'm going to do is shift S and cursor to
[0:38:55] selected. It will snap to the origin
[0:38:57] point of this object here. Make sure
[0:38:59] your origin point is in the center. If
[0:39:00] not, again, that's set origin origin to
[0:39:02] geometry. And then what we can do is
[0:39:04] instead of rotating around the bounding
[0:39:06] box center or the average of like the
[0:39:08] items kind of thing, we can do around
[0:39:10] the 3D cursor. Now you can see when I
[0:39:11] hit R, it's rotating around the 3D
[0:39:13] cursor rather than the origin point. So
[0:39:15] now what I can do is select this, shift
[0:39:18] Duplicate, hit R on our keyboard, and
[0:39:21] then type in 60 and then hit enter. So
[0:39:24] we did all of that in one go. And now
[0:39:27] what we can do is just do shift R, shift
[0:39:29] R, shift R, shift R, and it'll create
[0:39:32] our flower. just for us. Just like that.
[0:39:34] So, one more time. Again, just one more
[0:39:36] time. Actually, I'm going to do Alt D
[0:39:38] this time for link duplicates. So, if
[0:39:40] you edit one, it'll edit the other one.
[0:39:42] Um, so, sorry, I did say shift D
[0:39:45] initially, but I'm going to do alt D.
[0:39:47] Anyway, what I'm going to do is hit alt
[0:39:49] D
[0:39:51] and I'm going to hit R. By default, it's
[0:39:54] already grabbed when you hit alt D or
[0:39:56] shift D. So, I'm going to hit R instead
[0:39:58] and then it will go into rotate mode.
[0:40:01] That's type 60. Hit enter. And then
[0:40:04] shift R will repeat the last operation
[0:40:06] you just did. So we'll do shift R, shift
[0:40:09] R, shift R, shift R. And that way we
[0:40:11] have six pedals around here. And now if
[0:40:13] I edit any single one of them, SC kind
[0:40:16] of like that. You can see that it's
[0:40:19] going to edit the other one. And that's
[0:40:20] because these are instance instances
[0:40:23] rather than hard copies. Yeah. So of
[0:40:25] course you can always, you know, go here
[0:40:28] and edit it if you want. I just, you
[0:40:30] know, have some fun like so. Okay. So,
[0:40:32] once you get a flower that you like, I'm
[0:40:34] actually not going to ever come back to
[0:40:36] this flower. So, what I'm going to do is
[0:40:38] just select everything and with this
[0:40:40] active object, just do Ctrl + J. And now
[0:40:42] they're kind of all joined as one single
[0:40:44] object. If you have different
[0:40:46] subdivision levels on either of them,
[0:40:48] it's going to take the one that your
[0:40:49] active object has. So, just be uh
[0:40:52] conscious of that. Um, but I kind of
[0:40:54] like my flower, so I'm just going to
[0:40:56] leave it as is. Then I'm going to go
[0:40:58] into edit mode, select this vertex here,
[0:41:01] shift S, cursor to selected, snap it
[0:41:03] there. Select this, shift S, selection
[0:41:06] to cursor, and it'll just snap there.
[0:41:08] Scale it down a little bit. And then our
[0:41:11] rotate it again. It's rotating along my
[0:41:13] 3D cursor. So let's move this back to
[0:41:16] bounding box center. Maybe scale this up
[0:41:18] a little bit. Um, and there we kind of
[0:41:21] have our cute little flower right there.
[0:41:23] Now, of course, if you want to give some
[0:41:25] variation to, you know, some of the
[0:41:27] flowers so they're not identical, uh,
[0:41:29] you can totally do that if you want to.
[0:41:31] Just like some slight distortions. Okay.
[0:41:34] So, now I want to add like a calendar
[0:41:35] sort of thing. So, I'm just going to
[0:41:36] shift right click somewhere. I don't
[0:41:38] know, maybe here. And let's just put it
[0:41:39] over here. And then add a plane. Type
[0:41:41] plane. Scale it down just like so. Make
[0:41:43] it a little bit longer on the Y, smaller
[0:41:46] on the X. Go into edit mode. A E to
[0:41:49] extrude up. SX. Just bring it in. Bring
[0:41:52] this up a little bit. Kind of just like
[0:41:54] that. Then we can go here, apply our
[0:41:57] scale, go into edit mode, select these
[0:41:59] two faces, hit I to insert, then hit X
[0:42:02] to delete those faces. Then holding alt,
[0:42:05] select this loop, holding shift and alt
[0:42:07] to select this loop. Select both of
[0:42:09] them. Then do Ctrl + E and do bridge
[0:42:12] edge loops right here. And it'll kind of
[0:42:14] fill that inside for us. Just like that.
[0:42:17] Um, so I guess that's okay, but I kind
[0:42:21] of don't want this bulky thing here. So,
[0:42:23] we could just like make that a little
[0:42:25] bit smaller. Or if we don't like that,
[0:42:27] we can just select these faces and uh
[0:42:32] just delete those faces. Then select
[0:42:34] these edges like so. Uh, and then since
[0:42:36] we have face snapping on, I can just do
[0:42:38] GZ and snap it down to this face. Um,
[0:42:42] and then we can delete this face because
[0:42:43] we no longer need that. Uh, so there we
[0:42:46] kind of have a little bit of our
[0:42:47] calendar thing. Uh, I feel like it's a
[0:42:50] little bit too wide. So what I'm going
[0:42:52] to go into edit mode, probably select
[0:42:54] this side and just GX a little bit.
[0:42:57] Cool. Uh, then we can just copy over a
[0:43:00] bevel modifier. Ctrl L, copy modifier
[0:43:02] just to see how that looks. Apply scale
[0:43:04] shade auto smooth. Cool. Uh, then we
[0:43:07] kind of have our calendar thing there.
[0:43:09] Um, for the page itself, let's just
[0:43:11] select this phase. Shift Duplicate,
[0:43:13] right click, cancel. piece already by
[0:43:15] selection. And now this will be here.
[0:43:17] And we can go into edit mode. A to
[0:43:18] select everything and just extrude it
[0:43:20] outwards. There we now we kind of have
[0:43:22] like a calendar page. Scale it down
[0:43:24] maybe just a little bit like that. Okay.
[0:43:26] For the rings of the calendar, I think
[0:43:28] what would I'm just going to shift right
[0:43:30] click somewhere here and add a cylinder.
[0:43:34] And instead of 12, maybe we do like 16
[0:43:37] this time. Um because it might be
[0:43:39] noticeable. So let's just uh scale it
[0:43:42] somewhere here. RX90 to rotate it. Uh S
[0:43:45] Y just to scale it a little bit. Kind of
[0:43:48] like this. Shade auto smooth. Um that's
[0:43:52] okay. Let's go into edit mode. Let's uh
[0:43:55] insert these faces and delete them. And
[0:44:00] then let's shift alt shift alt select
[0:44:03] both of those loops like that. Control E
[0:44:06] bridge edge loops again. So now we kind
[0:44:08] of have a ring. Okay. Okay. So now what
[0:44:10] we want to do is add an array modifier.
[0:44:12] And um I'm going to put it in the Z
[0:44:15] direction. I think it's going into the
[0:44:16] local Z direction. And then I just want
[0:44:18] four of those just like this. And then
[0:44:20] we can like um gy and move it just so
[0:44:23] it's kind of even in space here for this
[0:44:25] bottom area. H I don't know if we'll
[0:44:27] ever see that. But what we can do is go
[0:44:29] into wireframe and just select these
[0:44:32] vertices down here and just hit X and
[0:44:35] delete those vertices. We'll come back
[0:44:37] and clean up everything a little bit
[0:44:38] later, but now we kind of have like our
[0:44:41] little cute little calendar thing here.
[0:44:43] Okay, for our speaker, uh, what I'm
[0:44:45] going to do is use two really, really
[0:44:48] helpful Blender add-ons. So, to get
[0:44:50] Blender add-ons these days, you have to
[0:44:52] go to their website on here. And the
[0:44:54] first one I want to use is Loop Tools.
[0:44:56] And this is an extremely popular add-on.
[0:44:58] You'll see it in a lot of Blender
[0:45:00] tutorials. You can just click and drag
[0:45:02] it into Blender and it will install. and
[0:45:05] then eventually ask you to enable it.
[0:45:08] Um, so I just clicked on it. You can see
[0:45:10] I already have it installed, but it'll
[0:45:12] just say activate and then you just hit
[0:45:15] activate. The other add-on I'm going to
[0:45:17] be using is extra mesh objects, which
[0:45:19] used to be in Blender natively in the
[0:45:22] older versions, but now it's on this
[0:45:24] story. Again, you just click and drag it
[0:45:25] and install like so. Okay, so for our
[0:45:27] speaker, I'm going to shift right click
[0:45:29] somewhere and add a round cube. This is
[0:45:32] part of the extra objects. And the
[0:45:34] reason we're using a round cube instead
[0:45:36] of a sphere is just because of the way
[0:45:38] that it's created. It'll help us a lot
[0:45:40] better than if we used a UV sphere. It
[0:45:42] won't be perfect, but it will be better.
[0:45:45] So, if I scale it down just arbitrarily,
[0:45:47] bring it up a little bit. Let's go into
[0:45:49] local view. Let's go into a side view.
[0:45:51] Let's go into wireframe. Let's go into
[0:45:54] edit mode, vertex select, and possibly
[0:45:56] select about here. Make sure we got
[0:45:58] everything. Cool. We did. And just do
[0:46:00] SZ0. And this will just level out
[0:46:03] everything on the same level. Then we
[0:46:05] can go back out into regular mode. Just
[0:46:08] scale that down a little bit. Cool. Uh
[0:46:11] just like so. And since our cursor is
[0:46:15] already down at the bottom, what we can
[0:46:16] just do right now is object set origin
[0:46:19] origin to 3D cursor. That way we'll just
[0:46:21] scale and all our transforms come from
[0:46:23] there. Then let's go back into solid
[0:46:26] view. Let's just select some faces. So
[0:46:28] maybe like here, control plus. Um, and
[0:46:31] then let's just control shift. And then
[0:46:34] let's just do control shift to select
[0:46:36] this side. Control shift to select this
[0:46:38] side. And then what we can do is just E
[0:46:40] and extrude it in just a little bit like
[0:46:42] that. And then we can rightclick a shade
[0:46:44] auto smooth. And then we can just copy
[0:46:46] over a bevel modifier. Ctrl L, copy
[0:46:48] modifier. And now you can see we kind of
[0:46:50] have a small cute little speaker just
[0:46:53] like that. And you can definitely see
[0:46:55] that this model also has some shading
[0:46:57] issues here. For us, it's not going to
[0:46:58] matter because we're so far away. And
[0:47:00] fixing it would take too much time and
[0:47:02] it's a little too advanced uh for this
[0:47:04] video. So, we can just leave it as is.
[0:47:06] However, we can fix a little bit of this
[0:47:08] if we go into profile and just adjust
[0:47:10] the shape a little bit and just kind of
[0:47:12] bring that up to like about here. So, it
[0:47:15] solves a little bit of our issues, but
[0:47:17] again, it doesn't really matter. Okay.
[0:47:19] And now I want to make some headphones.
[0:47:21] So, I'm going to make a headphone stand.
[0:47:22] First, I'm just going to shift right
[0:47:23] click somewhere. Shift A. Add a plane.
[0:47:26] Scale it down. Uh maybe SX a little bit.
[0:47:29] Kind of make it a little bit like that.
[0:47:31] Go into edit mode. E to extrude upwards.
[0:47:34] Um going to apply my scale. And this
[0:47:36] time I actually just want to give the
[0:47:37] bevel modifier right now. So I'm going
[0:47:38] to do CR L copy modifiers. Just like
[0:47:40] that. Shade auto smooth. And then select
[0:47:44] this edge. Shift G. Select similar
[0:47:46] length. Ctrl +B. Um and then I think we
[0:47:50] can go like this. But I don't want it to
[0:47:52] go inside. So I'm going to hit C and
[0:47:54] it'll just clamp it kind of like that.
[0:47:56] Um but I just want it like so. Shade
[0:47:59] smooth. Cool. Again, shading issues, but
[0:48:02] it's totally okay for us. Uh then in
[0:48:04] here, I'm probably just going to insert
[0:48:06] a little bit and then just extrude it
[0:48:07] down just to give some sort of inset
[0:48:09] there. Then I actually want it a little
[0:48:12] bit thicker. So I'm just going to select
[0:48:14] this edge loop
[0:48:16] and then hit alt s
[0:48:18] kind of inflate that a little bit there.
[0:48:20] or scale along the normals. Cool. Okay.
[0:48:23] So, for the stand itself, I'm going to
[0:48:25] go really basic. I'm just going to shift
[0:48:26] right click somewhere and I'm going to
[0:48:28] add a cylinder this time. And I'm at
[0:48:31] eight, but maybe I'll go to like 12
[0:48:33] because it'll be pretty noticeable.
[0:48:34] Whoops, not that. 12. And then I'm just
[0:48:37] going to scale it down here. S, shift Z.
[0:48:40] Uh, go into edit mode, GZ. Snap it to
[0:48:42] the face up there. You don't have to. I
[0:48:44] just like having the origin point there.
[0:48:47] Um, so maybe something like this. I
[0:48:49] don't want it too tall, but I definitely
[0:48:51] want it noticeable. Shade auto smooth.
[0:48:53] Cool. Maybe have it a little bit
[0:48:56] bulkier. Just like that. Add a mirror
[0:48:58] modifier. Select this as our object.
[0:49:02] Cool. Uh, and then we can just shift
[0:49:04] right click over here
[0:49:07] and add a maybe we can add another
[0:49:09] cylinder. And this time we probably only
[0:49:11] need like eight. So I'm just going to
[0:49:12] scale it down like so. And then R Y 90.
[0:49:16] Just like that. Go into edit mode.
[0:49:17] select this this face here and then just
[0:49:20] GX and snap it over here. So there we
[0:49:23] kind of have like our pole thing. Uh and
[0:49:24] then S shift X just to make it a little
[0:49:27] bit smaller than the other beams
[0:49:28] themselves. Cool. I don't know if that
[0:49:31] particularly matches because it kind of
[0:49:33] looks like there's edges there. From far
[0:49:36] away though with the headphones on
[0:49:38] there, I don't think anyone can tell. So
[0:49:39] we're just going to leave it as is.
[0:49:41] Okay. For the headphones, uh let's start
[0:49:43] with a cube. So I'm just going to shift
[0:49:45] a add a cube somewhere. This time, let's
[0:49:46] go into local view. So, I'm just going
[0:49:48] to go into local view. Let's go into a
[0:49:49] side view here. Let's do control one
[0:49:51] again. That just adds a level one
[0:49:53] subdivision surface. Actually, let's do
[0:49:55] control 2. Let's right click, shade
[0:49:57] smooth. Then, let's just do S uh
[0:50:00] probably S Y and kind of just get a
[0:50:02] general shape like this. I'm going to
[0:50:04] shift D, duplicate that, and just move
[0:50:06] it over to the side. And then for this
[0:50:08] one, I'm just going to add a simple loop
[0:50:10] cut. Um, maybe like over here. So, it
[0:50:12] kind of is with this one. Um, and then
[0:50:17] maybe I will select this face here and
[0:50:19] insert a little bit. And then just e
[0:50:21] extrude it inwards a little bit. So we
[0:50:23] kind of have a small little inset there.
[0:50:25] And then we kind of have our earphones.
[0:50:27] Um, and then maybe I'll just scale it up
[0:50:30] here a little bit. If you want, you can
[0:50:31] add like loop cuts and kind of style it.
[0:50:33] But I'm going for some really really
[0:50:35] simple um, headphones.
[0:50:39] Super cool. So usually headphones are
[0:50:41] rotated a little bit when they're
[0:50:42] resting. So, we can rotate it both of
[0:50:44] these just a little bit. Kind of like
[0:50:46] so. Uh, then for the top, we can just
[0:50:48] arbitrarily shift right click somewhere
[0:50:50] in the center here and add a cube and
[0:50:54] scale it down like so. GZ. Bring it up a
[0:50:56] little bit. Let's go back here and let's
[0:50:58] just eyeball the rotation. Doesn't have
[0:51:00] to be accurate. Let's go into edit mode,
[0:51:02] wireframe to select all the vertices and
[0:51:05] just bring it up kind of just like so.
[0:51:07] Cool. So, now what we can do is probably
[0:51:10] S Y just to scale it a little bit. kind
[0:51:12] of like this. And then we can also give
[0:51:14] a control 2 or control one should be
[0:51:16] enough subdivision surface modifier. And
[0:51:18] now let's add some bracing edges or
[0:51:21] control loops which we call them on all
[0:51:24] of the sides like so. And then here I
[0:51:28] don't want proportional editing. Sx. And
[0:51:30] I'm just going to scale it up just like
[0:51:31] that. And then let's just do shade
[0:51:33] smooth. Recall. So we kind of have that
[0:51:35] initial one. And then we can just
[0:51:37] duplicate this and make a another one
[0:51:40] right on the top. So, this is going to
[0:51:41] be overlaying just like this. SX just to
[0:51:44] scale it like so. It doesn't matter that
[0:51:46] it looks a little bit off. Um, you know,
[0:51:49] from far away, no one's going to tell.
[0:51:50] So, there we kind of have our other
[0:51:52] stuff. Um, so I feel like this is a
[0:51:55] little bit too large. Uh, so I'm just
[0:51:57] going to scale it along its local
[0:51:58] Z-axis, GZ. Move it down a little bit.
[0:52:01] And then this one can uh come down a
[0:52:04] little bit more. SCZ.
[0:52:07] You know, we just need some
[0:52:08] differentiation, but I don't want uh it
[0:52:11] to be too inaccurate. Even though we're
[0:52:12] going stylist, I feel like that's a
[0:52:14] little bit better. Cool. And then maybe
[0:52:16] expand this a little bit more. So, what
[0:52:18] I'm going to do now is just duplicate
[0:52:19] this. Uh, and then what I'm going to do
[0:52:21] is select all of these and do S Y and
[0:52:24] then hit Y again for the local Y-axis
[0:52:26] and then do negative one. And this is a
[0:52:28] really quick way just to mirror your
[0:52:29] object. So again, if I show that on like
[0:52:33] a extruded cube, let me just show you
[0:52:35] real quick. And I Well, oh, sorry, wrong
[0:52:38] wrong face. If I extrude this and I do s
[0:52:41] Y minus one, you can see it's just going
[0:52:44] to create that, right? So S Y - one is
[0:52:46] going to go like that. Now, I want to
[0:52:48] create that thing that you put on your
[0:52:50] head or rests on your head. I don't know
[0:52:51] what that's called. Now, there's quite a
[0:52:53] few methods to approach this. I'm going
[0:52:55] to be using a much more simple method,
[0:52:58] but it works for what we're going to be
[0:53:00] doing. So, what I'm going to do is I
[0:53:02] want the it to be a little bit bigger.
[0:53:04] So, I'm going to select these three
[0:53:05] faces. Remember, we added these edge
[0:53:08] loops, guard loops here. So, they are
[0:53:10] also part of the top face. Make sure to
[0:53:11] select that. Shifty duplicate, right
[0:53:14] click, cancel the movement, and just
[0:53:15] scale it up. Scale it up just a little
[0:53:17] bit like that. Cool. So, now we have
[0:53:20] something sort of like that. All right.
[0:53:22] Let's do that again. Let's shift
[0:53:24] duplicate that. And let's go into a side
[0:53:27] view here. And let's bring this one up
[0:53:30] to like where you think um your earphone
[0:53:34] headrest would be or like the tip of it
[0:53:37] pretty much. And then you rotate it
[0:53:39] arbitrarily to kind of get it
[0:53:41] perpendicular to whatever axis you're
[0:53:42] working on. In my case, it's Y. And then
[0:53:45] once it's near like you can just do S Y
[0:53:47] and then zero. And that'll just flatten
[0:53:49] out everything to make sure it's up
[0:53:51] completely perpendicular. Let's make
[0:53:53] sure we're in wireframe to select
[0:53:54] everything.
[0:53:56] So, uh, you can just guess, but you can
[0:53:58] always make adjustments later. So, if
[0:54:00] you're too high, too low, it's not
[0:54:01] really a big deal. So, now what we can
[0:54:03] do is select this, Ctrl L, just to
[0:54:06] quickly select linked or just select
[0:54:09] each one or, you know, control, you
[0:54:11] know, make sure you're actually
[0:54:12] selecting this one and not the inner
[0:54:14] one. Cool. And now what we can do is
[0:54:17] hold shift and select these as well. And
[0:54:20] then what we can do is Ctrl + E bridge
[0:54:22] edge loops. And you can see that okay,
[0:54:24] doesn't look great, but we can fix this.
[0:54:27] So if I come Whoops, I accidentally
[0:54:29] exited the menu. That's totally okay.
[0:54:30] You can just hit F9 to open your last
[0:54:33] menu of your operation.
[0:54:35] So what we can do, I might have
[0:54:37] different immediate defaults than you
[0:54:39] do. So just make sure to check for that.
[0:54:41] And what we can do is increase the
[0:54:43] number of cuts. And you can see already
[0:54:44] we kind of have something like that. Uh
[0:54:46] yeah. So I think six cuts is enough for
[0:54:49] us. I don't think we need any more than
[0:54:51] that. So um let's just check. Yeah, that
[0:54:54] looks okay. And then we can just do
[0:54:56] shade smooth like so. And then there we
[0:54:58] kind of have our top there. Now
[0:55:00] generally what we should have done was
[0:55:02] probably put some sort of mirror object
[0:55:04] here and not rotate these. That way it
[0:55:06] wouldn't be as confusing as what we're
[0:55:08] doing now. But that's totally okay
[0:55:09] because we can learn from that. So what
[0:55:10] we can do is select this edge loop here.
[0:55:13] Go back into a side view. And now we
[0:55:16] definitely need proportional editing.
[0:55:17] And just uh increase this a little bit
[0:55:20] until we get something that we like.
[0:55:22] Let's add a mirror modifier now. And
[0:55:26] here we wanted to do it along the Y. And
[0:55:28] then let's go into edit mode. G YY. Just
[0:55:30] move it out like so.
[0:55:33] Just so it's kind of like over here
[0:55:35] again. We want to turn on clipping. GY.
[0:55:38] Move it inside. So it's like so. Let's
[0:55:41] go into wireframe. Make sure these are
[0:55:43] kind of out. Cool. Um, and now we can
[0:55:46] just I guess we'll work from this
[0:55:48] location instead. So, GZZ. Um, like so.
[0:55:53] And kind of just bring it out
[0:55:54] arbitrarily.
[0:55:57] Center just a little bit. Uh, and now
[0:56:00] what we can do is actually delete this
[0:56:02] one because it's mirroring this entire
[0:56:04] thing. So, now we can just plug this in
[0:56:06] here somewhere arbitrarily like so. Uh,
[0:56:08] then we can just select the top cuz I
[0:56:09] want it a little bit thicker. Ctrl L.
[0:56:12] And uh probably let's turn off
[0:56:14] proportional editing. SX and just give
[0:56:17] it some depth a little bit there. Maybe
[0:56:19] select these top ones over here like so.
[0:56:23] And alt S and make those a little bit
[0:56:25] wider than the other ones. And then if
[0:56:28] you want the padding inside, you can
[0:56:29] totally do that. You can just like
[0:56:30] select these faces here. I'm holding
[0:56:31] control just to select those faces.
[0:56:33] Right. Shift Eyee duplicate. Right
[0:56:36] click. Cancel. Eextrude out a little
[0:56:38] bit. Cool. Uh cool. And there we kind of
[0:56:41] have like a a little bit more of a puff
[0:56:43] there. And then probably SX just to
[0:56:45] scale it up a little bit. Um maybe
[0:56:48] select these alt s just to make it a
[0:56:51] little bit more puffy. I don't know.
[0:56:53] Really up to you there. Uh so yeah, a
[0:56:56] little bit messy, but we did end up
[0:56:58] getting our headphones. So that's
[0:56:59] totally okay. So let's just scale that
[0:57:01] down. Let's come over here. Let's shift
[0:57:04] right click. And then with everything
[0:57:05] selected, shift S. Selection to cursor
[0:57:07] keep offset. So keep everything. So keep
[0:57:10] everything in line. If you do shift S
[0:57:12] selection to cursor, it'll snap every
[0:57:16] origin points object to that. So do
[0:57:19] shift S selection to keep offset. Scale
[0:57:21] it down or maybe something like so. GZ.
[0:57:25] And uh we can just kind of place it just
[0:57:28] like that. Uh so not particularly
[0:57:29] accurate. We can just scale this down on
[0:57:31] the Y a little bit. Scale this down. I
[0:57:33] want it a little bit more stylized. Um
[0:57:36] so maybe that's a little bit too much.
[0:57:38] Now, uh, these I don't want to touch.
[0:57:40] So, I'm just going to g y move those
[0:57:43] over here.
[0:57:45] Um, g y move that back here. Uh, so now
[0:57:50] we kind of have our headphones here. And
[0:57:52] of course, we can just adjust this a
[0:57:54] little bit. Um, really up to you. And I
[0:57:58] think we can actually just join these
[0:57:59] now. Uh, so let's apply our mirror
[0:58:01] modifier for this one. And, um, yeah,
[0:58:05] let's select this. Select all of these.
[0:58:08] Probably just Ctrl + J and join them
[0:58:10] now. And let's crank this up to two.
[0:58:13] Cool. Then what we can do is just, I
[0:58:15] don't know, play around with it until
[0:58:16] you get something that you like. And
[0:58:18] then now we can go into edit mode and go
[0:58:20] into wireframe. Um, and probably just,
[0:58:24] you know, rotate these up a little bit
[0:58:25] with proportional editing just so we get
[0:58:28] like a curve or something. Uh, maybe
[0:58:30] select a little bit more here. Um, let's
[0:58:33] include the bottom here as well.
[0:58:35] Same thing over here. Let's just rotate.
[0:58:38] Get something closer.
[0:58:40] Um maybe all of these like so.
[0:58:43] Cool. And it looks a little bit too
[0:58:46] small to everything. So, let's just
[0:58:48] scale up everything kind of just like
[0:58:50] that. Yeah. So, maybe if you watch this
[0:58:52] at the start of the video, I'll talk
[0:58:53] about how I start off with a room. But,
[0:58:56] I actually want to go for more like a
[0:58:58] open vibe rather than a room. Or else I
[0:59:00] think I'm going to actually get rid of
[0:59:02] this. I'll just keep it for like a maybe
[0:59:05] collection, but I don't think I'll be
[0:59:06] using that anymore. So, I'm just going
[0:59:07] to hide all that. Then, shift S, cursor
[0:59:10] to world origin, shift A, and I'm just
[0:59:12] going to add a plane, and just scale it
[0:59:14] up like so. Then, I go into edit mode,
[0:59:17] select these edges, and just extrude
[0:59:20] upwards. And let's delete this face
[0:59:22] here. Um, and let's give all of these,
[0:59:26] well, let's go back to object mode,
[0:59:28] apply our scale first. Let's go into
[0:59:30] edit mode and let's just control B and
[0:59:32] bevel and give it some a bunch of loop
[0:59:34] cuts just like that. Shade smooth, shift
[0:59:36] S. Bring it out just like that.
[0:59:41] Cool. So now we kind of have like a
[0:59:42] domain that we can work with, which we
[0:59:44] can also edit a little bit later if we
[0:59:46] want to. So now what we can do is let's
[0:59:48] just uh select these and whoops,
[0:59:50] deselect that with control and just move
[0:59:52] this somewhere else because I want my
[0:59:54] computer to live here. So, for Okay, so
[0:59:56] for a gaming PC, I'm going to shift
[0:59:58] right click somewhere and I'm going to
[1:00:00] add a plane. Probably go into top view
[1:00:02] and kind of just give a rough shape of
[1:00:04] what I want my uh PC to look like. So, I
[1:00:08] think I'm going to go like over here,
[1:00:09] add some loop cuts here. Um maybe add
[1:00:12] some loop cuts here. I don't actually
[1:00:14] know. So, that's why I'm kind of just
[1:00:15] adding a little bit more than I normally
[1:00:18] should. Um we might only need a few. I
[1:00:21] don't really know. Um, so it's fine. Uh,
[1:00:26] but maybe we can have like a gaming PC
[1:00:28] like this.
[1:00:30] And then we can select these two here
[1:00:32] and probably hit F to fill. So we kind
[1:00:34] of get like a small little corner there.
[1:00:36] Um, and then actually maybe we want a
[1:00:39] corner here as well. So we could like
[1:00:40] drag that in. Or or what we can do is
[1:00:44] actually just delete those edges and um
[1:00:49] just hit F to fill that. So we kind of
[1:00:51] have like a more more stylized
[1:00:54] um here. I don't maybe I just maybe I
[1:00:57] don't want it like this on that side. So
[1:01:00] here now we can have something that I
[1:01:01] like. Let's go into edit mode, hit A and
[1:01:03] just E and extrude that outward. That'll
[1:01:05] be the base. Then we can hold then we
[1:01:08] can just copy our modifier right now.
[1:01:10] Just like so. Shade auto smooth. Cool.
[1:01:14] So there's kind of like our base right
[1:01:15] there for our computer. Okay. For the
[1:01:17] glass center, what we can do is just use
[1:01:20] this. So, let's go into edit mode. Um,
[1:01:23] doesn't really matter. I'm going to hold
[1:01:24] Alt to select the edge loop. Uh, and it
[1:01:28] seems like we probably messed up
[1:01:29] somewhere because it's not selecting the
[1:01:31] whole edge loop, but it's totally okay.
[1:01:33] It doesn't really matter. We can hold
[1:01:35] shift alt and just select the remaining
[1:01:36] stuff. Um, and then I'm think I'm just
[1:01:39] going to hit E and extrude upwards on
[1:01:41] the Z-axis kind of like so.
[1:01:44] Um, then let's go into face select. Hold
[1:01:48] alt to select the entire loop there.
[1:01:50] Then let's go into face select and just
[1:01:52] select this whole loop here and P and
[1:01:54] separate by selection. So now it becomes
[1:01:56] its own thing. And just scale it in.
[1:01:58] Oops. S shift Z a little bit. Just like
[1:02:00] that. Scale it up to a height that you
[1:02:02] like. Maybe like S. Like so. And then
[1:02:06] for the top, shift D. Duplicate this and
[1:02:08] bring it over here. Let's just readjust
[1:02:10] everything so they're kind of sitting on
[1:02:13] top. So there we kind of have like our
[1:02:15] gaming PC. And this side looks a little
[1:02:18] bit too cornered. So what we can do is
[1:02:20] go into edit mode and select these
[1:02:23] vertices. Um let's make sure we select
[1:02:26] everything. So we can go into wireframe.
[1:02:28] Just select over here. Doesn't matter if
[1:02:30] you select the back. You can hold
[1:02:31] control and box select to deselect
[1:02:33] those. So it seems like we got
[1:02:35] everything here. So what we can do is go
[1:02:36] into solid GX and just move it up a
[1:02:39] little bit. Again, we're getting some
[1:02:40] shading issues, but that's totally okay.
[1:02:43] So yeah, and now we can just adjust it.
[1:02:45] Maybe these can be bigger. So instead of
[1:02:48] uh bounding box center, let's change
[1:02:50] individual origins. Make that a little
[1:02:52] bit bigger. Change back to bounding box
[1:02:53] center. Okay. So when it comes to the
[1:02:55] GPU fans and things like that, basically
[1:02:58] it kind of looks like this. And then you
[1:02:59] have your fan in the center like here.
[1:03:01] Let me just show you what most people
[1:03:03] would do is they would add a plane like
[1:03:07] over here. You can just watch for now.
[1:03:09] They would add a plane and then they
[1:03:11] would probably add a cylinder. So let's
[1:03:13] just add a cylinder. Come over here and
[1:03:16] just place it in the center. GZ like
[1:03:18] here. Add a boolean modifier. So if you
[1:03:21] used design software before, you've
[1:03:22] probably seen something like this. It
[1:03:24] also exists in 3D. Then you just select
[1:03:27] difference, select the cutout object as
[1:03:30] your cutting out object. And you can see
[1:03:32] that okay, now it's cutting out
[1:03:34] something here. You can't see it yet
[1:03:36] because it's not applied. But if you
[1:03:38] want to see it move around, you can come
[1:03:40] over here, go into object, go into
[1:03:43] viewport display right here, and then
[1:03:45] instead of texture, change it to bounds.
[1:03:47] Now, the object itself is still the
[1:03:49] same. But now you can see if you were to
[1:03:52] apply this, how it would cut out from
[1:03:54] your object. I'm just going to change
[1:03:56] that back to textured. Then let's come
[1:03:57] back over here and apply this boolean
[1:04:00] modifier. So now I can just delete this.
[1:04:01] And you can see that okay, indeed, we
[1:04:04] have something like this. for you it
[1:04:06] might work properly perfectly fine um
[1:04:10] and you would have like no issues. So it
[1:04:12] might work fine for you. Here you can
[1:04:14] see like okay it's not terrible uh and
[1:04:17] it doesn't seem like there's too many
[1:04:19] shading issues. So if you're just going
[1:04:20] for something like this it doesn't
[1:04:22] really have any issues, right? But look
[1:04:24] what happens when you shade auto smooth.
[1:04:26] You can start seeing some a little bit
[1:04:28] of shading issues right here and over
[1:04:31] here and over here. Honestly, it might
[1:04:33] not be a big deal if you're from far
[1:04:35] away. However, if you are close, it
[1:04:36] might be noticeable and it might look a
[1:04:38] little bit weird. You can cover that up
[1:04:40] with possibly normal textures and some
[1:04:42] other sort of trick, but it's kind of
[1:04:44] better just to avoid this entirely. Now,
[1:04:47] you definitely can fix this up if you
[1:04:49] want to, but that's a little too
[1:04:50] advanced and too timeconuming for this
[1:04:52] beginner course. So, we're going to
[1:04:54] avoid this method and we're going to use
[1:04:55] a different method. So, instead, what
[1:04:57] I'm going to do is shift A and add a
[1:04:59] plane and bring it up over here like so.
[1:05:02] and go into edit mode and subdivide it
[1:05:04] probably like three times like so. Then
[1:05:07] I'm going to go into top view. I'm going
[1:05:08] to select the probably these faces right
[1:05:11] here. I'm going to rightclick and again
[1:05:13] loop tools and change it into a circle.
[1:05:16] Then I'm going to hit I for like a guard
[1:05:18] loop something over here. Let's go back
[1:05:21] and just select these out a little bit
[1:05:22] and scale it up a little bit. Just like
[1:05:25] that. Now what we can do is hit control
[1:05:26] minus just to less our selection or
[1:05:29] again that's select more or less and
[1:05:31] then less right here. And then we can
[1:05:32] just delete these interfaces.
[1:05:35] So now we're left with this place for
[1:05:37] our fan. We can actually select this
[1:05:39] edge loop outside because it's a little
[1:05:41] bit too big and we don't want all that
[1:05:43] extra space. And then we can actually
[1:05:45] just delete these faces. So now we kind
[1:05:47] of have something like this. Super super
[1:05:49] cool. And now when I add a solidify
[1:05:53] modifier like so. We could just extrude,
[1:05:55] but I'm just going to add a solidify
[1:05:57] modifier. Uh then we can add an array
[1:05:59] modifier kind of like this. Let's put it
[1:06:01] up to three. Like so. Do shade auto
[1:06:04] smooth. Okay. Still no issues. Now let's
[1:06:07] copy over our bevel modifier. Ctrl L.
[1:06:10] Copy. Whoops. Sorry. Just come over here
[1:06:13] and copy to selected. Cool. And now you
[1:06:15] can see that the shading is a little bit
[1:06:17] better on here. It's still not perfect,
[1:06:18] but it's it's better than what it used
[1:06:20] to be. Now, the issue here is that it's
[1:06:23] beveling on both sides. So, what we can
[1:06:26] do is temporarily hide our array
[1:06:28] modifier in edit mode. And since we
[1:06:31] don't actually have the faces yet
[1:06:32] because we're using solidify, let's
[1:06:34] actually just apply it right now. Let's
[1:06:36] go into edit mode, face select, hold
[1:06:39] control, face select that, then shift
[1:06:42] over here. Now, just control and select
[1:06:45] that as well. Pick the shortest path X
[1:06:47] and delete those faces. Let's go back
[1:06:49] and set our array modifier again. Cool.
[1:06:52] So, we kind of have something like this.
[1:06:53] Okay. Now, we can apply our array
[1:06:56] modifier. And let's fill in the gap on
[1:06:59] the side here. So, if we go into edit
[1:07:01] mode, what you can do is select the face
[1:07:04] faces like this. Sorry, let me go back.
[1:07:06] Like this. And then hit F. And instead
[1:07:08] of having to select all of these and
[1:07:10] hitting F every single time, you can
[1:07:12] just select this edge and hit F and hit
[1:07:14] F and just keep hitting F until it
[1:07:17] repeats. So just one more time, we
[1:07:20] select these three edges, hit F, select
[1:07:22] this edge, hit FF, and it'll
[1:07:24] automatically fill that just for us. So
[1:07:27] now we kind of have a thing for our GPU
[1:07:29] thing. Again, there's still some shading
[1:07:32] issues which you can fix with another
[1:07:34] modifier called weighted normal, and
[1:07:35] this will help a little bit too. Uh,
[1:07:38] again, still not perfect because this is
[1:07:40] a little bit too close to each other.
[1:07:42] So, if you want to fix some of that
[1:07:44] pinching, you totally could. Uh, but
[1:07:46] again, it's going to be good enough for
[1:07:48] us. So, we'll just leave it like so. And
[1:07:50] then, of course, we can scale it. Let's
[1:07:52] see. Maybe something like this. Make it
[1:07:55] a little bit more thick and stylized.
[1:07:58] Uh, and then for the fan, what we can do
[1:07:59] is I think this is actually already in
[1:08:02] the center, which is actually really
[1:08:03] nice. Uh, so we can just do shift s
[1:08:05] cursor to selected which will just snap
[1:08:08] it there. Um, let's go to object mode
[1:08:10] and add it. We can always join it later.
[1:08:12] And let's add a cylinder. I don't think
[1:08:14] we need 12 because it's going to be so
[1:08:16] small. So maybe eight will suffice. Um,
[1:08:19] so sorry, my num lock key is off. So
[1:08:22] eight. Yeah, it doesn't look great from
[1:08:24] closeup, but from far away it'll look
[1:08:26] more than okay. Um, and then just scale
[1:08:28] it down a little bit. Kind of just like
[1:08:30] that. So, for the blades itself, you
[1:08:32] could totally import like a fan
[1:08:33] reference just to go off it. But,
[1:08:35] honestly, I'm just going to eyeball it.
[1:08:36] So, I'm going just going to add a plane
[1:08:39] um arbitrarily and then maybe go here
[1:08:42] and just move this slightly over here.
[1:08:44] Whoops. Let me turn off proportional
[1:08:46] editing. And then maybe move another one
[1:08:49] right here. Um I don't know. Try and get
[1:08:52] a regular shape of a blade. And then
[1:08:54] over here, maybe something over here.
[1:08:57] And we definitely want to loop cut down
[1:08:58] the center just to give it some shape
[1:09:00] over here. Um, so I'm kind of just
[1:09:04] eyeballing everything. Uh, but you could
[1:09:06] definitely import a reference if you
[1:09:08] need to. Maybe rotate some of these. Um,
[1:09:11] maybe maybe a little bit. I don't
[1:09:13] actually know. But I feel like this kind
[1:09:14] of looks good enough for a blade. So
[1:09:17] what we can do is add a solidify
[1:09:19] modifier.
[1:09:20] Just increase the thickness a little
[1:09:22] bit. And then we can add a subdivision
[1:09:24] surface. Uh, just like that. kind of
[1:09:26] looks like a blade. Shade smooth. Little
[1:09:28] bit of shading issues. That's fine. Then
[1:09:30] we can probably Now we can uh let's go
[1:09:32] into local view so it's not glitching
[1:09:34] out. Now we can probably move with
[1:09:36] proportional editing. Let's change our
[1:09:38] sphere of influence here. So here we
[1:09:41] might want a small curve here. Let's
[1:09:43] bring it down a little bit. Maybe like
[1:09:45] so. Doesn't have to be accurate. Up here
[1:09:48] we can probably bring it up a little
[1:09:49] bit. Um maybe increase that. Same thing
[1:09:52] here.
[1:09:54] Uh maybe bring this area down. I don't
[1:09:57] know. We'll see. Um kind of like
[1:10:00] something like that. So, okay. So, that
[1:10:02] looks good enough for me. If you want to
[1:10:05] play around with yours, you totally can.
[1:10:07] Um but that'll be all for the blade
[1:10:09] here. So, we can use the same method we
[1:10:12] did last time. Let's select this. Shift
[1:10:13] S cursor to selected. Let's change this
[1:10:16] to 3D cursor. Let's select this. Okay.
[1:10:18] So, I think I want six again. So, what
[1:10:20] I'm going to do is shift D again. Hit R
[1:10:23] and then type in 60. Hit enter, shift R,
[1:10:25] shift R, shift R, shift R. And there we
[1:10:27] have six. And honestly, I think I'm
[1:10:29] going to hold Alt and just increase this
[1:10:31] by one. That way it looks a little bit
[1:10:33] better. Actually, no. I'm just going to
[1:10:35] undo that. And I think it'll look fine.
[1:10:37] Just like that. Uh, so anyway, let's
[1:10:39] select these and hit F3, convert to
[1:10:43] mesh. That'll just that's just a faster
[1:10:45] way of applying all your modifiers.
[1:10:48] So you can see all my modifiers for all
[1:10:50] these are gone now. Um, and then what we
[1:10:52] can do is select all these and just join
[1:10:54] it here. Kind of just like this. Cool.
[1:10:57] Uh, and then this one. Um, if you don't
[1:11:00] want to change anything, what you can do
[1:11:01] is apply bevel and weighted normal. Uh,
[1:11:03] so now we can just duplicate this and
[1:11:06] over here. So I'm going to do GX and
[1:11:08] move it over here. You could use an
[1:11:09] array modifier if you want, but I'm just
[1:11:11] going to eyeball it cuz no one's going
[1:11:12] to notice and it's faster that way. So
[1:11:14] I'm just going to leave them separate
[1:11:15] for now. Uh, we'll come back to this a
[1:11:18] little bit later. Um, and then let's
[1:11:20] just place it in our computer somewhere.
[1:11:22] So maybe, oops, let's do again. I
[1:11:26] accidentally have it on 3D cursor. So
[1:11:27] let's make a bounding box center again.
[1:11:29] RX 90. Um, and just move it somewhere.
[1:11:34] That kind of looks good. Uh, and we can
[1:11:35] temporarily change this one to
[1:11:38] um, we can go into viewport display and
[1:11:40] change this one to wire or bounce. Uh,
[1:11:44] in this case, I think I'm just going to
[1:11:45] go with wire. So this will be a little
[1:11:47] bit more noticeable here. And it seems
[1:11:49] like on this side I did not uh fill it
[1:11:52] in. So let's just go into local view, go
[1:11:54] into edit mode again. We can select
[1:11:56] these, hit F, select this F FF, fill
[1:11:58] that in. We could have also just cut
[1:12:00] this in half and use a mirror modifier
[1:12:02] on both of these because it's the same.
[1:12:04] Um but you know, it doesn't really
[1:12:05] matter for us. Uh yeah. So what we can
[1:12:07] do now is let's just select this entire
[1:12:10] thing to go into local view like so.
[1:12:13] Make sure we don't have anything else
[1:12:14] selected. Cool. Head into local view
[1:12:16] here. And let's just shift right click
[1:12:18] somewhere and add a I don't know plane
[1:12:22] just over here. Go into edit mode. Uh
[1:12:24] just go into wireframe. Kind of get
[1:12:27] something that we like. We can turn off
[1:12:28] proportional editing. And this will be
[1:12:30] like our water cooler thing. Honestly,
[1:12:32] it doesn't really have to be that cool
[1:12:34] or anything. Maybe extrude again. Maybe
[1:12:36] e extrude again. Maybe, you know, it
[1:12:39] doesn't really matter. I'm just kind of
[1:12:40] doing whatever honestly. So this is like
[1:12:42] our GPU or something. Maybe it looks a
[1:12:45] little bit weird. Whatever. Doesn't
[1:12:46] really matter. Looks like I didn't
[1:12:48] select those fans. Oh well, it doesn't
[1:12:49] matter. Okay, so for the tubes, we're
[1:12:51] going to do the same thing we did for
[1:12:52] the plant stems. Shift A, search for a
[1:12:54] curve. Um, nums curve, basier curve.
[1:12:57] Doesn't really matter, honestly. I'm
[1:12:58] just going to go for basier. Let's go
[1:13:00] into top view. Uh, select this verticy.
[1:13:02] Let's just scale that down so we can see
[1:13:04] what we're doing. Since our cursor is
[1:13:06] over here, shift S, selection to cursor.
[1:13:08] It'll jump it over there. Um, kind of
[1:13:10] like so. And then we can just move this
[1:13:13] one as well. kind of just arbitrarily R
[1:13:17] R like so. And of course, we want to
[1:13:20] give it some depth just so we can see
[1:13:22] what we're doing. So again, that's in
[1:13:24] our data object properties and just
[1:13:27] increase the depth just a little bit.
[1:13:28] Kind of like that. Here, we can go into
[1:13:30] side view. This will kind of help out a
[1:13:32] lot. And if you need more geometry, you
[1:13:34] can just hit E to kind of extrude it
[1:13:35] like so. Rotate appropriately, scale it,
[1:13:39] whatever you need to um, you know, kind
[1:13:41] of have some water tubes and things like
[1:13:43] that. Uh, then we can obviously
[1:13:44] duplicate it. Oh, that looks like a This
[1:13:47] looks really weird. So, let's go into
[1:13:48] wireframe to make sure that's not messed
[1:13:50] up. Cool. Something like that. The same
[1:13:54] thing with this one. Let's just fix
[1:13:56] that. It's got some issues here. Um, so
[1:14:00] maybe over here. And then this one can
[1:14:02] be lower hanging. This one can be a
[1:14:05] little bit maybe hanging down here like
[1:14:08] that. Uh, we don't want these inside. So
[1:14:12] the less overlap we have the better. Um
[1:14:15] but you know it's not it's not a
[1:14:17] complete big deal. I think that's good
[1:14:18] enough. So let's just go out and yeah.
[1:14:22] So I'm going to leave this like this for
[1:14:24] now just so we can see everything. So
[1:14:25] the front faces I think I'm going to
[1:14:27] cover up whereas the side faces are
[1:14:29] going to be glass. So we'll just see
[1:14:31] this. Um and that should be good enough.
[1:14:33] Okay. Let's add a really really cute
[1:14:35] character now. So we can just shift
[1:14:37] somewhere and probably let's add a
[1:14:40] plane. Let's go scale it down a little
[1:14:42] bit. Let's go into local view actually.
[1:14:44] So we get rid of everything. E extrude
[1:14:46] it up. Apply our scale. And let's do
[1:14:49] control 2 for like um shade smooth.
[1:14:53] Maybe control 3 actually just so we get
[1:14:55] something a little more round like this.
[1:14:57] Maybe add a loop cut kind of like here.
[1:14:59] Uh so we have something that kind of
[1:15:01] looks like a plush. Maybe SX kind of a
[1:15:05] little bit like so. Uh then we can go
[1:15:06] into front view and maybe for the eyes
[1:15:09] we just shift a also add a cube this
[1:15:12] time. Um control 2 for that shade
[1:15:16] smooth. Come over here and add a mirror
[1:15:19] modifier like so. Come over here and do
[1:15:22] Y and X. Scale it up a little bit. Maybe
[1:15:26] SZ. Cool. Cool. Cool. And then maybe we
[1:15:30] can have some ears. So, I'm just going
[1:15:31] to duplicate this and uh maybe scale it
[1:15:34] like this. Sx kind of like this. SZZ on
[1:15:38] the local Z-axis. Go into edit mode.
[1:15:41] Probably insert this a little bit. Um
[1:15:43] there we kind of have like a flat sort
[1:15:45] of face thing. Let's go into edit mode
[1:15:47] and scale this XX. Just bring it down a
[1:15:50] little bit like so. Um
[1:15:53] cool. Let's also just copy this mirror
[1:15:55] modifier. So, copy modifiers. There we
[1:15:58] kind of have something cute. So for the
[1:16:00] whisker thing, what I'm going to do is
[1:16:02] go into a side view, shift right click
[1:16:03] somewhere in the center. And this time
[1:16:05] I'm going to shift A and this time if
[1:16:07] you come into mesh, you'll see this new
[1:16:09] thing here called a single verticy. And
[1:16:11] it'll add a single verticy only. And
[1:16:13] that comes with the extra objects add-on
[1:16:15] that we installed a little bit earlier.
[1:16:18] So instead, what we can do is do origin
[1:16:21] and verticy mirrored. And this will kind
[1:16:23] of just save us a lot of issues. By
[1:16:24] default, it'll jump us into edit mode on
[1:16:26] this. Just make sure you're in vertex
[1:16:28] select so you can see it. And then you
[1:16:30] can hit E and just extrude it outward
[1:16:32] and into like a shape of a whisker. Just
[1:16:34] like that. Let's make sure the mirror
[1:16:36] modifier is in the correct direction.
[1:16:38] And then here we can go into wireframe
[1:16:39] kind of just to see it a little bit
[1:16:40] better. So now you can just shape it how
[1:16:43] you want. And if you want verticy here,
[1:16:45] you can just do CtrlB and then hit V
[1:16:48] just to split it up a little bit and
[1:16:49] increase your mouse wheel just to get
[1:16:51] some more vertices if you need more
[1:16:53] vertices in between your other ones.
[1:16:56] Additionally, you can do CtrlR just for
[1:16:58] a loop cut just to place a single one in
[1:17:00] between just in case you need that. I
[1:17:03] think I just need four. And that kind of
[1:17:05] is good enough for my whisker. But, you
[1:17:07] know, make your whisker however you
[1:17:08] want. Okay. Now, for the whisker,
[1:17:10] instead of using a curve like we did
[1:17:12] earlier, let me go into side view. The
[1:17:14] reason I'm not going to be using a curve
[1:17:15] this time is because, you know, it kind
[1:17:17] of has this issue and then you have to
[1:17:19] fix that. I mean, we've dealt that with
[1:17:20] before, but it's just better not to do
[1:17:22] that again. And now that we have this
[1:17:25] extra objects add-on, what we can do if
[1:17:27] you come into mesh and go into single
[1:17:28] verticy, you can see this thing here
[1:17:30] called add single verticy. If you click
[1:17:32] on it, it'll automatically bring you
[1:17:34] into edit mode and it just it's
[1:17:36] literally just a single verticy. Make
[1:17:37] sure you're invertex select and hit E
[1:17:39] just to extrude it out. And then kind of
[1:17:41] just shape and then just shape it out
[1:17:43] into like a whisker sort of thing. If
[1:17:45] you need more vertices, you can just hit
[1:17:46] Ctrl R and place some loop cuts in
[1:17:49] between. Now, it's not really a loop
[1:17:52] cut, but yeah, I just call it loop cut
[1:17:53] anyway because it's the same hotkey.
[1:17:55] Here, you can do Ctrl +B and then do V
[1:17:58] if you want to increase the amount. And
[1:18:00] you can use your middle mouse button to
[1:18:02] increase the amount of vertices there,
[1:18:04] like so if you want it more smooth. I
[1:18:06] think I just need four. So, that's all
[1:18:08] I'm going to be doing. And I'm just
[1:18:10] going to shape it into like a whisker
[1:18:12] sort of thing.
[1:18:13] So, there we kind of have our whisker.
[1:18:16] Now what we can do is actually F3 and
[1:18:18] open the global menu and convert this to
[1:18:21] a curve. You can see it's in object
[1:18:23] convert to curves which means if you
[1:18:25] come up here object convert to curve
[1:18:27] it's also there as well but I usually
[1:18:29] just use the global menu and search for
[1:18:30] it because I know about it. Uh so now
[1:18:32] that it's a curve we can come into the
[1:18:34] curve object data properties and like we
[1:18:36] did for the stems and the pipes and
[1:18:39] everything we can just increase the
[1:18:40] depth holding shift just to make it a
[1:18:43] little bit slower like so. Then you'll
[1:18:45] notice that they don't automatically
[1:18:47] fill the caps. So we can just click fill
[1:18:48] the caps just like that. Right click,
[1:18:50] shade smooth. I think that's fine. But
[1:18:52] if you want, you can add like a
[1:18:54] subdivision. So like control 2, and
[1:18:55] that'll be really smooth. We're really
[1:18:57] far away, so I'm just going to undo that
[1:18:59] and leave it really low poly, kind of
[1:19:01] just like this. Cool. And now what we
[1:19:03] can do is add a mirror modifier just
[1:19:05] like so. Make sure it's on the Y-axis.
[1:19:07] Um, and that looks okay. But if you want
[1:19:10] to do it for the object, you can totally
[1:19:12] do the object itself. That way when you
[1:19:14] go into edit mode, you can kind of like
[1:19:15] adjust it like so. Uh anyway, let's just
[1:19:18] get out of local view and uh scale this
[1:19:21] down and place it on your desk
[1:19:22] somewhere. So, what we can do is
[1:19:24] actually make a baby Mr. Whiskers. Shift
[1:19:27] Duplicate. Um G, shift Z somewhere
[1:19:30] smaller, kind of like a little bit like
[1:19:33] so. Uh Sz just to scale it down a little
[1:19:36] bit. Make it a little bit more plump and
[1:19:38] round than Mr. Whiskers himself. and
[1:19:41] then scale it down. There we have There
[1:19:44] we have Mr. Whisker's kid. Mr. Whisker's
[1:19:47] son right there. Super super cool. Let's
[1:19:50] add a quick coffee somewhere. So, let's
[1:19:52] just shift A and add a cylinder like so.
[1:19:56] Maybe let's do like 16 this time. Scale
[1:19:59] it down a little bit. Uh, bring it up.
[1:20:01] GZ. Go into edit mode. A GZ and snap it
[1:20:04] here with face snapping. Um, right
[1:20:07] click, shade auto smooth. Go into edit
[1:20:09] mode. Select this. inset and just
[1:20:11] extrude it downwards. Apply a bevel
[1:20:13] modifier like so. Uh then we can just
[1:20:16] copy our bevel modifier over here. Uh
[1:20:19] copy modifier. Let's apply our scale
[1:20:22] just like so. And then maybe adjust the
[1:20:23] mount a little bit. Maybe we can inflate
[1:20:26] this a little bit with alt s. Cool. Um
[1:20:28] and then for the handle, let's just
[1:20:30] shift a add a Taurus. 48 might be too
[1:20:33] many. So maybe we can do like 24. Uh
[1:20:36] that's okay. Then we can just right
[1:20:38] click shade smooth. And then R Y90. Just
[1:20:41] bring it down kind of just like here. Go
[1:20:43] into edit mode. Sorry, local view. Go
[1:20:45] into edit mode. Wireframe. Select these
[1:20:49] vertices. Whoops. Let's go into
[1:20:50] wireframe. And then select these
[1:20:51] vertices. All deleted those. And um
[1:20:54] there we kind of have our mug. I'm just
[1:20:56] going to join that right now. So they
[1:20:57] become the same thing. Uh and then I'm
[1:20:59] just going to apply this bevel modifier
[1:21:01] and just join here right now. And then
[1:21:03] just shade smooth. That way we kind of
[1:21:05] just have our coffee cup uh by default.
[1:21:08] Okay. Okay, for the chair, let's just
[1:21:09] start with maybe a plane and just bring
[1:21:12] it up GZ. Kind of get a shape that we
[1:21:15] want. Let's add a subdivision surface
[1:21:17] modifier of two. And let's just add a
[1:21:19] loop cut over here. Maybe a loop cut
[1:21:22] over here. Maybe squeeze this down just
[1:21:25] a little bit. So, we kind of have
[1:21:26] something like that. And now, let's just
[1:21:28] add a solidify modifier just to see how
[1:21:31] that will look. Okay. And let's put this
[1:21:33] before our subdivision surface modifier.
[1:21:36] Now, let's do shade smooth. Cool. It
[1:21:38] doesn't look too bad.
[1:21:40] Uh, so what we actually need to do is
[1:21:42] actually apply our solidify modifier.
[1:21:45] Now, now that we have more geometry to
[1:21:47] work with, then we can just inflate this
[1:21:49] a little bit. And then maybe add two
[1:21:51] bracing loops right here. SC a little
[1:21:54] bit. Um, just to brace it up. And there
[1:21:56] can be our sort of uh RZ 90. And this
[1:22:01] can kind of be just our cherry bottom.
[1:22:03] Just like that. Super be super cool. We
[1:22:05] can select this. We'll do shift s cursor
[1:22:08] to selected. Snap that right there. And
[1:22:10] let's add a cylinder for the base. I
[1:22:13] think 16 is too many. So, we can do like
[1:22:15] 12. Scale that down a little bit. Maybe
[1:22:19] something like so. Cool. And let's go
[1:22:22] into edit mode. Bring that down. Whoops.
[1:22:25] I don't want to extrude yet. Bring that
[1:22:27] down a little bit. And then we can E,
[1:22:28] right click, cancel the movement. Scale
[1:22:30] it up first. And then E, extrude it
[1:22:32] down. Whoa, that's too big. But that's
[1:22:33] totally okay. Let's go into local view.
[1:22:34] Let's just hold alt s and with this loop
[1:22:37] selected. So we only want it a little
[1:22:39] bit bigger. Just like that. Let's do
[1:22:41] shade auto smooth. Kind of like that.
[1:22:42] All right. So let's make our table leg.
[1:22:44] I'm just going to go into local view.
[1:22:46] Let's just go into side view. Doesn't
[1:22:47] really matter. Then let's come over
[1:22:49] here. Let's uh let's do a cube this
[1:22:51] time. And let's just go start over here.
[1:22:53] Let's go into edit mode. Let's go into
[1:22:55] wireframe. Make sure we select
[1:22:56] everything. Let's just bring it down
[1:22:58] kind of something just like that. Now
[1:23:00] what we can do is same thing we did
[1:23:02] before. Rotate this arbitrarily parallel
[1:23:05] to the X Saxis and then Whoops. And then
[1:23:08] do Sz0 just to flatten it out there.
[1:23:12] Then we can possibly put it around here
[1:23:15] or something. Then select these as well.
[1:23:17] Remember it's selecting everything. It
[1:23:18] has to have the same amount of sides and
[1:23:21] geometry and everything. Ctrl + E bridge
[1:23:23] edge loops and just increase the number
[1:23:25] of cuts. Like so. Maybe two is good
[1:23:28] enough cuz no one's going to be looking
[1:23:30] at it that much. So, right click, shade,
[1:23:32] auto smooth. Super super cool. And then
[1:23:34] we just S Y scale in. Well, actually,
[1:23:36] maybe I'll just leave it a little bit
[1:23:37] more blocky.
[1:23:39] Cool. And then for the bottom here, we
[1:23:41] can just shift right click somewhere
[1:23:42] arbitrarily. Shift A. And this time, we
[1:23:45] can have another cylinder. So, I'm just
[1:23:47] going to search for that. Add that down
[1:23:49] there. 12. I think we might be able to
[1:23:51] live with 10 since it's so small. So,
[1:23:53] let me just do 10. Cool. RX90. Just like
[1:23:57] that. S Y. Make it kind of small. Scale
[1:24:01] it up. S Y GZ. Cool. Cool. Cool. Cool. S
[1:24:06] Y
[1:24:08] GZ. And then now we can have the table
[1:24:10] the cap for it. So we just go into edit
[1:24:12] mode, hold control to pick the shortest
[1:24:14] path. Well, I guess that's not the
[1:24:15] shortest path. So now we can just hold
[1:24:17] control and select those possibly here.
[1:24:20] Shift Duplicate, right click, cancel.
[1:24:22] Let's hit alt S just to scale it up a
[1:24:24] little bit so there's like a small
[1:24:25] little gap there. And then alt E,
[1:24:27] extrude along normals. And then just
[1:24:29] bring that up there. And now we kind of
[1:24:31] have our little wheel with our cap
[1:24:32] there. Do all of these stuff. Uh, so
[1:24:34] maybe over here, Ctrl L, copy modifiers.
[1:24:38] And let's just apply our scale just to
[1:24:40] make sure everything works. Looks cool
[1:24:42] actually. I mean, it doesn't look bad. I
[1:24:44] mean, this kind of looks bad, but from
[1:24:46] far away, no one's really going to be
[1:24:47] taking a look that deeply. Okay, let's
[1:24:49] just apply these modifiers. Um, so we
[1:24:52] can join them together. Uh, so this
[1:24:55] seems okay. Let's just join them
[1:24:56] together. Ctrl J. Uh, cool. Just like
[1:24:59] so. And now we're going to do that same
[1:25:01] exact thing. Let's do shift s cursor to
[1:25:04] selected. Go into top view. Let's select
[1:25:07] this. I think I want six legs again. So
[1:25:09] that's going to be 60°. Let's change
[1:25:11] this to 3D cursor. Okay. So, same thing.
[1:25:14] Let's just uh go in wireframe. Um,
[1:25:16] position this correctly. I think that's
[1:25:18] okay. Then shift D, R60.
[1:25:22] Don't touch anything. Shift R, shift R,
[1:25:24] shift R, shift R. There we have these.
[1:25:27] Now we can just uh rotate these a little
[1:25:29] bit. Um just so it's offset. I don't
[1:25:31] like how this is like parallel to the
[1:25:34] chest. Uh sorry to the chair. Um and I
[1:25:39] think we can just convert these to
[1:25:41] meshes. Now if you want to edit them,
[1:25:42] you totally can. But I'm just going to
[1:25:44] convert them and then just join it with
[1:25:45] this object right here. And again, if
[1:25:48] you do want to edit them, you totally
[1:25:49] have the option to, right? You can go
[1:25:51] into wireframe, probably go into edit
[1:25:53] mode and select over here. Uh you can
[1:25:55] deselect these um and then you can still
[1:25:58] adjust stuff like this. Same thing with
[1:26:00] the legs, right? You can go in the side
[1:26:01] view and select the legs and then adjust
[1:26:03] the legs. So you still have your option.
[1:26:05] It's a little more destructive by
[1:26:07] applying it. So I would honestly
[1:26:09] probably adjust it first before joining.
[1:26:12] You know, that's that's uh kind of up to
[1:26:14] you and and what you want to do. And
[1:26:15] then for the back of the chair, I think
[1:26:17] that will also just be a cube with
[1:26:19] control 2 subdivision. Shade shade shade
[1:26:23] auto smooth. Bring it down. Maybe
[1:26:25] something like this. Sz. Um, cool.
[1:26:28] Something like that. Maybe add some
[1:26:30] bracing edge loops. Maybe just like two
[1:26:32] here. Sy. I want it a little bit plumpy.
[1:26:35] Maybe in the center. Uh, we can have one
[1:26:38] there. And then maybe one over here. And
[1:26:41] then we can do sx and kind of like plump
[1:26:42] it out just a little bit. Like you know
[1:26:45] if you want to style maybe you add
[1:26:47] something like here. I don't know. Uh
[1:26:49] kind of up to you. But I'm just going to
[1:26:50] keep it really really simple. And for
[1:26:52] the back we can use probably the same
[1:26:54] exact method we've been using. Let's go
[1:26:56] into wireframe. Shift A. Add a cube.
[1:26:59] Scale that down. Let's go into edit
[1:27:02] mode. Wireframe E. Just extrude it up.
[1:27:04] Rotate a little bit somewhere around
[1:27:06] here. Cool. Uh, scale it. Maybe scale it
[1:27:10] up a little bit. E, extrude again.
[1:27:13] Rotate it. Um, I don't honestly I don't
[1:27:16] even know if we need to bridge edge
[1:27:18] loops this time. I feel like just doing
[1:27:19] it manually is good enough. And then
[1:27:21] subdivision surface about control 2. Add
[1:27:24] two bracing loops on this side. S Y
[1:27:27] scale that up kind of like that. Um, and
[1:27:31] then maybe and then two and then
[1:27:34] definitely two on this side. Okay. So to
[1:27:36] move these uh new tip, you can do G for
[1:27:39] grab and then hit G again and it'll kind
[1:27:41] of slide along the edge here. So hold
[1:27:42] alt to select this whole edge loop. GG
[1:27:45] to move along the edge to bring it up
[1:27:47] there. G alt to select this loop. GG to
[1:27:51] slide it down and brace this edge like
[1:27:53] there. And then shade, right click,
[1:27:55] shade, auto smooth. And there we kind of
[1:27:57] have our little thing right there. Uh
[1:28:00] honestly, I don't know if it's worth
[1:28:02] adding all that topology for this. So
[1:28:04] I'm actually going to delete that. And I
[1:28:06] think I'm just going to shift Duplicate
[1:28:08] this. Shift S selection to cursor.
[1:28:13] Scale that down. S Y kind of like this.
[1:28:16] And just uh probably do something
[1:28:19] something like this actually, which is
[1:28:21] really simple. Um but it gets the job
[1:28:24] done. And then I'm just going to move
[1:28:25] this here. Cool. And the center kind of
[1:28:28] just like that. So very a lot more
[1:28:31] simpler. And uh maybe we add some loop
[1:28:34] cuts here and one down here for And we
[1:28:38] don't want this to be a little bit
[1:28:39] inflated or maybe you do. I'm just going
[1:28:42] to Ctrl X to get rid of those bracing
[1:28:45] edges right there. So we effectively
[1:28:47] have the same thing here. But now it's
[1:28:48] kind of like that. Uh and then maybe we
[1:28:50] want a cushion. So I'm actually just
[1:28:52] going to select these faces. Shift
[1:28:54] Duplicate P separate by selection. Go
[1:28:57] into edit mode E and just extrude that
[1:28:59] up a little bit. Um, and let's just make
[1:29:02] it really inflated here. Just place it
[1:29:05] right on top. Just like that. Uh, and
[1:29:08] then maybe we can change the SL shape
[1:29:10] just a little bit. So, GG just to make
[1:29:13] it not completely perfect. Move it up a
[1:29:16] little bit here. GX. Move this. And this
[1:29:19] will kind of be like the back stand. And
[1:29:21] the And honestly, like stylistically,
[1:29:23] this kind of looks bad compared to how
[1:29:25] bulky everything is. So maybe we
[1:29:27] overkilled on six, which is fine because
[1:29:29] we can just select everything. Let's go
[1:29:31] into wireframe actually and make sure we
[1:29:32] select one of everything of each of
[1:29:34] these except one of them. Um, so maybe
[1:29:37] something like this. Let's do Ctrl L and
[1:29:40] delete vertices. Cool. We got rid of
[1:29:42] everything. This one we can just do Ctrl
[1:29:44] L. Uh, let's select here as well. Ctrl L
[1:29:48] P. Separate by selection. Very cool. So
[1:29:51] just like that, we can do is just select
[1:29:53] this. Go into local view. Let's go to
[1:29:55] top view. Reset the rotation a little
[1:29:57] bit. Well, I guess I kind of skewed it.
[1:29:59] Oh well, that's fine. Um, let's go back
[1:30:02] into outside of local view with this
[1:30:05] still orthographic. Let's go into
[1:30:06] wireframe here.
[1:30:08] Go into edit mode and just move uh move
[1:30:12] adjust this kind of a little bit like
[1:30:14] so. Um, so it's not like completely
[1:30:17] outside of the desk. So maybe something
[1:30:19] like this. Cool. Honestly,
[1:30:24] it might be even smaller like this. Uh,
[1:30:28] which is a little bit weird, but um I
[1:30:32] think it will work. I think it'll work
[1:30:33] for the stylistic look that we're going
[1:30:35] for. Uh, yeah. So, I just did that same
[1:30:38] shift R thing. Um, so I don't want to
[1:30:40] keep showing you that and waste your
[1:30:42] time, but this actually definitely looks
[1:30:44] a lot better than what we had
[1:30:45] originally. It's still a weird sort of
[1:30:47] proportion. Um, but you know, it's it
[1:30:50] was a lot it is a lot better than what
[1:30:52] we had originally. And let's just make
[1:30:53] this a little bit more bulkier with some
[1:30:56] support loops. S uh sy probably and just
[1:30:59] make it a little bit bulkier there.
[1:31:01] Cool. Yeah, but honestly, you know, just
[1:31:03] spend as much time as you want to. I
[1:31:05] don't want to waste your time here just
[1:31:07] uh nitpicking the models every single
[1:31:08] time. Um, but you know, it definitely
[1:31:10] looks better than what we had
[1:31:11] originally. All right, let's bring back
[1:31:13] our room. So, I'm just going to
[1:31:15] reactivate that just so we can see it
[1:31:17] again. Let's make sure. Okay, we can
[1:31:19] join these now. So, we can just join
[1:31:21] these. And let's just move these up all
[1:31:25] kind of just like this. All right, let's
[1:31:27] add like a chest here or something. Uh,
[1:31:30] or drawer. I don't know what they
[1:31:31] actually call it. So, I'm just going to
[1:31:32] add a plane here. Shift Z. Go into edit
[1:31:36] mode. E extrude it upwards. That looks
[1:31:38] way too big. So, I'm just going to S
[1:31:39] shift C it a little bit. That looks
[1:31:41] about right. Let's go into edit mode.
[1:31:43] Well, let's apply our scale. Go into
[1:31:44] edit mode. Select this inset a little
[1:31:47] bit like here. I think that looks okay.
[1:31:51] Then we can add two loop cuts like so.
[1:31:54] And we can just scale them arbitrarily.
[1:31:56] I kind of want three here. So just kind
[1:31:58] of eyeballing it. Maybe around here is
[1:32:00] okay. Then we can select this. Then we
[1:32:03] can select this face. Hit P and separate
[1:32:05] by selection. Then select go back in
[1:32:07] here. Hold alt to select these and shift
[1:32:10] and just Ctrl + X to dissolve those. And
[1:32:13] then we can also just delete this face
[1:32:15] here. So now we kind of have this thing
[1:32:16] by itself. Let's object. So origin
[1:32:18] origin back to geometry.
[1:32:20] Uh and then this will be like one of our
[1:32:23] drawers. So what we can do is let's go
[1:32:25] into wireframe here. Just E and extrude
[1:32:28] it out a little bit like here. I don't
[1:32:30] know if we want to see the inside, but
[1:32:32] maybe we do. So let's go into local view
[1:32:33] here. Let's go and just inset here and
[1:32:37] then extrude downwards. This way we kind
[1:32:39] of have like a you know a storage
[1:32:42] container like so. And for the handle we
[1:32:47] can just add two loop cuts here and
[1:32:49] bring this down just so like so. GZ. And
[1:32:52] then actually maybe we add one more here
[1:32:55] and one more here.
[1:32:57] And then let's just bring this down like
[1:32:59] so. And if I go out. Yeah, that looks
[1:33:02] that looks pretty good. Maybe bring it
[1:33:03] down a little bit more. Super cool. And
[1:33:06] then let's add a little bit of a gap
[1:33:08] there. so the hand can fit in. Let's
[1:33:10] just copy the bevel modifiers now.
[1:33:13] Sorry. Yeah, bevel modifiers. Come over
[1:33:15] here. Let's just do copy to selected.
[1:33:17] Let's apply our scale. That looks great.
[1:33:20] Let's add an array modifier here. We
[1:33:22] want it in the Z direction. So, let's
[1:33:24] get rid of that. Let's just move it in
[1:33:26] the Z direction.
[1:33:28] That looks great. Then we add three. And
[1:33:31] now it's looking a little too small. So,
[1:33:33] we can just go into edit mode and scale
[1:33:34] that up a little bit. Bring it down a
[1:33:37] little bit and then just lower the gap a
[1:33:39] little bit. Kind of like that. Okay,
[1:33:41] that looks pretty good for a drawer.
[1:33:43] Maybe we can increase the amount here
[1:33:45] just a little bit. And let's make sure
[1:33:48] we shade shade auto smooth for both of
[1:33:50] these shading issues here. I think this
[1:33:52] can be fixed with weighted normal. Same
[1:33:54] thing here. We can also add a weighted
[1:33:56] normal modifier and that kind of fixes
[1:33:57] some of the shading issues. Cool. So now
[1:33:59] we kind of have this sort of stylized
[1:34:02] thing. Maybe it can be a little bit
[1:34:04] thicker. We can hold alt to select this.
[1:34:06] Alt s and maybe like inflate it a little
[1:34:08] bit. And book. I'm going to add a plane.
[1:34:11] Let's just scale it down into an
[1:34:13] arbitrary book shape. That looks pretty
[1:34:15] good. Uh, you know, you can always
[1:34:17] change it later, so it's not really a
[1:34:18] big deal. Let's go into edit mode. E,
[1:34:20] and extrude it upwards. Cool. Let's
[1:34:22] apply our scale. Go into edit mode and
[1:34:23] select these faces here. And I think I'm
[1:34:26] going to shift duplicate them. I don't
[1:34:28] know if we have to or if we could just
[1:34:29] separate them, but I'm going to do it
[1:34:31] anyway just in case. Then I'm going to P
[1:34:33] separate by selection. So we kind of
[1:34:34] have this cover here. That way we kind
[1:34:36] of have a cover. And for the inner book
[1:34:37] itself, I'm just going to scale that
[1:34:39] down a little bit. Then let's select the
[1:34:40] cover. Go into edit mode. Add a loop cut
[1:34:43] here. And let's just do gy and move it
[1:34:45] out kind of a little bit like that.
[1:34:46] Let's add a subdivision surface modifier
[1:34:48] of two. Again, that's control 2. You can
[1:34:50] see it's right there. Let's go into edit
[1:34:51] mode, add two bracing edge loops here,
[1:34:54] and just scale it up on the S and X axis
[1:34:57] kind of like so. And then let's add
[1:34:59] another edge loop right here. And let's
[1:35:02] add one on the bottom as well. And let's
[1:35:03] just hold shift and alt to select both
[1:35:06] of them. Just like this. Gy. Bring it
[1:35:08] kind of really close to edge. Kind of
[1:35:10] just like that. Let's add a solidify
[1:35:12] modifier. We want to solidify before the
[1:35:15] subdivision modifier. So let's do like
[1:35:17] that. Right click. Let's do shade
[1:35:18] smooth. Let's just increase the
[1:35:20] thickness. So like so. Cool. Looking
[1:35:23] good so far. Let's go into edit mode and
[1:35:25] let's add a bracing edge loop here. And
[1:35:27] another one right here. Shift alt.
[1:35:30] Select both of those just like that.
[1:35:32] Right? And then let's just do gy and
[1:35:35] just brace that little curve there. So
[1:35:38] how much curve you want, you can
[1:35:39] determine that yourself. Let's move this
[1:35:41] book just to kind of fill in that gap a
[1:35:43] little bit there. And for this one,
[1:35:44] instead of subdivision surface, what we
[1:35:46] can do is just give it a bevel modifier.
[1:35:49] So let's come over here, select this,
[1:35:52] ctr L, copy modifiers like so. Shade
[1:35:54] auto smooth. Cool. Looking good. Uh, and
[1:35:57] then maybe we just increase the amount
[1:35:59] of segments there. And then of course we
[1:36:01] can increase the thickness kind of like
[1:36:03] that. Uh, and then let's make sure to
[1:36:05] check on even thickness just so we get a
[1:36:07] little bit more bulky there. But again,
[1:36:08] it's kind of up to your style and
[1:36:10] everything. So there we kind of have our
[1:36:12] stylized book. I might want to change
[1:36:14] make modifications later. So I'm going
[1:36:15] to shift duplicate move to a new
[1:36:17] collection called modifiers.
[1:36:20] And I'm just going to And then I'm also
[1:36:22] going to create another collection
[1:36:24] within that collection called book
[1:36:27] modifiers like so. This way. And I'm
[1:36:31] going to click and drag and put in the
[1:36:32] modifiers. This way. If I want to make
[1:36:34] changes to this book later, I can have a
[1:36:35] backup here. But for these, I'm just
[1:36:37] going to F3 convert to mesh. And then
[1:36:40] I'm just going to join them right now.
[1:36:41] Like so. Ctrl + J. We could have done
[1:36:43] that for some of our other objects if we
[1:36:45] wanted to come back to them. Um, but I
[1:36:47] didn't do that. So, but for the book, I
[1:36:49] definitely feel like I'm going to make
[1:36:50] variations of this. So, that's why I
[1:36:52] kind of wanted to keep that.
[1:36:53] Additionally, for these other ones, they
[1:36:54] still have their modifiers on there cuz
[1:36:56] we're going to be revisiting them in a
[1:36:58] little bit. A small little basket thing.
[1:37:00] So, I'm going to create a plane
[1:37:01] somewhere. Just scale it up in like a
[1:37:03] basket shape. Well, I guess baskets have
[1:37:06] multiple shapes, but anyway, same thing.
[1:37:08] Eextrude up. Let's delete this face.
[1:37:10] Let's give it a solidify modifier. Uh,
[1:37:12] let's just turn up the thickness a
[1:37:14] little bit. Let's turn even thickness.
[1:37:16] Let's also apply our scale just to make
[1:37:18] sure. Whoops. Wow. Now that's definitely
[1:37:19] messed up. Doesn't really matter though.
[1:37:22] Then let's add a subdivision surface
[1:37:24] modifier again. Uh again, we could just
[1:37:26] hit control 2. There. I think I'm going
[1:37:27] to give it two here. Then we'll do shade
[1:37:29] smooth. Now it Now it looks pretty good
[1:37:32] like a basket. I think I want to add
[1:37:34] like a guard loop down here. Now it kind
[1:37:36] of looks like a trash can. So what I'm
[1:37:38] going to do is probably add two loop
[1:37:41] cuts. Whoops. Add two loop cuts. And
[1:37:44] then just sx and scale it up there. So a
[1:37:47] little bit of a guard edge there. And
[1:37:49] then probably two over here. S y kind of
[1:37:52] like that. So that's kind of looking a
[1:37:54] little bit more like a basket now. Now
[1:37:56] let's just increase our thickness just a
[1:37:58] little bit. Um like so. Let's apply our
[1:38:02] solidify modifier so we have more
[1:38:03] geometry to work with. And I don't like
[1:38:06] how the top is so round. So I'm going to
[1:38:08] add another bracing edge loop there and
[1:38:10] kind of just pull it outward. And then
[1:38:12] maybe one in the center, too. Um, maybe
[1:38:15] that's too much. I think just one to
[1:38:17] pull out the enter is good. Let's go
[1:38:20] into edit mode. Let's add a loop cut
[1:38:22] here. And this way, I'll just make the
[1:38:24] thing a little bit more round. Now, we
[1:38:26] can go into wireframe. Let's just select
[1:38:28] these top vertices here and let's turn
[1:38:30] on proportional editing. Hit S and do X
[1:38:35] and just make it a little bit round like
[1:38:37] that. Cool. Let's go into solid view.
[1:38:40] That doesn't look terrible. We can pull
[1:38:42] these in if you want to make the inside
[1:38:45] a little bit thinner. Or what we can do
[1:38:48] instead is select these faces here.
[1:38:51] Shift controll just like that. And then
[1:38:53] alt s and whoops. Let's turn off
[1:38:55] proportion editing. Alt s and kind of
[1:38:57] just inflate the sides a little bit. Uh,
[1:39:00] cool. So we kind of like a little bit
[1:39:02] basket there. So let's come here and
[1:39:04] select the bottom. You can select one
[1:39:05] face, hold control shift and select the
[1:39:07] diagonal of another face. And I'll
[1:39:09] select everything in between. And if you
[1:39:12] want, you can hit I to inset it just to
[1:39:14] make it a little bit flatter there. And
[1:39:16] then G and Z and bring it down. This
[1:39:18] essentially adds another loop cut that
[1:39:20] way. Or you can just leave it inset. I
[1:39:22] think I'm just going to pull this one
[1:39:23] down, this edge loop down just a little
[1:39:25] bit. Maybe make it a little bit smaller.
[1:39:29] Um, actually, no. I think I'm going to
[1:39:31] make this a little bit smaller so it's
[1:39:32] kind of braced a little bit. Cool. That
[1:39:35] looks like a good basket. And then if
[1:39:37] you want to add some detail, we can add
[1:39:38] like two loop cuts here. Maybe SZ bring
[1:39:41] them down kind of like something over
[1:39:43] here. Uh maybe one over here. Cool.
[1:39:47] Let's select this loop cut. Let's do Alt
[1:39:49] E extrude along normals and kind of
[1:39:51] bring it up just a little bit like so.
[1:39:54] Cool. Then I don't like how it's like
[1:39:56] subdividing here. So what we can do is
[1:39:58] go into wireframe and select these
[1:40:01] control loops like so. And over here in
[1:40:06] item, there's this thing called mean
[1:40:07] crease. And when you increase the mean
[1:40:09] crease, you can see it's going to get
[1:40:11] rid of that for us. And now it's just
[1:40:13] going to leave something like that.
[1:40:14] Additionally, if you don't want to use
[1:40:16] that method and want more freedom, you
[1:40:17] can just add another control loop. And
[1:40:19] here, and kind of just pinch it up like
[1:40:21] that. That way, you have a little bit
[1:40:22] more flexibility and you still have some
[1:40:24] sort of blend. Or or you can just adjust
[1:40:26] the mean crease here a little bit, which
[1:40:28] is what I'm going to be doing. So, I'm
[1:40:29] just going to bring it up to maybe like
[1:40:31] Yeah. So, I'm just going to bring it up
[1:40:33] to a one actually cuz I kind of want it
[1:40:35] completely distinct. Um, and then maybe
[1:40:38] I want one more up here. SC, I'm just
[1:40:41] going to eyeball it. We could have made
[1:40:42] them identical in size, but honestly, it
[1:40:44] doesn't really matter. Um, cool. Let's
[1:40:46] do the same thing again. Alt E extrude
[1:40:48] long normals. Hold alt to select the
[1:40:51] loop. Go into edge select. Hold alt to
[1:40:54] select the loop. Alt to select the loop.
[1:40:57] And just increase the increase to all
[1:41:00] the way to one. Just like that. And then
[1:41:02] we kind of have something like that.
[1:41:03] Scale that down. S. Again, you can
[1:41:06] always change the size of stuff if you
[1:41:09] want to. Uh, let's select these faces
[1:41:12] here. Um, inside I I kind of just want
[1:41:16] to inflate the inside a little bit. So,
[1:41:17] I'm going to select these. Alt S kind.
[1:41:20] And I think if it's too round inside,
[1:41:22] you can add a bracing edge loop on the
[1:41:24] inside as well. Um, I don't think I need
[1:41:27] that, so I'm just going to leave it as
[1:41:28] is. And now that I'm looking at it, this
[1:41:30] looks a little too thin for the bulky
[1:41:31] vibe we're going. So, I'm going to
[1:41:32] select this edge loop, shift, alt, and
[1:41:34] select this edge loop. Just bring it up
[1:41:36] a little bit. Cool. That looks a little
[1:41:38] bit better. Um, and maybe the top is
[1:41:41] like too short now. So, we can just
[1:41:42] increase that. Cool. Anyway, um, I don't
[1:41:45] want to spend too much time on that. So,
[1:41:47] now we can just create the handle. I'm
[1:41:49] just going to use a Taurus for this
[1:41:50] because, uh, we could use some other
[1:41:53] method, but I'm just going to use a
[1:41:54] Taurus. Again, we don't need Probably 24
[1:41:57] is good enough for us. I'm just going to
[1:41:59] 24 is probably overkill too honestly,
[1:42:01] but whatever. Let's go into edit mode.
[1:42:03] Let's go into wireframe. Let's just
[1:42:05] delete these vertices here. Cool. Let's
[1:42:08] do RX90.
[1:42:09] Hit minus just because I'm on the wrong
[1:42:11] side. Let's just go somewhere over here.
[1:42:14] Kind of like this. Um, actually, I want
[1:42:17] the handle to come down a little bit.
[1:42:18] So, I'm going to go into wireframe. Just
[1:42:20] going to select these. Oops. Let's get
[1:42:22] rid of those. GZ. And just bring it down
[1:42:24] kind of like that. Cool. Add modifier.
[1:42:27] Mirror modifier right here. Select this.
[1:42:30] Let's do it in the Y direction. So from
[1:42:32] far away, this might be an issue. So
[1:42:33] let's just or actually close up. Let's
[1:42:35] just make it a little bit smaller. Uh
[1:42:38] maybe about the same size as the band
[1:42:40] itself. So there we kind of have like a
[1:42:42] small little basket thing. Cool. Okay.
[1:42:44] Let's add another type of flower inside
[1:42:46] here. So what I'm going to do is shift A
[1:42:49] and probably just add a cube. Let's go
[1:42:51] into edit mode. And whoops, I
[1:42:54] accidentally Let's just extrude this up.
[1:42:57] Uh, give it a subdivision surface
[1:42:59] modifier. Cool. Let's go into local view
[1:43:01] just to do this shade smooth. And, uh,
[1:43:04] maybe like make that a little bit
[1:43:06] smaller. Uh, and then for the sides, I'm
[1:43:08] just going to duplicate this one. GY SY.
[1:43:12] Kind of like that. And then I'm just
[1:43:14] going to go into side view and probably
[1:43:15] shape it up a little bit. So, definitely
[1:43:17] one down here.
[1:43:19] And oh, let's go into wireframe just to
[1:43:21] make sure I select everything like the
[1:43:23] ones behind
[1:43:26] this one. I might make it down a little
[1:43:27] bit. We probably need a guard loop on
[1:43:29] both sides just to kind of make it just
[1:43:33] so we can h have that inset there. Um,
[1:43:36] cool.
[1:43:38] So, yeah, you can definitely play around
[1:43:40] with it if you want to. Maybe maybe we
[1:43:42] can have like a bevel here.
[1:43:45] And let's do S Y and just like push it
[1:43:48] in a little bit so we get like a line
[1:43:50] there. Cool.
[1:43:53] Um, let's go into the other side view.
[1:43:55] Let's go into edit mode. Let's add like
[1:43:57] a loop cut here. Let's go into wireframe
[1:44:00] and let's just like shape this kind of
[1:44:02] like that. Actually, let's turn on
[1:44:03] proportional editing here. Select these.
[1:44:06] Let's just increase the sphere of
[1:44:07] influence a little bit. Kind of make it
[1:44:09] a little bit bendy. kind of like that. I
[1:44:12] don't know if I want this to completely
[1:44:13] wrap over, but uh it doesn't really
[1:44:15] matter cuz you can always change that.
[1:44:18] Cool. Now, let's just add a mirror
[1:44:20] modifier. Let's select this over here.
[1:44:22] Let's do it on the Y. Let's go up. Let's
[1:44:25] duplicate it. Let's do R 90 like so.
[1:44:28] Now, let's do it along the X and get rid
[1:44:30] of the Y. And let's just move this over
[1:44:32] here. All right. For the stem, you know
[1:44:34] the deal. We're going to shift right
[1:44:35] click somewhere where we want our stem
[1:44:37] to start. So, maybe like here. We're
[1:44:39] going to shift A at a single verticy,
[1:44:41] not a curve, cuz we're going to create a
[1:44:43] curve from this extruded single verticy.
[1:44:46] So maybe let's just move this up a
[1:44:48] little bit here. And we can rotate it. I
[1:44:50] guess it doesn't really matter anyway.
[1:44:52] Let's convert this to a curve. Convert
[1:44:54] to curve. Come over here. And then in
[1:44:56] bevel, just increase the depth a little
[1:44:58] bit. Cool. Just like that. Right click,
[1:45:00] shade smooth. Now, I do know that I want
[1:45:03] to revisit this a little bit later. Oh,
[1:45:06] looks like it's offcentered. So, let's
[1:45:08] go into wireframe here and center that.
[1:45:11] I do want to revisit this flower later
[1:45:13] and make variations of it. So, I'm going
[1:45:14] to do right now I'm going to shift
[1:45:16] duplicate this and move it into a new
[1:45:18] collection called flower v1 modifiers.
[1:45:23] Modifiers.
[1:45:25] And I'm just going to click and drag
[1:45:26] this into our modifiers collection like
[1:45:28] we did for the book. And since we
[1:45:30] already made a collection for it, we
[1:45:31] might as well make a collection for this
[1:45:33] called flower v1. And this is the one
[1:45:35] without modifiers. So now let's do F3
[1:45:38] convert this to mesh. Let's also convert
[1:45:40] these to mesh. So F3 convert to mesh.
[1:45:43] And let's join it with the bottom here
[1:45:45] because the origin point starts there.
[1:45:46] And that's kind of exactly why I wanted
[1:45:48] to start there instead of from the top.
[1:45:50] So now when we scale, it's like that.
[1:45:52] Cool. Let's place it in here. Shift S,
[1:45:54] selection to cursor. Scale it down a
[1:45:56] little bit. Cool. Scale it up maybe.
[1:46:00] Shift Duplicate. RZ. Shift D. One more
[1:46:04] time. Cool. Maybe something like that.
[1:46:06] Cool. Now we kind of have like a small
[1:46:08] little flower basket, which is really,
[1:46:09] really cute. All right, let's create
[1:46:11] like a billboard thing that you can like
[1:46:13] put shelf stuff on. So, what I'm going
[1:46:14] to do is shift right click or add a
[1:46:16] plane. This is actually the same way we
[1:46:17] did this. So, just a refresher, I guess.
[1:46:20] R Y. You can skip ahead if you don't
[1:46:21] want to watch this again. Let's then go
[1:46:23] into edit mode, subdivide, subdivide,
[1:46:25] subdivide. Cool. Let's select the center
[1:46:27] right here, right click, loop tools, go
[1:46:29] into circle, then add a guard loop a
[1:46:32] little bit like that. Then delete those
[1:46:34] faces. Let's add a solidify modifier
[1:46:37] like so. Gy, sorry, gx. Move that up.
[1:46:41] Turn on even thickness. Not that I think
[1:46:44] it changes anything here, but I don't
[1:46:45] think it does. Right click, shade auto
[1:46:47] smooth. Cool. Sweet. Let's uh go and
[1:46:50] apply our solidify modifier. Right now,
[1:46:51] let's select this edge loop here and
[1:46:53] just delete those faces. Let's add two
[1:46:56] array modifiers, one and two. This one
[1:46:59] is going to be zero, and then this one's
[1:47:01] going to be one. That way, we can have
[1:47:02] like a grid system. So, I don't know.
[1:47:04] Maybe I'm going to go for something uh
[1:47:07] four this way and then maybe four this
[1:47:09] way. Cool. I don't know. Whatever you
[1:47:12] want. Maybe five in this way. So, it's
[1:47:14] kind of just a little bit longer. But
[1:47:15] again, that's kind of really up to you.
[1:47:18] Cool. Sx. Maybe bring that up a little
[1:47:21] bit. GX.
[1:47:23] Cool. Circles might be a little bit too
[1:47:27] big. Let me see. Let's just select this
[1:47:29] loop. Alt S. Um I guess that's okay.
[1:47:32] Actually, it's not that big a deal. All
[1:47:34] right, let's copy over one of our bevel
[1:47:36] modifiers. So, I'll just do this one
[1:47:38] again. Copy to selected. Cool. And I
[1:47:40] think I want to make modifications to
[1:47:42] this. So, I'm going to move it to a new
[1:47:43] collection call.
[1:47:45] I don't know what they call this.
[1:47:46] Modifiers. I don't know what they call
[1:47:48] that. So, I'm just going to create that
[1:47:50] new collection. And um billboard
[1:47:53] modifiers is going to go in there. All
[1:47:54] right. So, now let's hit merge on all
[1:47:57] our array modifiers. So, the overlapping
[1:47:59] vertices like here and here would be
[1:48:01] merged. And then let's just apply that.
[1:48:03] Let's apply this one. Uh, and now what
[1:48:05] we can do is go into edit mode. Select
[1:48:08] this edge loop here. Select this edge
[1:48:09] loop here. Select this edge loop. Edge
[1:48:12] loop here. This one. This one is and
[1:48:15] down here. And down here. Whoops. And
[1:48:18] down here. Control E. Bridge edge loops.
[1:48:21] Cool. Just like that. Uh, so honestly,
[1:48:24] maybe instead of beveling this one, we
[1:48:26] can give it like a subdivision. So,
[1:48:28] let's just try that.
[1:48:30] Yeah, I guess if you want like this,
[1:48:33] this would be cooler for um I think it
[1:48:37] looks better with a subdivision surface
[1:48:38] than a bevel. Um but honestly, no one
[1:48:41] can tell. And subdivision surface will
[1:48:43] add a lot of geometry. So I feel like
[1:48:45] we'll just stick with bevel. Uh so bevel
[1:48:48] will be okay for this. Go for these ones
[1:48:50] down here. So I'm going to hit uh alt
[1:48:52] shift alt. Select this one as well.
[1:48:55] Shift duplicate right click cancel. P
[1:48:56] separated by selection. Cool. And now we
[1:49:00] can just sx scale it up a little bit.
[1:49:02] Um, looks like it's going that way for
[1:49:05] some reason. So, we can just do sx minus
[1:49:07] one. Cool. Let's select this loop here
[1:49:09] and hit fill to fill that. Same thing
[1:49:12] here. Let's over here and fill that. And
[1:49:14] let's apply our scale to make sure
[1:49:15] that's okay. And the bevel is way too
[1:49:18] strong. So, let's just um decrease that
[1:49:20] just a little bit there. Honestly, I
[1:49:22] don't even know if we want a bevel on
[1:49:23] this one, but either way, it's fine. Uh,
[1:49:26] so yeah, there we kind of have that.
[1:49:29] Shift, right click, add a plane. Let's
[1:49:32] scale it down. SY gy. Just place it
[1:49:36] right on top of one of these. Go into
[1:49:38] edit mode. E extrude upwards. Kind of
[1:49:40] like so. Let's copy over the bevel
[1:49:42] modifier. Copy modifiers. Cool. Apply
[1:49:44] our scale. Make sure everything's
[1:49:46] working. Shade auto smooth. Syx.
[1:49:50] Let's go into wireframe. Just layer it
[1:49:52] on right on top of there. kind of just
[1:49:55] and then this one can also have a
[1:49:56] weighted normal just to fix some of the
[1:49:58] shading issues. All right, let's fill up
[1:50:00] these two. So, what I'm going to do is
[1:50:01] select this, go select, control L, shift
[1:50:04] D, duplicate, GZ, move it over here.
[1:50:07] Let's turn on snapping. Okay, so I have
[1:50:08] vertex snapping already. GZ, just snap
[1:50:10] it to a vertex. Kind of like that. So,
[1:50:12] let's do the same thing again. Ctrl L.
[1:50:14] Let's do shift D, uh, Gy, and just snap
[1:50:18] it over here somewhere. gy and then snap
[1:50:20] it in the center. Same thing here. Okay,
[1:50:22] let's shift D duplicate GZ gy S Y. Scale
[1:50:26] it down. G Y. Kind of just like that.
[1:50:28] Let's create like a hook for one of
[1:50:30] these last ones. So, I'm going to go
[1:50:31] into edit mode on this. Let's just
[1:50:34] select where we want to start. Probably
[1:50:35] here. Shift S cursor to selected.
[1:50:37] Whoops. That'll just center it right
[1:50:39] there. Let's add a single verticy.
[1:50:41] Single vert like so. Remember, make sure
[1:50:44] you are in vertex select. Let's go to
[1:50:46] side view. Let's go into wireframe.
[1:50:48] Let's just hit E to extrude it out and
[1:50:51] lock it on the X- axis. E on the Z-axis
[1:50:54] and then E on the X- axis again. Kind of
[1:50:56] just like that. Then let's go into edit
[1:50:58] mode. Let's select these two vertices.
[1:50:59] Hit Ctrl +B for bevel. V to add some
[1:51:02] faces. Sorry, some more vertices. I'm
[1:51:05] going to use my middle mouse button. I
[1:51:07] think I just need one. So, I'm just
[1:51:08] going to go for one bevel. And maybe
[1:51:09] something like this for the hook. Cool.
[1:51:12] Then we can just F3 convert to a curve.
[1:51:15] Same thing like we did for the stem.
[1:51:16] Let's come down to bevel and just
[1:51:18] increase the depth a little bit. And
[1:51:20] actually, what we want to do is make it
[1:51:23] the size of the hole. So, let's just
[1:51:25] increase that. We can eyeball it. We
[1:51:26] don't have to snap it or do anything. As
[1:51:28] long as it looks good enough. If you
[1:51:30] want, you can still edit your curve.
[1:51:32] This looks This is definitely way too
[1:51:33] far out there. Um, maybe this is out a
[1:51:37] little bit too much. Uh, I don't know.
[1:51:38] All right, let's go into school. That
[1:51:40] looks nice. Let's shade smooth just to
[1:51:42] make sure. Okay, maybe we increase the
[1:51:44] resolution just a little bit. Okay,
[1:51:46] that's fine. Now we can just F3, convert
[1:51:48] to mesh. Let's go into edit mode. Let's
[1:51:50] select this edge loop and hit fill.
[1:51:52] Well, actually shade auto smooth this
[1:51:54] time. Now, I'm definitely seeing some
[1:51:55] issues here and here. Now, that might
[1:51:58] not be an issue. We could probably fix
[1:52:00] it with some rotation and some movement.
[1:52:02] Or what we can do is control B and kind
[1:52:03] of just like smooth it out a little bit.
[1:52:05] It's not a perfect solution fix because
[1:52:07] of the angle and the things like that,
[1:52:09] but it's definitely not noticeable
[1:52:11] anymore. Um, so that's totally fine. Uh,
[1:52:15] it definitely looks a little bit
[1:52:16] deflated here. You could edit that if
[1:52:18] you want. I'm not going to bother doing
[1:52:19] that. Anyway, let's just copy our bevel
[1:52:21] modifier to this. So, I'm just going to
[1:52:22] copy my modifier so it kind of looks a
[1:52:24] little bit similar to this one right
[1:52:26] here. Cool. Let's apply our scale just
[1:52:28] to make sure everything is fine. Okay.
[1:52:29] So, I actually I don't know, maybe I
[1:52:32] want to align it with with uh this hole
[1:52:34] here. Not that that makes sense. Um,
[1:52:36] just because I don't want it to take up
[1:52:38] everything. Uh, yeah. So, our picture
[1:52:40] frame honestly is just going to be our
[1:52:41] computer. So, I'm just going to
[1:52:42] duplicate that. Shift S. selection to
[1:52:44] cursor. Scale it down. GZ. Bring it up.
[1:52:47] SC kind of like so. That's pretty cool.
[1:52:49] Let's go into edit mode. Let's bring
[1:52:51] this down kind of like here. And GZ and
[1:52:54] uh over here. Over here. SC there. Cool.
[1:52:59] There's kind of like our picture frame.
[1:53:01] Now, for this one, I also did add five
[1:53:03] segments. Adjusted them out. And in
[1:53:06] geometry, I used arc. And in shading, I
[1:53:08] did harden normals, which I mentioned a
[1:53:10] little bit earlier in the video when I
[1:53:11] teleported from the future. And I'm just
[1:53:14] going to alt S and scale that in kind of
[1:53:17] a little bit. Like so. S Y. Cool. And
[1:53:21] then let's go into edit mode. Just
[1:53:22] select these faces and do GX. Move it
[1:53:26] out a little bit. Kind of like that. GY.
[1:53:29] GX. Bevel is definitely a little bit too
[1:53:32] strong here. So, I'm definitely going to
[1:53:33] reduce that a little bit. Kind of like
[1:53:35] so. All right. Let's go into edit mode.
[1:53:37] Let's go into this back view and let's
[1:53:38] create a picture frame stand. So, I
[1:53:41] actually I'm just kind of going off of
[1:53:42] memory here. I don't know what they look
[1:53:44] like. R Y 90. Maybe something like this.
[1:53:47] And then they rotate a little bit. Go
[1:53:49] into edit mode. Eextrude this out. E
[1:53:52] extrude this out. Y. Nope. GXX. Okay.
[1:53:56] It's going to be like this. Scale this
[1:53:58] down a little bit. Um, and then I think
[1:54:00] it's going to be resting on one of these
[1:54:02] sides. Actually, let's just merge this
[1:54:03] by at center. Um, and then I think it's
[1:54:06] going to be resting kind of like this.
[1:54:08] So, we can scale this down.
[1:54:10] like so.
[1:54:13] Cool. And then our y
[1:54:16] gy gx. Let's add a solidify modifier.
[1:54:23] Let's just rotate this a little bit and
[1:54:25] have it rest. I think that doesn't
[1:54:26] really make sense logically. So, I'm
[1:54:28] just going to move this up right here.
[1:54:30] Uh I don't actually know what the back
[1:54:32] of a picture frame looks like. And
[1:54:33] having a fold actually might be a little
[1:54:35] bit more realistic. I'm not going to
[1:54:37] bother adding a bevel modifier to this
[1:54:38] just because no one's going to be paying
[1:54:40] that close attention to it, if at all.
[1:54:43] It just kind of needs to be there. So, I
[1:54:46] don't want to add all that extra
[1:54:47] geometry and information for no reason.
[1:54:49] All right, so let's make a slipper. I'm
[1:54:51] just going to add a plane. Scale it down
[1:54:54] in like a slipper shape. Um, then I'm
[1:54:57] just going to extrude. All right, let's
[1:54:59] create a slipper. I'm just going to
[1:55:01] probably add a plane again and then just
[1:55:03] scale it in arbitrary shape of a
[1:55:07] slipper. Cool. Let's add a subdivision
[1:55:10] surface modifier.
[1:55:12] Cute. Let's add two control loops. Um,
[1:55:15] and
[1:55:17] I guess I kind of like it like that.
[1:55:18] Maybe scale it down a little bit. Maybe
[1:55:20] move this one down in the Y and kind of
[1:55:23] like scale that down. Maybe the back can
[1:55:25] be a little bit smaller. We're not going
[1:55:27] for a realized scale one. We're kind of
[1:55:28] going for a cute one. So, let's add a
[1:55:31] solidify modifier here. Um, let's go. We
[1:55:34] want to solidify it before we subdivide
[1:55:36] it. Let's increase some thickness a
[1:55:38] little bit. Cool. So, we got some
[1:55:40] chunkiness there. Um, let's do even
[1:55:44] thickness. And let's kick shade smooth.
[1:55:48] Cool. There's like the base of our
[1:55:49] slipper. All right. Let's go into local
[1:55:51] view and let's just add a plane. So, I'm
[1:55:55] just going to shift a add a plane. Uh,
[1:55:56] and I'm just going to scale that down
[1:55:58] until I get a shape that I want to
[1:56:00] cover. So, probably something like here.
[1:56:02] Gy GX. That looks pretty good. Let's add
[1:56:05] a loop cut down the center. Let's select
[1:56:07] that loop cut and let's go into
[1:56:09] wireframe actually and just bring that
[1:56:11] up. Honestly, it doesn't have to be
[1:56:12] perfectly straight up primarily because
[1:56:15] slippers in real life, their holders are
[1:56:17] never perfect. Having some distortion
[1:56:19] actually wouldn't be bad at all. But
[1:56:21] anyway, I'm just going to control B and
[1:56:23] scroll up on my mouse wheel uh for some
[1:56:26] more vertices until they're about even
[1:56:29] in length along the curve. So, I think
[1:56:31] that's going to be more than enough. So,
[1:56:33] that says eight there, which means it's
[1:56:35] probably 10 in total. And I'm not using
[1:56:37] a mirror modifier this time because I
[1:56:39] don't want them to be symmetrical. And
[1:56:41] I'm just going to select the middle one,
[1:56:42] turn on proportional editing, and kind
[1:56:44] of just uh bring it up until I get
[1:56:47] something round. And then let's bring
[1:56:49] out some of these. So this can be a
[1:56:51] little bit round. This one can be a
[1:56:53] little bit round as well. Cool. Like so.
[1:56:57] Might take a little bit of work, a
[1:56:59] little bit of effort, but that's totally
[1:57:01] okay. Um, and let's Okay, that's okay.
[1:57:05] Let's maybe have to rotate some of them.
[1:57:08] That's cool. Cool. Then we can just
[1:57:10] bring it down like so. Let's go into
[1:57:12] solid view. Um, let's add a we can just
[1:57:17] do control 2 for subdivision surface
[1:57:19] modifier. Add two control loops. S Y
[1:57:22] Whoops. Let's turn off proportion.
[1:57:23] Adding S Y. Move it out a little bit.
[1:57:26] And luckily, since it's inside, we don't
[1:57:28] actually need control loops down here to
[1:57:30] flatten out the bottom because it's
[1:57:32] inside anyway. So, we just need these.
[1:57:36] And honestly, maybe leaving this curved
[1:57:38] two is fine. Let's just apply scale
[1:57:40] shade smooth. Maybe one is okay. Yeah,
[1:57:43] one is actually more than enough for
[1:57:44] this. I wonder if one is here is fine as
[1:57:47] well. No. Okay, this one definitely
[1:57:49] needs two. Cool. Let's add a solidify
[1:57:52] modifier here. Let's do it before the
[1:57:54] subdivision. Even thickness and just
[1:57:58] bring it up a little bit. Kind of like
[1:57:59] that. Uh so there we kind of have our
[1:58:02] slipper gy. All right, let's adjust our
[1:58:05] slipper a little bit more. I think maybe
[1:58:08] just scale this down a tad bit.
[1:58:12] Um, and then let's just align this a
[1:58:14] little bit better. Cool. Yeah, doesn't
[1:58:17] have to be perfect. So, I'm just going
[1:58:18] to G, shift D, move it under over here.
[1:58:23] And then, of course, we need two. So,
[1:58:25] let's shift DG. And then, let's move it
[1:58:26] somewhere over here at a different
[1:58:28] rotation.
[1:58:29] All right, let's just add some boxes
[1:58:31] here. Uh, again, just a plane. Scale it
[1:58:34] down. Let's get in box shape. You know
[1:58:36] the drill. Extrude. Go here. This one
[1:58:39] I'm just going to P separate by
[1:58:40] selection because it'll cover the top.
[1:58:42] Let's just do object set origin. Origin
[1:58:45] to geometry. Scale that up. Go into edit
[1:58:47] mode. AE extruded upwards. Cool. Scale
[1:58:50] it down slightly. Select both of these.
[1:58:52] Come over here. Come over here and copy
[1:58:55] to selected. Apply our scale. Make sure
[1:58:57] that's good. Cool. Let's select these.
[1:58:59] Let's adjust the amount a little bit.
[1:59:00] Again, I'm holding alt so it affects
[1:59:02] both of them at the same time. And we
[1:59:03] don't need that many segments. So four
[1:59:06] should be okay. Kind of like so. All
[1:59:08] right. Now, let's add a small little
[1:59:10] sign detail here. I don't honestly, it's
[1:59:12] like a label or something. So, R Y 90.
[1:59:16] Scale it down. Cool. S Y like so. Go
[1:59:19] into edit mode. E extrude it out just a
[1:59:22] little bit. Let's add a loop cut down
[1:59:24] here and extrude this. And this can be
[1:59:26] like a symbol statement or something.
[1:59:28] So, it's like a box with some info. I'm
[1:59:30] not going to give this bevel modifier
[1:59:31] just because it's so far away. All
[1:59:33] right. Let's add like a small hanging
[1:59:34] plant here. So, it kind of fills up this
[1:59:36] empty space. So, what I'm going to do is
[1:59:38] shift right click and what I'm going to
[1:59:40] do is shift A and add for a single
[1:59:42] verticy like we did for all the other
[1:59:45] curves. Let's go into side view here.
[1:59:47] Again, make sure you're in vertex
[1:59:48] select. Let's go into wireframe. And I'm
[1:59:51] just going to extrude downwards like a
[1:59:53] wire sort of thing. Uh, sorry, I mean
[1:59:55] like a rope. We can turn our
[1:59:56] proportional editing. I don't know why I
[1:59:58] have that on. Generally, uh, you can use
[2:00:01] physics simulations to wrap your rope a
[2:00:03] little bit better around it and a lot
[2:00:05] more realistic. I'm just doing it this
[2:00:08] way. So, Ctrl + B and V just to bevel
[2:00:10] this area right here. Probably Ctrl + B
[2:00:12] and V to bevel up here as well. The
[2:00:15] reason I'm just doing it this way is
[2:00:16] because it's faster. Um, it might be
[2:00:20] less realistic, but it's definitely
[2:00:21] faster. So, I don't want it too far down
[2:00:24] actually. Maybe just like so. Here is
[2:00:26] like Okay, cool. Um, so it'll definitely
[2:00:30] be less realistic, but that's totally
[2:00:32] okay. Let's convert to curve. Let's uh
[2:00:34] increase the the depth. Let's increase
[2:00:36] the resolution here. Uh, right click,
[2:00:38] shade smooth. Let's add a subdivision
[2:00:40] surface modifier with control 2. And you
[2:00:42] can see we kind of already have
[2:00:43] something just like that. If you need to
[2:00:46] adjust your curve, you can totally do
[2:00:47] that. Uh, if you want to. Maybe I want
[2:00:50] to um, you know, I think that's okay.
[2:00:53] So, I'm just going to leave it like
[2:00:55] that. All right. Let's add a flower pot
[2:00:56] over here. So, what I'm going to do is
[2:00:58] just add a cylinder. 16 vertices is
[2:01:01] okay. Let's go into edit mode. Let's
[2:01:02] just add a loop cut here. I don't know.
[2:01:05] I think that's okay. Hold Alt to select
[2:01:07] that full loop. Alt E extrude along
[2:01:09] normals. Bring that up. Uh maybe this
[2:01:12] side. This we can expand it a little
[2:01:14] bit. S. Shift Z just to make it a tad
[2:01:18] bit wider. Cool. That's kind of cool.
[2:01:20] Then this here. Let's insert a little
[2:01:22] bit and just extrude downwards. Right
[2:01:25] click shade auto smooth. Let's copy over
[2:01:27] one of these bevel modifiers. Copy.
[2:01:30] Seven is definitely going to be too much
[2:01:31] for this pot. So we can lower that. And
[2:01:33] we can also lower them out as well. I
[2:01:35] don't want it too bulky. Cool. There's
[2:01:38] like our flower pot. Uh I don't like how
[2:01:40] the bottom is so wide, so I'm just going
[2:01:42] to angle that a little bit. And let's
[2:01:43] just move it kind of like that. Cool.
[2:01:46] Let's just scale it down.
[2:01:48] Um place it over here. Let's just make
[2:01:52] sure this is uh you know, this is like
[2:01:54] kind of looks like it's wrapping sort of
[2:01:56] thing. And then maybe we can actually
[2:01:58] just put these on the side here. Um,
[2:02:02] that way it kind of looks like it's uh
[2:02:04] connected to the bucket. If you want,
[2:02:05] you can add details here to make it more
[2:02:07] seamless, but I'm not going to bother
[2:02:08] doing that plant thing. So, what I'm
[2:02:10] going to do is go into top view. Let's
[2:02:11] add a plane. Let's go into local view
[2:02:13] for this. And I'm just going to shape.
[2:02:16] Let's add a loop cut here. And I'm just
[2:02:17] going to shape my thing to kind of look
[2:02:19] like a leaf. So, maybe let's E and
[2:02:21] extrude Y and scale that down.
[2:02:25] And Gy and bring this down. Maybe add a
[2:02:29] loop cut in the center here. Let's maybe
[2:02:31] extrude one more time.
[2:02:34] Gy. And let's make this a lot thinner.
[2:02:37] So we kind of have like a
[2:02:40] something like this. That kind of looks
[2:02:42] like a shape of a leaf, right? So now
[2:02:45] what we can do is add a subdivision
[2:02:47] surface modifier. One might be okay. One
[2:02:49] is okay, I think. Anyway, let's go in
[2:02:51] here. Let's just extrude upwards. All
[2:02:54] right. So there's our leaf. Right click.
[2:02:56] Shade smooth. And I want some detail in
[2:02:58] the center. So I'm going to go into edit
[2:03:00] mode and probably add like two loop
[2:03:02] cuts. One on this side and bring that
[2:03:06] in. And then one on Whoops. One on this
[2:03:08] side as well. Then one on this side and
[2:03:11] bring it in. And then with this middle
[2:03:13] one selected, hold control and probably
[2:03:16] just GZ and move that in a little bit.
[2:03:18] Yeah. And I guess if we want to, we can
[2:03:20] select these faces and just SX and move
[2:03:23] them a little bit closer just for a
[2:03:25] little bit more pinching here, you know.
[2:03:28] Anyway, let's create like a stem thing.
[2:03:29] I don't know what they call it. So,
[2:03:31] possibly here. Oh, actually, let's
[2:03:35] include these and just see what it gives
[2:03:36] us. Ey.
[2:03:38] Cool. So, that looks nice. Let's add two
[2:03:41] supporting loops here. S Y and kind of
[2:03:44] just pull it out. Sorry. along with the
[2:03:47] plant, we can have like a small bud, you
[2:03:49] know, like the things before they
[2:03:50] blossom or seeds or whatever they call
[2:03:52] that. So to do that one, I think what we
[2:03:55] can do is a plane again. Let's go into
[2:03:58] edit mode. Let's just extrude it up and
[2:04:00] add a subdivision surface modifier. And
[2:04:03] let's just scale this down a little bit
[2:04:06] so it's kind of like a bud shade smooth.
[2:04:09] Cool. Let's bring this down. GZ.
[2:04:13] Now it kind of looks like an egg, but we
[2:04:15] can bring down something like this.
[2:04:17] Cool. We can go into edit mode. We can
[2:04:19] insert this face here and probably
[2:04:21] extrude down. Let's add some control
[2:04:23] loops here
[2:04:25] and here. That might be a little bit too
[2:04:28] far down. So, we can just select this
[2:04:29] and bring this up a little bit. Okay.
[2:04:31] Now, since we're going to make multiple
[2:04:33] of these, what we have to do now is
[2:04:35] delete these faces right now. Uh that
[2:04:37] way we'll save because we'll never see
[2:04:39] them. We want to delete those. Now, the
[2:04:41] other models, I didn't preemptively
[2:04:42] delete some of them primarily because I
[2:04:45] was thinking of revisiting that later
[2:04:47] and they were kind of easy to fix later.
[2:04:49] However, for this, we definitely want to
[2:04:51] delete it in advance because we know
[2:04:52] we'll never see that and it'll just take
[2:04:54] up space. Anyway, let's come over here
[2:04:56] and I'm just going to add a cylinder.
[2:04:59] Now, 16 vertices is okay. Let's do RX
[2:05:02] 90. And let's just scale it down and Sy
[2:05:05] and kind of just scale it up and scale
[2:05:07] it down again. and shift shade auto
[2:05:11] smooth. And now what we can do is just
[2:05:13] shift duplicate this and kind of go like
[2:05:17] so. Shifty duplicate. Let's put over
[2:05:19] there. I kind of want it to taper off,
[2:05:23] which means the top has a much smaller
[2:05:25] leaf. So what we can do is just
[2:05:27] duplicate this. Duplicate.
[2:05:30] Um, and then I want to end on a leaf. So
[2:05:32] let's just make it smaller. We can
[2:05:34] change the rotation a little bit. Like
[2:05:36] so. All right. So yeah, I just
[2:05:38] duplicated a bunch of times and rotated
[2:05:39] a few of them on each side. And now what
[2:05:42] we want to do is add a bunch of loop
[2:05:44] cuts here. So honestly, I don't really
[2:05:46] know how many I'm doing. I feel like
[2:05:47] that'll be enough. You can always add
[2:05:49] more later. And now let's turn on
[2:05:51] proportional editing with O. Let's kind
[2:05:53] of just select the top. Well, let's go
[2:05:54] into wireframe. Make sure I select the
[2:05:56] back ones, too. And kind of just like
[2:05:58] thin it down a little bit. Uh so the top
[2:06:01] I definitely want it to be smaller than
[2:06:03] the other one. So let's just change the
[2:06:04] sphere of influence here. Um, I don't
[2:06:07] know if I want to merge it because then
[2:06:08] there'll be like a point and that'll be
[2:06:10] like too unrealistic. But something like
[2:06:13] this. Uh, so it's like a little bit
[2:06:15] thicker and then it thins out at the
[2:06:17] end. Cool, cool, cool. Maybe we can make
[2:06:19] this back thicker a little bit. Just
[2:06:21] kind of not too big, but just slightly
[2:06:23] thicker. Cool. So once your plant is
[2:06:27] done, uh, wh I guess we have to readjust
[2:06:29] these now.
[2:06:31] OB, of course, we got to adjust these.
[2:06:34] Let's make sure everything is inside.
[2:06:36] Make sure go to side view and everything
[2:06:38] is inside as well. All right. So, when
[2:06:40] you have a plant that you're happy with,
[2:06:42] uh, let's just select all this, shift
[2:06:44] duplicate, GX, and move this into a new
[2:06:47] collection. And I'll call this hanging
[2:06:48] plant. Hanging plant, and then
[2:06:50] modifiers.
[2:06:52] Uh, I think I had underscore. So, I'm
[2:06:54] just going to use the same navigation.
[2:06:56] I'm just going to click and drag this
[2:06:57] into our modifier collection. Right. So,
[2:07:00] then select these and let's move this to
[2:07:03] a new collection. hanging plant create.
[2:07:07] Cool. And we can just delete these
[2:07:08] because we don't need them anymore.
[2:07:10] Okay. So, make sure your everything is
[2:07:12] looking good. So, let me just check. Uh
[2:07:15] yeah. So, let's join these. And it seems
[2:07:17] like they have different levels of
[2:07:18] subdivision surface. So, we have to
[2:07:20] apply these first. I'm actually going to
[2:07:22] select all of these. I'm actually going
[2:07:24] to select all of these because I don't
[2:07:25] think they have to be on level two. I'm
[2:07:27] going to hit alt, hold alt, and just
[2:07:29] click this. And now you can see all of
[2:07:31] them will only have a level up one. So
[2:07:33] these all have a level one. Now we can
[2:07:34] just hit A to select everything. F3,
[2:07:36] convert to mesh. This will apply all the
[2:07:38] modifiers on all the leaves. And now we
[2:07:40] can just select everything and hold
[2:07:43] shift to select this as our active
[2:07:46] object. Ctrl + J. And now we just have a
[2:07:48] plant here. Okay. So now what we want to
[2:07:50] do is like bend it a little bit to make
[2:07:52] it a little more variety because real
[2:07:54] life plants are really straight like
[2:07:56] this, right? So what you could do is go
[2:07:58] into wireframe and turn on proportional
[2:08:01] editing. go into edit mode and honestly
[2:08:02] just like start moving stuff around with
[2:08:04] like proportional editing. And honestly,
[2:08:06] this is like an approach that is fairly
[2:08:08] fairly common. Or the other thing if you
[2:08:11] wanted to do a little more procedurally
[2:08:13] is to add a modifier. And this one is
[2:08:16] called a simple deform modifier. And
[2:08:19] right now it's really really messed up.
[2:08:21] So maybe let's apply our scale. And it's
[2:08:23] a little bit better here. And you can
[2:08:25] see that you can change the angle and
[2:08:28] it'll kind of like deform it, right?
[2:08:29] It's like doing the work for you. You
[2:08:31] can try and play around with these other
[2:08:34] axes as well and some of these other
[2:08:35] formats like bend. So bend is kind of
[2:08:38] doing that kind of cool thing. And then
[2:08:40] if you want you can add another simple
[2:08:41] deform modifier on top. So one of them
[2:08:43] is twisting whereas another one is
[2:08:45] bending them. Super super cool. Right.
[2:08:48] And then you can play with some of these
[2:08:50] other ones like taper which kind of
[2:08:52] already adds a taper for us on our
[2:08:54] object. Right? You can see that it's
[2:08:56] kind of tapering. It's making the bottom
[2:08:57] bigger than the top. So it kind of saves
[2:09:00] out on what we did already. And then you
[2:09:03] also have something like stretch and
[2:09:04] things like that. And then and then
[2:09:06] yeah, you have more complicated options
[2:09:07] here, but uh we're not going to be
[2:09:09] getting into that. So here, you know, we
[2:09:12] have something a little bit deformed
[2:09:13] kind of like that. And of course, if you
[2:09:15] want to combine it, you can move it
[2:09:16] yourself, right? And combine it with the
[2:09:18] modifiers. You know, no real right or
[2:09:20] wrong. So there, I kind of just moved it
[2:09:22] like that. So that was really cool. Um
[2:09:23] but, you know, really, really up to you.
[2:09:25] Use modifiers. Don't use modifiers. Not
[2:09:28] really a big deal. All right. The next
[2:09:30] thing we would do is since it's going to
[2:09:32] be hanging, it would be a lot easier if
[2:09:34] we could just like move one thing and
[2:09:36] have this move along with it. Right. So,
[2:09:39] we can actually do that with a curve
[2:09:41] modifier. So, if I do shift S, cursor 2
[2:09:44] selected, and just search for a curve.
[2:09:47] So, we can add a path curve here. And if
[2:09:49] I go into edit mode, you can see it's
[2:09:50] kind of like this. So, let's turn off
[2:09:52] proportional editing and let's just
[2:09:53] rotate the curve 90° kind of like this.
[2:09:56] Let's go into wireframe. Go into edit
[2:09:57] mode. Select everything and just S Y.
[2:09:59] Well, let's turn off proportional
[2:10:00] editing and just scale it up kind of
[2:10:02] like this, right? Doesn't have to be
[2:10:05] accurate. And you can always add more if
[2:10:06] you want. Then for the branch or sorry,
[2:10:10] yeah, the branch, add a modifier. And
[2:10:13] this time we're going to go for a deform
[2:10:16] curve modifier. You can see it's in the
[2:10:17] deform menu. And then the curve object
[2:10:20] we want is going to be this path that we
[2:10:22] just created here. And now what you can
[2:10:24] see is when I edit this curve, it's
[2:10:26] going to deform across my object. Right?
[2:10:31] So it's going to actually deform my
[2:10:32] object along that curve, which is
[2:10:34] really, really cool. Right? So the
[2:10:36] reason it's not working properly right
[2:10:38] now is probably because of the origin
[2:10:40] point. But that's fine because what you
[2:10:41] can do is just select the curve and then
[2:10:43] just move the curve up until it aligns
[2:10:46] with your object. And if you need, you
[2:10:47] can go into edit mode and just extrude
[2:10:49] out another one and uh adjust the points
[2:10:52] accordingly. Go back into object mode
[2:10:54] and adjust it accordingly. So now you
[2:10:56] can see we have this curve thing here
[2:10:57] that kind of deforms our thing for us.
[2:11:00] And this way we don't have to do like
[2:11:01] proportional editing or any of that
[2:11:03] stuff. We can just adjust the curve. So
[2:11:05] what we can do to reset everything is
[2:11:07] select everything, go SZ0 just to
[2:11:09] flatten it out. Go into top view and
[2:11:11] then move everything slightly close to
[2:11:13] each other in a straight line. doesn't
[2:11:16] have to be accurate. And then we can
[2:11:18] select everything sx0 and it'll strain
[2:11:20] out. So now we have this sort of thing
[2:11:22] that we can use anywhere. So let's go
[2:11:25] make sure everything is selected. Let's
[2:11:27] enter exit local view. Let's go back.
[2:11:30] Just scale this down. Um move it over
[2:11:32] here. Shift S. Selection to cursor. Keep
[2:11:34] offset. Kind of just move it somewhere
[2:11:37] over here like RR. Let's just rotate it
[2:11:40] somewhere arbitrarily. Let's just place
[2:11:42] it in our plot like here. All right. So,
[2:11:43] what we can do now, if you can't see
[2:11:45] your curve, that's fine. We called it,
[2:11:47] we added a nerves path. I never did in
[2:11:49] the file. So, we can just search for
[2:11:50] nerves path. You can see it's right
[2:11:52] here. Let's also move that to the
[2:11:54] hanging plant collection. So, I just hit
[2:11:56] M and then I'm just going to move it in
[2:11:57] there. And now it's selected. You can
[2:12:00] hit period on your numpad key just to
[2:12:02] jump to your selection and it'll show
[2:12:03] you in the outliner. I'm sure there's a
[2:12:05] way to do it without a numpad, but I'm
[2:12:07] not familiar with it. Either way, we're
[2:12:09] here now and it's inside hanging plane.
[2:12:11] So, that's nice. Now we can just go in
[2:12:12] edit mode and adjust our plant right
[2:12:14] like so. So here we can just adjust our
[2:12:18] plant um and uh you know make it hanging
[2:12:22] off off off the the thing here. Of
[2:12:25] course if you want you can use
[2:12:26] proportional editing. Uh so you can turn
[2:12:28] on proportional editing and kind of
[2:12:30] affect you know the sphere of influence
[2:12:32] of your stretch and things like that.
[2:12:33] And if you want to duplicate this make
[2:12:35] sure you select the path and your object
[2:12:37] and shift duplicate it that way. If you
[2:12:39] want to, you can go into edit mode and
[2:12:42] still adjust your curve. You can turn
[2:12:44] off some of these in edit mode so it's
[2:12:45] easier to edit and go into local view
[2:12:48] and you can still like scale it
[2:12:50] downwards or like extrude this outwards
[2:12:52] if you need to. Ctrl L duplicate this if
[2:12:55] you want. So you can still adjust it in
[2:12:58] here if you want to. Or when you're
[2:13:00] happy with it, you can just apply
[2:13:01] everything. Same with this as well. Just
[2:13:04] apply everything.
[2:13:06] Then you can just delete your path
[2:13:07] curves. And now since they're deformed,
[2:13:11] you can still now use your proportional
[2:13:13] editing just to kind of like tidy it up
[2:13:15] and stuff like that. Uh, and then for
[2:13:16] this flower here, I literally just
[2:13:18] duplicated the flower we made earlier,
[2:13:20] and then I selected each face of this,
[2:13:23] Ctrl L, and then just did Alt S just to
[2:13:25] inflate it a little bit, holding shift
[2:13:27] just to make it a little bit like that.
[2:13:28] So I just I literally just use this.
[2:13:30] Actually, let's just delete our keyboard
[2:13:32] reference image right now. Okay, let's
[2:13:34] create a piano. I'm just going to shift
[2:13:35] right click, add a cube. Let's scale it
[2:13:37] down kind of like so in a piano shape.
[2:13:40] Then let's just add two loop cuts for
[2:13:42] the edges. So two right here. Um and
[2:13:45] then let's G move it out. Let's add one
[2:13:48] for the back. Let's just select these
[2:13:49] two fa these faces and just extrude up
[2:13:52] just like that. S Y a little bit. Yeah.
[2:13:54] Cool. Cool. That's looking good. Let's
[2:13:55] apply our scale. Let's add a bevel
[2:13:57] modifier. So I'm just going to copy from
[2:13:58] here. Whoops. Ctrl L. Copy modifiers
[2:14:01] just like so. Um, and let's change this
[2:14:05] to arc just to finish the corners up a
[2:14:07] little bit. Looks good. Let's harden
[2:14:10] normals is on. Great. Right click,
[2:14:12] shade, auto smooth. Cool. Looking like a
[2:14:15] nice piano. May I don't know if the
[2:14:17] bottom needs to be a little bit thicker.
[2:14:19] Maybe it does. So, control shift. Get
[2:14:21] the two corners like we did earlier.
[2:14:23] Maybe just move that out a little bit.
[2:14:25] Um, maybe move this up a little bit.
[2:14:27] Yeah, cool. Cool. That's what we got.
[2:14:29] Now, what we can do is add a loop cut.
[2:14:32] Maybe about this size here. Let's just
[2:14:34] select this. Shift Duplicate, right
[2:14:35] click, cancel. P separate by selection.
[2:14:37] Let's select this edge loop here. Ctrl +
[2:14:39] X to dissolve that.
[2:14:42] Now, let's select this one. Let's go
[2:14:43] into edit mode. Hit A and E and extrude
[2:14:47] it upwards. Let's add let's add object
[2:14:50] set origin origin to geometry just to
[2:14:53] reset that a little bit. And the bevel
[2:14:55] is way too strong on this one. So, let's
[2:14:57] turn down the amount of segments. And
[2:14:59] let's definitely turn up about the
[2:15:00] amount. I think this also has way too
[2:15:03] many segments. I think seven is a little
[2:15:04] overkill. And amount's a little
[2:15:06] overkill, too. So, let's fix that. All
[2:15:08] right, let's just do sy. Scale it in
[2:15:11] just a little bit. So, there's like a
[2:15:12] little bit of a gap. Cool. Now, what we
[2:15:14] can do is add an array modifier. I think
[2:15:17] that spacing actually looks pretty good
[2:15:19] uh because of the bevel modifier, but we
[2:15:21] can increase it a little bit if we want
[2:15:23] to. I don't know. That's I guess that's
[2:15:26] okay. Cool. And then let's just increase
[2:15:28] that until we fill it up.
[2:15:32] Uh probably somewhere over here seems
[2:15:35] about right. And having that little bit
[2:15:38] gap, we can go and scale it up if you
[2:15:40] want, but maybe having that little gap,
[2:15:42] I think, is perfectly acceptable.
[2:15:45] All right. So, for the black piano keys,
[2:15:47] we can just shift duplicate this. Um
[2:15:50] let's just bring it up here. Let's go
[2:15:53] into edit mode. Let's uh uh let's
[2:15:57] actually just hide this in edit mode for
[2:15:59] this one. Let's hide this in edit mode.
[2:16:00] Go into edit mode. Ctrl L. Let's just
[2:16:04] scale this down a little bit. Um, move
[2:16:07] it right here
[2:16:09] about so. And let's shift duplicate it
[2:16:12] and have one over here. Let's lock it on
[2:16:15] the X- axis. And also put it in the
[2:16:17] center somewhere.
[2:16:20] So, this should also be a little bit
[2:16:22] centered. I'm kind of just looking at
[2:16:24] the center here. It doesn't have to be
[2:16:25] perfect. Cool. And then we probably have
[2:16:28] to change the array offset. So, let me
[2:16:30] just temporarily set this to zero. And
[2:16:32] let's just shift Duplicate this. Skip a
[2:16:35] key in between like so. So, we have two
[2:16:37] white keys in between. And then this
[2:16:39] one, let's just control shift ctr L
[2:16:42] shift D GX. Move it in the center as
[2:16:46] well. We don't have to snap it or be
[2:16:48] perfect or anything. It's totally fine.
[2:16:50] Okay. Now, we can just add another one
[2:16:52] here. So, let's come to array. Let's uh
[2:16:55] just increase this factory. Again, we
[2:16:57] want to skip one just like so. So,
[2:16:58] that'll be centered there. And then this
[2:17:00] one, let's add one more here. And let's
[2:17:03] just drag it to the end. Well, it looks
[2:17:06] like we're not going to be able to fit
[2:17:08] that, which is totally okay because what
[2:17:10] we can do, let's go into edit mode, go
[2:17:13] uh go into wireframe, select this side,
[2:17:15] and just git
[2:17:18] a little bit. Um, so, well, actually, we
[2:17:21] probably should have added one more key
[2:17:22] just to see how it is. Cool. Uh, let's
[2:17:24] just go back into edit mode, GX, and
[2:17:27] kind of move it back. Just like that.
[2:17:29] And then let's go into wireframe. Let's
[2:17:32] just select this. Let's go into top
[2:17:34] view. Let's box select this. Let's make
[2:17:37] sure
[2:17:39] um
[2:17:40] I think I want the bevel actually.
[2:17:43] That's fine. So, yeah, that that should
[2:17:45] be okay for us. And here, let's make a
[2:17:47] stand. So, I'm just going to shift right
[2:17:49] click, add a cylinder. 16 might be
[2:17:51] overkill because it's really small, but
[2:17:53] you know, whatever. It doesn't really
[2:17:54] matter. Let's do shade auto smooth.
[2:17:56] Let's go into local view. Let's do RX90
[2:17:58] just like so. Let's scale that up on the
[2:18:01] Yaxis. Let's go into edit mode. Let's
[2:18:03] add a loop cut here. Let's just delete
[2:18:05] those back vertices right now. And then
[2:18:07] let's give it a mirror modifier. Uh I
[2:18:10] think it'll be Z-axis. Cool. Let's turn
[2:18:12] on clipping so they don't go through
[2:18:13] each other. Cool. Let's go into edit
[2:18:15] mode. Let's add a loop cut here. Let's
[2:18:17] select this with alt. Let's come up
[2:18:19] here. Let's do select. Checker deselect.
[2:18:21] Alt D. Extrude along normals. and just
[2:18:23] hold shift and increase that just a
[2:18:25] little bit so we have that support right
[2:18:27] there. Let's go back out. Let's make it
[2:18:29] there. I'm not going to give this a
[2:18:30] bevel modifier because it's so small and
[2:18:33] no one's going to notice about it. So
[2:18:35] maybe I'll do SY just make it as small
[2:18:38] as the piano itself. Well, the piano
[2:18:40] seems to be going inside the room. And
[2:18:42] let's deselect the room. Um like so. I
[2:18:46] kind of want this to be slightly bigger
[2:18:47] than the piano itself. And if you have
[2:18:49] troubles with keep on always selecting
[2:18:51] this, you can just come up here, enable
[2:18:53] this thing. And then now if you click
[2:18:56] it, you can't select this anymore. So
[2:18:57] that really helps. Um, so we can just
[2:19:00] box select, move it out a little bit,
[2:19:02] move this. I kind of want it slightly
[2:19:04] wider like so. So that looks pretty good
[2:19:06] to me. Then what we can do is add
[2:19:09] another mirror modifier. So let's search
[2:19:11] for a mirror modifier. This time we want
[2:19:13] to do it on the origin of this. So, make
[2:19:16] sure this set origin origin to geometry.
[2:19:18] It's in the center of that. So, it'll be
[2:19:20] centered kind of like so. And then you
[2:19:22] can move this on the X if you want it a
[2:19:24] little bit wider. All right. Let's go
[2:19:25] into edit mode. Let's add like a loop
[2:19:28] cut maybe around this size here. And I
[2:19:30] think we select these faces to extrude
[2:19:32] them up. Let's go into side view. Let's
[2:19:34] go into wireframe. And let's just E
[2:19:36] extrude it upwards like so. And then we
[2:19:38] want to crisscross them like so. S0.
[2:19:42] Typically, there is like some sort of
[2:19:44] support up top here, but I don't think
[2:19:46] anyone's ever going to look down here.
[2:19:47] So, I'm not going to bother wasting my
[2:19:49] time for that. Uh, cool. So, like even
[2:19:52] if someone looks down, they'll kind of
[2:19:53] be like, "Oh, that's still fine anyway."
[2:19:55] So, there we kind of have our support.
[2:19:56] Okay. And I think I want to give the
[2:19:58] beams a bevel modifier, but not this
[2:20:00] bottom thing. So, what I'm going to do
[2:20:01] is hold Alt just to select this entire
[2:20:04] loop thing. So, let's make sure we get
[2:20:06] the top faces as well. Cool. Let's just
[2:20:08] P separate by selection. And then let's
[2:20:11] come over here and copy our copy to
[2:20:14] selected bevel modifier applier scale
[2:20:16] scale. Make sure that works. Four
[2:20:19] segments might be too much. Whoops, I'm
[2:20:21] changing the wrong one. So, four
[2:20:23] segments might be too much. Uh, three is
[2:20:26] okay. And then we can just adjust amount
[2:20:28] a little bit here. Uh, seems like the
[2:20:31] stand seems like the stand is a little
[2:20:33] bit too big compared to the piano. So,
[2:20:35] what we can do is just select the piano
[2:20:38] and deselect this. Just hit S to scale
[2:20:41] it up like so. Cool. Then this might be
[2:20:46] a little bit too close. So, we can just
[2:20:48] do G GX together. Maybe. And now for
[2:20:52] this thing here, we kind of have like
[2:20:53] this gaping hole because that's where we
[2:20:55] separated. We can fill that if we want
[2:20:58] to, but we're going to be ending up
[2:20:59] deleting that anyway. So, for the time
[2:21:01] being, we can just do R Y and do like
[2:21:04] 180 and just like now the hidden face is
[2:21:07] on the bottom instead. We'll we'll come
[2:21:09] back and be deleting hidden faces
[2:21:11] anyway. So, for now, we can just leave
[2:21:13] that as a temporary fix. All right,
[2:21:15] let's come up here and let's cut out a
[2:21:18] window. So, arbitrarily shape the window
[2:21:21] how you want it. Then, let's uh well, we
[2:21:24] can't select that. So, let's look for
[2:21:26] our maybe collection, which is right
[2:21:28] here. And let's activate selection
[2:21:30] again. Now we can select it. So if you
[2:21:33] want, you can shift duplicate this and
[2:21:34] move it into modifiers. Uh we probably
[2:21:37] should have named it. Oh well, it
[2:21:38] doesn't really matter. So let's apply
[2:21:40] our solidify modifier once you get a
[2:21:42] size that you like. Cool. Now let's add
[2:21:45] a boolean modifier. So let's search for
[2:21:47] boolean
[2:21:49] and difference and select our cutout
[2:21:51] object. Cool. And now let's just come
[2:21:54] over here, visibility, and instead of
[2:21:56] textured, let's just do wire. And now
[2:21:59] let's just adjust our cutting out object
[2:22:01] to get a shape that we want, a shape
[2:22:03] that I like. And I'm actually going to
[2:22:05] leave it square here. But if you want,
[2:22:08] you can add you can go cut it out first
[2:22:11] and then go for a boolean. But I'm going
[2:22:14] to apply my bevel first and then apply
[2:22:16] my boolean. And now I'm just going to
[2:22:18] delete this. And everything looks good.
[2:22:20] So for the window, the first thing I'm
[2:22:22] going to do is probably shift Duplicate,
[2:22:24] right click, cancel, p separate by
[2:22:26] selection. And and then this piece right
[2:22:27] here, let's right click, set origin
[2:22:29] origin to geometry. It'll be kind of
[2:22:30] like the start of our thing. So let's
[2:22:33] apply our scale just to make sure that
[2:22:34] works. Let's add a loop cut down the
[2:22:37] center. And this first half will be our
[2:22:40] first one, our first window, and the
[2:22:42] second half will be the second. So let's
[2:22:43] also select this and P separate by
[2:22:45] selection. Uh disable selection for the
[2:22:47] house so we don't keep selecting. Let's
[2:22:48] select both them. Right click, set
[2:22:50] origin origin to geometry. So now we
[2:22:52] kind of have something like that. Let's
[2:22:53] just scale this down on the Y gy. Let's
[2:22:56] go into edit mode, A, and just extrude
[2:22:59] that kind of like so. Let's go into edit
[2:23:02] mode. Let's uh let's apply our scale
[2:23:05] just to make sure. And then let's just
[2:23:07] hit I to insert this. And then with both
[2:23:09] of them still selected, let's delete
[2:23:10] those faces. Now, let's do the same
[2:23:13] thing for this one back here, except
[2:23:15] this time it's going to be a little bit
[2:23:17] up here, like so. Let's go into edit
[2:23:20] mode. Hit a extrude everything. Cool.
[2:23:23] Just like that. Let's select these two
[2:23:25] faces. Hit I to insert.
[2:23:28] You can make it as thick as you want or
[2:23:30] just change it later. Delete faces. All
[2:23:33] right. Now, let's go in both of them.
[2:23:34] Let's shift alt and select this loop.
[2:23:36] Shift alt select that loop. Shift alt
[2:23:38] select this loop. Shift alt select this
[2:23:40] loop. That's just like that. Then we'll
[2:23:42] do Ctrl E bridge edge loops. And that'll
[2:23:44] kind of fill in the frame for us. Let's
[2:23:46] select this one and copy to selected.
[2:23:49] And uh let's make sure to apply our
[2:23:51] scale to make sure that's working.
[2:23:52] Actually, the amount looks a little bit
[2:23:54] too much. So, I'm just going to reduce
[2:23:55] that a little bit. Cool. Yeah. And I'm
[2:23:58] definitely going to inflate these a
[2:24:00] little bit. So, I'm just going to hit
[2:24:01] Alt S and make that a little bit
[2:24:04] thicker. Just like that. Reactivate
[2:24:05] selection on our cube. Let's select all
[2:24:08] three of these. Go into edit mode. go
[2:24:09] into wireframe and let's just select all
[2:24:11] these and probably S shift Y and just
[2:24:15] make it a little bit bigger.
[2:24:17] But again, that's kind of all up to you
[2:24:19] and what you want to do with your your
[2:24:22] window and things like that. Maybe
[2:24:24] center with piano. Cool. All right,
[2:24:26] let's use the draw cube tool just to for
[2:24:29] our I don't know what they call this at
[2:24:31] the top, our window blinds. So, I'm just
[2:24:33] going to add that there. And then let's
[2:24:35] go back. Let's go into local view. Then,
[2:24:37] let's just extrude upwards. Hold this.
[2:24:40] Alt D. Oh, let's deselect this back one.
[2:24:42] And then alt D. Extrude along normals. S
[2:24:44] to scale evenly. Kind of just like so.
[2:24:47] Then we kind of have a top there. Uh
[2:24:49] maybe the top can be a little bit taller
[2:24:51] than the other one. So I'm just going to
[2:24:52] select that. Bring Let's copy a bevel
[2:24:54] modifier over. Ctrl L. Copy modifiers.
[2:24:57] Apply our scale. Make sure that works.
[2:24:58] Seems like I don't have a bevel modifier
[2:25:00] in this one. So let's just copy this
[2:25:01] one.
[2:25:03] Okay. For the window blinds, I'm just
[2:25:05] going to select this face. Shift
[2:25:06] Duplicate. Right click P. separate by
[2:25:08] selection. Let's uh right click, set
[2:25:11] origin origin to geometry. Let's just
[2:25:12] scale this down arbitrarily. Uh
[2:25:15] definitely in the Y. Actually, I don't
[2:25:16] know if I wanted to do it in the X. So,
[2:25:18] let's make that back up. Let's go into
[2:25:20] edit mode. Let's just e extrude it
[2:25:22] downwards a little bit. Let's apply our
[2:25:24] rotation and location just in case. And
[2:25:27] let's add a array modifier like so.
[2:25:31] Let's come down here. Let's change this
[2:25:33] to zero. And I'm guessing it's going to
[2:25:34] be in the one. So, yeah, it will be. We
[2:25:37] don't need that much of a bevel cuz it's
[2:25:39] very not noticeable. So, let's reduce
[2:25:41] the amount of segments. One is fine
[2:25:43] enough. And let's just change this to
[2:25:44] like four or something. We can have uh
[2:25:47] one of those hanging things. So, I'm
[2:25:48] just going to put it here. I'm going to
[2:25:50] shift right click. And I'm going to have
[2:25:53] a Taurus. And I'm going to make this
[2:25:54] really like low poly. So, like 12. Well,
[2:25:58] I'm going to click and drag both of them
[2:25:59] and just set them at to 10 actually. So,
[2:26:02] cuz it's so small. and do right click
[2:26:04] shade auto smooth R Y90.
[2:26:07] Okay, let's shift D duplicate that.
[2:26:09] Bring that down. Let's do RZ90. Kind of
[2:26:12] like so. Let's go into edit mode on this
[2:26:14] one and just select the Well, let's make
[2:26:16] sure we're in R frame. Let's just delete
[2:26:18] those vertices there. And actually, now
[2:26:22] we just bring both of these up. And then
[2:26:23] let's just bring this down a little bit.
[2:26:25] GZ. Cool. So, we kind of have like a
[2:26:28] small little hook there from really
[2:26:30] matter anyway. What we can do now is
[2:26:32] just shift a add a cylinder.
[2:26:36] And we probably only need like 10 here
[2:26:38] as well. So I'm just going to scale that
[2:26:39] down. Not going to give this a bevel
[2:26:41] modifier or anything either. Let's go
[2:26:43] into edit mode. Let's just select that
[2:26:44] face right there. And let's just GZ
[2:26:47] bring it down kind of like so. The
[2:26:49] bottom. We can also have a small board.
[2:26:50] So I'm just going to shift duplicate
[2:26:52] this. Move this down here. Get rid of
[2:26:54] the array modifier. And just move it in
[2:26:58] alignment. Sx.
[2:27:00] object set origin origin geometry sx a
[2:27:03] little bit gx. Cool. It doesn't have to
[2:27:06] be anything fancy here.
[2:27:10] All right, let's create a microphone.
[2:27:11] I'm just going to shift A and probably
[2:27:13] add a cube. Add control 2 subdivision
[2:27:15] service modifier. Scale it up a little
[2:27:17] bit. Two guard loops per usual. S. Scale
[2:27:20] them up kind of in a microphone shape.
[2:27:22] That looks nice, smooth. Let's go into
[2:27:24] edit mode. Let's create a holder. So, I
[2:27:26] think I'm going to have a loop cut here.
[2:27:28] Now let's select this loop here. Let's
[2:27:30] do alt e extrude along normals kind of
[2:27:32] like so.
[2:27:34] That looks about right. Then let's
[2:27:36] select these edge loops here. Like so.
[2:27:39] Same thing we did for the basket. Uh
[2:27:42] let's come over here and let's just
[2:27:44] increase mean increase like so. Let's go
[2:27:46] back. Let's select this edge loop again.
[2:27:48] Let's hit Ctrl+ to increase our
[2:27:50] selection. Let's just P separate by
[2:27:52] selection. Kind of like that. So now
[2:27:54] it's kind of somewhat like this. All
[2:27:57] right. And then for the top, uh, maybe
[2:27:59] we can shift D, duplicate, right click,
[2:28:02] cancel, P, separate by selection. Then
[2:28:04] we can extrude this up a little bit. And
[2:28:06] let's add a guard loop down here. So it
[2:28:08] kind of flattens out on the top. Let's
[2:28:09] just use that to cover the top like so.
[2:28:12] Then let's go into edit mode. Maybe add
[2:28:14] two loop cuts here. SX, whoops, SY.
[2:28:17] Sorry. Let's select these two. Shift
[2:28:19] Duplicate. Right click, cancel piece
[2:28:21] separate by selection. Then let's go
[2:28:23] back into edit mode. Shift alt. Whoops.
[2:28:26] shift out the loops that we created and
[2:28:28] Ctrl X just to dissolve those. Now we
[2:28:30] have this thing right here. Let's just
[2:28:32] GX move it in place. Go into edit mode.
[2:28:34] AE extrude outwards. Just like that. GZ
[2:28:36] bring it down. And uh for this we can
[2:28:41] add probably a control loop here.
[2:28:43] Selected all those. And we can just GX
[2:28:45] and move that in there. That might be a
[2:28:47] little bit too in. So I'm going to add
[2:28:48] another loop cut here. And just bring
[2:28:49] this out like so. All right. And let's
[2:28:52] just add a mirror modifier to this. And
[2:28:55] uh let's select our object here. All
[2:28:56] right, let's select our microphone and
[2:28:59] just go into local view to create a
[2:29:00] stand for it. So, doesn't really matter,
[2:29:03] honestly. I think I'm just going to uh
[2:29:04] select this bottom here. Shift
[2:29:06] duplicate. Right click, cancel. P
[2:29:07] separate by selection. And I'm just
[2:29:10] going to bring it down somewhere
[2:29:11] arbitrarily. Let's uh e extrude it
[2:29:13] upwards. Two guard loops like so. We
[2:29:17] could probably use like a cylinder,
[2:29:18] honestly, but whatever. Uh, and then
[2:29:20] let's go into top view just to make sure
[2:29:22] it's it's about the same size as the
[2:29:24] microphone or maybe a little bit bigger.
[2:29:26] But again, that's kind of up to you.
[2:29:27] Let's move it GY. Use a plane rather
[2:29:29] than a subdivision thing just because it
[2:29:31] won't be noticeable. So again, I'm just
[2:29:33] going to add a plane here. Go into like
[2:29:36] so. Go over here. S Y. Go into edit
[2:29:39] mode. E extrude upwards. Maybe move it
[2:29:42] back a little bit. And then I'm just
[2:29:44] going to add a loop cut here like so.
[2:29:46] And just extrude this. And let's go into
[2:29:50] the side here and just move it kind of
[2:29:51] like that. Let's go into wireframe and
[2:29:53] adjust this. Um, if you want to add like
[2:29:57] a cylinder here, just so it kind of has
[2:29:59] a joint, working joint, you totally can.
[2:30:01] Uh, I feel like no one's going to pay
[2:30:03] attention to that, so I'm not even going
[2:30:05] to I'm not going to bother looking for
[2:30:07] it. I'm not going to bother adding it.
[2:30:09] But depending on your project, you might
[2:30:11] want to add that. Um, so this looks a
[2:30:14] little bit too tall for my liking. And
[2:30:15] then maybe we can copy a bevel modifier
[2:30:17] just to this one just to see. Let's
[2:30:19] apply our scale. Uh let's just reduce
[2:30:22] the amount a little bit. Cool. So
[2:30:25] that'll be it. Right click. Shade auto
[2:30:27] smooth. Cool. Uh so this kind of looks a
[2:30:30] little bit too wide. So I'm just going
[2:30:32] to select everything. Sift Z. Shift Z.
[2:30:35] And just scale it like that. If you want
[2:30:37] to give it more of like a holder style,
[2:30:39] you could totally add like two loop cuts
[2:30:41] here. and then delete uh probably these
[2:30:44] faces as well as these faces, X faces.
[2:30:47] Then you could just like fill in all the
[2:30:49] edges, but I'm not going to be doing
[2:30:50] that um because no one's going to be
[2:30:52] paying that close attention. All right,
[2:30:54] let's add like a egg carpet. So, I'm
[2:30:56] just going to shift A and add a plane
[2:30:59] like so. Uh this was inspired by Nikki
[2:31:01] Blender, which is a she's a really
[2:31:03] popular uh 3D artist. You should totally
[2:31:06] check her out. Um, but basically I'm
[2:31:10] just making a random shape uh that's u
[2:31:14] you know in like a egg splatter sort of
[2:31:15] format. Doesn't honestly it really does
[2:31:17] not matter what your shape is. Then just
[2:31:19] add control 2 subdivision surface
[2:31:22] modifier. Go into edit mode E extrude
[2:31:24] upwards. Right click shade smooth. So
[2:31:26] this is kind of like our carpet. Uh S
[2:31:28] shift C. Let's just make it a little bit
[2:31:30] bigger. Cool. Let's just uh select one
[2:31:32] of these. Shift Duplicate. Right click
[2:31:34] cancel. Puppy by selection. Let's go
[2:31:35] into edit mode. Let's make it a little
[2:31:38] bit like this. Sunnyside up egg. I think
[2:31:40] that's what they call it. And uh this
[2:31:43] will be like our carpet. And this might
[2:31:45] be like a pillar or something. All
[2:31:46] right. Let's uh add a lamp. So I'm just
[2:31:48] going to probably add a plane here. Give
[2:31:51] it a subdivision surface modifier. Let's
[2:31:53] e extrude it upwards in like a I don't
[2:31:56] know like a lamp shape. And let's just
[2:31:58] alt s extrude. Maybe add control loop
[2:32:01] here. Bring that in a little bit. Right
[2:32:03] click shade smooth. That kind of looks
[2:32:05] like an okay lamp. Um, maybe we can
[2:32:08] bring this down a little bit. Let's add
[2:32:09] a guard loop over here. Down on the
[2:32:11] bottom here. Maybe one more over here.
[2:32:14] Cool. And then let's just scale this
[2:32:16] down and bring that up. Cool. Then we
[2:32:19] can add like a control loop over here.
[2:32:21] Like so. Shift alt shift alt sift z.
[2:32:25] Bring it a little bit like that. Now for
[2:32:27] the top, we can just add a cylinder. So
[2:32:30] let's just add a cylinder. 12 should be
[2:32:32] okay. Let's scale it down. Go into edit
[2:32:34] mode. Let's select both of these and
[2:32:37] just delete those faces. Let's select
[2:32:39] this. Alt extrude along normals like so.
[2:32:42] Let's select this edge loop and then
[2:32:43] just scale it down like so. Let's go
[2:32:46] over here. Just scale it upwards kind of
[2:32:48] like so. Cool. And maybe maybe I want
[2:32:50] like a like a bulkier kind of lamp.
[2:32:53] Something like that. That looks kind of
[2:32:55] cute. Right click shade auto smooth.
[2:32:57] Yeah, I don't think it's worth adding a
[2:32:59] light bulb in there. And I don't think
[2:33:00] it's worth adding a bevel or subdivision
[2:33:02] to this either cuz it's so small. All
[2:33:04] right, let's add a shelf. Shift DG,
[2:33:06] shift Y. Let's move it somewhere here.
[2:33:09] Let's go into edit mode. Let's just
[2:33:10] bring that out on the Y-axis a little
[2:33:12] bit. Cool. Let's just shift Duplicate.
[2:33:15] Right click, cancel. And let's just uh
[2:33:18] make it a little bit smaller. Let's just
[2:33:20] bring it down like here. Let's do RX.
[2:33:23] Just scale it like so. Uh GX. Cool. That
[2:33:27] looks okay. Maybe scale it a little bit
[2:33:29] more. GZ GY. Let's get rid of the bevel
[2:33:32] modifier here. Let's go into edit mode.
[2:33:34] Select. Let's select this edge. GZ and
[2:33:36] just snap it to this vertex here. Also,
[2:33:39] let's make sure align rotation to target
[2:33:41] is off. GZ. Let's just snap it to that
[2:33:42] vertex here. Let's go into wireframe.
[2:33:46] And uh this one can gy GZ. And also snap
[2:33:50] it to this vertex here. So, we kind of
[2:33:52] something like this. Uh actually, we
[2:33:54] should probably just use face instead.
[2:33:56] Um and then this one. Let's go into
[2:33:57] wireframe. Let's select this. Gy, snap
[2:34:00] it to this face. Gy, snap to this face
[2:34:02] as well. Uh, and then let's add a mirror
[2:34:04] modifier. And let's just select this
[2:34:06] object here. Well, actually, it's
[2:34:08] definitely going to be noticeable. So,
[2:34:09] let's copy over a bevel modifier.
[2:34:13] And let's just apply our scale. And
[2:34:15] that's way too much. So, let's reduce
[2:34:17] that a little bit. Cool. And then we
[2:34:19] might have to adjust it. And let's just
[2:34:20] go into edit mode and make this a little
[2:34:22] bit bigger. I added some sticky notes,
[2:34:24] which are just planes that I rotated and
[2:34:26] extruded. And uh to move them around,
[2:34:28] shift D. And I just used face snapping
[2:34:31] to move them around. And then just RX or
[2:34:33] whatever axis to rotate them. All right,
[2:34:35] let's add a Bobo plushy up here. So I'm
[2:34:37] going to shift right click, add a plane,
[2:34:39] just like so. Scale it down. Go into
[2:34:42] edit mode. You know the deal. And to
[2:34:44] support loops already SZ. Just like
[2:34:46] that. Let's add Go into object mode.
[2:34:49] Let's add a subdivision service
[2:34:50] modifier. Let's right click shade
[2:34:52] smooth. That looks a little bit too
[2:34:53] much. Then let's add some more loop
[2:34:56] cuts. Let's go into side view. I want it
[2:34:57] a little bit bulky. So, let's go just
[2:34:59] like this. Let's turn on proportional
[2:35:01] editing. Let's scale that up. Make it a
[2:35:03] little bit bulky. Just like that. Cool.
[2:35:04] Let's jump there. Kind of looking like a
[2:35:06] boba already. Let's go into edit mode.
[2:35:09] Let's shift Duplicate this. Right click
[2:35:11] cancel. P separated by selection. Let's
[2:35:14] go into edit mode. E extrude that up.
[2:35:16] And this will kind of be like our cap.
[2:35:18] Let's S shift Z. Open it up a little
[2:35:19] bit. Right click. Set origin. Origin to
[2:35:21] geometry. Let's go uh let's select both
[2:35:24] of these. Let's hit insert. just to
[2:35:26] insert that a little bit. And then maybe
[2:35:28] alt extrude along normals and then just
[2:35:30] bring it in just like that. Kind of
[2:35:32] something like that. S shift z
[2:35:35] kind of like that. And let's just put it
[2:35:36] on the top right there. Cool. Just like
[2:35:39] that. And then maybe we want another
[2:35:41] support loop here just to make it a
[2:35:43] little bit more straight there. And uh
[2:35:45] let's expand this a little bit more. So
[2:35:47] what we can do is select both of them
[2:35:49] and go into edit mode and then still
[2:35:50] scale it up proportionally. So the top
[2:35:52] is also scaling. All right. So, let's uh
[2:35:55] turn our proportional editing. And I
[2:35:57] don't like how this one is going through
[2:35:59] this one. So, what we can do is just
[2:36:01] take this entire top face. Let's go out
[2:36:03] and just bring it down a little bit so
[2:36:05] it's covered there. All right. Now,
[2:36:06] let's just select this face right here.
[2:36:08] Shift Duplicate. Right click. Cancel.
[2:36:09] Piece everybody selection. Then, S,
[2:36:11] shift Z. Scale it down. G. Move it over
[2:36:14] here. Go into edit mode. E to extrude it
[2:36:16] all. If you need to go into wireframe,
[2:36:18] you totally can. I'm not. But cool.
[2:36:20] Let's tilt it a little bit. Cool. Let's
[2:36:21] just squash this down a little bit. Um,
[2:36:23] let's move this down. All right, let's
[2:36:26] go into local view. Uh, side view.
[2:36:29] Doesn't really matter. It's just going
[2:36:30] to be another plane. Let's do RX90.
[2:36:33] Scale it down. Let's do control 1.
[2:36:36] Control 2. Cool. Let's just go into edit
[2:36:39] mode. Extrude it out a little bit. Cool.
[2:36:41] RZ. Right click. Shade smooth. And um
[2:36:45] RZ. Cool. Add modifier. Mirror modifier.
[2:36:49] Maybe something like so. Just kind of
[2:36:52] like that. RZ GY.
[2:36:56] Maybe ext. Maybe bring that out a little
[2:36:58] bit more. And for the mouth, let's just
[2:37:00] duplicate this. Uh, get rid of the
[2:37:02] mirror modifier.
[2:37:04] Gy. Let's just snap it to the center
[2:37:06] because we have face select. All right.
[2:37:08] Let's just do SX. Let's go into edit
[2:37:11] mode. Let's add a loop cut here. Let's
[2:37:14] go into Let's just bring it down kind of
[2:37:17] like so. Maybe scale it down a little
[2:37:20] bit. And there we kind of have. All
[2:37:21] right, let's add some piano details. I'm
[2:37:22] going to add a loop cut. SX GX. Move it
[2:37:25] in. Let's h take this face insert a
[2:37:28] little bit. E extrude downwards. Let's
[2:37:30] just go into edit mode. Shift Duplicate.
[2:37:31] Right click. Cancel. Per by selection.
[2:37:33] Object. Set origin. Origin to geometry.
[2:37:36] Sx. Bring that down. Go into edit mode.
[2:37:38] E extrude that upwards. S. All right.
[2:37:42] Now I want to add like some clickable
[2:37:43] icons. So instead of modeling it, what
[2:37:46] the typical workflow is to find an SVG
[2:37:48] online and import that into Blender to
[2:37:50] use it. So SVG repo has a lot of really
[2:37:54] awesome ones that are I think public
[2:37:55] domain license. So find, you know,
[2:37:58] whatever logo you want. Hopefully it's
[2:38:00] here somewhere and just download it.
[2:38:03] Just make sure when you click on it, you
[2:38:04] check the license. This one's MIT, so
[2:38:07] this is fine. And if the logo you're
[2:38:08] looking for doesn't exist on SVG repo,
[2:38:10] you know, you can just type in your
[2:38:12] company logo SVG and try and find a
[2:38:14] resource there. Again, just make sure to
[2:38:16] check the license. So now what you can
[2:38:18] do is come uh here, file, import, and
[2:38:21] make sure to select SVG, not SVG as
[2:38:23] grease pencil, just regular SVG, and you
[2:38:25] can import it. So it imports as a curve.
[2:38:28] You can see right here. Now, it might be
[2:38:30] extremely small, so you can just scale
[2:38:32] it up and just bring it up there. Now,
[2:38:34] because it's a curve, we have all those
[2:38:36] things that we did when we were making
[2:38:38] other curves, right? So, in geometry, we
[2:38:40] have this extrude thing that we can
[2:38:42] extrude a little bit. And then we also
[2:38:44] have this bevel thing right here. So, if
[2:38:45] you want to add a little bit of bevel to
[2:38:47] the corners, you totally can do that.
[2:38:48] So, we can increase that bevel there.
[2:38:50] And you can see we it makes it a little
[2:38:52] bit more stylized. Just like that. So, I
[2:38:54] think that actually looks pretty good
[2:38:55] for the GitHub logo. So, once I'm done,
[2:38:57] I can convert to mesh. Right click, set
[2:39:01] origin origin to geometry. And now it
[2:39:02] just be its own object. All right, I'm
[2:39:04] going to do the same thing for the other
[2:39:05] ones. So again, we go to This time we're
[2:39:08] going to go to YouTube. Let's select
[2:39:10] YouTube. Let's scale it up. Let's
[2:39:12] extrude it a little bit. Let's add some
[2:39:14] bevel.
[2:39:17] Cool. That looks good. I don't think for
[2:39:18] curves you need to apply your scale.
[2:39:20] Yeah, it didn't change anything, but
[2:39:22] yeah. So, this also looks good. And of
[2:39:24] course, when you convert it to a mesh,
[2:39:26] well, I guess you don't have to convert
[2:39:28] it to a mesh yet until we start getting
[2:39:30] to
[2:39:32] like the baking stage, but I'm just
[2:39:35] going to do it anyway because I kind of
[2:39:36] confirmed that I want these like so. You
[2:39:38] also'll notice that some of these have
[2:39:40] the wrong shading applied. So, you can
[2:39:42] right click and shade auto smooth, and
[2:39:43] I'll fix that up right there. Okay. Now,
[2:39:45] for each of these, I'm just going to add
[2:39:47] some sort of background to hold them.
[2:39:49] So, cursor to selected and shift A and
[2:39:52] add a plane. uh RX90.
[2:39:55] Scale it down. Go into edit mode. I
[2:39:58] think we can just extrude it this time.
[2:40:00] Uh let's go into local view. Let's just
[2:40:02] select these edges. Shift G. Select
[2:40:04] similar length. Ctrl +B. And just give
[2:40:07] it a a small little bevel. Just like
[2:40:10] that. Right click, shade, auto smooth.
[2:40:12] Let's copy over one of these. Copy. Ctrl
[2:40:15] L. Copy modifiers. That's looking good.
[2:40:18] And we can just have that send just like
[2:40:20] there. And then we can angle it, of
[2:40:22] course.
[2:40:23] All right, let's add a circle. Um, 16
[2:40:27] should be okay. R Y 90. Cool. Let's go
[2:40:30] into edit mode. Let's just scale that
[2:40:31] down. Shift X like so. Let's go into
[2:40:34] edit mode. Let's just extrude that out
[2:40:37] on the X-axis.
[2:40:39] Let's fill that in. Let's insert that.
[2:40:42] And let's extrude that in just to get a
[2:40:44] clock like so. Right click, shade, auto
[2:40:46] smooth. Let's copy. Let's apply our
[2:40:49] scale. Let's copy over a bevel modifier.
[2:40:53] Like so. That seems to be too much. So,
[2:40:56] we can lower it.
[2:40:58] And it looks a little bit too. So, let's
[2:41:00] add a subdivision surface modifier of
[2:41:02] one. Uh, hands should just be a simple
[2:41:05] plane, I guess. I guess you can do it
[2:41:07] whatever you want to do it with. Let's
[2:41:09] go into edit mode. Let's just e extrude
[2:41:11] that out a little bit. I don't want it
[2:41:13] too thick. Let's go into wireframe just
[2:41:16] to see what that is. Okay. GX. Let's
[2:41:18] move it out. GX. And then snap it. Cool.
[2:41:19] Let's go into edit mode. Let's get make
[2:41:21] sure we select everything. GC GZ. This
[2:41:24] will be the hourhand. And then let's
[2:41:26] just duplicate that and move it along
[2:41:29] the X. SXX.
[2:41:32] Make it smaller into ourh hand. And then
[2:41:35] let's also just add a cylinder here. And
[2:41:37] we probably only need like 10. So I'm
[2:41:39] just going to scale that down. Probably
[2:41:41] even less than 10. Oh well. R Y90.
[2:41:45] Cool. Just like that. Okay. Let's add a
[2:41:48] small table. You already know the drill.
[2:41:49] We're going to add a plane. We're going
[2:41:50] to hit control 2 to give that
[2:41:52] subdivision. We're going to e extrude
[2:41:53] that out. We're going to give it two
[2:41:55] guard loops with controlr. Just like
[2:41:56] that. We're going to scale it up. Let's
[2:41:58] turn up proportional editing. We're just
[2:41:59] going to scale it up. Right. We're going
[2:42:01] to right click, shade smooth. Just like
[2:42:02] that. And for the legs, you already know
[2:42:04] the drill. We're just going to shift
[2:42:05] duplicate, right click, cancel. We're
[2:42:06] going to go into coffee. We're going to
[2:42:07] go scale this down just like so. Let's
[2:42:09] go into wireframe just to get an
[2:42:11] arbitrary size that we want. We're going
[2:42:13] to add a mirror modifier right here.
[2:42:14] We're going to select this object as our
[2:42:16] mirror object. And we're also going to
[2:42:18] do it on the Y-axis. Then we're going to
[2:42:20] go into edit mode. And what we're going
[2:42:21] to do is probably select this bottom
[2:42:24] face here. Hit control plus to select
[2:42:25] that control loop up there. GZ. And
[2:42:27] we're just going to snap it down to the
[2:42:29] bottom. Just like that. And then if we
[2:42:30] want, we can we can scale that up a
[2:42:32] little bit. And maybe maybe even make it
[2:42:34] a little bit more round by bringing that
[2:42:35] up. And then we got something really
[2:42:37] really cute and stylized in that. We can
[2:42:38] do RX and then R Y90. And then we have
[2:42:41] something really really cute like that.
[2:42:42] SZZ. Just bring it up just like that.
[2:42:44] And there we have our table desk thing.
[2:42:47] All right. For the pizza, you already
[2:42:48] know the deal. We're going to take this.
[2:42:49] We're going to shift duplicate. Right
[2:42:51] click. Cancel. P separate by selection.
[2:42:53] Let's go into edit mode. Let's add two.
[2:42:55] Well, since it's rotated, let's do alt R
[2:42:57] so it's back to the default rotation.
[2:43:00] Not that we have to. It's just easier to
[2:43:01] work with. Let's add two loop cuts here.
[2:43:03] Let's scale them down. Maybe sx. Let's
[2:43:06] add another one here. Let's go into edit
[2:43:08] mode. Let's just bring this forward just
[2:43:09] to make a pizza shape. Just like that.
[2:43:11] We definitely need one back here just to
[2:43:12] give it, you know, some pizza shape.
[2:43:14] Let's go into edit mode. Let's e extrude
[2:43:16] that down. There we got a nice cute
[2:43:18] pizza. Maybe we want to give some
[2:43:20] stylization here and scale that up a
[2:43:22] little bit. I don't know. Really up to
[2:43:23] you there. For the crust, I think I'm
[2:43:25] just going to go in edit mode, hold
[2:43:26] control, select all that. P separate by
[2:43:28] selection. Go into edit mode. Just like
[2:43:29] that. Let's go into edit mode. AE
[2:43:31] extrude outwards. Kind of like so. Let's
[2:43:34] reset. Set origin origin to geometry.
[2:43:36] Let's gy move it in there. Sz scale it
[2:43:39] up. Sx. And just adjust it like so. And
[2:43:43] you know, really up to you at this point
[2:43:44] here. Let's go in the pizza. And I don't
[2:43:46] like how it's so round. So, let's add a
[2:43:48] guard loop here and just make it flatter
[2:43:49] at the bottom. Uh, I don't know. I don't
[2:43:51] think I want one for the crust. Maybe I
[2:43:53] do. I don't know. Really up to you
[2:43:54] there. So, for the cheese, what we're
[2:43:56] going to do is go into edit mode. Just
[2:43:57] select all these top faces right here.
[2:43:58] Hit Ctrl+ to increase your selection.
[2:44:00] You can see it gets the top half of the
[2:44:02] pizza. What we're going to do, shift D,
[2:44:03] click right click cancel. If we separate
[2:44:04] by selection, and you can double click
[2:44:06] to select the overlapping thing. And
[2:44:08] then you can just scale it up just a
[2:44:10] little bit. So, like so. Then what you
[2:44:12] can do is rightclick and subdivide as
[2:44:14] necessary. And then once you subdivide,
[2:44:17] turn on proportional editing like so and
[2:44:18] just edit the cheese like so and make a
[2:44:21] cheese around there. Of course, if you
[2:44:22] always need more geometry, you can
[2:44:24] totally do that. And if you feel like
[2:44:25] places don't want cheese, you can
[2:44:27] actually select the face and delete
[2:44:28] those faces like so. And then you can
[2:44:30] just come around and keep on adjusting
[2:44:32] your cheese all around. Maybe this
[2:44:34] doesn't need a face here. And uh get
[2:44:37] some nice looking pizza cheese just like
[2:44:39] that. Of course, you can also get rid of
[2:44:41] edge loops that you don't want either
[2:44:42] with Ctrl X. So once you get some
[2:44:45] good-looking cheese, you can see I added
[2:44:46] a bunch of loop cuts and whatnot for my
[2:44:48] cheese. Of course, we can add a solidify
[2:44:50] modifier just like this. Let's bring it
[2:44:52] up here and let's change the thickness
[2:44:54] just to give it, you know, some depth to
[2:44:56] that cheese. Now it looks really, really
[2:44:57] cheesy. For the toppings like pepperoni,
[2:44:59] let's just use this P separate by
[2:45:01] selection. Let's go into edit mode. E
[2:45:03] extrude upwards. I insert a little bit
[2:45:05] extrude downwards. There we kind of
[2:45:07] already have a pepperoni that we can put
[2:45:08] along our pizza. Just like that. For an
[2:45:11] onion, we can actually just duplicate
[2:45:12] this and go into local view and delete
[2:45:15] the bottom and top faces. Now, it's a
[2:45:17] little bit messed up because we don't
[2:45:18] have this side, but we'll never see it
[2:45:20] because it's blocked by the cheese
[2:45:21] itself. And then you can just add like
[2:45:22] two loops cuts here to give it a little
[2:45:24] bit more rigidness. And now what you
[2:45:26] have here is an onion ring. Typically, I
[2:45:29] don't think I would take that approach
[2:45:30] with an onion ring unless it's to save
[2:45:32] time. I would probably use like a
[2:45:33] cylinder. Definitely not 32, but I would
[2:45:36] select both of these sides like here. I
[2:45:38] I would sorry I would insert them first
[2:45:40] then delete them then select both of
[2:45:42] these edge loops like so and then
[2:45:46] control E bridge edge loops and then
[2:45:48] this is definitely more of an onion ring
[2:45:50] rhyme and then I would add like a loop
[2:45:51] cut here. So one for the white part and
[2:45:53] then one for the purple part and then if
[2:45:55] you wanted inner purple part you could
[2:45:56] totally add another loop cut there just
[2:45:58] for the inner purple part as well. Uh
[2:46:00] but just to save time if you wanted to
[2:46:02] go the other route that I just showed
[2:46:03] you you totally could. There will be
[2:46:05] differences in topology, but you know,
[2:46:07] it kind of really just depends on on
[2:46:09] your scene and your vibe. So, I
[2:46:10] definitely want some leaves on my pizza.
[2:46:12] So, again, that's going to be the same
[2:46:13] thing. I'm going to shift duplicate,
[2:46:14] right click, anzo piece, rever, alt, r,
[2:46:17] reset our rotation, just like so. Let's
[2:46:18] go into edit mode. Let's add, I don't
[2:46:20] know, maybe two loop cuts. Let's sx
[2:46:23] scale that down. Let's add another one
[2:46:24] here. And let's just bring that down
[2:46:27] just like so. And uh let's uh go into
[2:46:30] edit mode. Probably bring gy bring this
[2:46:33] up. Maybe this one specifically. And
[2:46:35] then use some proportional editing.
[2:46:37] Cool.
[2:46:38] And then add loop cuts just to make the
[2:46:41] shape of your leaf for your pizza.
[2:46:44] Really up to you what you want there for
[2:46:46] your leaf. And then of course you want
[2:46:47] to add a solidify modifier. Again, we
[2:46:49] want to solidify before subdivided. And
[2:46:52] there we can have like a leaf for our
[2:46:54] pizza. Cool. You can see I have my pizza
[2:46:55] here and my leaves here. And I'm just
[2:46:57] adjusting uh the the the roundness a
[2:47:00] little bit just manually. Um, not too
[2:47:03] big a deal. I'm trying to reduce the
[2:47:04] amount of olu lap as much as possible,
[2:47:07] but we'll come back and uh deal with all
[2:47:09] that later. So, now we kind of have a
[2:47:10] really, really cute piece of pizza. For
[2:47:12] the soda can, you already know what
[2:47:14] we're going to do. We're going to take
[2:47:16] this shifty duplicate, right click,
[2:47:17] cancel P, separate by selection, alt R,
[2:47:19] reset that rotation, go into edit mode.
[2:47:21] Let's e extrude that up. Let's go into
[2:47:23] local view just so we get rid of
[2:47:24] everything. Let's add controlr, two loop
[2:47:26] cuts, SZ just to scale it up. Just like
[2:47:28] that. Let's change the whole can just
[2:47:30] like that. Let's maybe add three more
[2:47:32] loop cuts in the center here just to
[2:47:34] give it some bulkiness. So let's go into
[2:47:35] wireframe. Let's make sure we select
[2:47:37] that. Let's turn on proportional editing
[2:47:38] with O. Let's hit S just to scale it.
[2:47:40] And let's just bulk it up kind of like
[2:47:42] that. Make it a little bit cute. Just
[2:47:43] like that. Then for this top here, let's
[2:47:46] I to insert that a little bit. And let's
[2:47:48] just E and extrude that down. And this
[2:47:50] is way too smooth. So what we can do is
[2:47:52] actually insert again. And then we get a
[2:47:54] control loop right there for the ring
[2:47:56] around that. Super cool. And then for
[2:47:58] that pin thing, what we can do is shift
[2:48:00] D, duplicate, right click, cancel P,
[2:48:01] separate by selection. Then right click,
[2:48:03] set origin, origin to geometry. Scale
[2:48:05] that down, make it SX. Probably add a
[2:48:08] loop cut here. Let's select both of
[2:48:10] these faces. Let's hit I to insert. And
[2:48:13] then I hit I again for individual faces.
[2:48:15] And just hit X and delete those faces.
[2:48:18] Let's go into edit mode. Eextrude that
[2:48:20] up just like so. That looks pretty good.
[2:48:22] And then for the little pin in there,
[2:48:24] what we can do again is shift duplicate
[2:48:25] right click cancel piece upward by
[2:48:27] selection click set origin origin to
[2:48:29] geometry. Scale this down. Go into edit
[2:48:31] mode. Hit AE extruded upwards. Shift S
[2:48:34] selection to cursor. Scale that down and
[2:48:37] just put it like that. There we kind of
[2:48:38] have our our soda can. And then we can
[2:48:41] give some adjustments here. So maybe we
[2:48:43] want it a little bit inside on the
[2:48:47] Whoops. Let's turn off proportional
[2:48:49] editing. And maybe we want a little bit
[2:48:50] of the inside over here. And then
[2:48:53] another one on the top here. This gives
[2:48:55] it some a little bit more of a Coke
[2:48:57] bottle shape. So we can have another one
[2:48:59] possibly.
[2:49:01] It's giving more of a can vibe this way.
[2:49:04] Same thing down here. For this, we can
[2:49:06] probably inset and e extrude down a
[2:49:08] little bit. And then if you want to add
[2:49:09] more detail, you can totally add more
[2:49:11] detail. Um, but I think just one
[2:49:14] extrusion down. This was good enough for
[2:49:16] a stylized can. And I'm actually going
[2:49:18] to get rid of the bottom extrude because
[2:49:19] it's going to be covered up from the
[2:49:21] top. If you want to rotate it, can you
[2:49:22] can leave it for more realism, but I
[2:49:24] think what I'm just going to do is add
[2:49:26] like a guard loop over here. And
[2:49:28] honestly, just scale this down kind of
[2:49:30] like so. Um, so it has some resemblance
[2:49:33] of a bottom there. Okay, let's just add
[2:49:36] something here to fill up the empty
[2:49:38] space. I'm going to shift duplicate RZ
[2:49:40] 90. Let's see if that's the right way.
[2:49:43] Cool. It is. Let's just move it over
[2:49:45] here. Cool. Bring it up. S Y. So, this
[2:49:50] time I also want a hanging plant, but
[2:49:52] we're going to do it a little bit
[2:49:53] differently this time because I want a
[2:49:54] lot of them. So, I'm actually going to
[2:49:57] use this thing that we created really,
[2:49:59] really early. Uh, this sort of bold sort
[2:50:01] of looking thing. I just realized it's
[2:50:03] really inside there. And I think for
[2:50:06] this one, I'm going to reuse this. So,
[2:50:07] I'm going to shift duplicate, shift S,
[2:50:09] selection to cursor up there, like so.
[2:50:12] And then for this one, I think what I'm
[2:50:14] going to do is add a loop cut here and
[2:50:15] just bring it in like that. So then it
[2:50:17] becomes more of like a vase. So this
[2:50:19] will be more like a hanging plant pot.
[2:50:23] Whereas let's do S, shift C, and just
[2:50:25] bring it out a little bit. This will be
[2:50:27] like a plant, you know, like a bowl to
[2:50:29] hold a plant. So this is more like a
[2:50:32] vase of flowers. And then here is going
[2:50:33] to be like a bowl of hanging plant. Uh
[2:50:37] let's just add a bezier curve. Well,
[2:50:39] this is also a bezier curve. So, I'm
[2:50:40] just going to shift duplicate this
[2:50:41] bezier curve that we created earlier.
[2:50:43] Shift S, selection to cursor, keep
[2:50:45] offset. I'm definitely going to make the
[2:50:47] stem a little bit thinner. So, I'm going
[2:50:48] to come over here and in round I'm just
[2:50:51] going to turn down the resolution a
[2:50:53] little bit. Cool. Maybe something like
[2:50:55] that. And I'm just going to reshape it
[2:50:57] into like a hanging plant sort of vibe.
[2:50:59] So, um you know what I'm going to do is
[2:51:02] put it around here. Move this down like
[2:51:05] so. Probably rotate this for sure.
[2:51:10] Move that down.
[2:51:13] Move this down. Definitely rotate. Give
[2:51:15] that a rotation
[2:51:17] like so. Probably definitely extrude
[2:51:19] that. So, the next thing we have to do
[2:51:21] is make another leaf. So, if you want to
[2:51:23] copy one of our old leaves, like this
[2:51:25] pizza thing. This is making me so
[2:51:27] hungry. Oh my gosh. Uh, but if you want
[2:51:30] to, you could totally do that. But what
[2:51:32] I'm going to do is probably just, you
[2:51:33] know, shift A, add another plane, and
[2:51:36] make a completely new leaf. So, I'm just
[2:51:38] going to bring that up. And the only
[2:51:41] reason I'm making a new leaf is just for
[2:51:43] variety, but like you definitely don't
[2:51:44] have to. Like, I don't know if a lot of
[2:51:47] people can tell that it's a new leaf or
[2:51:50] not, especially when you're like
[2:51:51] scattering it. So, you know, it's really
[2:51:53] up to you. But, you know, I'm just going
[2:51:54] to create a really really basic new leaf
[2:51:57] like so arbitrary shape. If you want to,
[2:52:00] you can import like a reference and
[2:52:02] whatnot and like,
[2:52:04] you know, create something cool like
[2:52:06] that. So again, probably control 1.
[2:52:08] Yeah, control one is more than enough
[2:52:10] for this sort of leaf. Let's just go
[2:52:12] into edit mode and let's just add a
[2:52:14] center here. Door control B just to
[2:52:16] bevel it. Move our mouse up once just to
[2:52:19] get the center one. And then let's just
[2:52:20] hold control to pick the shortest path.
[2:52:23] And like our other leaves, let's just GZ
[2:52:25] and move it down a little bit. Kind of
[2:52:27] like so. And let's add a solidify
[2:52:29] modifier. Again, we want to solidify it
[2:52:31] before the subdivision. So we can
[2:52:33] increase that a little bit. And I think
[2:52:35] this time instead of extruding it from
[2:52:37] the leaf itself, what we can do instead
[2:52:39] is add a cylinder.
[2:52:44] And 32 is way too many. I think I'll go
[2:52:46] with 12 cuz it's going to be really
[2:52:48] really small. So I'm just going to 12
[2:52:50] might be overkill, but whatever. Or X90.
[2:52:53] And then shade auto smooth. Move it
[2:52:55] somewhere over here.
[2:52:57] Let's go into edit mode. Select this
[2:52:59] face and just extend out a little bit.
[2:53:01] Kind of like so. can do is add a few
[2:53:04] loop cuts on here like so. And then with
[2:53:07] proportional editing and selecting this
[2:53:10] like so, we can give it a slight tape
[2:53:12] taper. So, we can just scale it down a
[2:53:15] little bit. Again, if you want to use
[2:53:16] the taper modifier thing, the simple
[2:53:18] deform thing that we used earlier, you
[2:53:20] totally could. I'm just doing it
[2:53:21] manually because it's faster and you
[2:53:23] have more control
[2:53:26] for what we're doing here. So, I kind of
[2:53:28] want to keep it somewhat equal to the
[2:53:30] scale of the leaf. Cool. And when you're
[2:53:32] happy with that, what you can do is F3,
[2:53:34] convert to mesh. If you wanted to save a
[2:53:37] copy of it, you totally could, but I
[2:53:39] think I'm good with that. So now I'm
[2:53:41] just going to hit Ctrl + J and join them
[2:53:42] together so it's one single object.
[2:53:44] Cool. Let's apply our scale and
[2:53:45] everything. Make sure everything's okay.
[2:53:47] I feel like this has to be a bit a
[2:53:49] little bit bigger. So I'm going to do
[2:53:50] Ctrl L and just Whoops. Let's turn off
[2:53:53] proportion SY and just scale it up just
[2:53:56] a little bit. Kind of like so. Now what
[2:53:58] we can do is go into edit mode and
[2:53:59] probably turn on proportional editing.
[2:54:01] give some sort of distortions to this.
[2:54:04] Now we need to reset this origin point
[2:54:06] to over here. So what we can do is just
[2:54:08] hit control period G Y in this case and
[2:54:11] just snap it to this face right here and
[2:54:14] control period to confirm that.
[2:54:16] Alternatively, you could just select
[2:54:17] this shift S cursor to selected. It will
[2:54:20] snap to that selected face. And then you
[2:54:22] could do object set origin origin to 3D
[2:54:24] cursor. Nothing changed because we
[2:54:26] already set it there anyway. This is
[2:54:28] necessary because we're going to be
[2:54:30] using a particle system and that origin
[2:54:32] point is going to be based on that
[2:54:33] particle system. Now, what we can do
[2:54:35] once you have a curve that you like. So,
[2:54:36] I'm just going to duplicate this because
[2:54:38] we're going to be using it several times
[2:54:39] for multiple hanging plants. Once you
[2:54:42] have a curve that you like, you can F3
[2:54:44] and convert it to a mesh. Then, you can
[2:54:46] do the same thing we did last time. So,
[2:54:47] we can come over here. Oh, well, we
[2:54:49] could have filled caps first. Oh, well,
[2:54:50] we can just hit F to fill that now. and
[2:54:53] then select it and then you know just
[2:54:55] kind of taper it off with whatever you
[2:54:57] want to go for. Okay, now we can select
[2:55:00] this mesh right and add a particle
[2:55:02] system right here and just hit plus. Now
[2:55:06] you can see it looks like a bunch of
[2:55:07] blobs. So let's change it to hair
[2:55:09] instead. Now we don't want that many
[2:55:11] because there's so many. So what we can
[2:55:13] do is set it to like 100 and see what
[2:55:15] that gives us. Now, instead of like hair
[2:55:17] particles like you see here, we want to
[2:55:19] use the object that we created, this
[2:55:20] leaf right here. Under render, instead
[2:55:23] of as path, we're going to render as
[2:55:25] object. And then the instance object,
[2:55:27] the object that we're going to instance
[2:55:28] across this curve is going to be our
[2:55:30] leaf. So, we can just eyeball this leaf
[2:55:32] right here. And you can see our leaf is
[2:55:34] right there. Now, in render, you can
[2:55:36] adjust the scale of it as well as the
[2:55:38] scale randomness. You can see some
[2:55:40] leaves are going to be random whereas
[2:55:42] others are not. Cool. Now, it doesn't
[2:55:44] look particularly realistic because
[2:55:47] everything is kind of like on one side.
[2:55:49] Maybe you like that, but I don't. So,
[2:55:50] what I'm going to do is tick advanced.
[2:55:52] And you can see when I hit advanced,
[2:55:54] there's going to be this new thing here
[2:55:56] called rotation. So, we can click on
[2:55:58] rotation. You can see we can change it
[2:56:01] through like normal and then change the
[2:56:02] phase. Uh you can try velocity here,
[2:56:05] which is the default, which might work
[2:56:07] for you. Yeah, just play around with
[2:56:08] something that you like. I mean, go
[2:56:09] through these. I don't really know
[2:56:11] honestly. I would honestly just trial
[2:56:13] and error at this point. And of course,
[2:56:15] you can like adjust the number of leaves
[2:56:17] that you want and the overall size of
[2:56:20] it. And then you also you can still
[2:56:22] change the number and the length and
[2:56:25] then also the seed, you know, like
[2:56:26] Minecraft seeds and whatnot. So if you
[2:56:29] want to, you can just reuse this similar
[2:56:31] thing and do it again. But particle
[2:56:33] systems act like materials. So if you
[2:56:36] adjust this one, it's going to adjust
[2:56:37] the other one as well. So what you want
[2:56:39] to do instead is hit this copy thing
[2:56:40] here. So you can give a name to it if
[2:56:42] you want or you just hit copy and it'll
[2:56:44] automatically add 01. And now you can
[2:56:46] see when I edit this one, it's not going
[2:56:48] to edit this one. It's only editing this
[2:56:50] one here. So they kind of act the same
[2:56:52] as materials. Now if you do want to
[2:56:54] adjust the curve, well, you still have
[2:56:56] that option, too, right? It doesn't have
[2:56:57] to be a curve to edit it. You can edit
[2:57:00] it in its mesh form as well. So yeah,
[2:57:04] that way you don't have to create a
[2:57:06] bunch of curves. But again, we still
[2:57:07] have our other curve here that you can
[2:57:10] adjust as a bezier and do all the
[2:57:12] transformations that we did earlier if
[2:57:13] you wanted to go that route. And for my
[2:57:16] emitter object, you can see if I adjust
[2:57:18] it here, it's going to affect my other
[2:57:21] particle system. So, if you're kind of
[2:57:24] happy with what it is, what you can do
[2:57:26] is just hide it. That way, uh, you don't
[2:57:29] have to accidentally think about it and
[2:57:31] stuff like that. And then what I think
[2:57:32] I'm going to do is just have one extra
[2:57:35] curve here. just delete it and just put
[2:57:37] like a small little patch inside here.
[2:57:39] Kind of like so. Let's just delete those
[2:57:42] extra vertices that we don't need. Um
[2:57:45] like so just the bottom of here. We can
[2:57:47] definitely uh duplicate this one and
[2:57:50] tone down the number. So it might be a
[2:57:52] little bit messed up close up, but from
[2:57:54] far away, you know, no one's going to be
[2:57:55] able to tell. It kind of just looks like
[2:57:57] a pot that's filled with a bunch of
[2:58:00] leaves, right? Actually, now that I
[2:58:02] think about it, I don't think uh this
[2:58:04] actually gives the vibe I'm going for.
[2:58:06] Like, even if I make it really big and
[2:58:09] stylized. Um, so I could probably spend
[2:58:11] some time changing the leaf, but I don't
[2:58:13] think it overall matches the scene
[2:58:15] anyway. So, I'm actually just going to
[2:58:16] get rid of that. I think maybe what I
[2:58:18] put in here is like a bowl of eggs. So,
[2:58:19] I'm just going to like shift Duplicate P
[2:58:22] separate by selection, double click to
[2:58:24] select that, and probably just extrude
[2:58:26] this up. Um, set origin origin to
[2:58:30] geometry. I don't know, like a bird's
[2:58:32] nest sort of thing. Like I don't know.
[2:58:34] Yeah, you know, use your imagination. I
[2:58:36] don't actually know because I haven't
[2:58:38] planned this in advance. Um, but you
[2:58:40] know, I'm just going to I'm just going
[2:58:41] to make like a bowl of eggs or
[2:58:43] something. So, that's a little bit funny
[2:58:45] and a little bit cute at the same time.
[2:58:47] So, there's a bit of empty space here.
[2:58:48] So, I want to add a wall outlet. So,
[2:58:50] what I'm going to do is shift A and
[2:58:52] probably search for a plane. Let's just
[2:58:54] do R Y90 like so. Let's scale it down
[2:58:57] into like an arbitrary wall outlet
[2:58:59] shape. It doesn't really have to be
[2:59:01] exact. That looks okay. Then what we can
[2:59:03] do is probably extrude it out just a
[2:59:05] little bit
[2:59:07] and maybe scale that down a little bit.
[2:59:09] Then what we can do is hit A, select
[2:59:11] everything, subdivide it, subdivide it,
[2:59:13] subdivide it. And this looks okay. Then
[2:59:15] we can select like these three and
[2:59:17] probably just extrude it in. And then
[2:59:20] for the this one, I think we can just
[2:59:22] hit I to insert and then maybe S to make
[2:59:24] it a little bit smaller. and then GZ and
[2:59:27] then just insert that as well. Cool.
[2:59:29] Then let's copy over a bevel modifier.
[2:59:31] So I'm just going to copy over from
[2:59:33] here. Cropy modifiers. Cool. So that's
[2:59:36] one of our outlets. And let's just add
[2:59:38] an array modifier like so. That looks
[2:59:40] okay. We can increase the X just a
[2:59:43] little bit like so. And I want it ver
[2:59:46] horizontally. So I'm going to do it like
[2:59:47] that.
[2:59:49] And if you want to give it a back, you
[2:59:50] totally can. So if you want to do that,
[2:59:53] we can just go into edit mode. We can
[2:59:54] just select any one of these faces.
[2:59:56] Shift Duplicate, right click, cancel P,
[2:59:57] separate by selection.
[3:00:00] And let's get rid of the ray modifier.
[3:00:03] Let's get rid of the bevel modifier
[3:00:04] object. Set origin origin to geometry.
[3:00:06] And just scale it up. GZ.
[3:00:10] Go out S Y Gy Sz.
[3:00:16] Cool. And then I guess we can extrude
[3:00:18] this out a little bit.
[3:00:21] And let's go into wireframe and just
[3:00:22] select that and just move uh this out.
[3:00:26] Cool. Just like that. And then we have
[3:00:28] our wall outlet.
[3:00:31] And since it's so small, I'm actually
[3:00:32] going to get rid of the bevel on this
[3:00:34] one. Okay. Now, I want to add some text.
[3:00:36] So, the really nice thing is that
[3:00:37] there's this text object right here. And
[3:00:40] if you rotate it and go into edit mode,
[3:00:43] you can just start typing. And you have
[3:00:44] all the features that you would have.
[3:00:47] Well, not all, but a lot of the features
[3:00:48] that you would have of a regular text
[3:00:50] box like on PowerPoint or Word and so on
[3:00:52] so forth. Like I can hit A. I can hold
[3:00:55] shift to type. I can hit enter for a new
[3:00:57] line. So on so forth. I can do Ctrl +B
[3:00:59] to bold or control I for italic italic.
[3:01:02] Nothing's changing here because in the
[3:01:04] font itself, the default font uses the
[3:01:07] same font for the regular, the bold,
[3:01:09] italic, and so on so forth. So what you
[3:01:10] can do is go online like Google Fonts or
[3:01:13] Font Space and find a font that you
[3:01:15] like. Not every font will work properly,
[3:01:18] but you know, just play around until you
[3:01:20] find something that you like and that
[3:01:22] works. Then you just download it. You
[3:01:24] don't have to install it on your
[3:01:25] computer. You can just download it on
[3:01:26] your computer. And then when you have it
[3:01:28] downloaded, you can navigate to there to
[3:01:31] your fonts wherever you downloaded it.
[3:01:33] It doesn't have to be in the fonts
[3:01:34] folder. If you put in downloads, that's
[3:01:36] fine as well. So here, I can just try
[3:01:38] some random one. And you can see I tried
[3:01:40] this one. And you can see I tried that
[3:01:41] one and it updated there. Now, this
[3:01:43] isn't updated because technically it's
[3:01:45] bolded. So, I'd have to update the bold
[3:01:47] version of the font as well. You can see
[3:01:48] if I retype it though, it's going to be
[3:01:50] okay. And then you have a a lot of
[3:01:52] really, really cool options here. So,
[3:01:53] let me choose a different font, maybe
[3:01:54] like a black. If I come over here and do
[3:01:57] none, you can see it's only going to
[3:01:59] keep the outline. And then if I do
[3:02:00] extrude, you can see it's going to
[3:02:03] extrude that. And then you kind of get
[3:02:04] like this, I don't know, like
[3:02:06] surrounding text sort of vibe, which is
[3:02:08] really cool. And then you also have this
[3:02:10] thing like bevel, right? So, you can
[3:02:11] bevel it up. Um, so you can combine
[3:02:14] these and and see what you get and see
[3:02:17] what you like. When you're going for
[3:02:18] like static image renders, you know,
[3:02:21] leaving it as a text object is
[3:02:22] completely fine. We need to convert it
[3:02:24] to a mesh. So, let me just show you. If
[3:02:26] I F3, convert this to a mesh and go into
[3:02:28] edit mode. You can see now it becomes a
[3:02:30] mesh itself, and you can't edit the text
[3:02:32] anymore. With typing, it's just like an
[3:02:34] actual object now that you move around
[3:02:36] and adjust. Now, when it comes to text,
[3:02:38] it there usually is a lot of issues with
[3:02:40] the topology. As you can tell, this is a
[3:02:42] really really bad mess. Some fonts are
[3:02:44] better than others, but this one is this
[3:02:47] one is okay for like the I's and and the
[3:02:49] K's and so so on so forth, but for
[3:02:51] these, you know, it's definitely a
[3:02:53] little bit suspicious. One thing I know
[3:02:55] is that there's usually a lot of
[3:02:57] overlapping vertices. So, hit A to
[3:02:59] select everything, hit M to merge
[3:03:01] vertices by distance, and set it to like
[3:03:03] 0001. You can see I removed 7,839
[3:03:07] vertices and nothing visually changed at
[3:03:10] all. So, it just got rid of all those
[3:03:11] overlapping vertices, which saved some
[3:03:13] information. Depending on your font, you
[3:03:15] can get away with the rematch modifier
[3:03:17] and turning down the voxil size until
[3:03:20] you get something you like. The issue
[3:03:22] with using this rematch modifier is,
[3:03:24] take a look at my scene statistics. This
[3:03:27] is 76,000 vertices. This right alone,
[3:03:30] let me get rid of it. You can see it's
[3:03:31] 45,000.
[3:03:33] So, if I read it, by the time I get to
[3:03:36] something really small that looks good,
[3:03:39] it's going to start lagging my computer.
[3:03:40] And you can see now it's 682,000
[3:03:42] vertices. And it still looks a little
[3:03:45] bit suspicious close up. You also have
[3:03:48] this option here like blocks, which you
[3:03:50] can increase the octry depth and
[3:03:52] hopefully get something. But you should
[3:03:54] be careful with this because if you go
[3:03:55] too high, it's going to crash your file
[3:03:57] and maybe even crash your computer. The
[3:03:59] downside of Blender is that there's very
[3:04:00] few safeguards when it comes to
[3:04:02] parameters. So, just be careful with
[3:04:04] that. For a lot of fonts, remsh doesn't
[3:04:06] work. And for this font, it seems like
[3:04:08] remsh isn't working either. You can see
[3:04:10] when I duplicate this and apply the
[3:04:12] modifier what it actually does. So, if I
[3:04:15] go into edit mode, you can see if I get
[3:04:17] really really close, everything is like
[3:04:20] starting into becoming into quads. So,
[3:04:23] the topology is definitely better, but
[3:04:24] there's way too many quads here. What
[3:04:26] you could do is go into edit mode, a
[3:04:29] select everything, and unsubdivide.
[3:04:32] Again, if your computer can't handle it,
[3:04:34] don't even bother. Uh, you also have
[3:04:36] like this decimate modifier here that
[3:04:37] you can play with. Unsubdivide or
[3:04:40] collapse and just bring this down and
[3:04:41] it'll kind of merge some of the
[3:04:43] geometries. Again, be careful with these
[3:04:45] methods because it might crash your
[3:04:46] computer. If it's like this, you know,
[3:04:48] it's fine just to leave it unless it's
[3:04:50] causing shading issues during baking. If
[3:04:52] you don't know what that is, that's
[3:04:53] totally okay. If there's no shading
[3:04:55] issues, if it looks fine, then it's okay
[3:04:57] just to leave text as is. If you need to
[3:04:59] fix it up, then yeah, you would spend
[3:05:00] some time tracing the font and remaking
[3:05:03] yourself or just get a better font that
[3:05:06] works out of the box. There's very few
[3:05:08] fonts I know that work out of the box,
[3:05:10] but some fonts will work better with the
[3:05:12] rematch modifier than others. Okay,
[3:05:14] let's make some lights that hang from
[3:05:15] here and here. So, the first thing we
[3:05:17] need is a light bulb. So, I'm just going
[3:05:19] to shift a at a plane. Again, we want
[3:05:22] the subdivision surface. You already
[3:05:23] know where we're going to go. We're
[3:05:24] going to e extrude upwards like that.
[3:05:26] We're going to add two loop cuts just
[3:05:27] like this. This will be kind of the
[3:05:29] base. And maybe one more support loop up
[3:05:31] here. So, it's kind of like that. Right
[3:05:32] click, shade smooth. Cool. Now, we can
[3:05:34] just select this top, extrude it
[3:05:36] outwards. Probably expand that a little
[3:05:37] bit. Maybe make it a little bit longer.
[3:05:39] And then just one more bracing loop
[3:05:41] right here. And maybe we scale that
[3:05:43] down. Cool. Uh let's just scale this up
[3:05:46] just a little bit more just to give it a
[3:05:48] more light bulb sort of a shape. Cool.
[3:05:51] And there's kind of like our light bulb.
[3:05:53] Maybe we can select this bottom face.
[3:05:54] Plus, plus
[3:05:57] uh maybetrl+ one more time. Hit alt s
[3:06:00] and just scale that down a little bit.
[3:06:02] Cool. Uh and then I think we just P
[3:06:04] separate by selection here. That way
[3:06:05] it's kind of separate from the bulb
[3:06:07] itself. And let's just select both of
[3:06:08] these. Right click, set origin origin to
[3:06:10] geometry. And uh let's just scale this
[3:06:12] one up. Oops. All right. There I have my
[3:06:14] light bulb. So let's just check if one
[3:06:17] is enough. So one is definitely not
[3:06:20] enough. So, I'm going to keep it at two.
[3:06:21] I'm just going to convert these to a
[3:06:23] mesh now. And then I'm going to join
[3:06:25] them together just like so. Now, what we
[3:06:27] can do is use an So, let's just do RX90.
[3:06:30] Whoops. Let's just hit minus so it goes
[3:06:31] this way. And let's just shift S cursor
[3:06:34] to selected. Let's shift A and add a
[3:06:36] path curve. Cool. Let's add an array
[3:06:38] modifier for this one. Let's just
[3:06:40] increase the X a little bit. And I don't
[3:06:43] know, maybe like six. Then, let's add a
[3:06:45] curve modifier like so. And just select
[3:06:48] the path that we created.
[3:06:50] So now once we edit this curve, it
[3:06:52] should be around it should be adjusting
[3:06:56] uh our thing. So if we make it really
[3:06:57] long, we can increase the array modifier
[3:07:00] here. And you can see that we're going
[3:07:01] to get some more light bulbs just like
[3:07:02] that. You could also use the particle
[3:07:05] system method that we used earlier,
[3:07:07] which is totally valid as well. Uh but
[3:07:10] I'm just going to be using this method.
[3:07:11] So now all I have to do is just move
[3:07:13] this into the hanging position. So,
[3:07:17] uh, I want to one going over there and
[3:07:19] one over going over there. So, that's
[3:07:21] all I'm going to be doing. Of course,
[3:07:22] for the curve itself, we definitely want
[3:07:24] to give it some depth.
[3:07:27] So, I'm just going to increase that. So,
[3:07:29] shift right click, shift S, selection to
[3:07:32] cursor.
[3:07:34] Then, let's select this one. Shift right
[3:07:37] click here. Shift S, selection to
[3:07:39] cursor.
[3:07:41] And then, we can just adjust these like
[3:07:43] so.
[3:07:45] Uh we can also resize these just a
[3:07:47] little bit if they're too big. Cool. And
[3:07:50] then we can also adjust, you know, how
[3:07:52] much how the factor here as well. Now we
[3:07:54] just duplicate this. Shift Duplicate.
[3:07:56] And same thing what we can do. Same
[3:07:59] thing. Let's just uh go into edit mode.
[3:08:01] Select this probably over here. Shift
[3:08:03] STction to cursor over here as well.
[3:08:07] Probably somewhere over here. Shift S,
[3:08:09] selection to cursor. And we can just
[3:08:11] adjust the curve accordingly. And here
[3:08:13] we probably only need four rather than
[3:08:15] five.
[3:08:17] And we can set a little bit stronger of
[3:08:19] an offset. And then we can remove some
[3:08:21] extra vertices that we don't need. So we
[3:08:24] didn't need five vertices there. Cool.
[3:08:26] Let's go to top view and just move that
[3:08:28] in. Uh and then it looks like four is
[3:08:30] too many. And then maybe we can do gy
[3:08:32] and just move this along the curve just
[3:08:34] a little bit more. Now they do seem to
[3:08:36] be a little bit off. So what we can do
[3:08:37] is go into edit mode and gz and just
[3:08:40] move it up a little bit. And now you can
[3:08:42] see it's kind of inside which is okay.
[3:08:44] Now it looks like it's not centered. So
[3:08:45] we can go into edit mode and g y just a
[3:08:48] tad bit. Maybe one more g y. Cool. And
[3:08:52] if you wanted to go through it, you can
[3:08:54] do gz and just move it up just a little
[3:08:56] bit more. And now you can see it's
[3:08:58] running through that. Oh, I guess I
[3:08:59] should have done it with this one as
[3:09:00] well. Oh well. GZ. Just move it up a
[3:09:02] little bit. Uh go into edit mode. Now
[3:09:05] this one's too far ahead. So we can just
[3:09:07] move it out slightly. Cool. g y just one
[3:09:11] more time. And when you're done, you can
[3:09:13] just uh you know convert them to a mesh.
[3:09:16] F3, convert to mesh. And then if you
[3:09:18] need to make any adjustments, you can
[3:09:20] totally go into edit mode and turn on
[3:09:22] proportional editing and just make some
[3:09:24] adjustments. Or, you know, honestly go
[3:09:26] here, ctr L, and like and select this.
[3:09:29] Ctrl L and delete these as well. Or of
[3:09:32] course, you know, you can just select
[3:09:33] it. Ctrl L to select linked stuff and
[3:09:36] just move it where you need it to be. So
[3:09:38] if you want to rotate around the wire,
[3:09:39] you can just actually select a portion
[3:09:41] of the wire. Something like that. Shift
[3:09:43] S, cursor to selected, it will snap
[3:09:45] around there. Then hitting period key,
[3:09:47] you can change to 3D cursor pivot point,
[3:09:49] which is the same thing we were doing up
[3:09:50] here. Transform pivot point. You can
[3:09:53] just use the period key and switch to
[3:09:55] that. Then in edit mode on this, select
[3:09:57] anything, ctr L just to select linked.
[3:10:00] And now you can just do R R and it'll
[3:10:01] rotate around that 3D cursor. Of course,
[3:10:03] you can use the other ones as well. Um,
[3:10:05] but I'm going to go back to bounding box
[3:10:07] center. And I actually kind of like the
[3:10:09] rotations that it already gave us. Yeah.
[3:10:11] Now, let's add some floorboards. I did
[3:10:13] remove the egg thing and the pizza thing
[3:10:15] and the foot rest cuz I don't know what
[3:10:17] I want here yet. But let's just do the
[3:10:19] floor anyway. All right. Let's go into
[3:10:21] local view because right now I want to
[3:10:22] add some floor planks. So, what I'm
[3:10:24] going to do is select this shift
[3:10:25] duplicate right click cancel piece of by
[3:10:27] selection. And what I'm going to do is
[3:10:30] probably expand this on the SY. So, for
[3:10:33] now, I'm just going to leave it like
[3:10:34] this. And let's reset set origin origin
[3:10:36] to geometry. And what I'm going to do is
[3:10:38] add as many loop cuts as thick as you
[3:10:40] want your planks. So if you want your
[3:10:43] planks this thick, then you would add
[3:10:45] this many loop cuts. Like each plank is
[3:10:47] this thick. And now what we can do is
[3:10:49] add three loop cuts cuz I want an
[3:10:51] alternating pattern. If you want to uh
[3:10:54] add more alternating pattern, you can
[3:10:55] add more loop cuts and adjust them as
[3:10:57] necessary. But I'm going to make mine
[3:10:59] fairly even. So now what I'm going to do
[3:11:01] is shift alt and select all of these
[3:11:03] loop cuts. And I'm going to select on
[3:11:07] this one. And then I'm going to just
[3:11:08] alternate. So two and then one and then
[3:11:11] two and then one and then two. Of
[3:11:13] course, if you want, you can also start
[3:11:15] with two. One, two, one, so on so forth.
[3:11:17] Now what we can do is just hit bevel,
[3:11:19] crb to bevel, but make it really, really
[3:11:21] small. Just like that. And then we can
[3:11:22] delete those faces. And now what we can
[3:11:25] do is a e and just extrude upwards. Make
[3:11:28] sure to apply our scale. And then what
[3:11:30] we can do is add a bevel modifier just
[3:11:32] like so. And shading. I definitely want
[3:11:34] to harden the normals. Maybe turn up to
[3:11:36] like three segments. And then we can
[3:11:38] just adjust the amount until we get some
[3:11:39] planks that we like. So that looks
[3:11:41] really nice. So I think I'm just going
[3:11:43] to leave it like that. Okay. Let's make
[3:11:45] sure they're not overlapping. I guess we
[3:11:46] probably should have done the planks
[3:11:48] first, but that's totally okay. We can
[3:11:49] just go into wireframe, select both of
[3:11:51] these, and just GZ and move it down like
[3:11:54] so. Make sure everything is resting
[3:11:56] here. Just like that. Okay. Okay, for
[3:11:58] like a wall outlet, we can probably add
[3:11:59] like a cylinder just to cover something
[3:12:02] up. 32 is way too many. Let's just do
[3:12:04] 12. Let's just scale that down over the
[3:12:06] outlet. RX90, just like so. Then we can
[3:12:09] probably select this face, extrude it,
[3:12:10] and just Whoops. Definitely not.
[3:12:12] Proportional editing. Then we can just
[3:12:14] select this and expand it a little bit.
[3:12:16] Uh, and then right click, shade auto
[3:12:18] smooth. Maybe scale this down a little
[3:12:20] bit more so it's a little bit more
[3:12:21] defined. And then there you can just use
[3:12:23] like a curve to plug it in. And then I'm
[3:12:26] just going to shifty duplicate this
[3:12:28] curve and shift S selection to cursor
[3:12:31] just like so. And I'm just going to
[3:12:33] adjust this over here. And GX move it a
[3:12:38] little bit. RZ kind of like so. Let's
[3:12:41] just move it like that. And now it kind
[3:12:42] of looks like we're using our curve
[3:12:44] outlet. Uh and you can see if I hide
[3:12:46] this real quick, you can see I did the
[3:12:47] same exact thing for the computer as
[3:12:48] well. All right, let's add like a cap to
[3:12:51] the top here. So what I'm going to do is
[3:12:52] probably shift right click somewhere and
[3:12:54] just shift a add a plane. like so. And
[3:12:57] I'm just going to scale it down, you
[3:12:59] know, about a little bit sized above the
[3:13:03] thing. Let's just go into edit mode and
[3:13:05] let's just gy bring it over here. Let's
[3:13:08] add a loop cut here about the same size.
[3:13:13] And let's just do ex and snap it over.
[3:13:16] And then I want it lingering a little
[3:13:18] bit over the edge of the room.
[3:13:22] We can go in edit mode and just extrude
[3:13:23] upwards. If you want to give it a
[3:13:25] solidify modifier instead, just to see
[3:13:27] how it looks first, you can totally do
[3:13:28] that. And I kind of want one for the
[3:13:31] bottom as well. So, let me just move
[3:13:32] this down. Let's just go in here and
[3:13:35] let's go into edit mode. Select this.
[3:13:36] Shift Duplicate. Right click cancel. B
[3:13:38] separate by selection. You already know
[3:13:39] how it is. Double click just to get
[3:13:41] that. Um, let's just scale it up.
[3:13:43] Whoops. Let's do right click, set origin
[3:13:46] origin to geometry. Scale that up just a
[3:13:48] little bit. I don't know, maybe about
[3:13:50] the same out as the other one. Right. So
[3:13:53] about here. I'm just lining that up and
[3:13:55] lining this up here. If it's not
[3:13:56] perfect, it's totally fine. We can just
[3:13:59] extrude that out. Apply our scale. Uh
[3:14:01] let's come over here. Ctrl L. Copy
[3:14:03] modifiers. Cool. And then I think I want
[3:14:06] a little bit more detail here at the
[3:14:09] top. So what I'm going to do is go into
[3:14:10] edit mode. Let's just select this. And
[3:14:13] uh let's just make this up a little bit.
[3:14:15] And then for this thing, let's go and
[3:14:17] let's go into solid mode. And let's go
[3:14:20] and just select these bottom faces here.
[3:14:22] Let's uh insert them a little bit. And
[3:14:25] then extrude downwards. So there we kind
[3:14:27] of have something like that. Cool. And
[3:14:29] maybe what we can do is
[3:14:31] let's see B be these.
[3:14:35] That way it's got a little bit more
[3:14:37] style. What we can try instead is maybe
[3:14:40] a custom inset. So, if we do Crl +B and
[3:14:43] then we come over to the bevel menu.
[3:14:45] Whoops. Let's come over to the bevel
[3:14:47] menu. We can come to custom profile type
[3:14:50] and kind of just make it inverted this
[3:14:52] way instead. That also looks pretty
[3:14:54] cool. So, I'm going to shade auto smooth
[3:14:56] this one. Um, that's cool. Uh,
[3:14:59] additionally, if you don't like doing it
[3:15:01] that way, you can just do Ctrl +B and
[3:15:03] instead of custom super ellipse and then
[3:15:05] just change the shape inward a little
[3:15:07] bit and that would kind of give you a
[3:15:09] similar effect. So shape by default is
[3:15:11] 0.5. We can just bring that down just a
[3:15:14] little bit like so. Definitely a little
[3:15:15] bit less sharp than if we make a custom
[3:15:17] one. So let's just see if we can do
[3:15:20] something like a cool bend. That looks
[3:15:23] pretty sick actually. But like honestly
[3:15:25] just find something that you like. All
[3:15:28] right. So the next thing is kind of a
[3:15:30] combination of everything. We're going
[3:15:31] to be doing materials. We're going to be
[3:15:33] joining objects. We're going to be
[3:15:35] deleting things and saving information
[3:15:37] and space in our GB file. So, this one
[3:15:40] is going to be a pretty pretty intense
[3:15:43] section. So, what I like to do at this
[3:15:46] point, if you're not organized with your
[3:15:47] collections, which I am definitely not
[3:15:49] organized with my collections or naming
[3:15:51] conventions at all, what you should do
[3:15:53] is come up here and file and save
[3:15:55] incremental or save a copy. Save
[3:15:58] incremental will just add a one to your
[3:16:00] Blender file and create a completely new
[3:16:02] copy, which is what I like to do. So,
[3:16:04] just save incremental and you can see it
[3:16:06] says room portfolio 1.blend. And now you
[3:16:08] can come over here and file save as. And
[3:16:10] you can see that we have these two the
[3:16:13] our original one and then we also have
[3:16:14] the one that we are currently on. And
[3:16:16] you can rename that if you want to. So
[3:16:18] typically when I'm working on a new
[3:16:21] project, I also I set some initial
[3:16:23] materials as I'm working and I delete
[3:16:24] phases as I'm working. So it's kind of a
[3:16:27] wishy back and forth. There's no reason
[3:16:30] in particular for this video that I'm
[3:16:31] doing it in this order other than I just
[3:16:34] want distinct sections for this video.
[3:16:36] So, let's go first into either material
[3:16:39] preview or rendered mode. And make sure
[3:16:41] to change your render engine from EV to
[3:16:44] cycles because we're going to be baking
[3:16:45] our lights or saving the calculated
[3:16:48] light data into our image textures.
[3:16:51] Again, if you don't know what that is,
[3:16:52] that's totally okay. Just uh know for
[3:16:54] now that we should be in cycles. And for
[3:16:56] your viewport thing, make sure to tone
[3:16:58] down the max samples. It might start
[3:17:00] really high like 256. you know, adjust
[3:17:03] it, you know, to your computer, what
[3:17:05] your computer can handle smoothly. If
[3:17:06] your computer can handle more, you can
[3:17:08] definitely increase that. And then you
[3:17:10] can also turn on this D noiseis thing,
[3:17:11] which will kind of get rid of some of
[3:17:13] the fuzz. So, what we can do is just
[3:17:14] come over here and drag up a new window.
[3:17:17] If you don't like that, you can just hit
[3:17:18] F3 and split view. And you can choose
[3:17:21] one of these, and then it'll give you
[3:17:22] the same sort of option there. You can
[3:17:24] also rightclick and just do join down or
[3:17:28] right click and vertical split, and
[3:17:30] it'll kind of give you the same thing
[3:17:31] there. So, let's come over here and
[3:17:33] switch this to the shader editor where
[3:17:35] we edit our materials
[3:17:37] and let's change it from object to
[3:17:40] world. This will change our world
[3:17:42] lighting. So, let's go back into
[3:17:43] rendered mode and let's search for a sky
[3:17:46] texture. And let's just plug that in
[3:17:48] right here. So, what this will do, it'll
[3:17:51] add a builtin sky texture for us from
[3:17:54] Blender. And let's just hide this entire
[3:17:56] background for now. So, I'm just going
[3:17:57] to hide that. So, we have a lot of
[3:17:59] options here. We can do like the
[3:18:00] rotation of the sun to change the
[3:18:03] sunlight, the strength of it, the sun
[3:18:06] size, which which pretty much
[3:18:07] determines, you know, how how smooth the
[3:18:10] shadow is. If you want a really harsh
[3:18:12] shadow, for example, you can have a
[3:18:14] really small sun size or you can have go
[3:18:17] for something a little bit softer. You
[3:18:18] can always adjust your lighting later.
[3:18:20] You so you know, don't put too much
[3:18:21] pressure on yourself to get the lighting
[3:18:23] correct at the very moment. Okay, cool.
[3:18:25] So now what we can do is select anything
[3:18:27] and then let's go back to object mode
[3:18:30] and give it some materials. So this one
[3:18:32] I'll call floor plank. Floor plank. So
[3:18:35] initially we can just start with with
[3:18:37] basic colors for now. So for planks, I
[3:18:39] don't know. I think I'm going for
[3:18:41] something a little more stylized. So, I
[3:18:43] might bring this down and instead of
[3:18:45] making it like the cliche brown that you
[3:18:47] expect, I might uh, you know, make it
[3:18:50] make it a little bit reddish like uh the
[3:18:53] Acadia trees in in in Minecraft or
[3:18:55] something like pink or something. Uh,
[3:18:57] you know, but again, really up to your
[3:18:59] scene and what you're trying to go for.
[3:19:01] I forgot to mention like make sure to
[3:19:03] set this to your GPU if you have a good
[3:19:05] GPU because it'll speed up
[3:19:07] significantly. And I'm also going to
[3:19:09] turn on D noiseis just so I don't blind
[3:19:11] you guys with all my noise. And there's
[3:19:13] also this noise threshold thing which
[3:19:14] where you can adjust how much noise you
[3:19:16] want it to get through. Obviously the
[3:19:17] more noise the more performant. But the
[3:19:19] more you know fuzzy it's going to look
[3:19:21] when you when you move around like D
[3:19:23] noiseis you can see all that fuzz uh
[3:19:26] without there. So when you're in D
[3:19:28] noiseis also make sure to click use GPU
[3:19:31] if you have a good G GPU because it'll
[3:19:33] run a lot faster that way. Render will
[3:19:35] come back to that. Right now, we're just
[3:19:37] dealing with the viewport. Now, if you
[3:19:38] don't like manually getting your colors,
[3:19:40] what you can do is find a color palette
[3:19:43] that you like online, maybe like this
[3:19:45] one, and just export it as an image. And
[3:19:49] then back in Blender, what we can do is
[3:19:50] come over here and go into the image
[3:19:52] editor and hit open and just navigate to
[3:19:55] that color file. So now what I can do is
[3:19:58] select this, select this eyropper tool,
[3:20:00] and just select from my color palette
[3:20:02] here. Right, just like that. Cool.
[3:20:06] That's really that's a really really
[3:20:07] handy thing. Again, it doesn't have to
[3:20:09] be a color palette. It can be any image
[3:20:10] that you like the colors of. You can
[3:20:12] just sample from that image. You have a
[3:20:14] lot of other properties here that will
[3:20:16] adjust how your material reacts to
[3:20:18] light. I'm not going to be covering that
[3:20:20] in this video primarily because it won't
[3:20:22] be affecting much of what we're going to
[3:20:24] be doing. Now, there's a lot of other
[3:20:26] material properties that comes with the
[3:20:28] default principled BSDF shader that will
[3:20:31] affect the way that your material looks.
[3:20:33] For us, however, I'm kind of just
[3:20:35] sticking only to the roughness slider,
[3:20:37] which basically determines how shiny it
[3:20:38] is, you can see if I move it to zero,
[3:20:41] it's really, really shiny. And if I move
[3:20:43] it up, it's going to be very matte and
[3:20:45] flat pastley kind of color, right? So
[3:20:49] again, roughness, you can imagine a
[3:20:52] really rough surface is like dirt. Dirt
[3:20:54] is really rough. So when light goes in
[3:20:56] there, it scatters, right? And something
[3:20:58] smooth like a knife or a sword is really
[3:21:01] shiny. The metal is really shiny. And
[3:21:03] that's because it's going to bounce off
[3:21:05] those light rays just like that. So the
[3:21:08] higher the roughness, the more like dirt
[3:21:09] it is. The lower the roughness, the more
[3:21:11] metal metalish it kind of is. And of
[3:21:14] course, you also have like this metallic
[3:21:15] slider that you can play with as well.
[3:21:17] But when it comes to colors, I'm just
[3:21:20] going to be adjusting the roughness
[3:21:22] primarily rather than anything over
[3:21:24] here. Now, another alternative to
[3:21:27] creating materials is what we call
[3:21:29] procedural materials. So instead of just
[3:21:31] using regular base colors, we use math
[3:21:34] functions to adjust those colors in
[3:21:36] certain ways until they look like
[3:21:39] something else. For example, if I search
[3:21:41] for a noise texture and holding control
[3:21:44] shift and click on this will allow me
[3:21:46] just to quickly preview it, you can see
[3:21:48] the noise texture is a bunch of black
[3:21:51] and white. Well, we know that Blender
[3:21:53] behind the scenes is all math, right?
[3:21:56] That's why metallic goes from 0 to one
[3:21:58] and roughness goes from 0 to one. Right?
[3:22:01] We have all these mathematical values
[3:22:03] that we're just changing and Blender is
[3:22:05] just calculating that for us. For a
[3:22:06] noise texture, visually what is
[3:22:08] happening here is that the black values
[3:22:11] are the values that are closer to zero
[3:22:14] and the whiter values are the ones that
[3:22:15] are closer to one. Which means if we
[3:22:18] take some sort of color, so instead of,
[3:22:21] you know, showing like zeros and ones
[3:22:23] all across this floor, it's just going
[3:22:25] to show a grayscale value. So the more
[3:22:27] black it is, the closer it is to zero.
[3:22:29] And the more white it is, the more close
[3:22:31] it is to one. So how do we use a noise
[3:22:34] texture to change, you know, like the
[3:22:36] darkness or the color of our color at
[3:22:38] different points? Like for example, this
[3:22:40] place would be more brown and this place
[3:22:42] would be uh more light brown, for
[3:22:44] example. Well, we can't just plug this
[3:22:46] in here. You can see if I do control
[3:22:48] shift and click on that, we don't
[3:22:49] actually see anything because this is
[3:22:51] not a color value. However, if we take
[3:22:53] the color value and put it in there. So,
[3:22:55] what we see now is that we're not
[3:22:57] providing any color values for this
[3:22:59] noise texture to select from. So, what
[3:23:01] it's doing is just selecting colors from
[3:23:03] like the rainbow spectrum or the visible
[3:23:06] spectrum or whatever color space it's
[3:23:08] operating in. So, let's take a look at a
[3:23:10] places that are very very noticeably
[3:23:12] different along the rainbow spectrum.
[3:23:15] So, purple and red. So, let's take a
[3:23:17] look at purple and red areas. So, this
[3:23:20] seems to be red, but I don't know if I
[3:23:22] can find any specifically red places.
[3:23:24] This kind of red, but anyway, let's take
[3:23:26] a look at this dark blue and violet sort
[3:23:29] of area. So, if I go back just to the
[3:23:31] regular noise texture, you can see that
[3:23:33] it's very black. Well, it's not
[3:23:35] completely black. It's like a grayscale
[3:23:37] black. That means the value is closer to
[3:23:39] zero. So if you can imagine a spectrum
[3:23:41] like this, all the way to the left would
[3:23:43] be zero, which would be completely
[3:23:44] purple. All the way to the right is one,
[3:23:47] which is completely red. So right now
[3:23:49] it's just sampling between values
[3:23:51] between 0 and one across this sort of
[3:23:53] color spectrum. So for these these uh
[3:23:56] wider spaces, we can expect them to be a
[3:23:59] shade of yellowish orange um or slightly
[3:24:03] red. These aren't really that dark. So,
[3:24:05] we can probably expect these lighter
[3:24:06] areas to be about uh you know right here
[3:24:09] like 0.7 or 0.6 or something like that.
[3:24:13] And if I go back here, you can see
[3:24:15] indeed the lighter areas, keep an eye on
[3:24:18] this lighter area is around orange,
[3:24:20] close to red, right? Right. It's
[3:24:22] orang-ish yellowish. Um or honestly, it
[3:24:25] might be close to red, but that's
[3:24:27] essentially what it's doing. So, what we
[3:24:29] need to do is add a color ramp node. Oh,
[3:24:31] if I plug in the color ramp node, I just
[3:24:33] want to show you what that does real
[3:24:34] quick. We get this sort of grayish
[3:24:37] color, right? And how does that make
[3:24:40] sense? Well, what we have here is a
[3:24:42] scale pretty much from or a range I
[3:24:45] should say from zero to one of black
[3:24:49] representing zero and white representing
[3:24:51] one. And then you have this thing here
[3:24:53] called a factor slider that determines
[3:24:55] you know how much we want to go to one
[3:24:58] side of the color or zero in this case
[3:24:59] is black versus to on another side which
[3:25:02] is one which means completely white. So
[3:25:04] you can think if I change it to like
[3:25:05] 0.782 it's going to sample right here
[3:25:08] and give it like a slightly grayish
[3:25:10] color. Whereas if I sample over 0.11
[3:25:13] it's closer to black and it's going to
[3:25:15] sample like a a color that's closer to
[3:25:17] black. So instead of creating a
[3:25:19] consistent sampling, why don't we use a
[3:25:22] random set of black and white values
[3:25:24] like through this noise texture to
[3:25:26] adjust the factor here. So now you can
[3:25:28] see if I plug in the factor here into
[3:25:31] the color ramp factor and the color ramp
[3:25:34] color into the base color, you can see
[3:25:37] now if I go into rendered mode, we're
[3:25:40] definitely we're going to see different
[3:25:41] colors. So let's just make that more
[3:25:43] pronounced. I'm going to make the black
[3:25:45] like a red, like a really light red. And
[3:25:48] then I'm going to make this like a
[3:25:50] really really dark blue. And you can see
[3:25:52] some areas have patches of blue. Now
[3:25:54] it's kind of hard to see because
[3:25:55] everything is what do you call it? It's
[3:25:57] like way too smooth and blurry. So if I
[3:25:59] turn up the scale, you're going to see
[3:26:01] now you can definitely see some areas
[3:26:03] are blue and other areas are red. So if
[3:26:05] I go back and do control shift and click
[3:26:07] this again, you can see as we adjust the
[3:26:09] black and white values, it's going to
[3:26:10] sample from this color ramp here random
[3:26:13] values of black and white of 0 to 1 from
[3:26:16] these colors here and plug it into our
[3:26:18] base color. Let's say at this point you
[3:26:20] can see it's really black, which means
[3:26:21] it's really really close to zero, which
[3:26:24] means it's really really close to red
[3:26:25] here on this side. So if I go back and
[3:26:29] control shiftclick on this, you can see
[3:26:30] that corner is very very red. And you
[3:26:33] can see the areas that are blue are more
[3:26:36] white cuz they're closer to one. So
[3:26:38] again, keep your eyes right here. It
[3:26:40] should be really, really blue. And
[3:26:42] indeed, you can see the blue values
[3:26:44] right there. Now, if you want to adjust
[3:26:46] how much red and blue it is, what you
[3:26:48] can do is actually adjust the slider.
[3:26:50] And what this does, it will increase the
[3:26:52] amount of reds. And if you do this,
[3:26:54] it'll increase the amount of blues. So,
[3:26:56] how does that make sense? Well, what we
[3:26:58] have right is a noise texture that's
[3:27:00] generating random values of 0 and one.
[3:27:04] And since this goes from 0 to one, it's
[3:27:06] just sampling from here and here and
[3:27:08] here and here and here. When you move
[3:27:10] your slider from, let's say, this side
[3:27:12] to this side, effectively what we're
[3:27:14] doing is like any value 0.5 or above is
[3:27:19] just going to be this blue color. So
[3:27:21] that's exactly why we see so much blue
[3:27:23] here because let's say we have 0.8 8. If
[3:27:26] the slider was here and we had 0.8, it
[3:27:28] would be like a a dark shade of blue,
[3:27:30] right? But now what we're effectively
[3:27:32] saying is 0.8 is going to be the same
[3:27:34] shade of blue of 0.9 1, you know, 0.5 so
[3:27:38] on so forth. So all the grayscale values
[3:27:40] that are within this range are just
[3:27:42] going to share the same exact color. So
[3:27:44] that's why we see more blue here. So how
[3:27:45] do we how do we invert it then? Well,
[3:27:48] you just click the slider and then just
[3:27:50] drag it across each other. And you can
[3:27:52] see it's going to flip just like that
[3:27:54] because the sampling is staying the
[3:27:56] same, but we're adjusting where it's
[3:27:59] sampling from. So that's also exactly
[3:28:00] why when you bring them closer together,
[3:28:03] the edges start becoming a lot more
[3:28:05] harsher. Right now it's like a now it's
[3:28:08] like a distinct pattern. Whereas when
[3:28:10] it's far away, you can see it's like
[3:28:12] more smoothed out like a cloudy fluffy
[3:28:15] vibe. Because right now, if you move
[3:28:17] them so close, it's basically, okay,
[3:28:20] either take red or take blue. There's no
[3:28:22] like in between grayscale values at this
[3:28:24] point anymore because they're so close
[3:28:25] to each other. So, it's like take red or
[3:28:28] take blue. When you spread them out,
[3:28:29] it's like, oh, you have all these huge
[3:28:32] range of values to sample from. So,
[3:28:34] hopefully that made sense. And of
[3:28:36] course, you have all these parameters
[3:28:37] that you can change around and you can
[3:28:39] combine textures. So, you can make
[3:28:42] another noise texture for the scale, for
[3:28:44] example. And what you're doing is
[3:28:47] instead of having a flat scale, you're
[3:28:49] creating a noise texture generating
[3:28:51] black and white that's also determining
[3:28:53] random amounts of scale values. We'll be
[3:28:55] making at least one procedural material
[3:28:57] together later, but I want to move on
[3:29:00] now to the third way of texturing or
[3:29:03] adding materials to your scene. So, what
[3:29:05] is PBR materials? Well, it's just a
[3:29:08] method of, you know, giving materials to
[3:29:11] your scene that kind of resembles, you
[3:29:14] know, physically accurate things like
[3:29:16] when you take your camera and you take a
[3:29:17] photo of something, it looks realistic,
[3:29:19] right? So, in 3D software, we just call
[3:29:21] this PBR. So, what better way to go for
[3:29:24] physically based rendering than, you
[3:29:27] know, to use actual images as your
[3:29:29] information data, right? So, if you go
[3:29:31] online and just search for like PBR
[3:29:33] materials on like Ambient CG or
[3:29:35] Polyhaven, which are two very very
[3:29:37] popular sites with I think open source
[3:29:40] licenses like some sort of public
[3:29:42] license. Um, uh, CC0. Yeah. So, you can
[3:29:45] use it for like commercial stuff. Just
[3:29:47] make sure to take a look because some
[3:29:49] sites, some of their textures have
[3:29:51] different licenses from others. Yeah.
[3:29:53] Just make sure to check for that. But
[3:29:55] what you have here is if you click on
[3:29:57] one of these, let's say, let's say I
[3:29:59] kind of like this one to put into my
[3:30:02] scene. What you can see is that we get a
[3:30:03] bunch of images. And these images are
[3:30:05] going to determine, you know, how our 3D
[3:30:08] software calculates light when
[3:30:09] interacting with this. So, let's just
[3:30:12] download this at 4K. For here, I'm going
[3:30:14] to shift A and search for an image
[3:30:16] texture. So, instead of using like a
[3:30:18] base color, we're going to use the color
[3:30:20] from an image. Again, you know, an image
[3:30:23] is just a bunch of colors, right? What
[3:30:25] we're seeing here, literally, if you
[3:30:27] don't think about the software, is, you
[3:30:30] know, hundreds, if not thousands of
[3:30:32] pixels on her screen coloring this shade
[3:30:34] of thing and then coloring this a
[3:30:36] different shade of color and so on so
[3:30:38] forth. So, an image is pretty much the
[3:30:39] same thing. A digital image, it's just a
[3:30:41] bunch of pixels of different colors. So,
[3:30:43] if I open So, if I open that oak veneer
[3:30:47] image that we downloaded, it's called
[3:30:48] diffuse. Diff, short for diffuse, which
[3:30:51] just pretty much means color. If I
[3:30:53] double click on that, and if I take that
[3:30:55] and hook it up into the base color, you
[3:30:57] can see, oh my gosh, we have our image
[3:31:00] that's now appearing on our 3D surface.
[3:31:03] That's awesome. But how do we change
[3:31:05] that? Well, if you remember from my
[3:31:07] previous video when I talked about image
[3:31:09] textures, we need to adjust our UV map.
[3:31:12] So UV mapping is taking the idea that
[3:31:15] you have a 2D image and you're mapping
[3:31:17] it into this 3D virtual simulated space,
[3:31:20] right? What we're looking at is a 2D
[3:31:22] computer screen. There is no actual 3D
[3:31:25] space. It's all mathematical
[3:31:26] calculations. So what we need to do is
[3:31:28] map from a 2D coordinate system into a
[3:31:31] simulated 3D coordinate system. So what
[3:31:33] we can do is come over here and go to
[3:31:35] the UV editor to adjust our UVs. And
[3:31:38] then let's switch to our oak veneer
[3:31:40] image, which is what the one that we're
[3:31:42] using. Now, if I go into edit mode and
[3:31:44] hit A to select everything, you can see
[3:31:46] this is our UV map. Basically, what it's
[3:31:49] saying is out of this 2D image, take
[3:31:51] this area and put it on that specific
[3:31:55] face. So, if I select like a face, for
[3:31:57] example, you're going to see like, okay,
[3:31:59] take all these pixels in this area and
[3:32:01] put it on this 3D model. And you can see
[3:32:03] when I get close to it, it's really,
[3:32:05] really blurry and pixelated. Why does
[3:32:07] that make sense? Well, if we take a look
[3:32:10] at the entire image texture, which is
[3:32:12] 4K, we're only using a fraction of those
[3:32:14] pixels. So, if I select this like so,
[3:32:18] and I scale it up to take more of the
[3:32:23] image texture, you can see what we have
[3:32:24] is a lot more pixels and it's a covering
[3:32:27] a lot more area. Basically, we're saying
[3:32:29] take all of this and shove it into this
[3:32:31] small little area, which is why it's a
[3:32:32] lot more detailed than these other ones,
[3:32:36] for example. So ideally when you're
[3:32:38] using uh UV mapping, you want to take up
[3:32:41] as much of the image texture as
[3:32:42] possible, right? And the reason you want
[3:32:45] to do that is because you get better
[3:32:47] resolution and your textures look nicer.
[3:32:50] Now, what about issues like this where
[3:32:52] it's on the side and you can see kind of
[3:32:53] like the seam and uh if I select the
[3:32:56] side, you can see it looks nothing like
[3:32:58] it does on over here. So even if I try
[3:33:02] scaling it, even if I try moving it,
[3:33:04] it's just not going to work. it kind of
[3:33:06] just looks really really weird. So what
[3:33:08] we can do is unwrap the model better. So
[3:33:10] UV mapping is pretty much the idea that
[3:33:13] you know how do we map a 2D you know
[3:33:16] texture into a 3D space, right? What we
[3:33:18] were doing originally is just adjusting
[3:33:20] the UV map like the scale, the rotation
[3:33:22] and everything. But we can also adjust
[3:33:24] how it looks. So, if I come back here
[3:33:26] and hit A and U and unwrap and do smart
[3:33:29] UV project, it'll kind of use some
[3:33:32] algorithms behind the scenes to unwrap
[3:33:34] this object for us and try and flatten
[3:33:37] it out to lay down on a 2D image
[3:33:39] texture. So, if I hit smart UV project
[3:33:42] and just hit unwrap, you can see that it
[3:33:45] actually did a fairly decent job. So,
[3:33:47] now when I click on this face, you can
[3:33:48] see it actually has some area and I can
[3:33:51] change it around just like that. You'll
[3:33:53] also notice okay now from this face and
[3:33:56] this face there seems to be like this
[3:33:57] sort of edge or this sort of seam we
[3:33:59] call it. Now the reason for that is
[3:34:01] because they're using two completely
[3:34:03] different places of the texture right
[3:34:05] you can see this is over here and this
[3:34:07] is over here there's no continuous in
[3:34:10] the texture. So what if you did So what
[3:34:12] if you wanted a continuous texture?
[3:34:14] Well, you would just R90 get it in the
[3:34:17] same sort of direction and then you
[3:34:19] would move this right here. Um, you
[3:34:21] know, somewhere super close. And you can
[3:34:23] if I just wait, let me just move it one
[3:34:25] more meter just like that. Sorry, like
[3:34:28] one more pixel. You can see it's
[3:34:30] perfectly lined up. And if I go out, it
[3:34:32] looks pretty much seamless, right?
[3:34:34] Because it's continuing on from the
[3:34:36] image, which is clearly continuous here.
[3:34:39] They are noticeable close up, but when
[3:34:41] you're far away, no one's really going
[3:34:43] to tell at all. So, so sometimes your
[3:34:45] seams will not matter. So, more
[3:34:47] visually, you can imagine that
[3:34:49] everywhere that's cut like here, here,
[3:34:51] here, here, here, these are all what we
[3:34:54] call seams. So, if I quickly add a cube
[3:34:56] and I give it the same material, which
[3:34:58] is floor plank, by default, a cube will
[3:35:01] have a decent unwrap for it. So if you
[3:35:03] wanted to mark seams yourself, you can
[3:35:05] imagine that we would have a cut on this
[3:35:07] edge, a cut on this edge, a cut on this
[3:35:09] edge, a cut on that edge, and then you
[3:35:12] would need these two as well, which
[3:35:14] means you would need to cut out here and
[3:35:16] here as well, as well as the top. So you
[3:35:18] can slice here, slice, slice, slice,
[3:35:21] slice. Right? So let's do that. We would
[3:35:25] select this edge, Ctrl + E, and do mark
[3:35:27] seam. And you can see that turns red.
[3:35:29] Actually, let me just go into solid
[3:35:30] view. Ctrl + E, mark seam. So again,
[3:35:34] we're just looking at the top. So we're
[3:35:35] slicing here, slicing here. And then we
[3:35:37] also want to slice here as well as the
[3:35:39] edges, right? So kind of just like this,
[3:35:42] which is what we said. Now I just do
[3:35:43] control E mark seam. And if I go here,
[3:35:47] you can see these are going to be our
[3:35:48] seams. And now if I hit a U unwrap, and
[3:35:52] just do angle based, you can see we get
[3:35:54] the same exact unwrap. Now what if we
[3:35:57] mark all the edges for example E and
[3:36:00] mark all of them as seams. And now if I
[3:36:02] do U and unwrap angle based. And now
[3:36:04] what we get is three separate faces. So
[3:36:06] if I turn up here UV sync selection, I
[3:36:09] can just easily select on one of these.
[3:36:11] You can see they're all completely
[3:36:13] separate. Now this is also the case with
[3:36:15] a properly unwrapped cube. You can see I
[3:36:17] can just move that individually just
[3:36:18] like so. We're just changing the UV map,
[3:36:20] right? But with properly marked seams,
[3:36:23] what it gives Blender when it unwraps is
[3:36:26] more information to determine the
[3:36:28] relationship between the faces. For
[3:36:30] example, if I come to this corner here,
[3:36:32] you can see that it continues on across
[3:36:34] the corner like so. Whereas on here,
[3:36:37] it's not continuing across the corner.
[3:36:39] And you can just tell there's a seam
[3:36:41] there. Same with this back side here,
[3:36:44] you can see that it doesn't continue at
[3:36:46] all. There's no continuous. But if I go
[3:36:48] to this one, you can see that it
[3:36:51] continues around the corner. And it's
[3:36:53] also the same on this side. And you can
[3:36:55] see indeed on this side as well, there's
[3:36:57] no continuousing on this corner either.
[3:37:00] So with a proper unwrap, we get
[3:37:03] something quote unquote more realistic
[3:37:05] as in we don't see as many of these hard
[3:37:07] distinguishments. Like in real life,
[3:37:09] yeah, there are definitely cases where
[3:37:11] you have like these noticeable
[3:37:13] differences in textures, but generally
[3:37:15] you don't like that because it looks a
[3:37:17] little bit jarring and it looks a little
[3:37:18] bit less realistic. So the general rule
[3:37:20] of thumb is when you're unwrapping
[3:37:22] something, you kind of want to get the
[3:37:23] least amount of seams with the most
[3:37:25] continuous sort amount of result as well
[3:37:28] as with the least amount of distortion.
[3:37:30] So a cube is probably not a great
[3:37:32] example of that. But if I go and select
[3:37:34] this and distort some of the vertices,
[3:37:37] for example, you can see this is what we
[3:37:39] call distortion. And again, that's
[3:37:41] obviously not realistic. So when you're
[3:37:43] unwrapping, you want to look out for
[3:37:45] distortion and you want to look out for
[3:37:47] the number of seams you have. So yeah,
[3:37:48] UV unwrapping just like modeling is like
[3:37:51] problem solving. You'll have to do a lot
[3:37:53] of trial and error and develop your
[3:37:54] intuition over time because when you get
[3:37:57] more complicated models rather than
[3:37:59] just, you know, the primitive objects
[3:38:00] here, uh you're going to have to, you
[3:38:02] know, try and guess where to mark seams
[3:38:04] and things like that. General rule of
[3:38:06] thumb is you want to minimize the amount
[3:38:07] of seams you have, minimize the amount
[3:38:09] of distortion you have. Obviously,
[3:38:11] that's just the general rule of thumb.
[3:38:12] There's definitely cases where there's
[3:38:14] an exception to that. Um, but you know,
[3:38:16] for this course, I'm just going to be
[3:38:18] sticking with that general rule of
[3:38:19] thumb. So, another way to adjust the
[3:38:21] texture instead of adjusting the UV map
[3:38:23] or the image is to adjust the
[3:38:26] relationship between the UV map and the
[3:38:28] image. So, the way to do that is search
[3:38:31] for a mapping node and plugging in that
[3:38:34] mapping node for their vector value
[3:38:36] here. Now, it seems to be broken and
[3:38:37] that's because this mapping doesn't have
[3:38:39] any sort of coordinate system. So, then
[3:38:42] we need to add a texture coordinate
[3:38:43] node. texture coordinate node. We and we
[3:38:46] can give it the UV map that we used as
[3:38:48] the texture coordinate. So, we get the
[3:38:50] same exact thing. However, now I have a
[3:38:53] lot of options here. I can change like
[3:38:55] the scale. So, I can do like five. And
[3:38:57] you can see, take a look at that. We're
[3:38:59] repeating the texture five times now
[3:39:01] instead of just one. And you can kind of
[3:39:02] see it starts repeating. So, just to
[3:39:04] really really drive that point home, if
[3:39:06] I turn this to like 200, for example,
[3:39:08] you can see that the 4K texture block
[3:39:11] block, it's just repeating over and over
[3:39:14] again. So, now if I go here, and that's
[3:39:16] exactly what this parameter right here
[3:39:18] does. It says repeat the texture. This
[3:39:20] doesn't adjust the image itself. The
[3:39:22] image is still 4K by 4K and it still
[3:39:24] looks like this. And it doesn't adjust
[3:39:26] the UV map either, right? The UV map is
[3:39:29] still here and it looks exactly the
[3:39:30] same. What it's adjusting though is the
[3:39:33] relationship between the UV map and the
[3:39:35] image texture.
[3:39:37] So effectively, if I make this go back
[3:39:40] to one, for example, and I scale this up
[3:39:43] to 200, I'm just going to type 200. You
[3:39:46] can see we get the same result. However,
[3:39:48] now our UV map is like this really
[3:39:50] ginormous thing, right? So you might be
[3:39:52] wondering, okay, it seems like it's out
[3:39:54] in the oblivion, so where is it getting
[3:39:56] all its texture? Well, again, that's
[3:39:58] where this comes from. It's called
[3:40:00] repeat. So you can imagine that this
[3:40:02] texture will just keep on repeating in
[3:40:04] this gray area over and over again. And
[3:40:06] that's where our UV map is getting the
[3:40:07] information. You can see if I change
[3:40:09] this to clip for example, only the faces
[3:40:12] that are inside this texture are going
[3:40:15] to have the material and everything else
[3:40:16] is going to be clipped. So if I select
[3:40:18] this face here, for example, and I just
[3:40:20] move it out of the texture, you can see
[3:40:22] that the texture is no longer repeating.
[3:40:25] It's just being clipped. So there's
[3:40:26] nothing there, which is why it's black.
[3:40:27] Okay. So hopefully that makes sense. I'm
[3:40:29] going to change that back to repeat. So,
[3:40:31] when you're working with PBR materials,
[3:40:32] there's kind of three ways to adjust
[3:40:34] things. You can adjust the image texture
[3:40:36] itself. Of course, you can also adjust
[3:40:38] the image texture itself because it's
[3:40:40] just color, right? So, you can use the
[3:40:42] color data from an image to determine
[3:40:46] another set of colors for example. So,
[3:40:49] here you can see now everything is black
[3:40:51] and white. And what if I change this to
[3:40:54] like red for example, and then I'll
[3:40:56] change this to like blue. You can see
[3:40:58] what we have now are wood planks that
[3:41:00] are red and blue. It's taking the
[3:41:02] grayscale color data information here
[3:41:05] and using it to sample from this color
[3:41:07] ramp here. And then like other photo
[3:41:09] editing and video editing softwares, you
[3:41:11] also have things like the curves. So you
[3:41:13] might have seen this before. So if I
[3:41:16] plug this in here, control shiftclick,
[3:41:18] just click here. And you can see if I
[3:41:19] want to, let's say, turn up the reds,
[3:41:21] you can see that, you know, it's going
[3:41:23] to be a lot more red. If I want to lower
[3:41:25] the blues, you know, I can do that as
[3:41:28] well. Then you also have, you know, the
[3:41:29] other common operations like hue,
[3:41:31] saturation, like so.
[3:41:34] And you know, when I take out all the
[3:41:35] saturation, it goes away, right? You
[3:41:37] know, just like your photo editing
[3:41:39] software. All right. So, those are kind
[3:41:41] of the basics of working with any sort
[3:41:43] of image texture. Now, when it comes to
[3:41:46] PBR, remember, we get all this other
[3:41:48] information here as well. So, what are
[3:41:50] all of these? Well, you know, in real
[3:41:52] life, if you put your hand around like a
[3:41:55] wooden desk or something, you're going
[3:41:56] to feel different amounts of roughness
[3:41:58] across your surface, and that means
[3:42:00] light's going to interact with those
[3:42:02] areas at different places, which is why
[3:42:04] we also have these other materials again
[3:42:07] to tell the 3D software how to calculate
[3:42:10] these mathematical calculations more
[3:42:12] realistically. Now, instead of shift
[3:42:14] duplicating this uh or highlighting all
[3:42:17] these and duplicating them multiple
[3:42:19] times like so, there's this really
[3:42:21] helpful add-on, if you come into edit
[3:42:23] preferences, search for node wrangler,
[3:42:25] and make sure to check that it's
[3:42:27] enabled. And what you can do instead, if
[3:42:29] I just get rid of all this is just
[3:42:32] select the principal BSDF, control shift
[3:42:34] T, navigate to oak textures, select
[3:42:37] everything, and just hit principal
[3:42:38] texture setup.
[3:42:41] And you can see it'll set up everything
[3:42:43] for us. It'll give us the nodes that we
[3:42:45] need. It'll set up the diffuse into the
[3:42:47] base color, the roughness map into the
[3:42:51] roughness channel. Here you can also see
[3:42:53] that for the color space, we set it as
[3:42:55] non-color because it's just because
[3:42:57] there is no color information here. It's
[3:42:59] a range of zeros and ones determined by
[3:43:01] grayscale, right? So if I go to the
[3:43:04] roughness map here, you can see it's a
[3:43:05] grayscale image. So the areas that are
[3:43:07] here are closer to zero, which means
[3:43:09] it's going to be less rough and more
[3:43:11] shiny. And the areas that are white are
[3:43:13] going to be more rough and less shiny.
[3:43:14] It's closer to zero, which means the
[3:43:16] roughness value at this point of the
[3:43:18] image or in our simulated 3D environment
[3:43:21] should be a lot more shiny. So if I go
[3:43:23] into edit mode and just select the face
[3:43:25] where this is and then hit period to
[3:43:27] jump there, I guess it's kind of hard to
[3:43:29] tell because these are it's not really
[3:43:31] close to black at all. So, it's really
[3:43:33] really kind of hard to tell from this
[3:43:35] specific lighting, but this is supposed
[3:43:37] to going to be more shiny than the areas
[3:43:40] that are wider. And then again, here you
[3:43:42] can see it gives us our mapping node
[3:43:43] that we can play around which will
[3:43:45] affect all the textures here. So, for
[3:43:47] these other ones like displacement,
[3:43:49] essentially what we're doing is
[3:43:51] displacing the geometry so it's more
[3:43:53] realistic, right? Again, if you move
[3:43:54] your hand around a wood plank, certain
[3:43:57] areas are going to be higher than
[3:43:58] others. So, essentially what we're doing
[3:44:00] here is displacing it. Now, since we
[3:44:01] just have a plank by itself, we're not
[3:44:04] really going to see much displacement
[3:44:05] here at all. Even if we, you know, crank
[3:44:07] up the scale or the midle or whatever.
[3:44:09] However, if I duplicate this and bring
[3:44:11] it up and I go into Whoops. Let's piece
[3:44:14] over by selection. And I go into edit
[3:44:17] mode, for example, and just subdivide
[3:44:18] this a lot. And then I give it a
[3:44:21] displacement modifier like so. And I
[3:44:24] create a new texture for it. So, here we
[3:44:27] can just create a clouds for example.
[3:44:30] You can see it's it's displacing that,
[3:44:33] right? And we can change like the
[3:44:34] strength of it and how much it's
[3:44:36] displacing. But if we don't have, you
[3:44:38] know, if I go into edit mode here and
[3:44:41] unsubdivide
[3:44:42] and unsubdivide and unsubdivide and
[3:44:45] unsubdivide again and one last time, you
[3:44:49] can see that the displacement barely
[3:44:52] does anything. So for us again, it's not
[3:44:54] really a big deal because we're so far
[3:44:56] away. you know, the minor displacements
[3:44:58] of wood planks wouldn't really be
[3:45:00] noticeable even if we did have some in
[3:45:02] this case. Now, we also have this thing
[3:45:04] called ambient occlusion, and basically
[3:45:07] it adds like soft shadows where objects
[3:45:09] are like close to each other sort of
[3:45:11] thing. And that kind of gives a, you
[3:45:13] know, a bigger sense of depth and
[3:45:14] realism as well. Now, it's not hooked up
[3:45:17] automatically because it's not it's not
[3:45:19] like a map like anything else. You have
[3:45:21] to like mix it with your base color in
[3:45:23] order to like change it and so on so
[3:45:25] forth. That's a little more advanced, so
[3:45:27] I'm not going to be covering that. But
[3:45:28] that's kind of what ambient occlusion
[3:45:30] is. And what you have, this last thing
[3:45:32] here is a normal map. And basically that
[3:45:34] just, you know, adjusts like quote
[3:45:36] unquote the normal of your surface,
[3:45:39] which determines, you know, how lighting
[3:45:40] is calculated when hitting that surface.
[3:45:43] So this is going to be, it's not going
[3:45:44] to be an accurate explanation, but just
[3:45:46] for like a more general explanation.
[3:45:49] Let's say you have a surface like this
[3:45:51] and the normal is pointing this way. And
[3:45:54] let's say your light is coming from
[3:45:56] here. So this is kind of like your light
[3:45:57] source. Based on this normal, your light
[3:46:00] source is going to take that factor into
[3:46:03] consideration and then sort of, you
[3:46:05] know, have some sort of reflection of
[3:46:06] angle. However, if you have a normal map
[3:46:09] that adjusts the normal in some sort of
[3:46:13] way, for example, let's say the normal
[3:46:15] is now pointing this way. If your light
[3:46:17] is hitting your surface, it might, you
[3:46:19] know, now reflect this way. I don't know
[3:46:22] if that's accurate or not, but you know,
[3:46:23] obviously it's going to depend on your
[3:46:25] surface. So, if the light is reflecting
[3:46:27] differently based on your normal map
[3:46:29] because it's adjusting how the normal is
[3:46:32] looking, which affects the vector math
[3:46:34] behind the scenes, then your surface
[3:46:36] will look different. And that's kind of
[3:46:38] what a normal map is doing. So a lot of
[3:46:41] time normal maps are used to quote
[3:46:43] unquote fake geometry because if you
[3:46:45] adjust the lighting or the mathematical
[3:46:48] calculation, you can essentially create
[3:46:50] things that look like they have geometry
[3:46:52] even if there's no actual geometry
[3:46:54] there. As in you don't have to add extra
[3:46:56] vertices for more detail. The lighting
[3:46:59] will kind of do the work for you. So
[3:47:00] here's an example from Bruno Simon, one
[3:47:03] of his experiments, open source repo.
[3:47:05] You can see if I look at the edge here,
[3:47:07] it seems like, okay, there's definitely
[3:47:08] some sort of insets there. There's
[3:47:10] definitely some sort of loop cuts.
[3:47:11] There's definitely some sort of extra
[3:47:13] geometry there, right? There has to be.
[3:47:15] But in reality, there actually isn't.
[3:47:18] So, I just downloaded case.gb
[3:47:20] by opening it in a new tab. And now,
[3:47:22] when I go back into Blender and import
[3:47:24] that, you can see that if I go into
[3:47:26] wireframe or solid, let me just go into
[3:47:28] edit mode. There's actually no geometry
[3:47:29] here at all. Even though we visually see
[3:47:32] it, there's nothing here. And that is
[3:47:34] the power of a normal map. So instead of
[3:47:36] adding all that information here, we can
[3:47:37] just use a normal map to do that for us.
[3:47:40] Now the topology, you might wonder why
[3:47:42] does it look so bad? It's because
[3:47:43] everything is triangulated for 3GS to
[3:47:45] handle, which is another thing that
[3:47:47] you'll learn about later down the road,
[3:47:48] but it's not really important right now.
[3:47:50] So that's kind of like the power of a
[3:47:53] normal map.
[3:47:56] So just to recap the three ways we
[3:47:58] learned to give our stuff some materials
[3:48:00] is one just use the base color the
[3:48:02] principled BSDF. The second is to use
[3:48:04] some procedural materials which we use
[3:48:06] mathematical calculations to create
[3:48:09] materials and then we have PBR materials
[3:48:11] which are image textures that we find
[3:48:12] online. Now of course you can combine
[3:48:14] methods in the same scene and even
[3:48:17] methods with each other right you can
[3:48:19] use some procedural elements to you know
[3:48:21] affect the base color and so on so
[3:48:23] forth. Additionally, there's other
[3:48:24] methods that I'm not covering in this
[3:48:26] video like texture painting where you
[3:48:27] literally create an image texture and
[3:48:29] paint on it and then you know wherever
[3:48:31] your UV map is since it's just an image
[3:48:33] is just mapping there. So, you could
[3:48:35] texture paint directly in Blender or you
[3:48:37] could like paint in Photoshop and then
[3:48:39] upload the image texture into Blender
[3:48:41] and just use that. There's other
[3:48:42] software out there where you can like
[3:48:43] paint on an image texture and if you
[3:48:45] have a plugin to Blender, as long as you
[3:48:47] save the image in that 3D software, it
[3:48:50] will automatically update the image in
[3:48:52] Blender as well. That way you can have
[3:48:53] like quote unquote real-time updates as
[3:48:55] you paint and save. However, for us,
[3:48:57] we're just going to be primarily
[3:48:58] sticking to either PBR materials that
[3:49:00] you find online, base colors, or some
[3:49:02] basic procedural materials. So, as we
[3:49:05] start applying our materials now and
[3:49:07] going around and applying materials,
[3:49:08] there's a few things we need to keep in
[3:49:10] mind. The first thing is we're going to
[3:49:12] have to start applying our modifiers now
[3:49:14] and confirming that's actually what we
[3:49:16] want. So, if I go for this here, it is a
[3:49:18] bevel modifier. Okay, that looks great,
[3:49:20] but do I really need that many segments?
[3:49:22] So now you can like change it down and
[3:49:24] see if it works or not. So here, three
[3:49:26] looks the same as four. So maybe we
[3:49:28] should just go for three in that case.
[3:49:30] And you can also adjust the amount.
[3:49:32] You're like, okay, do I really want it
[3:49:33] that beveled? And so on so forth. So the
[3:49:35] first thing is you're going to have to,
[3:49:37] you know, apply all these modifiers. And
[3:49:39] that means destructive, which means it
[3:49:41] will be difficult to change later when
[3:49:43] you go back to it. So, make sure you
[3:49:45] really really have something that you
[3:49:46] want before you apply your modifiers. Or
[3:49:48] again, like we did earlier in the video,
[3:49:50] you can duplicate the whole thing, you
[3:49:52] know, your objects together and just
[3:49:53] move that into the modifiers collection.
[3:49:56] Or again, you can come up over here,
[3:49:57] file, save incremental, and start from
[3:50:00] there. So, I think I said it earlier in
[3:50:01] the video, but the first thing we have
[3:50:02] to do is apply our scale. And this will
[3:50:05] also affect our unwrap as well. So,
[3:50:07] apply your scale and make sure nothing
[3:50:08] breaks. And it seems like nothing break.
[3:50:10] But if something did, then make sure to
[3:50:13] fix that. Actually, it does look like
[3:50:15] the applying scale affected this, which
[3:50:18] means I accidentally forgot to apply my
[3:50:20] scale before I applied the modifier or
[3:50:22] sorry, added the modifier. So here you
[3:50:24] can see Z. If I apply my scale, this is
[3:50:26] now messed up. So I can fix this just by
[3:50:28] adjusting the thickness of the solidify
[3:50:30] modifier back there. Also, you know,
[3:50:33] when you're adjusting your things,
[3:50:34] again, this is kind of the time to, you
[3:50:37] know, make sure that's kind of the model
[3:50:39] that you actually want. Additionally,
[3:50:40] you might have to add some extra
[3:50:41] geometry. Like, let's say you want the
[3:50:43] center of this cup to be a different
[3:50:45] color. Well, then you would have to go
[3:50:46] into edit mode, add two loop cuts here,
[3:50:49] and over here, create a new material
[3:50:52] called mug, and another one called like
[3:50:54] mug inside. Mug inside inside. and you
[3:51:00] would assign it to these set of faces
[3:51:02] whereas this one would be something
[3:51:04] else. You can see we assigned it here
[3:51:07] and then this one would be like I don't
[3:51:08] know something like that. Now you don't
[3:51:11] have to add extra geometry to change the
[3:51:13] material at different places on the
[3:51:15] mesh. As noted when we did procedural
[3:51:17] images or image textures they have
[3:51:18] different colors too but for a lot of
[3:51:21] cases you will have to add extra
[3:51:22] geometry to split it up because it just
[3:51:24] makes it easier and you don't have to do
[3:51:26] the mathematical calculations here. Like
[3:51:27] if you wanted to simulate this same
[3:51:29] behavior with Blender nodes, you could
[3:51:32] you could do that, but it would take a
[3:51:33] lot more time and that's kind of too
[3:51:35] in-depth for this video. You know, as
[3:51:37] you go around your scene, you know,
[3:51:38] keep, you know, apply your modifiers,
[3:51:40] make sure it's kind of final. You know,
[3:51:42] save backups if you need to. So, the
[3:51:44] second thing you have to keep in mind is
[3:51:46] starting to join your objects and
[3:51:48] getting rid of extra geometry. So, for
[3:51:51] example, this cactus right here, these
[3:51:53] are three separate objects right now.
[3:51:55] But when I want to animate them, I want
[3:51:57] to animate it just like this, right? I
[3:51:59] don't want it to like animate this in
[3:52:01] and then this in. If you do, then you
[3:52:03] would leave them separate. But I don't.
[3:52:05] I just want to animate this entire thing
[3:52:06] just like that. So what I'd have to do
[3:52:08] is convert this to a mesh, right? Apply
[3:52:10] my modifiers and then join one of them.
[3:52:12] So now they're together. However, you
[3:52:14] can see that the origin point is right
[3:52:16] here. Which means if I animate it like
[3:52:18] from a scale of zero to one in like 3GS,
[3:52:21] it's going to animate from this starting
[3:52:23] point. But that looks kind of awkward.
[3:52:25] What if I want it to start from the
[3:52:26] bottom? Well, I can hit control period
[3:52:28] and that'll bring up this right here.
[3:52:31] And I can do GZ and snap it to the
[3:52:33] bottom. Because we have face select, I'm
[3:52:35] just snapping it to the bottom. And then
[3:52:37] I can hit control period just to convert
[3:52:39] that. So now the origin point is at the
[3:52:41] bottom of the plant. So if I scale from
[3:52:42] 0 to one, it'll come like that. And that
[3:52:44] looks that looks better for what I'm
[3:52:46] going for. Now let me undo the join. And
[3:52:48] the other issue we have to fix is all
[3:52:51] this overlapping right here. We have to
[3:52:53] fix that because this place will take up
[3:52:55] some sort of place on our UV image.
[3:52:58] Because if I go into edit mode, let me
[3:53:00] unwrap this real quick. You can see that
[3:53:02] all this empty space is taking up pixels
[3:53:05] on our image texture. That means other
[3:53:07] areas that could be bigger on the image
[3:53:09] texture and have higher resolution is
[3:53:12] being sacrificed by this area here,
[3:53:14] which isn't being seen at all. So, you
[3:53:17] could come here and adjust that, right?
[3:53:19] And just hide it. But since it's not
[3:53:21] being seen, why not just delete it? At
[3:53:23] this point, you have to make some sort
[3:53:24] of adjustments, right? You can probably
[3:53:26] like take some of these and delete these
[3:53:28] vertices. And then for these ones, you
[3:53:30] can probably just move them slightly. A
[3:53:33] little bit of overlap is fine. You don't
[3:53:35] have to be a perfectionist here, but you
[3:53:37] want to kind of get rid of anything that
[3:53:39] is overlapping or that it's wasting
[3:53:42] texture space. Like when you're going
[3:53:44] for image renders or small scenes like
[3:53:47] this, it doesn't really matter. But when
[3:53:48] you're going for like animated scenes in
[3:53:50] Blender that have a lot of moving parts,
[3:53:52] you know, every bit of optimization
[3:53:54] counts. And this is kind of like the
[3:53:56] same idea when it comes to the browser.
[3:53:58] You know, you want to save on
[3:53:59] information. That way, your users won't
[3:54:01] have to load as long and there might be
[3:54:03] less performance issues. You know,
[3:54:05] there's this general idea that, you
[3:54:06] know, if users have to wait a few
[3:54:08] seconds to use your website, they'll
[3:54:10] kind of click off. Obviously, the
[3:54:11] demographic is a little bit different
[3:54:13] for interactive websites, but you know,
[3:54:16] that's that's still something to keep in
[3:54:18] mind. So, again, this is going to take,
[3:54:20] you know, quite a bit of your time. So,
[3:54:22] you know, just be patient. Just have
[3:54:23] fun. You know, turn on music if that
[3:54:25] helps and so on so forth. Again, you
[3:54:27] don't have to be a perfectionist about
[3:54:28] it. So, same thing with like the bottom
[3:54:30] of this here. I don't think I'll ever
[3:54:32] need it. So, I can just delete that.
[3:54:34] Now, the issue becomes is do in the
[3:54:37] future if I want to animate this, will I
[3:54:39] ever make it bounce up? If the answer is
[3:54:41] I will make it bounce up, well, can my
[3:54:43] camera see underneath? And if my camera
[3:54:45] is always like this, then I can never
[3:54:47] see underneath anyway. So, I'm safe to
[3:54:49] delete that face. If my camera can go
[3:54:51] here, you know, we're just going to see
[3:54:53] through that and it'll look really
[3:54:54] awkward. So, when you're deleting faces,
[3:54:56] when you're joining objects, fixing
[3:54:59] their origin points, you know,
[3:55:00] confirming what kind of modifiers you
[3:55:03] actually want and the shape that you
[3:55:04] want and adding materials. These are all
[3:55:06] things to consider and keep in mind, you
[3:55:09] know, like just to drive that point
[3:55:10] home, it really really depends on what
[3:55:13] you need in order to determine how you
[3:55:14] want to join your objects. Like let's
[3:55:17] say you want to animate all these at the
[3:55:19] same time, but when the user clicks on
[3:55:22] it, you're only animating these. In
[3:55:23] which case, you might join these
[3:55:25] together, but then leave these two
[3:55:27] separate. What if you want all of them
[3:55:28] to go at the same time, but when you
[3:55:30] click on it, all three of them go in
[3:55:31] different separate ways? Well, in that
[3:55:34] case, it's like you would check for the
[3:55:36] name and then like make the scale go to
[3:55:38] one and then tell GAB to play with
[3:55:40] previous or whatever animation method
[3:55:42] you're using. Whereas, if you joined all
[3:55:44] of them together, you know, it would
[3:55:45] just be like, oh, name check if it's
[3:55:47] cactus. If it is, set it scale to, you
[3:55:49] know, this animation timeline or
[3:55:50] whatever it is. Keeping them separate
[3:55:52] has more flexibility. But if you don't
[3:55:53] need the flexibility, then there's no
[3:55:55] reason to keep them separate. I also say
[3:55:56] there's this thing called GPU draw calls
[3:55:59] which will be reduced the more you join
[3:56:01] objects. So that is also a performance
[3:56:03] optimization. So let's say for example
[3:56:06] this entire scene you're never going to
[3:56:08] animate this or you're going to animate
[3:56:10] it together like this but no user
[3:56:12] interaction. They can't click on
[3:56:13] anything doesn't really matter. Then you
[3:56:15] can just control J and join everything.
[3:56:16] Obviously there's a little bit messed up
[3:56:18] things when I join them. But now
[3:56:20] everything acts like one single object
[3:56:22] and that's a that reduces the amount of
[3:56:24] GPU draw cost. Again that's just some
[3:56:26] advanced concept but it doesn't really
[3:56:28] matter. Just keep in mind what you want
[3:56:29] to do for your scene. I can just tell
[3:56:32] you from experience that you're probably
[3:56:34] likely not going to mess up anything and
[3:56:37] the biggest issue will be our texture
[3:56:39] rather than, you know, you joining
[3:56:40] objects together, which I'll talk about
[3:56:42] later in the video. Okay, so before we
[3:56:44] start going around and materializing our
[3:56:46] scene and adjusting everything, of
[3:56:48] course, you kind of want to also play
[3:56:50] around with your light at the same time.
[3:56:52] So, let's go back to the world and take
[3:56:53] a look at some other lighting methods
[3:56:55] that we can use. So, by default, it's
[3:56:56] just a background, like some sort of
[3:56:58] ambient color, right? And you can change
[3:57:00] that and adjust it like so. And then we
[3:57:02] added this really cool sky texture thing
[3:57:05] that comes in with Blender that kind of
[3:57:07] looks like a realistic sky. Another
[3:57:08] lighting method to use is HDRI. You can
[3:57:11] find a lot of great ones for free on
[3:57:13] polyhaven.com.
[3:57:15] So they're just high dynamic range
[3:57:17] images that provide lighting information
[3:57:20] that the 3D software uses for their
[3:57:22] mathematical calculations. So this looks
[3:57:24] really really beautiful. So what what we
[3:57:26] can do is download it. I'm going to go
[3:57:28] for 4K. 2K might be enough for you. You
[3:57:31] know, 8K is generally overkill, but you
[3:57:33] know, do with whatever you need to do.
[3:57:36] So, in order to use that HDR file, we
[3:57:37] need to search for an environment
[3:57:39] texture and plug it in like that. Now,
[3:57:42] be pink because Blender is telling us,
[3:57:44] okay, it doesn't find anything. That's
[3:57:45] why by default it's pink. So, we can
[3:57:47] navigate to it, right, and open it here.
[3:57:50] But again, why search for an environment
[3:57:52] texture? Since we have node wrangler
[3:57:54] installed, we can just do control T and
[3:57:56] it'll automatically add environment
[3:57:57] texture to us as well as the mapping and
[3:58:00] texture coordinate node for us. So I
[3:58:01] open my HDR file and you can see that
[3:58:05] now it's lighting up my scene. So if I
[3:58:07] hit M to mute this, you can see it's
[3:58:09] just going to take the background, but I
[3:58:10] can hit M again to reshow it. And then I
[3:58:13] can adjust the strength of my HDRI. You
[3:58:15] see the shadows are really, really soft
[3:58:17] because the light source is so expansive
[3:58:19] and large, which is what we did with the
[3:58:22] sky texture, right? We increased the
[3:58:23] size and it increased the shadow. You
[3:58:25] can see as I rotate it, for example,
[3:58:28] it's getting darker. Why? Because the
[3:58:30] light source is coming from over there
[3:58:32] now and there's nothing over there. It's
[3:58:34] just a bunch of clouds. So, here's
[3:58:36] another one with that I downloaded from
[3:58:38] Polyhaven that definitely looks that
[3:58:40] definitely has a lot more harsh shadows.
[3:58:42] And you can see how realistic that looks
[3:58:45] already and we barely even did anything.
[3:58:47] So, when lighting your world, these are
[3:58:49] generally the two very common methods to
[3:58:51] light your world. Use an HDRI or use a
[3:58:54] sky texture. Doesn't really matter.
[3:58:56] Really, really up to you. Are there
[3:58:57] other methods to light the sky?
[3:58:58] Absolutely. You can create your own sky
[3:59:00] if you wanted to rather than use
[3:59:02] blenders, but that's a little more
[3:59:04] complicated. And of course, if you don't
[3:59:05] want to use world lighting, you can use
[3:59:08] the actual built-in lighting objects,
[3:59:10] right? Like if you shift A and come here
[3:59:13] and search for light, you have these
[3:59:14] things like spotlights that act like a
[3:59:18] spotlight, right? And you can see I can
[3:59:20] change like the power of it. I can
[3:59:22] change the color of it and a lot of
[3:59:24] other things about it like how wide it
[3:59:26] is and so on so forth. Then you also
[3:59:28] have other kinds of light. You have like
[3:59:29] a sunlight itself that you can use and
[3:59:32] you can hit R to like rotate it, you
[3:59:34] know, so on so forth. Its position
[3:59:36] doesn't matter. So just place it
[3:59:37] somewhere that you like. Click on it and
[3:59:39] you can see that you know it's going to
[3:59:42] adjust that. And of course you can
[3:59:43] combine these lighting methods with your
[3:59:45] other lighting methods. So here you can
[3:59:48] see there's like a slight red glow from
[3:59:50] there. And our HDRI is still affecting
[3:59:51] that. And our sun is as well. You can
[3:59:53] see there's a separate shadow for this
[3:59:56] sun and a separate shadow for this thing
[3:59:59] right here. You have a lot of options
[4:00:00] there. You can play around with the
[4:00:02] lights. You know, at this point it's all
[4:00:03] about just experimenting what looks nice
[4:00:05] for you. you know, change the shape of
[4:00:07] things, change, you know, into like
[4:00:09] ellipse, for example. What does that do?
[4:00:11] So on so forth. Oh, maybe I want some
[4:00:15] lighting here or some over here and over
[4:00:17] here and so on so forth. So another
[4:00:19] really common way to light your scene is
[4:00:21] with an emission shader. So if I click
[4:00:24] on one of these, for example, let me go
[4:00:26] back to object and give it a new
[4:00:28] material called name.
[4:00:30] In principle BSDF, there's this thing
[4:00:32] here called emission. And if I turn up
[4:00:34] the emission, you can see it's going to
[4:00:36] start emitting light. And then I can
[4:00:38] change the color like so. And now it's
[4:00:41] like some sort of really really cool
[4:00:43] neon glowing thing. Now the downside of
[4:00:45] using emission here is that it might
[4:00:47] look a little bit off in 3GS without
[4:00:49] doing some sort of extra steps. It might
[4:00:51] be passable most of the time without
[4:00:53] doing extra steps, but sometimes you do
[4:00:55] have to use extra steps just to make it
[4:00:58] a little bit more realistic. Not always,
[4:01:00] but often times you do. So what people
[4:01:02] like to do is sometimes they'll add like
[4:01:04] a plane in the background. Let's say let
[4:01:06] me just go into wireframe. Let's just
[4:01:08] say I place like a strip here for
[4:01:11] example as uh sy like here. So no one
[4:01:15] can actually really see it but it's just
[4:01:17] going to be lighting my scene. And if I
[4:01:19] go into rendered view just give it a new
[4:01:21] material call it light strip.
[4:01:24] Come into emission and just make it like
[4:01:27] orange or something and turn that up.
[4:01:29] You can see we're kind of getting like
[4:01:30] that's pretty cool actually. Like that's
[4:01:32] a really really cool effect, right? So
[4:01:33] if you go to the world and you plug this
[4:01:36] in just for some better lighting and
[4:01:39] then change this to like 05 for like a
[4:01:41] nighttime scene, you can see we're kind
[4:01:43] of getting some really cool vibes right
[4:01:45] now. So honestly, you know, at this
[4:01:47] point, just have fun. Experiment with
[4:01:49] different kinds of lights, different
[4:01:50] kind of HDRI. Find something that you
[4:01:52] like, different emissions. You can also
[4:01:54] use an emission node if you want to
[4:01:56] rather than the principal BSDF emission.
[4:01:58] it'll kind of have a similar effect. Uh,
[4:02:00] right. Um, and of course there's also
[4:02:02] things you can plug in to change the
[4:02:04] emission, uh, you know, like a gradient
[4:02:07] or or whatnot, but I'm just going to
[4:02:08] stick really really basic for now. But
[4:02:10] yeah, just have fun. You know,
[4:02:12] experiment with your lighting,
[4:02:13] experiment with your materials. Again,
[4:02:15] keep in mind the things that I mentioned
[4:02:16] earlier when you're applying stuff. I'll
[4:02:18] say when you're working with like
[4:02:19] emitter objects that are only there for
[4:02:21] the lighting and not for the scene
[4:02:23] itself, it's generally good practice to
[4:02:24] move it to a new collection like
[4:02:26] emitters or something. That way you know
[4:02:28] that they're not going to be exported.
[4:02:29] They're just only there for the or for
[4:02:31] the lighting. And typically what you do,
[4:02:33] you can't hide it because it'll get rid
[4:02:35] of it. What you can do is come into
[4:02:37] object object properties and under
[4:02:39] visibility you can just turn off camera.
[4:02:41] So you can't see it. You can still
[4:02:43] select it. You can't see it. Uh but it
[4:02:46] will still emit the light. So that's one
[4:02:47] way to remove it from the viewport if
[4:02:49] you want to while still including the
[4:02:51] light. Like if you want to, you can look
[4:02:52] up lighting theory at this point and
[4:02:54] like look at like threepoint light
[4:02:55] system, things like that, you know, how
[4:02:57] to get better se lighting in scenes. So
[4:03:00] you could totally go that route if you
[4:03:02] wanted to, but I highly encourage you
[4:03:04] just to have fun and explore what looks
[4:03:06] cool rather than dive into the theory
[4:03:08] straight off the bat. But if you want to
[4:03:10] dive straight out into professional
[4:03:12] lighting tips and things like that, then
[4:03:14] totally go for it. Another cool trick
[4:03:16] for deleting faces quickly or areas
[4:03:18] quickly. Let's say I go here. Let me
[4:03:20] convert this to a mesh. Make sure my
[4:03:22] modifiers are applied and go into local
[4:03:23] view. Instead of going into edit mode
[4:03:25] and you know like selecting all these
[4:03:27] bottom faces, what you can do is shift G
[4:03:29] and select similar by area which will
[4:03:32] select also the top because it has the
[4:03:34] same amount of area. Or what you can do
[4:03:36] is selected shift G select similar
[4:03:38] normal. And since all the normals for
[4:03:41] this are pointing down, it's going to
[4:03:43] select all the other things we are in
[4:03:45] edit mode with the normal pointing the
[4:03:46] same direction. So now I can just hit X
[4:03:48] and delete those faces. And you can see
[4:03:50] it deleted all those bottom faces for
[4:03:51] us. That way we don't have to waste our
[4:03:53] time, you know, going into bottom
[4:03:54] orthographic and then selecting all them
[4:03:56] with box select and then deleting them
[4:03:57] or worst case holding shift and
[4:03:59] selecting each one of them. Now
[4:04:01] definitely, you know, utilize snapping
[4:04:02] when you're moving things out of things.
[4:04:04] That way it'll just speed up your
[4:04:05] workflow as well. Another really handy
[4:04:07] trick is to bulk rename things. So you
[4:04:10] can see that oh I accidentally select
[4:04:12] those. You can see we have a bunch of
[4:04:14] sticky notes here and they're all named
[4:04:15] like planes. So what we can do instead
[4:04:17] of just hitting F2 which will name the
[4:04:19] active object we can do Ctrl F2 and this
[4:04:21] will bring up this thing called batch
[4:04:23] rename. And in batch name out of the
[4:04:25] selected objects that we have not the
[4:04:26] all the objects just the selected
[4:04:28] objects that we have. We can use a
[4:04:30] regular expression. You can toggle it on
[4:04:31] and off here. Find everything that fits
[4:04:33] that regular expression and replace it
[4:04:35] with a new name. So here what I'm doing
[4:04:37] is anything that starts with plain dot
[4:04:39] right plain dot and then you know any
[4:04:41] number after it find that and then
[4:04:43] replace it with sticky note. So when I
[4:04:44] hit okay you can see that everything is
[4:04:46] now called sticky note and then it just
[4:04:48] automatically increments with the
[4:04:50] default blender setting there 01. Now if
[4:04:52] you don't like the 0001 now you can do
[4:04:55] Ctrl+ F2 again and go back to selected
[4:04:58] and then this time you can find 0 and
[4:05:01] then replace it with underscore instead.
[4:05:04] So if I hit okay now you can have sticky
[4:05:06] note_1_2.
[4:05:08] I'm sure there's a regular expression
[4:05:10] where you don't have to do it a second
[4:05:11] time and it'll just automatically
[4:05:12] increment in this format. Um but I'm not
[4:05:15] aware of it at this specific moment.
[4:05:16] Either way, I like this naming
[4:05:18] convention better because in 3GS, if you
[4:05:20] have like a space, let's say this like
[4:05:22] sticky note one, for example, when you
[4:05:25] log out this mesh in the GB file, it's
[4:05:28] going to have underscores automatically
[4:05:31] added to it. So, that's why I just add
[4:05:33] underscores here anyway. What about
[4:05:35] capitalization? Uh, that doesn't really
[4:05:37] have any significance for us. I just
[4:05:38] leave it capitalized because Blender
[4:05:41] leaves their mesh name capitalized. But
[4:05:43] honestly, if you want to leave it lower
[4:05:44] case and you prefer that, like totally
[4:05:46] go for it. Another really cool tip and
[4:05:48] trick that you can use is just holding
[4:05:49] control or command and using your middle
[4:05:51] mouse button to switch between settings.
[4:05:53] Remember when we were changing this, we
[4:05:55] would click on it and change it. You can
[4:05:56] actually just hold control and use your
[4:05:58] middle mouse button and it'll go through
[4:06:00] those options for you. That way you
[4:06:02] don't have to, you know, open up the
[4:06:04] menu every single time. And this works
[4:06:05] for everything. So roughness, you can
[4:06:07] use your middle mouse button to go up
[4:06:09] and down, but when you hold control or
[4:06:10] command, you'll just increment by, I
[4:06:13] think, 0.1 on the roughness slider. Same
[4:06:16] thing here on the extrude, so on so
[4:06:18] forth, and so on so forth. So I guess
[4:06:20] another I would just generally show you
[4:06:22] how I would workflow when I'm quickly
[4:06:24] adding materials. I would like select
[4:06:27] all the objects that I want to share the
[4:06:28] same material. Like let's say these all
[4:06:30] share the same material. Then I'll shift
[4:06:32] select this, Ctrl L, and link materials.
[4:06:35] Then I would go into edit mode and just
[4:06:37] hit a U unwrap and smart UV project just
[4:06:40] to make sure everything looks good. And
[4:06:42] if it doesn't, then I would select one
[4:06:43] of these and either duplicate it because
[4:06:46] again it's no longer float plank and
[4:06:48] then adjust the mapping node or I just
[4:06:50] come in here and adjust the UV
[4:06:51] accordingly. Like so. Of course, if you
[4:06:53] want one of these to be 90 and the other
[4:06:55] one to be 180, you can totally do that
[4:06:56] as well. Really quick, you can just link
[4:06:58] materials, adjust them how you need,
[4:06:59] unwrap how you need. I'll say just from
[4:07:02] experience, you shouldn't have too much
[4:07:03] issues with the basic UV unwrap. But if
[4:07:06] you have to, you know, definitely mark
[4:07:07] seams and try and go from there when you
[4:07:09] unwrap. Also, make sure before you
[4:07:11] unwrap to apply your scale. I just have
[4:07:13] a habit of always applying my scale.
[4:07:15] Even though we already did that, I kind
[4:07:17] of do it just in case I accidentally
[4:07:19] touch something. It's not a big deal if
[4:07:20] you unwrapped with a messed up scale
[4:07:22] because you can always just apply your
[4:07:23] scale and unwrap again. Okay, so let's
[4:07:25] create our first procedural material.
[4:07:27] Right now, this is just a flat color
[4:07:29] with, you know, a decently high
[4:07:31] roughness, and it looks fine. It looks
[4:07:32] pretty good, actually. But what if we
[4:07:34] want to add a little bit more spice to
[4:07:36] this? Well, we could do that with a
[4:07:37] color ramp, right? So, if we add a color
[4:07:39] ramp here, and let's say we, I don't
[4:07:42] know, make it Let's say we just make it
[4:07:44] this color right here. And then this,
[4:07:46] and this color, we can just click on it
[4:07:47] and make it this color, except let's
[4:07:49] make it, you know, a little bit blue,
[4:07:52] kind of like or purple, kind of like
[4:07:53] that. And then I'll hook it up and place
[4:07:55] it in here. But again, it's still a flat
[4:07:57] color. It's picking a color in between
[4:07:59] because it's set at 0.5. You can see as
[4:08:01] I go here, it's going to be this color.
[4:08:03] And if I go here, it's going to be that
[4:08:04] color. What we need is another sort of
[4:08:07] texture, right? We used a noise texture
[4:08:08] earlier. So now there's also this thing
[4:08:10] called a gradient texture. And I'm just
[4:08:12] telling you this stuff, but you know,
[4:08:14] over time you'll discover the built-in
[4:08:16] stuff that you can use to create your
[4:08:17] things. So now I can just take the
[4:08:19] factory channel of the gradient texture
[4:08:21] and plug it in here. But let's preview
[4:08:23] it first. You can see this is what the
[4:08:25] gradient texture looks like. It goes
[4:08:27] from black to white linearly. And you
[4:08:29] can see that you have multiple options
[4:08:31] here. Again, we can use our control to
[4:08:33] go in between them. That changes how the
[4:08:34] gradient looks. So everywhere that is
[4:08:37] black is going to be this pinkish color.
[4:08:39] And everywhere is white is going to be
[4:08:40] closer to this purplish bluish color. So
[4:08:43] if I take the factor here, plug it in
[4:08:45] here, then I control shiftclick
[4:08:48] principled BSDF, that's exactly what we
[4:08:50] see. All the darker areas or the areas
[4:08:53] closer to black are this color whereas
[4:08:56] all the areas that are white are closer
[4:08:57] to this color. And now we kind of get
[4:08:59] some variety already. Now what if we
[4:09:01] want to control you know where the
[4:09:03] gradient is on the mesh. Well again we
[4:09:05] do ctrt with node wrangler and we have a
[4:09:08] texture coordinate node and a mapping
[4:09:10] node that we can adjust. So now let me
[4:09:11] just go back to material preview because
[4:09:13] it'll be easier to see. But look what
[4:09:15] happens. Uh let's also just preview the
[4:09:16] gradient texture here. Look what happens
[4:09:19] when I change something like the Y
[4:09:21] location. So now we have something like
[4:09:23] that. So let's go back into rendered
[4:09:25] view real quick and go back to the
[4:09:27] principal BSDF. And you can see now over
[4:09:29] here is all blue. Wow. How cool is that?
[4:09:31] So you you'll also notice this time we
[4:09:33] didn't use the UV for the texture
[4:09:35] coordinate. We used generated. So as I
[4:09:38] cycle through this with control shift
[4:09:39] and leftclick, it's like what am I even
[4:09:41] looking at? So, if you want to know
[4:09:43] that, uh, you can take a look at the
[4:09:44] Blender documentation for a little bit
[4:09:46] more detail here on the differences
[4:09:48] between the texture coordinate system.
[4:09:50] This is a little bit getting into the
[4:09:52] weeds, so I'm not going to be diving
[4:09:54] into here, but for us, you know,
[4:09:55] generated works perfectly fine. So, you
[4:09:57] know, for now, this is not something you
[4:10:00] really have to worry about. Cool. So, we
[4:10:02] actually made our first procedural
[4:10:03] texture. That's really, really cool.
[4:10:05] Okay, but what if we want different
[4:10:07] patterns? You know, not just a gradient
[4:10:09] texture. What if we want like other
[4:10:10] patterns in in in our scene? It doesn't
[4:10:13] seem like we really have any more inputs
[4:10:15] here to place there, right? So, that's
[4:10:17] where this thing comes comes in called a
[4:10:19] mix color node. There's a lot of other
[4:10:22] sort of mix mix nodes on here, but we're
[4:10:24] going for the mix color because we're
[4:10:26] working with colors. So, let's select
[4:10:27] these. Uh, sorry, this is kind of close
[4:10:29] to this one for some reason. If we
[4:10:31] duplicate this with shift D and we plug
[4:10:34] this in here and we plug this one in
[4:10:37] here and then plug this into the base
[4:10:39] color, we're not going to see much yet.
[4:10:41] So, let's change this to something else
[4:10:43] like uh green. And let's change this to
[4:10:46] like, I don't know, orange or something
[4:10:48] like so. And let's change this Y value a
[4:10:51] little bit. And now you can see it's
[4:10:54] probably over there. the whiter areas of
[4:10:56] this color are mixing to each other with
[4:11:00] the lighter areas of this color, which
[4:11:02] is why we don't get completely green and
[4:11:04] we don't get completely pink. Because
[4:11:05] right now what we have is they're mixing
[4:11:08] together. So we're seeing 50% of this
[4:11:11] color at the grayscale value of that
[4:11:14] color specifically and 50% of the color
[4:11:17] that's being sampled at that grayscale
[4:11:18] value along this. So you can see if I
[4:11:21] change this to one, it's going to go for
[4:11:23] this one. It's going to take this whole
[4:11:25] thing. And if I go for this one, it's
[4:11:27] going to go back. If I turn this to
[4:11:28] zero, it's going to take 100% of this
[4:11:32] color instead. So here you can see, you
[4:11:34] can see if it was just this by itself,
[4:11:36] which I can just prove right now, it
[4:11:38] would look exactly the same. Cool. Okay.
[4:11:41] So, let me actually just replace this
[4:11:43] with like a noise texture real quick.
[4:11:44] That way we kind of have something
[4:11:46] easier just to see. So, let me put it in
[4:11:48] there. Let me delete this and click this
[4:11:50] like here. And uh let's just temporarily
[4:11:54] change this to one. Let's make these
[4:11:56] colors a little more distinct. So this
[4:11:57] green will be extremely green and like
[4:11:59] kind of dark. And let's also bring them
[4:12:01] up kind of like this. So they're really
[4:12:03] really close to each other. So now we
[4:12:06] have something that looks really really
[4:12:07] funky. So let's change this back to 0.5.
[4:12:11] Now in this case we get something but
[4:12:13] everything seems to be a little quote
[4:12:15] unquote faded and not as realistic. And
[4:12:18] why is that? Well, that's because we're
[4:12:20] linearly interpolating between two
[4:12:22] colors. They're mixing between each
[4:12:24] other. If we What if we add colors?
[4:12:27] Well, now it becomes even brighter.
[4:12:28] Well, you can imagine now what we're
[4:12:30] doing is like taking two different
[4:12:32] colored flashlights and pointing them in
[4:12:35] the same area. No matter what color the
[4:12:37] flashlights are, that area is going to
[4:12:38] be brighter. So, that's why when adding
[4:12:40] colors, we get this brighter effect. So,
[4:12:42] typically when we're adding two
[4:12:44] different patterns together, what we
[4:12:45] actually want to do is multiply. And
[4:12:47] this is more realistic to how light is.
[4:12:49] So if I go back to mix, you can see it's
[4:12:51] a little bright. If I go to multiply,
[4:12:53] it's a little more dark. And if I go to
[4:12:55] add, it becomes significantly higher. So
[4:12:57] if you remember from my previous video
[4:13:00] when we talked about colors, there's
[4:13:01] different ways to resemble colors,
[4:13:02] right? You can go from 0 to 255 or you
[4:13:05] can have hexadimal or you can have a
[4:13:08] float value between 0 and one. So if you
[4:13:10] have a float value of 0ero to one and
[4:13:13] like three channels are GB which mix
[4:13:16] together to make other colors that means
[4:13:18] the higher amount of one you have the
[4:13:19] more reds you have in your image. So if
[4:13:22] you wanted a completely red image this
[4:13:24] would be 1 zero and zero. All right so
[4:13:26] let's go back in Blender just to take
[4:13:28] out all the noise all the extra stuff
[4:13:30] here. And let's just do that right now.
[4:13:32] So let's also select one of these. Oh,
[4:13:34] by the way, if you want, you can add
[4:13:36] like different nodes here as well to
[4:13:38] adjust the gradient sort of thing. But
[4:13:40] you can also subtract one. So, I'm going
[4:13:42] to get rid of one of them. And I'm
[4:13:43] literally just going to make this
[4:13:45] completely red. And for this one, I'm
[4:13:47] going to get rid of one of these. And
[4:13:51] I'll just make it completely green. And
[4:13:52] I'll make this green like a light green.
[4:13:55] So, right now, uh, we're on add. Let me
[4:13:58] go back to mix real quick. Right now,
[4:14:00] what we're getting is a mix between 50%
[4:14:03] of red and 50% of green. So, if I were
[4:14:07] to duplicate this, let me just duplicate
[4:14:09] this real quick and add another one here
[4:14:12] like so. And make this other side one uh
[4:14:17] the color of our red. So, let's come
[4:14:18] here and just pick the eyropper tool and
[4:14:20] pick that red color. You can see right
[4:14:22] in the center is the exact same color
[4:14:24] that we're getting right here. Some
[4:14:26] yellowish orang-ish color, right?
[4:14:29] Because what we're doing is we're
[4:14:30] linearly interpolating between the two
[4:14:32] colors which again are represented using
[4:14:35] zeros and ones which is why this factors
[4:14:38] between zero and one. So mix is linearly
[4:14:40] interpolating between the colors which
[4:14:42] again colors are just mathematical
[4:14:44] numbers to tell computers how to make
[4:14:46] colors pretty much. So if you can
[4:14:48] imagine uh we have our red color here
[4:14:51] and we have our green color here. So
[4:14:53] let's just imagine it's 0 1 0. It's
[4:14:55] obviously not but let's just assume it
[4:14:57] is. What we're doing as we change the
[4:14:59] factory slider in this case is we're
[4:15:02] going like let's say we move it like one
[4:15:05] nudge then what we get is red would be
[4:15:08] like I don't know 0.9 and then green
[4:15:11] would become like 0.1 right and then we
[4:15:14] move another tiny nudge red would become
[4:15:16] 0.8 and then green would become 0.2 two.
[4:15:20] So this is going to be our final color.
[4:15:22] So if we move it halfway center, we
[4:15:24] would get 0.5 red, 0.5 green, and that's
[4:15:27] why we get the mix that we do. So this
[4:15:29] would be our final output color. Now,
[4:15:30] how does that change if we do add, for
[4:15:32] example, if we do add our colors
[4:15:34] together? If we add our colors, why is
[4:15:36] this suddenly completely like bright
[4:15:38] orange? Let's say again we have our two
[4:15:40] colors, our pure red color and our pure
[4:15:42] green color. What AD does it linearly
[4:15:45] interpolates like the mix one but except
[4:15:48] instead of going between two colors it
[4:15:50] will take a I don't know vector outcome
[4:15:52] and interpolate between your initial one
[4:15:54] which is going to be the A channel and
[4:15:56] your final output. So since we're doing
[4:15:58] an addition operator we're going to be
[4:16:00] adding vectors together. And if you
[4:16:02] remember from like middle school or high
[4:16:04] school to add vectors you take the X the
[4:16:06] Y and the Z. In this case the separate
[4:16:08] channels RG and B. So 1 + 0 is 1. 0 + 1
[4:16:12] is 1. 0 + 0 is 0. So this is the final
[4:16:14] vector. So what we're interpolating
[4:16:16] between is this vector and our initial
[4:16:20] vector which is just red like so. So
[4:16:23] imagine if we have 0.5. What we can
[4:16:26] expect is 1 comma 0.5 comma 0. Why does
[4:16:31] this make sense? Well, we can't linearly
[4:16:34] interpolate between 1 and 1 because
[4:16:36] they're the same value. Same with 0 and
[4:16:38] 0. However, from 0 to 1, we have all the
[4:16:40] values between 0 and 1 to interpolate.
[4:16:43] So, if we change this to 0.6, we can
[4:16:45] imagine that this would also be 0.6. 1
[4:16:48] comma 0.6 comma 0. So, here you can see
[4:16:51] well, this uses between 0 and 255, but I
[4:16:54] just scaled it up. So, this is 1, right?
[4:16:57] This is 255 out of 255, which is 1. And
[4:16:59] then this is about 0.5 of 225, which is
[4:17:03] 127.5, but it just rounded up. And you
[4:17:06] can see what we get is we get orange,
[4:17:08] which is exactly what we see here. All
[4:17:10] right. So now what if we change from add
[4:17:13] to multiply? Why is it red at 0.5? Why
[4:17:17] is it our original color at zero? And
[4:17:20] why at one is it completely black? Well,
[4:17:22] if we do this again, but this time we
[4:17:25] multiply vectors. So here's our red
[4:17:26] color. Here's our green color. This time
[4:17:29] we're multiplying vectors. Same thing
[4:17:31] like addition, we take their separate
[4:17:33] components. So 1 * 0 is 0. 0 * 1 is 0. 0
[4:17:38] * 0 is also 0. So this is our resulting
[4:17:41] vector which means we're going from this
[4:17:43] our red vector and linearly
[4:17:45] interpolating to 0 comma 0 comma 0. So
[4:17:48] that means when we move our factor
[4:17:50] slider to 0.9 what we're doing is going
[4:17:52] from one getting closer to zero. So we
[4:17:55] can expect our outcome to be 0.1
[4:17:58] comma 0 comma 0. And since this is so
[4:18:01] close to black, that's why we're getting
[4:18:03] closer and closer to black until we
[4:18:06] increase our factor to one. And then of
[4:18:08] course, if our factor is zero, that
[4:18:10] means we're at the our starting point,
[4:18:11] our starting vector right here. So you
[4:18:13] can see that's exactly why when we go
[4:18:15] here, it's completely red, our original
[4:18:17] color. And when we go here, it's
[4:18:19] completely black. Okay. So what if we
[4:18:22] multiply the same color by each other?
[4:18:24] Then we should expect no interpolation
[4:18:26] at all, right? Because 1 comma 0 comma 0
[4:18:29] * 1 comma 0 comma 0 is just 1 comma 0
[4:18:34] comma 0. There's no value between our
[4:18:36] starting vector 1 and 1, 0 and 0 0 and 0
[4:18:39] to interpolate between. So no matter
[4:18:41] where we adjust our factor slider, it
[4:18:43] should stay the same exact color. So I
[4:18:45] can prove that by duplicating this and
[4:18:48] hooking it up into the factory slider
[4:18:50] and adjusting the factory slider. Now
[4:18:52] what we do see is that it gets slightly
[4:18:54] darker. So how does this make sense?
[4:18:56] Well, if I click on this, it's not
[4:18:58] actually completely red. You can see
[4:19:00] there's a little bit of blue and 0.776
[4:19:03] of red. There's no green, though. What
[4:19:05] that means is that our starting color is
[4:19:07] 0.7. I completely forgot already. And
[4:19:10] then this was like 0.01.
[4:19:13] So, our starting vector multiplied by
[4:19:16] our ending vector, which is just happens
[4:19:18] to be the same thing, right? 0.01. Well,
[4:19:22] when you multiply decimals together or
[4:19:24] fractions together, you get something
[4:19:25] even smaller, right? So 0 I don't know,
[4:19:28] this is probably around like 58 or
[4:19:30] something. So you get 0.58. I don't know
[4:19:33] if that's accurate. Then 0 * 0 is 0. And
[4:19:35] then this you just add two zeros. So 01.
[4:19:38] So again, this is closer to 0, which is
[4:19:40] closer to black, the black color, right?
[4:19:43] Anyway, to really drive that point home,
[4:19:45] I can just show you if I change this to
[4:19:46] one and change this to zero. And same
[4:19:49] here, I change this to one and change
[4:19:52] this to zero. And now I adjust my factor
[4:19:54] slider. You can see there's absolutely
[4:19:56] no difference on the color whatsoever.
[4:19:58] Obviously, there's a lot of other
[4:19:59] blending modes and things to do here,
[4:20:01] which you can find on the Blender
[4:20:03] documentation, which isn't great
[4:20:05] specifically on explaining these from
[4:20:08] what I remember. But I do remember there
[4:20:10] was a YouTuber that went into detail on
[4:20:12] every single node and the math behind
[4:20:14] each node. So, if you really want to get
[4:20:16] into the nitty-gritty details, I'll make
[4:20:18] sure to link that if I remember it. It
[4:20:21] was like a really small video and it
[4:20:23] wasn't popular, so I kind of forgot
[4:20:24] about it, but uh it's definitely
[4:20:26] something that I wanted to watch myself.
[4:20:28] I think for most 3D artists, it's kind
[4:20:30] of a combination between intuition and
[4:20:32] mathematics knowledge. Obviously, some
[4:20:34] 3D artists are going to be more math
[4:20:36] heavy than others, but to me, I kind of
[4:20:38] want to know the math behind things
[4:20:40] because these concepts are transferring
[4:20:42] into other software like Photoshop, and
[4:20:44] it also transfers intuitively to when
[4:20:47] you're programming with shaders and
[4:20:49] things like that as well. I'm generally
[4:20:50] more on the math heavy side or at least
[4:20:52] trying to become more math heavy. You
[4:20:54] don't you don't really have to be good
[4:20:55] at math to be a 3D artist. you know, you
[4:20:58] can stick with the conventional
[4:20:59] texturing methods and developing your
[4:21:01] intuition over time. Watching other 3D
[4:21:03] artists make their materials kind of
[4:21:06] helps build you a nice intuition and you
[4:21:08] don't really have to know the math
[4:21:10] behind things. So, for us, you know, I
[4:21:12] didn't really have to explain all the
[4:21:13] vector math at all and we could have
[4:21:15] probably got a good result just you
[4:21:16] using my first explanation about mixing
[4:21:19] and adding and that sort of stuff, but I
[4:21:21] kind of just wanted to talk about a
[4:21:23] little bit about the math behind the
[4:21:24] scenes there. So why don't we just have
[4:21:26] some fun and explore another procedural
[4:21:28] material. So if I do search for our mix
[4:21:30] color node like we had earlier. Right
[4:21:33] now it's just going to be between these
[4:21:34] two gray values. So let's add a color
[4:21:35] ramp node like so. And let's just take
[4:21:41] this right here and let's just sample it
[4:21:43] from our base color. And I'm just going
[4:21:45] to get rid of this for now. And then we
[4:21:47] can just hook it up here. And then hook
[4:21:49] this up just like that. Cool. So we're
[4:21:52] mixing between this pink and this right
[4:21:54] here. If I hit mute, you can see it's
[4:21:57] going to go back to that original paint
[4:21:58] color. Cool. Let's change this mix to
[4:22:01] multiply, which we discussed earlier.
[4:22:04] And let's duplicate this color ramp. But
[4:22:06] let's add another color here. And maybe
[4:22:08] let's change this to some arbitrarily
[4:22:11] completely different color like orange
[4:22:13] or brown. And then this one can be like,
[4:22:15] I don't know, green or yellow or
[4:22:17] something like that. And then let's just
[4:22:20] plug that in there. So again, you know,
[4:22:23] if you wanted to, you could come to
[4:22:25] these color nodes, open them up, look at
[4:22:27] the values, and do the multip
[4:22:29] multiplication calculation. And then you
[4:22:32] can see what values this would be
[4:22:34] interpolating between. So if you want
[4:22:36] to, you can totally do that. Now, what
[4:22:38] if I want to, you know, have some sort
[4:22:40] of pattern, not just flat color? Well,
[4:22:42] we know how to do that, right? We can
[4:22:44] add like something like a noise texture.
[4:22:46] And there's other textures that you can
[4:22:48] explore as well. take that pl plug it in
[4:22:51] here. It's going to be randomly sampling
[4:22:52] from here. So, if I hit control shift t,
[4:22:55] you can see this is what we're getting.
[4:22:57] Now, you might be saying, okay, this
[4:22:58] looks really cool, right? But how come
[4:23:01] it's only, you know, how come it's only
[4:23:03] very very gray, right? There's no really
[4:23:06] solid blacks or solid whites. How do I
[4:23:09] fix that? How do I change that? Well,
[4:23:11] you actually can change that with a
[4:23:12] color ramp node. Again, remember we have
[4:23:15] these black and white grayscale values
[4:23:17] that are sampling between 0 and one from
[4:23:19] this. So, what if we sample from here
[4:23:21] first and based on this sample size,
[4:23:23] we're resampling to this color ramp
[4:23:26] node. So, if I plug it in here and let
[4:23:28] me mute this, you can see nothing
[4:23:29] changes. But watch what happens when I
[4:23:31] increase the blacks. You can see there's
[4:23:33] now going to be an increasing amount of
[4:23:35] black places until, you know, it hits
[4:23:39] 100%. Okay, so I'm going to put this at
[4:23:41] like 0.2. two and I reset this one. And
[4:23:45] then I'm going to put this at like 0.8.
[4:23:48] So we know that the noise texture here
[4:23:50] is generating values between 0 and 1. I
[4:23:53] think when we previewed it, it's likely
[4:23:55] not 0 to 1. It's probably like 0.2 to
[4:23:57] like 0.6 or something like that. But
[4:24:00] anyway, just assume that it's 0 to one
[4:24:02] because I think technically it is random
[4:24:05] values between 0 and one. These random
[4:24:06] values kind of follow a specific formula
[4:24:09] which we know as a noise texture. So
[4:24:12] assume it generates a value of 0.9
[4:24:16] without this color ramp node in the
[4:24:18] picture. We would just come over here,
[4:24:20] right? And then pick the color at 0.9.
[4:24:22] So whatever color this is of that
[4:24:24] grayscale value of 0.9, it's going to
[4:24:26] show this color on on that object. Now
[4:24:28] what happens with this color ramp in the
[4:24:30] mix? Well, let's say it generates 0.9.
[4:24:33] 0.9 is now going to go here. And what we
[4:24:36] get is completely white because this is
[4:24:38] completely white. So it's just saying
[4:24:40] all the values above 0.8 just make it
[4:24:42] white. So what it returns is a value of
[4:24:45] one and then we take that value of one
[4:24:48] and then we sample at this value of one.
[4:24:51] If the noise texture generates 0.9, what
[4:24:53] we would expect is this color. But now
[4:24:55] that we add this color ramp node and
[4:24:57] then move this down here, what we get is
[4:24:59] an output of one and in this factor that
[4:25:02] means we get this color showing up at
[4:25:04] that model. So that's pretty cool and
[4:25:05] that's exactly why we get the effect
[4:25:07] that we do. So here you can see I'm
[4:25:09] either sampling between this color or
[4:25:11] this color. And then here I'm
[4:25:13] determining how much it is. So if you
[4:25:15] think about it, this is essentially
[4:25:16] controlling, you know, how smooth the
[4:25:18] blend is, right? So you have either this
[4:25:21] color or either this color, right? As I
[4:25:25] bring them closer, it's like this color
[4:25:26] or this color like I talked about
[4:25:28] earlier. And here it's determining how
[4:25:30] much of each color you have, right? So
[4:25:32] if I increase this, you can see it's
[4:25:34] going to increase that. If you I
[4:25:35] increase this, it's going to increase
[4:25:37] the other color. However, you know,
[4:25:39] again, if I leave this really really
[4:25:41] spread out, it's going to be really
[4:25:42] smooth interpolation. But here again, if
[4:25:46] I increase this, it's going to increase
[4:25:47] one that color. If I increase this, it's
[4:25:50] going to increase this other color here.
[4:25:52] So basically, you have one that's
[4:25:54] determining how much amount of color you
[4:25:56] have in one or the other. And then you
[4:25:58] have another one that's determining how
[4:26:00] smooth and harsh harsh the blend is.
[4:26:02] Okay. So, let's go back to our principal
[4:26:04] BSDF and let's see if we can see
[4:26:07] something by probably increasing the
[4:26:09] colors a little bit and probably uh
[4:26:11] increasing the scale a little bit. And
[4:26:13] now you can see we can start seeing
[4:26:14] something. So, we already start seeing
[4:26:16] something, but let's just adjust the
[4:26:18] scale even more. Let's make it really
[4:26:20] big. And now we can have like this sort
[4:26:22] of wall texture pattern here. And it
[4:26:25] looks a little bit more visually
[4:26:26] interesting than just a flat color. And
[4:26:28] then you have all these other options
[4:26:30] that you can play with like distortion.
[4:26:32] You know, you can play around with the
[4:26:34] scale. What happens if the scale is like
[4:26:36] this, for example? It almost looks like
[4:26:39] some sort of mystical dungeon dragon
[4:26:42] sort of thing, right? And now, of
[4:26:44] course, what you can also do is use your
[4:26:48] information from your color ramp to
[4:26:50] determine how rough it is at certain
[4:26:52] areas. So, if I take this color and plug
[4:26:55] it into the roughness, everywhere that's
[4:26:58] going to be more black is going to be
[4:27:00] less rough, and everywhere that's more
[4:27:02] white is going to be more rough. So, you
[4:27:04] can see if I preview this, take a look
[4:27:07] at the black areas. They're going to be
[4:27:09] more shiny than the rough areas. So, if
[4:27:11] I go back here and principal BSDF, you
[4:27:14] can see that this black area, these
[4:27:17] black areas are reflecting the light.
[4:27:19] Really, really simple. whereas all the
[4:27:21] whiter areas are a lot more rough and
[4:27:23] not as reflective. So you kind of
[4:27:25] already get a pretty cool effect here.
[4:27:27] Now what if you want to invert it? You
[4:27:28] know what if you want the white areas to
[4:27:30] be shiny and the black areas to be
[4:27:32] rough? Well, you can do that, right? You
[4:27:33] can just duplicate the color ramp node
[4:27:35] and place it here again. And to invert
[4:27:37] it, you just do this, right?
[4:27:41] You just flip it. Now you can see all
[4:27:43] the white areas are really shiny and all
[4:27:45] the black areas are really rough. Well,
[4:27:47] what if you want to increase the amount
[4:27:49] of shiny areas? Well, you would just
[4:27:50] increase the black values, right? Like
[4:27:53] so. And now you can see that the
[4:27:56] majority of the model is really, really
[4:27:58] shiny and glossy. Yeah. So, the point
[4:28:00] that I'm trying to make is you can just
[4:28:03] play around with things and honestly
[4:28:05] just have fun. And you might actually
[4:28:07] create some really cool things that you
[4:28:09] never knew how to create before. And you
[4:28:11] might actually save it to use later,
[4:28:13] which is really, really awesome. Like
[4:28:14] here, you can see I kind of already have
[4:28:16] like a pinkish wall color, which is
[4:28:18] looking pretty sweet here. And all it
[4:28:19] was is some random noise texture I
[4:28:22] generated, some random color ramp I
[4:28:24] moved and some random colors that I
[4:28:26] chose. Over time, you know, as you
[4:28:28] experiment, as you have fun, you're
[4:28:30] going to develop your intuition. Even if
[4:28:31] you don't understand the math behind it,
[4:28:33] you'll develop your intuition on how to
[4:28:35] create cool stuff. So, I encourage you
[4:28:37] just to take the time to like shift a
[4:28:39] search, search for like textures, plug
[4:28:42] in random stuff like, okay, wave
[4:28:44] texture, that looks pretty cool. But
[4:28:46] what does that look like if I use this
[4:28:48] instead? What if I control shift? What
[4:28:50] does that look like? Oh, it kind of
[4:28:52] looks like that. That's pretty cool. And
[4:28:53] now you can see we kind of have like a
[4:28:55] like a more cozy house sort of vibe. And
[4:28:58] then of course we can do the same thing
[4:28:59] for the roughness here. And you can see
[4:29:01] all the wider areas are more reflective
[4:29:03] than the other ones. What if I want to,
[4:29:05] you know, take the noise texture, its
[4:29:07] factor, and change the distortion of
[4:29:10] those lines based on the noise. What if
[4:29:12] I want to change its scale based on the
[4:29:14] noise? What are we getting there? Let me
[4:29:16] control shift. Wow, now that looks
[4:29:18] really, really crazy. What if I add What
[4:29:22] if I get rid of these and hit CtrlT with
[4:29:24] no wrangler and adjust the rotation of
[4:29:26] this texture? Wow. What about the Z
[4:29:28] direction? What about the scale? Now,
[4:29:31] let me go back to my principal BSDF.
[4:29:33] What does that do? Wow, it looks like a
[4:29:36] bunch of lines patterns. And now you can
[4:29:38] see that wow, we only have one face
[4:29:41] here, but it looks like we have a
[4:29:42] striped pattern here. I really encourage
[4:29:44] you just to have fun and explore things.
[4:29:46] And when you're ready to go online and
[4:29:49] search for other procedural tutorials
[4:29:51] out there, because there's a lot of them
[4:29:52] out there, I do encourage you to have
[4:29:55] some fun first. Okay, so let's create
[4:29:57] our first procedural material together
[4:29:58] that I'm actually going to be using for
[4:30:00] this project. And it'll be a wall
[4:30:02] texture. Although we're creating a room,
[4:30:03] I kind of also want to go for a wall. So
[4:30:05] I was looking up random images of old
[4:30:08] agent houses. And just by observing it,
[4:30:10] you know, like any other big problem,
[4:30:12] you want to take your large problem,
[4:30:14] which in this case is creating a wall
[4:30:16] texture, and then break it down into its
[4:30:18] smaller parts. So just by observing it,
[4:30:20] we kind of see some cracks here. And I
[4:30:22] guess the image isn't that good, but
[4:30:24] there's definitely some cracks here that
[4:30:25] you can see, similar with over here.
[4:30:29] And at the bottom here, it's generally a
[4:30:31] little more darker and kind of like
[4:30:33] fades up and gets a little bit more
[4:30:35] clear uh you know in the center here.
[4:30:36] And that makes sense because a lot of
[4:30:38] objects are smaller like this wheel or
[4:30:39] whatever this thing here and it's going
[4:30:41] to like hit the wall and scrap off
[4:30:43] paint. There might be flooding. People
[4:30:45] might accidentally kick the side. You
[4:30:46] know, people might kick up dirt on the
[4:30:48] side and so on so forth. So, it kind of
[4:30:50] makes sense that the bottom would be a
[4:30:51] little bit darker. So, we kind of have
[4:30:53] three areas. We need some sort of noise
[4:30:55] texture for the cracks. And then we need
[4:30:57] some sort of like gradient texture where
[4:30:59] the bottom is darker. And then of course
[4:31:01] we need our base color. So I encourage
[4:31:03] you to pause the video and try and give
[4:31:05] yourself some time to figure out how to
[4:31:07] make the room texture with the blended
[4:31:09] noise texture with the bottom to be a
[4:31:11] little bit darker and then when you try
[4:31:13] come back to the video. Okay. So the
[4:31:15] first thing we need is definitely a
[4:31:16] color ramp node because that's how we
[4:31:18] get multiple colors, right? So let's do
[4:31:20] color ramp. And for this color, we can
[4:31:23] just arbitrarily send it to here. And
[4:31:25] for this color, let's just set it at
[4:31:27] something like purple. And then let's
[4:31:29] add one more in the center. And let's
[4:31:31] just make that like bluish. And let's
[4:31:33] just plug in the color for this color.
[4:31:35] Now again, we're just sampling from the
[4:31:37] center right here. Which is why we only
[4:31:39] see a flat solid color. So if we want to
[4:31:42] make random samples at different
[4:31:43] grayscale values between 0 and one,
[4:31:45] right? We can use a texture that's based
[4:31:48] on some mathematical formula that
[4:31:50] someone developed. So again, if you
[4:31:52] search texture, you have a lot of
[4:31:53] different kinds of textures. We want a
[4:31:55] gradient texture. So let's search for a
[4:31:58] gradient texture. And let's just plug it
[4:32:00] in this right here. Again, you can
[4:32:02] preview it just like this. And you can
[4:32:03] see this is what the gradient texture
[4:32:05] looks like. Now, just to help visualize
[4:32:06] this a little bit easier, I'm going to
[4:32:08] go to material preview. And I'm also
[4:32:09] just going to add a cube and link the
[4:32:12] material just so we have the same
[4:32:14] material here. And you can see it's more
[4:32:15] visually clear what's happening. Now,
[4:32:17] you might be saying now like, "Andrew,
[4:32:19] we did something really cool, but how
[4:32:21] does that really help me at all? I don't
[4:32:23] understand what's happening and how you
[4:32:25] figured that out." So, let's take a
[4:32:26] brief look at the mathematics of what's
[4:32:29] happening behind the scenes because at
[4:32:31] the end of the day, everything is a
[4:32:32] little bit about math. By default, this
[4:32:34] gradient texture, it needs to know how
[4:32:36] to position itself along your object.
[4:32:39] So, in order to do that, we use
[4:32:41] directional vectors. So, you probably
[4:32:43] remember from like middle school or high
[4:32:45] school when we were working with vectors
[4:32:47] and trigonometry and linear algebra and
[4:32:49] that kind of stuff. By default, this
[4:32:50] gradient texture is using a vector
[4:32:52] that's pointing in the x-axis direction.
[4:32:54] So, let me just create that real quick.
[4:32:55] I'm going to shift duplicate right click
[4:32:57] cancel p by selection. Then I'm going to
[4:32:58] right click, set origin, origin to
[4:33:00] geometry, go into edit mode, extrude
[4:33:01] this out. E, right click, cancel, scale
[4:33:03] it up. E, and then just Well, that's
[4:33:06] like a really large vector, but anyway.
[4:33:08] So you can imagine by default our
[4:33:11] directional vector is 1 comma 0 comma 0.
[4:33:13] When you normalize vectors you pretty
[4:33:15] much just get a direction. We're
[4:33:16] interpolating between the direction. So
[4:33:19] 0 2 1, right? Which is exactly why
[4:33:22] across our cube here we're getting zero.
[4:33:25] We're sampling zero here. And then we're
[4:33:28] linearly interpolating all the samples
[4:33:29] to one. And then that's why we see this
[4:33:31] color over here. Cool. So what if we
[4:33:34] wanted it from to go from bottom to top
[4:33:37] like we said we did. Well, again, we can
[4:33:39] do CtrlT with node wrangler for a
[4:33:41] mapping node. And we can rotate it along
[4:33:43] the Y-axis 90°. And now you can see what
[4:33:46] happens. It goes from top to bottom. So
[4:33:48] when we rotate it 90° along the Y-axis,
[4:33:51] just like here, R Y. And I'll do 90.
[4:33:55] Take a look. Our directional vector is
[4:33:57] now pointing from the bottom to the top.
[4:33:59] So now that it's pointing from the
[4:34:01] bottom to the top, it essentially shares
[4:34:03] the same exact directional vector as a
[4:34:07] vector that's pointing up in the Z-axis
[4:34:09] direction. So now we're linearly
[4:34:11] interpolating between 0 and one in the
[4:34:14] Z-axis. And that's why this is happening
[4:34:16] here. So now this is the time to talk
[4:34:19] about texture coordinate systems. So for
[4:34:21] generated objects, it's going to be
[4:34:23] based on the object's local space, which
[4:34:26] means essentially take into your
[4:34:28] object's rotation to determine where it
[4:34:30] starts. That's exactly why on this
[4:34:31] object here, the bottom quote unquote
[4:34:34] bottom is this color and the quote
[4:34:37] unquote top and the left on this side is
[4:34:39] quote unquote this color. Actually,
[4:34:41] let's make these a little more distinct
[4:34:43] here. Again, if I rotate along the
[4:34:44] Y-axis, if I move it like this, you're
[4:34:46] like, "Oh, that's clearly the bottom."
[4:34:48] But now that it's like this, it's like,
[4:34:50] "Oh, that's clearly on the right side,
[4:34:52] right? Wasn't it just at the bottom?"
[4:34:54] So, in order to quote unquote fix this
[4:34:56] or adjust it, we can do control A and
[4:34:59] apply a rotation. And now you can see it
[4:35:02] follows the same exact pattern as this
[4:35:04] one right here. Okay. So, let's revisit
[4:35:05] the Blender documentation and take a
[4:35:08] look at what generated coordinates do.
[4:35:10] So, it says automatically generate
[4:35:11] texture coordinates based on the
[4:35:13] bounding box of the surface as a range
[4:35:16] from 0.0 0 to 1.0. So what is a bounding
[4:35:20] box? I mean we were you doing it when we
[4:35:22] were holding different items and scaling
[4:35:24] it like so. You know what is a bounding
[4:35:27] box? Well, you can imagine a bounding
[4:35:29] box is like if you drew a box around
[4:35:32] your object, what would it look like? So
[4:35:34] for for this thing right here, it
[4:35:37] doesn't look like a box, but if you were
[4:35:39] to draw a box around it, it would
[4:35:40] definitely look like a box. Same thing
[4:35:42] with here. If I move this over here and
[4:35:44] I scale this in, you can imagine that if
[4:35:47] we drew a box, it would be this length
[4:35:49] width uh you know up to to the width of
[4:35:53] this over here. Come over here. Come
[4:35:55] over here, you know, over here. So if I
[4:35:57] just draw that real quick. So from top
[4:35:59] view, the bounding box of selecting this
[4:36:02] would kind of look like this. So
[4:36:04] selecting this and this object would
[4:36:07] kind of look like that, right? So
[4:36:09] obviously it would start from down here
[4:36:11] but you know just like length and width
[4:36:13] wise that's kind of what it would look
[4:36:15] like. The bounding box you can just
[4:36:16] imagine it goes to this height and it
[4:36:18] goes to the bottom height there. So
[4:36:20] exact. So when you select one object
[4:36:22] then uh since this is a box well it's
[4:36:24] just the bounding box is going to look
[4:36:25] the same as this cube itself. We know
[4:36:27] that an object is made up of a bunch of
[4:36:30] points. Like we know there's vertices
[4:36:32] and we also call these points but like
[4:36:34] this entire face every single thing you
[4:36:36] see that makes up this face has a point
[4:36:39] because if there's no point on on this
[4:36:41] 3D surface then there would be like a
[4:36:43] hole or something cuz we need to take
[4:36:44] into that mathematical calculation. So
[4:36:46] we can imagine generated let's just
[4:36:48] assume this right here is the front of
[4:36:50] the cube. That means we can say this
[4:36:52] corner is 0 comma 0 comma 0. This right
[4:36:55] corner would be comma 1 comma 0 comma 0.
[4:36:59] Right? This corner would be 0 comma 1
[4:37:02] comma 0, right? It's in the positive y-
[4:37:05] axis as you can see up here. And then
[4:37:07] the one that we can't see back here, we
[4:37:09] can just say that's going to be 1 comma
[4:37:12] 1 comma 0. Now, all points in 3D space
[4:37:15] are actually technically vectors. This
[4:37:17] case from the object's local space
[4:37:19] origin point. Since we're using
[4:37:21] generated coordinates, the origin is
[4:37:22] going to start at one of the corners. So
[4:37:24] that means at this point here, we
[4:37:26] technically have a vector like this.
[4:37:28] Same thing with like a center piece over
[4:37:30] here. We can say that's probably 0.5 in
[4:37:32] the x 0.5x 0 0 in the y- ais direction
[4:37:36] and 0.5 in the z direction. So we would
[4:37:40] have like a vector like this. Now the
[4:37:42] reason we distinguish between points and
[4:37:44] vectors is because vectors are typically
[4:37:46] associated with like magnitude or like
[4:37:48] some sort of direction or velocity and
[4:37:50] things like that. Whereas points are
[4:37:51] usually just like absolute values that
[4:37:53] you have in space. So even though points
[4:37:55] are technically vectors, we still
[4:37:57] conceptually distinguish between points
[4:37:59] and vectors. Okay. So now that we know
[4:38:01] that our object is a bunch of points in
[4:38:04] 3D space, which ultimately determines,
[4:38:06] you know, the physical pixels on our
[4:38:07] screen, how to color something, how do
[4:38:09] we take into consideration these vectors
[4:38:11] given that we have a directional vector
[4:38:14] for our gradient? Well, if you remember
[4:38:16] from probably middle school or high
[4:38:17] school, you've dealt with this thing
[4:38:19] called the dot productduct before. And
[4:38:21] it basically tells us you know how how
[4:38:23] similar are two vectors in this case
[4:38:25] against Khan Academy is how much two
[4:38:27] vectors point in the same direction. So
[4:38:29] the dotproduct is actually exactly what
[4:38:31] Blender is doing behind the scenes. We
[4:38:33] have this directional vector and then
[4:38:35] these together we have our coordinate
[4:38:37] system or a point in 3D space that is
[4:38:40] also a vector that is taking the dot
[4:38:42] product times our gradient textures
[4:38:44] directional vector. So there's multiple
[4:38:46] formulas to calculate the dot
[4:38:48] productduct between two vectors. So I'll
[4:38:50] show you the most two common ways like
[4:38:53] which which is this which you saw on
[4:38:54] Khan Academy and then also like this a
[4:38:57] really common way of doing it. Here you
[4:38:58] can see these two symbols means the
[4:39:00] magnitude of a and the magnitude of b.
[4:39:03] In order to calculate the magnitude of a
[4:39:04] vector we square all its values. So
[4:39:06] 0.5^2 + 0 2 + 0.5^ squ and technically
[4:39:13] these should be in parenthesis. Oh well
[4:39:14] it doesn't really matter. And then we
[4:39:16] take the square root of that whole
[4:39:18] thing. So if you remember this is the
[4:39:20] magnitude but it's also just technically
[4:39:22] the distance formula if you want to find
[4:39:24] the distance between two points. So if
[4:39:26] we do this mathematical calculation is
[4:39:28] we get 0.25 here 0.25 0.25. So add 0.25
[4:39:34] plus 0.25 you get the<unk> of 0.5 which
[4:39:38] equals about.707.
[4:39:40] Now the magnitude of 0 comma 0 comma 1
[4:39:44] it would just be 0^ 2 + 0 2 which is 0 +
[4:39:48] 1^ 2 which is 1. So it's the square root
[4:39:50] of 1 which just equals 1. So we multiply
[4:39:53] this result by 1. So it just be 0.70
[4:39:56] right? And now like the formula says we
[4:39:58] take the cosine between the two vectors.
[4:40:00] So since our directional vector is
[4:40:02] completely up then then the value of
[4:40:03] theta or the angle between these two is
[4:40:06] just 45° right? And the cosine of 45°
[4:40:09] surprisingly is this exact value right
[4:40:12] here. And multiplying this value by the
[4:40:15] same exact value ends up getting 0.5.
[4:40:17] Now, why does that make sense? Well,
[4:40:19] we're taking the square root of 0.5,
[4:40:21] which is this. We're multiplying it by
[4:40:23] 1, so it's just the same thing. And then
[4:40:25] it just so happens that the cosine of
[4:40:27] 45° is also the square root of 0.5. So,
[4:40:31] in the end, we end up getting 0.5. And I
[4:40:33] can show you right here on this
[4:40:34] calculator, the cosine of 45° * the
[4:40:36] roo<unk> of 0.5 is just 0.5. So this
[4:40:39] resulting value 0.5 is going to be the
[4:40:43] quote unquote grayscale value to sample
[4:40:45] from our color ramp at this point in
[4:40:47] space on our mesh, which is exactly why
[4:40:50] right in the center right here we have
[4:40:52] this color. Now the other way to
[4:40:53] calculate the dot product might be
[4:40:55] easier here. So if we look at here, you
[4:40:57] basically just take the values, multiply
[4:40:59] them by together, x * x, y * y, z * z,
[4:41:02] and then add all the resulting values.
[4:41:05] So let's do that. We did multiplication
[4:41:07] earlier. 0.5 * 0 is going to be 0. 0 * 0
[4:41:12] is 0. So add these together. And then
[4:41:14] 0.5 * 1 is going to be 0.5. So what is
[4:41:18] our result? What is our result? Well,
[4:41:19] our result is 0.5, which is the same
[4:41:21] thing that we get here. And of course
[4:41:23] the same value that we're going to be
[4:41:25] sampling from our color ramp here. So
[4:41:26] you can confirm this with any point
[4:41:28] along our generated texture coordinate
[4:41:31] system taking the dot product to our
[4:41:34] gradient directional vector. Like for
[4:41:36] example this entire bottom why is it you
[4:41:38] know the value of zero? Why is it
[4:41:39] sampling here? If you take a look
[4:41:41] everything in the z direction which is
[4:41:43] our directional vector is zero and
[4:41:45] everything in our directional vector in
[4:41:47] the x and y is completely zero. So the
[4:41:49] result will always be 0 comma 0 comma 0.
[4:41:52] So if 0 0 is always the resulting
[4:41:54] formula, then we get 0 plus 0 plus 0.
[4:41:57] And what is that? Well, it's just 0,
[4:41:58] right? So that's why the entire bottom
[4:42:00] is the zero color here. Okay? So now we
[4:42:03] know how the gradient texture is
[4:42:04] working. So even if I have something
[4:42:06] like this, why does it show exactly what
[4:42:09] we kind of expect still? We can
[4:42:11] visualize that there's some sort of
[4:42:12] bounding box here for our generated
[4:42:14] coordinate system, right? So, it's kind
[4:42:16] of like this
[4:42:18] around our object. Okay. So, let's take
[4:42:21] a look at this. Why is this a completely
[4:42:24] different shape from a cube, but it's
[4:42:25] still working properly? Well, again,
[4:42:27] let's just assume that this corner is 0
[4:42:30] comma 0 comma 0. Well, let's take a
[4:42:33] place like here. Now, we can say that's
[4:42:35] probably like 0.5
[4:42:38] in the x direction, right? We're looking
[4:42:40] at the x direction here as slight angle.
[4:42:42] And then in the z direction, it's going
[4:42:44] to be 0.5. And then it's not completely
[4:42:46] to the end of the bounding box. It's a
[4:42:48] little bit in between, right? Because we
[4:42:49] have that little bit of thickness. So
[4:42:51] that would be like 0.9 or 0.8 or
[4:42:53] something like that. And then we have
[4:42:55] our directional vector again, which is 0
[4:42:57] comma 0 comma 1. So look what happens
[4:43:00] again if we multiply 0 0 + 0 0.5. In
[4:43:05] this case, the only thing that actually
[4:43:07] matters is the zcoordinate of that point
[4:43:10] in 3D space. So if I create a curve real
[4:43:12] quick uh just to simulate our you know
[4:43:15] our our vector and let me just shift
[4:43:18] right click shift s selection to cursor
[4:43:20] and uh let me just delete these
[4:43:21] vertices. So even though we have a
[4:43:23] vector that looks like this right the
[4:43:26] only thing that matters at the end of
[4:43:27] the day when we do our dotproduct is the
[4:43:30] zcoordinate all the the x coordinate and
[4:43:33] the y coordinate didn't actually affect
[4:43:35] the mathematical calculation at all. So
[4:43:37] we still get that blue color right here.
[4:43:38] So again, you know, if we want to make a
[4:43:41] easier distinguishment, we can just
[4:43:42] change this, right? Which I think I
[4:43:45] accidentally did when I was recording
[4:43:46] the last 5 minutes, but oh well. All the
[4:43:48] grayscale values that gradient texture
[4:43:50] is generating between 0.441 just to use
[4:43:54] this color rather than a linearly
[4:43:56] interpolated version. You actually want
[4:43:58] it constant. Rather than keeping them
[4:44:00] close together, you can just come over
[4:44:02] here and change the interpolation mode
[4:44:04] to constant. And look what happens. we
[4:44:07] get that stripe pattern just like when I
[4:44:09] was talking about adding loop cuts for
[4:44:10] this mug to add that stuff. Well, now we
[4:44:14] know how to make something striped just
[4:44:16] like this. Of course, we would just take
[4:44:18] this color, right? Copy the hex value
[4:44:20] here and place it for this color right
[4:44:22] here
[4:44:24] like so. And then we have something
[4:44:26] striped and then we can just adjust the
[4:44:27] sliders here to determine our stripe for
[4:44:30] our mug texture. Or of course,
[4:44:32] additionally, we have this mapping node
[4:44:33] and you can adjust it like so. I was
[4:44:35] planning to go into the math behind that
[4:44:37] one as well, but I feel like it would
[4:44:40] take really, really long and this video
[4:44:42] would go on for hours if I explained
[4:44:44] every single mathematical thing behind
[4:44:45] the nodes. Now, remember, we want the
[4:44:47] top to be lighter than the bottom. So,
[4:44:50] I'm going to get rid of the center one,
[4:44:52] and I'm just going to take this value
[4:44:54] and just make it a little bit darker.
[4:44:56] And voila, part one of our material is
[4:44:59] completely done. Just like that, we have
[4:45:02] a darker bottom and we have a lighter
[4:45:05] top. Now, over time, you'll find out
[4:45:07] that there are multiple ways to do the
[4:45:09] same thing because at the end of the
[4:45:11] day, all these nodes are just math
[4:45:13] behind the scenes. So, you could do some
[4:45:14] really complicated node setup and
[4:45:16] actually have the same result as someone
[4:45:17] that has a lot less nodes than you do.
[4:45:19] Over time, you know, you'll get better
[4:45:21] at developing intuition and kind of just
[4:45:23] like knowing what's available to you.
[4:45:25] So, I'll just give a short example for
[4:45:27] this one. Instead of using the gradient
[4:45:29] texture node, there's this other node
[4:45:31] called separate XYZ. And if I go to the
[4:45:33] Blender documentation here, you can see
[4:45:35] that it splits a vector into its
[4:45:37] individual components. So, we know that
[4:45:39] the generated coordinis
[4:45:47] based on the object's bounding box
[4:45:49] center. Why don't we take the generated
[4:45:51] coordinate system, use that as an input,
[4:45:53] and then we only care about the Z
[4:45:55] because we're going from bottom to top.
[4:45:57] So, we can just use that Z and plug it
[4:45:59] in the factor and take a look at what we
[4:46:01] get. We literally get the same exact
[4:46:03] thing whether I use the gradient texture
[4:46:05] here or the separate XYZ. So, in this
[4:46:08] case, there's actually no dot product
[4:46:10] calculation at all. We're just taking
[4:46:12] the directional vector directly 0 to 1
[4:46:15] and sampling those values. And you can
[4:46:16] also see here that I don't have a
[4:46:18] mapping node. I could add a mapping node
[4:46:20] if I wanted to. Let me duplicate and put
[4:46:22] it here. But now it's messed up because
[4:46:24] we rotated 90 degrees. We actually don't
[4:46:26] need to rotate it at all. You might also
[4:46:28] be wondering, okay, if this is quote
[4:46:30] unquote, like you said, better, Andrew,
[4:46:32] then why does this even exist in the
[4:46:33] first place? Well, for our use case,
[4:46:35] this is quote unquote better just
[4:46:37] because there's less setup and things to
[4:46:39] change, less moving parts, less
[4:46:41] mathematical calculations, and you kind
[4:46:43] of just intuitively understand it a
[4:46:44] little bit better. Maybe not because I
[4:46:46] went into detail here but you know over
[4:46:48] time this will become easier to
[4:46:50] understand than this if that makes any
[4:46:52] sense. Now there are a lot of use cases
[4:46:53] where you know taking this approach and
[4:46:55] the flexibility of this approach is
[4:46:57] necessary compared to using separate XYZ
[4:47:00] node for us yes quote unquote this is
[4:47:02] better but does it really matter at the
[4:47:05] end of the day? No it doesn't really
[4:47:06] matter. No it's just about getting a
[4:47:07] result and you know developing your
[4:47:09] intuition on how to get a result. Part
[4:47:11] one of two of our texture is done. So
[4:47:13] let me get rid of this. And now what we
[4:47:15] want is a noise texture. So how do we do
[4:47:16] that? Well, we're going to create a
[4:47:18] noise texture. We're going to create a
[4:47:19] color ramp to sample from. Like so. Plug
[4:47:22] the factor over here. And to mix the
[4:47:25] colors, we're going to use a mix color
[4:47:27] node. Drop it in here. And we're going
[4:47:29] to change it to multiply. Then I'm going
[4:47:30] to take this color and place it in here.
[4:47:32] And now you can see we have that noise
[4:47:34] as well as the darker gradient here. So
[4:47:36] of course we can always preview the
[4:47:37] noise texture just to see what that's
[4:47:38] generating. What kind of values? Maybe
[4:47:40] we can make it a little bit bigger. And
[4:47:42] then we can control shiftclick the color
[4:47:44] ramp just to see the color itself. So
[4:47:47] maybe we want to make this a little bit
[4:47:49] brownish and this to be I don't know
[4:47:52] maybe like a pinkish too but like a
[4:47:53] lighter pink. Maybe let's increase the
[4:47:55] intensity about this just a little bit
[4:47:57] like so. And let's go back to principal
[4:47:59] BSDF. Let's go to render view and take a
[4:48:01] look. We have a darker bottom. We've got
[4:48:03] some noise around here. Maybe we can
[4:48:05] increase the darker spots a little bit
[4:48:07] more. So we got a little bit of grungy
[4:48:09] noise dirt around our walls. All right.
[4:48:11] So, we kind of have our gradient texture
[4:48:13] from darker to lighter. And then we have
[4:48:16] our noise texture, which is like rugged
[4:48:18] dirt and wear and tear. So, the last
[4:48:19] thing we need are cracks on our surface.
[4:48:22] So, how do we do cracks on our surface?
[4:48:24] Well, we could create another multiply
[4:48:26] thing, create another toys texture, and
[4:48:28] then make it a little bit darker and
[4:48:30] then probably stretch it so it looks
[4:48:31] like cracks or, you know, like wavy
[4:48:34] lines and so on so forth. And that would
[4:48:35] be okay. Whatever style you're going
[4:48:37] for, that actually might be better than
[4:48:38] what I'm about to show you. But the way
[4:48:40] I'm going to be doing it is plugging a
[4:48:41] noise texture into this normal output
[4:48:44] right here. If you remember earlier in
[4:48:45] the video, we talked about how people
[4:48:47] often use normals to quote unquote fake
[4:48:49] geometry. And that's exactly what we're
[4:48:51] going to be doing. So you'll notice that
[4:48:53] it's a purple input, which means it
[4:48:55] takes a different kind of input. So we
[4:48:57] have to use a bump node. So if you
[4:48:59] search for a bump node and plug it in
[4:49:01] the normal, just like that. Now
[4:49:02] nothing's going to change because
[4:49:03] there's no height information put into
[4:49:05] this bump node at all. What if we add a
[4:49:07] color ramp to that? So let's add a color
[4:49:09] ramp. Let's plug the color data, the
[4:49:11] grayscale value of the color data into
[4:49:13] the height values. And then let's add a
[4:49:15] new texture here called a vori texture,
[4:49:17] which is just another formula that
[4:49:19] someone made up. So if you look up, you
[4:49:21] know, vori texture online or like vori
[4:49:23] noise, you'll get you'll see different
[4:49:26] formulas for different kinds of popular
[4:49:29] noises that are often adapted and reused
[4:49:31] for different scenarios. Again, you
[4:49:33] know, these are just mathematical
[4:49:34] formulas that someone came up with. And
[4:49:36] let's take our vinary texture. its color
[4:49:38] data into the color ramp factor. So, and
[4:49:41] voila, just like that, we get cracks
[4:49:43] along the surface and we didn't add any
[4:49:46] extra geometry for these cracks
[4:49:47] whatsoever. So, if I preview the verary
[4:49:50] texture color information, you can see
[4:49:52] that we have a bunch of random different
[4:49:54] colors. So when I take that color
[4:49:56] information and use it to sample with
[4:49:57] the color ramp, it's converting it to
[4:49:59] grayscale and sampling from my grayscale
[4:50:02] color ramp, which is determining the
[4:50:03] height or quote unquote our, you know,
[4:50:05] kind of cracked or like depth of our
[4:50:07] quote unquote cracks. So if I preview
[4:50:09] the color ramp, you can see, yeah, zero
[4:50:11] and ones uh for the height information.
[4:50:13] So basically what's happening here is
[4:50:14] that the distinguishment between the two
[4:50:16] colors, the borders is going to
[4:50:18] determine the intensity of how big that
[4:50:21] crack appears or how deep the crack
[4:50:23] appears. So if I go back here into the
[4:50:25] principal BSDF, notice that from here to
[4:50:28] here, there's a very very solid looking
[4:50:31] crack here. Whereas over here on there,
[4:50:34] the it doesn't look like it's as deep of
[4:50:36] a crack. And why is that? Well, if I go
[4:50:38] to the color ramp, you can see that the
[4:50:40] shade of gray here is very close to the
[4:50:42] shade of gray here. Whereas over here,
[4:50:44] the shade of gray is very distinguished
[4:50:47] between these two. Okay, so now you
[4:50:49] might be wondering, okay, how do we, you
[4:50:51] know, make how do we get fewer cracks?
[4:50:53] Well, we can just take our color rep
[4:50:54] node, right? And just bring up the
[4:50:56] blacks.
[4:50:57] And you can see as I preview my thing,
[4:51:00] all the blacker areas, the less
[4:51:02] distinguished ones are not going to have
[4:51:04] that many cracks. You can see the cracks
[4:51:06] are here because there's a clear
[4:51:08] distinguish distinguishment between
[4:51:10] these grayscale values. Whereas in the
[4:51:12] black areas, there's very, very few
[4:51:15] cracks, if any at all. Okay. So, what if
[4:51:17] I want to make more cracks? Well, I
[4:51:20] could probably increase the amount of
[4:51:22] scale here on the vinary texture. And
[4:51:24] now you can see we increase the amount
[4:51:26] of cracks like that. What if we want to
[4:51:28] increase it in another direction or
[4:51:31] another way? Well, again, we have our
[4:51:32] mapping node, right? So, we can do
[4:51:34] CtrlT. Let's reset the scale to five. I
[4:51:37] think that was the default. And look
[4:51:38] what happens when I adjust the scale and
[4:51:40] the X.
[4:51:42] So, think about what's happening here.
[4:51:43] It's taking our generator cord system 0
[4:51:45] to one and it's increasing scale of our
[4:51:48] entire texture. This is just adjusting
[4:51:50] you know the scale within its own
[4:51:52] mathematical calculations. Whereas this
[4:51:54] is adjusting the scale of the entire
[4:51:56] vinary texture along the generated axis.
[4:51:59] So that means if you want more you know
[4:52:02] of these in the Z-axis well then you
[4:52:04] just increase the scale on Z right cool.
[4:52:08] And now you get like this sort of
[4:52:09] pattern right? However for this one you
[4:52:10] know when you're adjusting the scale
[4:52:12] it's just adjusting the you know the
[4:52:13] cracks rather than the amount. Now of
[4:52:16] course you know you can change things
[4:52:17] like the location as well. So, so you
[4:52:19] can take a look at this this set of
[4:52:21] crack here. If I move it in the X
[4:52:23] direction, you can see we're adjusting
[4:52:24] the location of it. Now, you might be
[4:52:27] asking, you know, why when I move in the
[4:52:29] positive X on this mapping node, it's
[4:52:31] going in the negative X direction and
[4:52:33] why when I move it on the Z direction in
[4:52:35] the positive, it's going down. How does
[4:52:37] that make any sense? Well, I was going
[4:52:39] to explain that in this video, but I
[4:52:41] feel like you can figure that out on
[4:52:42] your own. And if you have any questions,
[4:52:43] you know, feel free to reach out to me.
[4:52:45] Just to recap, this is controlling the
[4:52:47] entire texture. The texture is just
[4:52:49] controlling its own mathematical
[4:52:50] formula. So if you want more noise
[4:52:52] patterns, of course, you can just
[4:52:53] duplicate this. Come over here. Create
[4:52:57] another multiply. Plug it in here. Plug
[4:52:59] it in here. This time maybe we can make
[4:53:02] our noise texture really, really small
[4:53:04] like this. Let's make this color like, I
[4:53:07] don't know, like red or something. Let's
[4:53:10] make this color like bluish. And let's
[4:53:12] go back to our principal BSDF. And now
[4:53:14] you can see that we have a really really
[4:53:17] small noise. All right. So just to recap
[4:53:19] what we have, I kind of just moved
[4:53:20] things around a little bit. But you can
[4:53:22] also join them together to create a
[4:53:24] frame. So if I do Ctrl + J, you can see
[4:53:26] it'll create a frame that you can click
[4:53:28] and drag together. So what we have here
[4:53:30] is our dirt bottom gradient, which I'll
[4:53:34] also put for my label here, which is
[4:53:37] technically also the base color, but
[4:53:39] whatever. And then we have a larger
[4:53:41] noise. So we can probably Ctrl + J and
[4:53:44] just call it large noise for dirt. And
[4:53:48] then over here we have smaller
[4:53:52] smaller wall texture for plaster like
[4:53:55] thingy bobber. And I'll just copy that
[4:53:59] into label as well. And then over here
[4:54:01] we have wall cracks. Ctrl J.
[4:54:04] Wall cracks. Just like that. At any
[4:54:08] point if you want to adjust the wall
[4:54:09] cracks you come here. If you want to
[4:54:10] adjust the small wall texture, you can
[4:54:12] come over here, adjust the larger noise
[4:54:15] to appear like dirt, you can adjust
[4:54:17] here. If you want to adjust the bottom
[4:54:18] gradient, you can come over here and
[4:54:20] adjust that. So, I just want to say
[4:54:21] congratulations. You created your first
[4:54:24] quote unquote professional level
[4:54:26] procedural material and we only covered
[4:54:28] the foundations and basics of these
[4:54:30] shader nodes so far. Just with these
[4:54:32] foundations, you can create so many
[4:54:34] different kinds of textures and explore
[4:54:36] so many different routes from here. like
[4:54:38] you can use another noise texture to
[4:54:39] adjust the scale of this noise texture
[4:54:41] and so on so forth and you kind of
[4:54:43] understand intuitively even though we
[4:54:45] haven't done it yet what that actually
[4:54:46] does. Now the other really really cool
[4:54:48] thing is we actually understand the math
[4:54:50] behind everything that we're using on
[4:54:52] these nodes and if we pick a random
[4:54:54] point on our object we can go through
[4:54:56] the mathematical calculations to find
[4:54:58] out the resulting color at that point in
[4:55:00] in our 3D space on our object. So
[4:55:02] hopefully by covering these foundations
[4:55:04] in this section when you explore your
[4:55:06] own materials, you have kind of a
[4:55:08] starting point to explore. And hopefully
[4:55:10] also when you go and explore more
[4:55:12] complicated procedural materials and
[4:55:14] procedural material tutorials, you kind
[4:55:16] of have like a baseline understanding of
[4:55:17] how to follow things and what people are
[4:55:19] actually doing in those tutorials. So
[4:55:21] I'm going to hit control spacebar. By
[4:55:23] the way, I'm using control spacebar just
[4:55:25] to maximize my scenes like that. So if
[4:55:27] you just hover over something and hit
[4:55:28] control spacebar, it'll just maximize
[4:55:30] that scene. You could also just come to
[4:55:32] the view tab in any sort of viewer and
[4:55:34] just go into area and do toggle maximize
[4:55:37] area. You know, I'll also say you could
[4:55:39] probably sell this procedural material
[4:55:41] for $1 or $3 and honestly get like a few
[4:55:44] sales. So, another small tip, if you did
[4:55:46] shift D to move these around and then
[4:55:48] you later want to change something like
[4:55:49] this pen right here, I want to add, you
[4:55:52] know, a base black to the tip here. Like
[4:55:54] for this tip, I want to give it a base
[4:55:58] black material and assign it. But these
[4:56:01] aren't instances. So these don't update
[4:56:04] because they're not instances. If you
[4:56:06] did alt d, they would have been. But
[4:56:08] that's fine because you can just do ctr
[4:56:10] link object data. And then they will
[4:56:12] become instances. However, since we are
[4:56:15] baking, uh, we actually have to go one
[4:56:17] step further and select all these and do
[4:56:19] f3 and do make single user object and
[4:56:22] data. That way they're completely
[4:56:24] independent objects. Another issue you
[4:56:26] might encounter is when you join two
[4:56:27] objects, your procedural material
[4:56:29] changes and glitches. That's because if
[4:56:31] you're using the generated coordinate
[4:56:33] system, that's based on your bounding
[4:56:34] box. And when you join two separate
[4:56:35] objects, they become one single object
[4:56:37] and the bounding box updates, right?
[4:56:40] Which means your coordinate system also
[4:56:41] updates. So you'll probably have to
[4:56:42] shift your mapping node a little bit to
[4:56:44] make your procedural texture work again.
[4:56:47] The other alternative is you can bake
[4:56:49] first and then join your objects later.
[4:56:51] So if you don't want to mess with your
[4:56:53] mapping nodes and want to join your
[4:56:54] objects later, you can actually
[4:56:56] completely totally do that perfectly
[4:56:57] fine. Another thing you might have to
[4:56:59] fix is your normals. So I covered this
[4:57:02] in my previous video, but you can come
[4:57:04] up to viewport overlays and check face
[4:57:06] orientation to see which direction your
[4:57:08] normals are pointing. Everything that is
[4:57:10] visible, we want it to be blue because
[4:57:13] the 3D software needs to know which side
[4:57:15] of our completely flat geometry is the
[4:57:18] side that should be interacting with
[4:57:20] light. So for these, you can just select
[4:57:22] them and go into edit mode. Alt N and
[4:57:25] hit flip. Just like that. If you want,
[4:57:27] you can hit A to select everything. Go
[4:57:28] into edit mode, A to select everything.
[4:57:30] And you can probably do recalculate
[4:57:32] outside and see if that helps. And
[4:57:34] actually, it did solve all our issues.
[4:57:36] You might also have issues like this
[4:57:37] where you accidentally delete a face and
[4:57:39] just like I did. So I accidentally
[4:57:41] deleted this inside of this computer.
[4:57:43] So, I'm actually going to shift alt and
[4:57:45] just select all those and just do
[4:57:48] control E bridge edge loops. Now, the
[4:57:50] shading is messed up here because now
[4:57:53] the shading is messed up because I've
[4:57:55] shade smooth on here. So, there's kind
[4:57:56] of two ways to fix it. One, you can do
[4:57:58] shade auto smooth or since these this
[4:58:01] area here needs flat shading because
[4:58:03] it's two flat faces, you can just
[4:58:05] rightclick and well, make sure you're in
[4:58:07] face select, you can just rightclick and
[4:58:09] do shade flat, and it'll shade these
[4:58:12] faces flat. whereas everything else
[4:58:14] would be shade smoothed. Or again, you
[4:58:16] could just do shade auto smooth and that
[4:58:18] would work as well. Or alternatively,
[4:58:19] you can select the edges that should be
[4:58:22] sharp and just do control and dot
[4:58:24] control E and do mark sharp here. And
[4:58:26] now you can see that also fixes the
[4:58:28] shading issues that we have. So you'll
[4:58:30] also see like these other small issues
[4:58:32] here like this is red on the inside
[4:58:34] because it's hollow. If I go in here,
[4:58:35] you can see it's hollow, which means in
[4:58:38] the 3D environment when I'm looking
[4:58:40] through here, I'm going to see straight
[4:58:42] through it and see this table leg
[4:58:44] instead. So to simulate that, like I did
[4:58:46] in my previous video, you can go into
[4:58:48] solid view, come over here, and do back
[4:58:50] face coloring. And you can see I can see
[4:58:52] that table like right through there.
[4:58:56] That's what we would see in 3GS. So
[4:58:58] let's turn off back face coloring. Okay.
[4:59:00] So to fix this issue, let's just
[4:59:02] confirm. My max camera angle is going to
[4:59:04] be here. So you can see we have some
[4:59:05] redness here. Honestly, this might not
[4:59:07] be an issue here, but whatever. Uh, so
[4:59:10] we'll have some issues over here. So
[4:59:12] let's just get the top and a little bit
[4:59:14] of the side. So let's go into edit mode.
[4:59:16] Let's hold click on this. Let's hold
[4:59:19] control and select around here. It'll
[4:59:22] pick the shortest path there. I think we
[4:59:24] can hold control and pick these two
[4:59:26] faces as well. And then maybe this one.
[4:59:30] And I think I'm going to select this top
[4:59:32] over here, too. Whoops. Let's get rid of
[4:59:35] this. I don't need to select that. And
[4:59:38] okay, we're kind of selecting these
[4:59:40] faces right now. And oh, whoops. I
[4:59:42] accidentally selected that.
[4:59:45] And for some reason, it's actually
[4:59:47] selecting that. Okay. So, these are the
[4:59:49] faces that are blue on the outside,
[4:59:52] which is what we want, but we also want
[4:59:54] them blue on the inside. So, what I'm
[4:59:56] going to do is just shift Duplicate
[4:59:58] them, right click, cancel,
[5:00:02] and then scale it down just a little
[5:00:03] bit. And then I'm going to hit Alt N
[5:00:05] with them still selected, and hit flip.
[5:00:07] And now we have a fixed thing.
[5:00:11] So, if I go back into out, go to the max
[5:00:15] angle here, no red, max angle here, no
[5:00:18] red either. Cool. And of course, you
[5:00:20] know, make sure to fix things that are
[5:00:22] floating and things like that. To make
[5:00:24] this glass material, I just used a glass
[5:00:26] BSDF. Turn down the roughness and index
[5:00:29] of refraction. Now, it doesn't really
[5:00:31] matter how you make your glass because
[5:00:32] there's multiple ways to make glass. I
[5:00:34] just did it this way cuz it was the
[5:00:36] quickest. We will be replacing the
[5:00:37] material with a glass-like material in
[5:00:40] 3GS. If you're curious on how I made
[5:00:43] like the fish and stuff, again, they're
[5:00:44] just subdivision service modifiers. So,
[5:00:47] I think earlier in the video, I used
[5:00:48] round cubes, which are pretty much just
[5:00:50] cubes with subdivision service modifier.
[5:00:52] So for the fish specifically, I just
[5:00:54] added a cube, give it control 2,
[5:00:57] subdivision surface, and I applied it
[5:00:59] first, and then I went to edit mode,
[5:01:01] just scale it up. Uh, took these top
[5:01:04] faces like so. Inset, extrude, gx. Same
[5:01:09] thing with the back here. Uh, I think I
[5:01:11] just extruded here. I don't actually
[5:01:12] remember. I might have inset first. And
[5:01:14] then I extrude out, scaled out. And then
[5:01:16] once you get a general shape, you can
[5:01:17] just add control 2 with another
[5:01:19] subdivision service modifier. And you
[5:01:20] get a fish really, really quick. Just
[5:01:22] like that.
[5:01:24] All right. So now we're ready for
[5:01:25] baking. So baking is the idea that you
[5:01:29] save some sort of information
[5:01:31] beforehand. So when you come back to it,
[5:01:34] it becomes easier or faster, more
[5:01:36] performant or it just saves you time
[5:01:38] later down the road. So baking can be
[5:01:40] for done for a lot of things like
[5:01:41] animations. But for us, we're going to
[5:01:43] be doing it with the lighting.
[5:01:45] Everything you're seeing when you're in
[5:01:46] rendered mode is being calculated as you
[5:01:48] move your screen. That's why it's so
[5:01:50] laggy for some people and that's why we
[5:01:52] have the noise threshold and everything.
[5:01:54] And that's exactly why when we go into
[5:01:56] the shader editor and we adjust the
[5:01:58] lighting, you know, we can see these
[5:01:59] updates because everything is being
[5:02:02] calculated mathematically behind the
[5:02:04] scenes. And these mathematical
[5:02:05] calculations like the ray tracing
[5:02:07] basically, you know, simulating how
[5:02:08] light bounces would really really hurt
[5:02:11] the performance on the browser. Since we
[5:02:13] have static lighting or lighting that
[5:02:15] won't change, it's better just to save
[5:02:17] that as part of the texture. So this
[5:02:18] color change between this lighted area
[5:02:20] and this lighted area that information
[5:02:22] can just stay in that texture. That way
[5:02:24] when we use it, we don't actually have
[5:02:26] to use any lighting because the image
[5:02:28] looks like that already. Then obviously
[5:02:30] the downside of baking your lighting is
[5:02:32] that you can have dynamic shadows for
[5:02:34] your baked lights. You can still use
[5:02:36] baked textures and real-time lighting
[5:02:38] for shadows. Or you could use like a
[5:02:40] simulated planes that act like shadows,
[5:02:42] but for the bakedin shadows like these,
[5:02:45] they can't really be changed, you know,
[5:02:47] in in real time easily. You can see on
[5:02:49] this website, I think it won sight of
[5:02:51] the day on awards, they also baked their
[5:02:54] textures. And you can see here, they
[5:02:56] baked his hand with the lighting source
[5:02:58] there. So that's where the shadow is,
[5:03:00] but his hand is moving, but that shadow
[5:03:02] is not updating. So, while we get better
[5:03:04] performance, you know, we lose a little
[5:03:06] bit of realism, but you know, when
[5:03:08] you're when your site is really
[5:03:09] interactive and there's a lot going on,
[5:03:11] very very few people are going to be
[5:03:13] paying attention to that shadow. So,
[5:03:15] here's another website that won site of
[5:03:17] the day on awarders.com. You can see
[5:03:20] they have some fairly realistic lighting
[5:03:22] like here. And none of this is actually
[5:03:25] real-time lighting. So if you take a
[5:03:26] look at their textures, the lighting is
[5:03:29] actually baked into here. You can see at
[5:03:31] some point the GB model that is on this
[5:03:34] file is mapping to one of these light
[5:03:35] rays, which is why we have all this
[5:03:37] realistic looking lighting. So since the
[5:03:39] lighting information is stored directly
[5:03:41] in the texture, we don't have to do any
[5:03:42] expensive realtime mathematical
[5:03:44] calculations. If you remember when we
[5:03:46] were working with procedural materials,
[5:03:48] we had to UV unwrap our model in order
[5:03:51] to place a 2D image into our simulated
[5:03:54] 3D space. So, we're going to be doing
[5:03:56] the same thing, except this time, we're
[5:03:58] going to be creating our 2D image
[5:04:00] texture and trying to unwrap our 3D
[5:04:03] model and place it into that texture and
[5:04:05] save that lighting information onto that
[5:04:07] texture. Now, depending on how large
[5:04:09] your scene is, you might need more than
[5:04:11] one texture. I'll say from my
[5:04:13] experience, I feel like I might have to
[5:04:15] go for more than one texture here,
[5:04:17] possibly two. So, how would you know?
[5:04:19] Well, honestly, you probably wouldn't
[5:04:21] until you started baking, just to see
[5:04:23] what results you get. Now, you might be
[5:04:25] asking, okay, Andrew, how did you
[5:04:27] intuitively know that you might need at
[5:04:29] least two textures here? Well, first,
[5:04:31] it's definitely based on, you know, how
[5:04:33] many objects you have and the size of
[5:04:35] those objects, as well as what kind of
[5:04:37] material is on those textures. When we
[5:04:39] bake, we generally stick to powers of
[5:04:41] two. So, let me draw like a cube here.
[5:04:44] So, we have like 1024 pixels by 1024
[5:04:47] pixels, which is like 1K, and then 2040,
[5:04:50] right? 204080 by 20480 and then 4K 4096
[5:04:55] by 4096 and things like that. So since
[5:04:58] your image has a specific amount of
[5:05:01] pixels you can use about it. If you have
[5:05:03] a bunch of large objects that means
[5:05:05] they're going to take up more space on
[5:05:06] your texture which means more resolution
[5:05:08] and more pixels. Whereas smaller objects
[5:05:10] on your scene are going to take less.
[5:05:12] And this should make some sort of
[5:05:14] intuitive sense. If it's smaller then
[5:05:16] the resolution doesn't have to be as
[5:05:17] high. It's the same idea when you scale
[5:05:18] up an image, it starts getting blurry.
[5:05:20] So, you need a higher resolution in
[5:05:22] order to prevent it from getting as
[5:05:24] blurry. However, this isn't a general
[5:05:25] truth because if you have like, for
[5:05:28] example, a really large face that isn't
[5:05:31] really primarily part of your scene, for
[5:05:34] example, back here, what you can do is
[5:05:36] take a UV and actually scale it down and
[5:05:38] make it really, really small. So yes,
[5:05:40] this side would look really blurry, but
[5:05:42] now other areas of your scene can take
[5:05:45] up more of that texture and get a higher
[5:05:47] resolution. So if you keep this large,
[5:05:49] for example, it'll take up more pixels
[5:05:51] and then possibly some of your other
[5:05:53] models that you want more detailed will
[5:05:55] become, you know, a little bit more
[5:05:56] blurry. Another factor affecting this
[5:05:58] issue is the type of material that's
[5:06:01] actually on your object. So, if it's a
[5:06:02] flat color like this, then you actually
[5:06:05] don't need as much of a larger area
[5:06:07] compared to if it was like a realistic
[5:06:09] PBR material. A blurred solid color
[5:06:11] would look quote unquote less blurred
[5:06:13] than a material that's very very
[5:06:15] detailed. So, for example, this poster
[5:06:17] right here, it might be smaller than my
[5:06:19] chair, but my chair might actually take
[5:06:21] less space on my texture just because
[5:06:23] this has more detail and I want it to
[5:06:25] have a little bit more detail and more
[5:06:26] pixels to bake in there. So, when I said
[5:06:28] two textures, I meant two 4K textures
[5:06:31] cuz I kind of want to maximize quality
[5:06:33] rather than like load times. And I think
[5:06:36] with compression methods, given that
[5:06:37] most of mine are solid colors rather
[5:06:39] than PBR materials, it should be low
[5:06:41] enough. Now, there are a lot of advanced
[5:06:43] compression methods, but you know, I'm
[5:06:44] not going to get it into this video. Or
[5:06:46] you can watch my Minecraft video where I
[5:06:48] talk a little bit more in depth for some
[5:06:50] more complicated compression methods.
[5:06:52] Okay. So, when we're baking and UV
[5:06:54] editing, there's this other tab here
[5:06:56] that we generally use called the UV
[5:06:58] editing tab. Same with shading, which
[5:07:01] typically when you're doing lighting and
[5:07:03] material, you go to the shader tab or
[5:07:05] the shading workspace to, you know, work
[5:07:07] with that. That way, you kind of have
[5:07:09] like a separation of concerns. But, you
[5:07:10] know, I've just gotten so used to just
[5:07:12] creating my own workspace uh in the
[5:07:14] default layout that I don't really
[5:07:16] separate them anymore. You can also come
[5:07:18] over here and create your own workspace
[5:07:19] if you wanted to. But Blender does have
[5:07:21] these separate workspaces for us just
[5:07:23] with like some sort of setup already. So
[5:07:25] that's what I'm going to be doing for
[5:07:26] this video. I'm just going to create a
[5:07:27] new tab here and create a UV editor. I'm
[5:07:30] going to get rid of the shading and I'm
[5:07:32] going to get rid of this as well. And
[5:07:33] I'm going to make this side a little bit
[5:07:35] smaller. Just like that. One of the most
[5:07:37] difficult things about unwrapping is
[5:07:39] unwrapping it. Well, so when it comes to
[5:07:40] simple objects like cubes, all these
[5:07:42] primitive objects, if you go into edit
[5:07:44] mode, they have, you know, a default
[5:07:46] unwrap that's very good and continuous.
[5:07:48] Right now, it's really straightforward
[5:07:50] for a cube because, well, Blender gave
[5:07:52] it to us. But what about more
[5:07:53] complicated objects like this? How do we
[5:07:55] know we UV unwrapped it properly? Well,
[5:07:57] Blender actually has this really helpful
[5:07:59] thing and it's called a UV grid. So, if
[5:08:02] I come to the shader editor and I search
[5:08:05] for an image texture. So, I'm just going
[5:08:06] to shift a search for an image texture
[5:08:08] like so. Create a new image texture and
[5:08:10] you can just call it whatever. I'm just
[5:08:12] going to call it UV grid helper
[5:08:14] tutorial. And you and then since we're
[5:08:17] going for 4K, I'm going to click and
[5:08:18] drag down here and do 4096 just like
[5:08:21] this. And then under generated type,
[5:08:23] instead of blank, you can do UV grid.
[5:08:25] Now, we don't need an alpha channel. We
[5:08:26] don't have any transparency, so we can
[5:08:28] uncheck that. But honestly, it doesn't
[5:08:29] really matter if you keep it there.
[5:08:30] Create a new image here. And then click
[5:08:32] and drag that into the base color. So,
[5:08:35] I'm on the wood material because I
[5:08:36] select this here. So, let me just copy
[5:08:38] that to the cube like link materials.
[5:08:41] Let's go to material preview. And now
[5:08:43] you can see everywhere that's using my
[5:08:44] wood material is now using this UV grid.
[5:08:46] This UV grid will show us a lot about
[5:08:49] our unwrap and how proper it is. I think
[5:08:51] I said it earlier in the video, but
[5:08:53] areas with similar amounts of detail
[5:08:57] space should have roughly equal sized
[5:09:01] cubes or squares in this case. So here
[5:09:03] it actually seems that these aren't
[5:09:04] terrible. But you can see that some of
[5:09:06] these cubes are being a little bit
[5:09:07] stretched, but it's fairly consistent
[5:09:09] across the whole thing, which means it's
[5:09:11] probably not as big of an issue. Now,
[5:09:14] watch what happens when I go into edit
[5:09:15] mode and start distorting this. Take a
[5:09:17] look at that. That means if we had an
[5:09:19] image, any other image across his face,
[5:09:21] it would start completely distorting.
[5:09:22] Like this poster, if I go into edit mode
[5:09:24] and start dragging that, take a look
[5:09:26] what's happening to my image. You know,
[5:09:28] that doesn't look great. So this UV
[5:09:30] texture kind of helps us determine that.
[5:09:32] It'll also show us, you know,
[5:09:33] distinguishly where are the seams or the
[5:09:35] areas that we cut it out. Example here,
[5:09:37] you can see that there's definitely a
[5:09:39] clear seam over here because the blocks
[5:09:41] aren't really continuing and there's
[5:09:43] like a hard line. So when you're
[5:09:44] unwrapping and cutting seams, you kind
[5:09:46] of want to make it you kind of want to
[5:09:48] find a places to hide those seams. Now,
[5:09:51] if you want to see the stretching, you
[5:09:52] can actually come into the UV editor.
[5:09:55] Let's actually open up our UV grid
[5:09:57] helper like so. And when you go into
[5:09:59] edit mode, make sure you're in edit mode
[5:10:01] to see everything. You can come use your
[5:10:03] middle mouse button to click and drag
[5:10:05] over here. Come over to overlays and
[5:10:07] turn on UV stretch. Like so. Just like
[5:10:10] that. And generally what you want is
[5:10:12] everything to be this solid blue color,
[5:10:13] which means there's very, very little
[5:10:15] stretching. And if I take one of these
[5:10:16] UVs and move it, you can see it's
[5:10:19] changing color, which means it's
[5:10:20] definitely stretching really, really
[5:10:22] hard. And you can also see that updated
[5:10:24] on my texture as I move this around.
[5:10:27] It's really really distorting just like
[5:10:28] that. So I'm just going to undo all
[5:10:30] those changes here. I'll also say you
[5:10:33] know notice when I select over here for
[5:10:35] some reason it's also selecting vertices
[5:10:37] over here. Now how does that make any
[5:10:39] sense? If it's the same verticy why is
[5:10:41] it appearing over here as well? Well in
[5:10:43] real life imagine you know when you're
[5:10:45] like doing reverse origami or like you
[5:10:47] know trying to wrap something from a 2D
[5:10:49] onto like a 3D object. You need areas to
[5:10:51] cut which we called seam. So the areas
[5:10:54] that we cut or the seams, they quote
[5:10:56] unquote split it into two visual
[5:10:57] vertices, but essentially it's the same
[5:10:59] exact verticy. And they don't have to be
[5:11:01] right next to each other on your UV map.
[5:11:03] If you don't understand whatever I'm
[5:11:05] talking about right now, that's totally
[5:11:06] okay because I feel like you'll get it,
[5:11:09] you know, as we go through this chapter.
[5:11:11] So by default, when I hit unwrap, you
[5:11:13] know, Blender already has, you know, a
[5:11:15] default area that it quote unquote marks
[5:11:16] seams for us automatically, but we can
[5:11:18] also mark our own seams and unwrap
[5:11:20] there. So, you might be wondering, okay,
[5:11:22] how do I even know where to mark seams?
[5:11:24] It doesn't really make sense. I can
[5:11:26] visualize it for a cube, sure, but like
[5:11:28] what about these other objects? So,
[5:11:29] there's a few methods that I'll talk
[5:11:31] about in a little bit. But first, I
[5:11:32] don't actually like adjusting the
[5:11:35] material itself to use this UV grid
[5:11:37] texture. And the reason for that is just
[5:11:39] because it requires an extra step. So,
[5:11:41] I'm just going to unhook that. I'm going
[5:11:42] to still leave it here, but I'm going to
[5:11:43] unhook that and bring my wood material
[5:11:45] back in here. What I'm going to do
[5:11:46] overstead is come over here. Make sure
[5:11:49] you are in solid view. If you come over
[5:11:51] here and go into color, you can select
[5:11:54] texture. And what texture will do is it
[5:11:57] will use your image texture as what
[5:11:59] you're seeing on the UV. However, you
[5:12:01] know, if I still go into material
[5:12:02] preview or rendered, you can see that
[5:12:04] it's still going to see the wood. It's
[5:12:05] only in solid view. So, you'll often see
[5:12:07] people use mat caps like this one, which
[5:12:10] kind of helps with if you have any
[5:12:12] shading issues. You might have seen, you
[5:12:14] know, some things like this, which kind
[5:12:16] of highlights, you know, the edges and
[5:12:17] cavity maps and things like that. You
[5:12:19] can also see like you have this cavity
[5:12:21] option here as well. So, a lot of
[5:12:23] options, but you know, it doesn't really
[5:12:25] matter for us at the moment. Right now,
[5:12:26] I'm just going to go back into studio
[5:12:28] and I'm just going to use texture.
[5:12:30] Another thing I like to do when I'm
[5:12:32] editing instead of, you know, having to
[5:12:33] mark seams like E and mark seam and then
[5:12:37] A and then unwrap and then, you know, do
[5:12:39] an unwrap. So, what I like to do instead
[5:12:42] is do a live unwrap. So if you come over
[5:12:44] to the options in edit mode and do live
[5:12:46] unwrap and then with live unwrap enabled
[5:12:49] when you use the shortest path like
[5:12:51] control and pick shortest path here what
[5:12:54] you can do instead of select for edge
[5:12:56] tag you can do tag seam and now as as I
[5:13:01] hold control and pick my shortest path
[5:13:02] it's going to live UV unwrap for me. So
[5:13:05] you can see as I'm holding holding
[5:13:06] control and clicking on my sides it's
[5:13:09] updating my UV map just like that. So
[5:13:11] instead of always having to hit a U
[5:13:14] unwrap, it will just unwrap for you as
[5:13:16] you start marking your seams. To get rid
[5:13:18] of them, you can hold control and pick
[5:13:20] the shortest path. And if there's
[5:13:21] already a seam there, it will just get
[5:13:23] rid of it for you. So I'm just holding
[5:13:24] control and get rid of these seams right
[5:13:26] here. So earlier in the video, I
[5:13:28] mentioned about UV unwrapping intuition.
[5:13:30] So now I kind of just want to talk a few
[5:13:32] of those now. So when it comes to UV
[5:13:34] unwrapping, what you generally want to
[5:13:36] think about even when you're unwrapping
[5:13:38] complicated objects like this or this or
[5:13:41] this or this is try and think of it as
[5:13:43] its default primitive object. That'll be
[5:13:45] a little more clear once we get started.
[5:13:47] But even some of the most scaryl looking
[5:13:49] models actually have very very simple UV
[5:13:52] unwraps if you think of them in terms of
[5:13:54] primitive objects. And what you'll find
[5:13:56] is a lot of them are going to be like
[5:13:59] cylinders like in a sort of cylinder
[5:14:01] sort of unwrap or a cube. So if I go
[5:14:03] into edit mode, you can see by default
[5:14:06] it's unwrap. Well, now we don't see any
[5:14:08] seams here because you know it's just
[5:14:09] built into Blender. But what we can do
[5:14:10] is hit A to select everything UV and
[5:14:13] come to seams from islands. So every
[5:14:16] individual set of connected UV faces is
[5:14:18] what we call an island. So here we can
[5:14:20] do UV seams from islands. And now you
[5:14:22] can see we have those seams on on over
[5:14:24] here. Take a look at how they do it.
[5:14:26] They cut out the top and they cut out
[5:14:27] the bottom. Now again, just imagine you
[5:14:29] had a piece of paper in this shape and
[5:14:31] you need to flatten it into 2D shape. If
[5:14:33] you cut off the top and cut off the
[5:14:35] bottom, let's just come over here and
[5:14:37] clear the seam with control E clear
[5:14:39] seam. Also, right click and do add to
[5:14:42] quick favorites. I have it quick
[5:14:43] favorites. So, it's showing remove, but
[5:14:45] add it because it'll it'll speed up your
[5:14:47] workflow. So, if you do Q, you can just
[5:14:49] do clear seam instead of going to Ctrl E
[5:14:52] and clear seam. Or again, you can set
[5:14:54] your own hotkey if you wanted to. So
[5:14:57] take a look at what happens when I
[5:14:58] remove their seam. We get this extreme
[5:15:01] stretching here. Now, why does that make
[5:15:03] sense? Well, you have this thing here
[5:15:04] that we call a ring. And imagine you had
[5:15:07] a piece of paper in this ring format,
[5:15:09] and you had to like flatten it on the
[5:15:11] ground. That would be impossible without
[5:15:13] ripping the paper. In 3D, you can't like
[5:15:15] rip that, right? So instead, they just
[5:15:17] display it as stretching. If you want to
[5:15:19] flatten a ring, you need to chop it up
[5:15:22] somewhere. So it can be anywhere across
[5:15:23] the ring. You just need to break it up
[5:15:25] somewhere so it can flatten. So we just
[5:15:27] mark seam and look we get it back. So
[5:15:29] this is something that you'll see over
[5:15:30] and over again even in complicated
[5:15:32] objects which is why I kind of wanted to
[5:15:34] mention that. The second general
[5:15:36] intuition when it comes to unwrapping
[5:15:38] hard surface models and maybe even
[5:15:40] organic models is to look at individual
[5:15:42] parts as individual primitive objects.
[5:15:45] So kind of tying into the first general
[5:15:47] guideline. So if I go into edit mode and
[5:15:50] like I inset this for example and then
[5:15:52] extrude downwards you can see okay now
[5:15:54] we get some differences in the UVs
[5:15:56] compared to this and this you know
[5:15:58] generally we want to keep everything
[5:16:00] right the same size now obviously
[5:16:02] different circumstances and things like
[5:16:04] that but general rule of thumb you want
[5:16:05] to keep everything roughly the same
[5:16:07] textual density and then you can tinker
[5:16:09] with that a little bit later but I'll
[5:16:11] get into that a little bit later. So in
[5:16:14] order to fix this how would we fix this?
[5:16:17] Well, if you think about it, just ignore
[5:16:18] the rest of this cube. Honestly, if you
[5:16:20] want to do like this, Ctrl I, and then
[5:16:22] hit H to hide it. Like, just view this
[5:16:24] for a second. What does it look like? If
[5:16:26] you said cylinder, you would actually be
[5:16:28] kind of correct. We have a ring and then
[5:16:30] we have a bottom face. If you said cube,
[5:16:32] you would also be correct. But in this
[5:16:34] case, the cylinder unwrap for this quote
[5:16:36] unquote cube actually works a lot
[5:16:38] better. So, if I do Alt H to rehide
[5:16:41] those stuff, sorry, unhide that stuff.
[5:16:43] We already know how to unwrap a
[5:16:44] cylinder. So we can just apply it to
[5:16:46] this same sort of area here. Hold alt,
[5:16:49] select this loop, Q or Ctrl + E, mark
[5:16:53] seam. And then we can just select this
[5:16:54] bottom face. It'll select all the sides
[5:16:56] for us. E mark seam. Now we're getting
[5:16:59] somewhere. And then of course we're
[5:17:01] getting that distortion because we have
[5:17:02] a ring that we can flatten right right
[5:17:05] over here. So we just pick any sort of
[5:17:07] one of these corners just like on the
[5:17:09] cylinder. E mark seam. And take a look
[5:17:12] at that. We just fixed up this entire
[5:17:14] place. So because we cut this out from
[5:17:17] this side of the cube, this we can now
[5:17:20] just envision this entire side of the
[5:17:22] cube as the same as any other side of
[5:17:24] this cube. Which means we can just
[5:17:26] unwrap this like a normal cube now. So
[5:17:28] we can just do something like this. And
[5:17:31] just shift shift control E mark seam.
[5:17:35] And then down the side over here like
[5:17:37] so.
[5:17:39] Control oh on this one as well. control
[5:17:41] E mark seam and take a look at that. We
[5:17:43] have our default cube unwrap and then we
[5:17:46] have our side unwrap over here. So what
[5:17:48] you see here is we have a quote unquote
[5:17:50] cylinder and then a quote unquote
[5:17:52] default regular cube with you know some
[5:17:55] sort of extra geometry there. Now you
[5:17:56] might be asking okay why do we just have
[5:17:58] one seam you know why not I place it
[5:18:00] here and here and here and well and you
[5:18:04] know mark seam is there as well. I mean,
[5:18:07] that's perfectly valid as well. But
[5:18:09] again, we're trying to minimize the
[5:18:10] amount of seams. But if for some reason
[5:18:12] you do need those extra seams there,
[5:18:15] then you can totally do that. But for
[5:18:16] us, that isn't really necessary. All we
[5:18:18] really need is just to cut out the ring
[5:18:20] once. Okay. So, I kind of hope that
[5:18:22] clears up UV unwrapping as you'll find
[5:18:24] that a lot of really, really complicated
[5:18:26] objects can be broken down into their
[5:18:28] perimeter shapes. So, just ignored the
[5:18:32] fact that for every single material, I
[5:18:35] copy and pasted the UV grid helper into
[5:18:38] their materials. So, I just went through
[5:18:40] each of them and just Ctrl +V paste it
[5:18:42] and made sure it was the active one,
[5:18:44] which you can see here. Everything's
[5:18:46] really large because none of the UVs are
[5:18:48] set, but they'll update as we update our
[5:18:50] things. So, let's unwrap our first thing
[5:18:52] together. Probably this piano over here.
[5:18:55] And all these green edges means they're
[5:18:57] sharp edges. And that's likely from our
[5:18:59] weighted normal modifier or when we used
[5:19:02] bevel and we did harden normals, we're
[5:19:04] marking all these sharp edges. And then
[5:19:06] typically when you comes to UV
[5:19:08] unwrapping, if you want to go the quick
[5:19:10] way about it, you can just hit U unwrap
[5:19:13] and do smart UV project. And 66 by
[5:19:16] default works fairly well for hard
[5:19:18] surface models. And if you hit unwrap,
[5:19:20] you can see that, you know, we get a not
[5:19:23] too terrible unwrap here. And then you
[5:19:26] can do what we did previously, Q seams
[5:19:27] from islands. And then you can kind of
[5:19:29] just go in edit mode and see, you know,
[5:19:32] what sort of unwrap they give us here.
[5:19:34] So the from far away, you know, it
[5:19:36] doesn't seem too bad. And this is
[5:19:38] honestly passable because we're working
[5:19:40] with solid colors. And for the most
[5:19:42] part, you know, there's minimal
[5:19:44] distortion. Professionally, you know, it
[5:19:46] looks a little bit weird, right? Like
[5:19:48] over here, you'd kind of expect it to
[5:19:50] continue the loop rather than go up and
[5:19:52] then down over here. Same thing. Same
[5:19:55] thing over here. It seems like there it
[5:19:57] kind of like goes janky to the left and
[5:19:59] whatnot. Same over here, it seems like
[5:20:02] this doesn't really continue. Goes to
[5:20:03] the side. So, and if we look at, you
[5:20:05] know, these other areas again here, you
[5:20:07] can see this is symmetrical geometry,
[5:20:10] but over here it's going on the left.
[5:20:11] And then here it's going on, well, it's
[5:20:13] also going on the left here, but like
[5:20:15] left relative to this side. And this is
[5:20:17] like left relative to this side. So it's
[5:20:20] a little bit inconsistent. And then here
[5:20:22] we just have a basic cylinder, but
[5:20:23] they're adding like multiple seams
[5:20:25] across the cylinder which are just extra
[5:20:27] seams. So even if I get rid of these,
[5:20:30] for example, Q clear seam, like
[5:20:32] nothing's going to change over here
[5:20:34] because we already have one that's
[5:20:36] breaking the the ring over here. Yeah,
[5:20:38] it's not the perfect, but it does save
[5:20:40] you a lot of time. Now, the UV unwrap
[5:20:43] may not be perfect, but it does give you
[5:20:44] a general guideline on how to approach
[5:20:46] your model. So, here we have a lot of
[5:20:49] bevel modifiers. So, if I add a cube
[5:20:51] real quick, and let me just link one of
[5:20:54] these materials with this. I'm just
[5:20:56] going to manually bevel this like over
[5:20:59] here. When you want to unwrap this
[5:21:00] beveled cube, you might be wondering,
[5:21:02] there's so many edges. There's like one
[5:21:04] here, there's one here, there's one
[5:21:05] here, there's one here. You know, it's
[5:21:08] like which one do you select? You know,
[5:21:09] in the past there was just one single
[5:21:11] one and now there's like multiple. Well,
[5:21:13] again, honestly, it really really
[5:21:15] depends on what your priority is.
[5:21:17] Generally, what I like to do, like let's
[5:21:19] say your only goal is to minimize
[5:21:21] distortion along these sort of corners
[5:21:23] because that's where it's going to have
[5:21:25] the most issue. Then what you would do
[5:21:27] is have a seam on every single sides of
[5:21:30] the bevel. So, for example, I'd select,
[5:21:33] well, actually, I don't have to select
[5:21:34] all of them. I can just select one,
[5:21:35] shift G, select similar area, and it'll
[5:21:38] just select all of them because, you
[5:21:40] know, they have the same length and
[5:21:41] width. And I do mark seam. Now, of
[5:21:44] course, we have all this distortion
[5:21:45] because this entire thing, if I hold, if
[5:21:47] I select this face and do Ctrl L, you
[5:21:49] can see, you know, imagine trying to
[5:21:51] flatten that out. So, what we can do is
[5:21:53] probably select all of these, right?
[5:21:55] Shift G, select a similar area. So, we
[5:21:58] get all of these and dot control E mark
[5:22:00] seam. And take a look at that. we get
[5:22:02] something that is very very well tixel
[5:22:05] density optimized. Now obviously the
[5:22:07] downside here is we have all these extra
[5:22:09] seams here. So we could get rid of
[5:22:11] these. So if I do clear seam you can see
[5:22:13] it goes from something like this to
[5:22:15] something like this. So yes we have some
[5:22:17] distortion and stretching here but you
[5:22:19] know at least it continues now and the
[5:22:21] distortion is very very minimal. Of
[5:22:23] course if you marked every single edge
[5:22:25] you know as a seam we would get perfect
[5:22:27] blue every single time right because
[5:22:29] everything is just its own individual
[5:22:31] face. But that's way too many seams. If
[5:22:33] we made every single corner like this,
[5:22:35] then every single corner would be like
[5:22:36] this. And and that would be a pretty
[5:22:38] good unwrap if your goal was to to
[5:22:40] minimize distortion. Now, what if your
[5:22:42] second goal is to minimize the amount of
[5:22:45] seams possible? Well, if you look at it
[5:22:47] again, you can see a ring here. Or if
[5:22:49] you want to visualize it this way, you
[5:22:51] can do that as well. Then maybe you can
[5:22:53] just unwrap it like a cylinder.
[5:22:55] Distortion might not be your primary
[5:22:57] goal, but minimizing seam. So you could
[5:22:59] have like one over here. Mark your seam.
[5:23:01] And then maybe you want over here. Ctrl
[5:23:03] + E, mark your seam. And then anywhere
[5:23:05] along the ring, you can fix that just by
[5:23:07] marking a seam. So you can just pick
[5:23:09] somewhere where no one will see or less
[5:23:12] frequently see. And just mark the seam
[5:23:13] there. And take a look what we get. We
[5:23:16] get fairly equal tixel density, just a
[5:23:19] little bit stretching along the sides
[5:23:20] over here, of course. But for all
[5:23:22] intended purposes, we minimize the
[5:23:24] amount of seams, and it looks pretty
[5:23:25] good equal in texel density. If you kind
[5:23:28] of want to get the best of quote unquote
[5:23:30] both worlds in this scenario, you can
[5:23:32] try and do what UV project is doing. So
[5:23:35] unwrap here and hit Q seam from islands,
[5:23:37] you can see what they're trying to do.
[5:23:39] They're kind of just trying to slice
[5:23:41] along the center bevel. In this case, we
[5:23:44] don't actually have a center bevel
[5:23:45] because we have a even number 1 2 3 4.
[5:23:49] If I had one with five, which I'll just
[5:23:52] create real quick, ctr Link materials.
[5:23:54] And here I'll just uh Ctrl +B center
[5:23:57] one. So this should have five here. And
[5:23:59] then now I do UV unwrap smart UV project
[5:24:01] unwrap cube seams from islands. You can
[5:24:04] see what it does is it cuts through the
[5:24:07] center. Now it's cutting everything. So
[5:24:09] we have six individual
[5:24:11] faces. Now originally I said that was
[5:24:13] bad because there's no relationship
[5:24:15] information. But since we're doing
[5:24:16] baking and we're not using this map for
[5:24:19] texturing, this is kind of ideal in the
[5:24:21] sense that it will fit along our UV map
[5:24:24] with other objects very very well. And
[5:24:26] we're maximizing the amount of texture
[5:24:28] space along along this entire object.
[5:24:31] And of course, you know, since it's a
[5:24:32] beveled cube, I went back to the one
[5:24:34] with just three bevels. And then, of
[5:24:36] course, you know, since it's just a
[5:24:38] cube, you can use the same method that
[5:24:40] we did to unwrap the cube. And you can
[5:24:42] see here we get the default cube unwrap
[5:24:44] except with the beveled areas obviously
[5:24:46] being stretched there. So there's pros
[5:24:48] and cons to each of these methods. It
[5:24:50] depends on what you're working with as
[5:24:51] you expand your knowledge in Blender.
[5:24:53] For us, does the method actually matter?
[5:24:55] And the answer is no because our seams
[5:24:59] aren't going to be that visible when we
[5:25:01] bake. And since we're working with solid
[5:25:03] colors, even if we have some major
[5:25:05] distortion like this, that means over
[5:25:07] here would have a lot less resolution
[5:25:09] compared to over here. But since we're
[5:25:10] working with a color, colors when
[5:25:12] they're blurry will look a lot more
[5:25:15] similar to each other from a high
[5:25:17] resolution and low resolution area
[5:25:19] compared to things like PBR materials or
[5:25:22] like actual images, you know, that we
[5:25:24] had on on the photo frames and things
[5:25:26] like that. So, we have a very very
[5:25:28] flexible way to approach our unwrap. So,
[5:25:31] just when you're unwrapping, don't you
[5:25:32] don't actually have to care about, you
[5:25:34] know, what method am I using? Is it the
[5:25:35] best? You know, is this right? Whatever.
[5:25:38] just try and follow the general
[5:25:39] guidelines like across the areas you
[5:25:41] want similar size squares, you want to
[5:25:43] minimize distortion, and you kind of
[5:25:45] want to minimize the amount of seams.
[5:25:47] But again, you know, that really
[5:25:48] actually ends up depending on your use
[5:25:50] case. So, you'll definitely see me use a
[5:25:52] lot of different approaches and methods
[5:25:54] when I'm UV unwrapping. I'll try and
[5:25:56] explain why I'm making that decision as
[5:25:58] I do it. But honestly, sometimes the
[5:26:00] answer might just be because I want to
[5:26:01] save time and that's kind of like the
[5:26:03] only reason because again, we're doing
[5:26:04] this for baking a texture rather than
[5:26:08] exporting it to texture or texturing it.
[5:26:10] So, we we could actually have extremely
[5:26:12] sloppy UVs. Like even on over here, we
[5:26:15] could have like one UV like this. And if
[5:26:18] we baked with this, even though it's
[5:26:20] distortion, this would actually look
[5:26:22] perfectly fine. Because essentially what
[5:26:24] we're doing is we're taking that solid
[5:26:25] color and spreading it across the
[5:26:27] texture like this. But again, with
[5:26:29] colors, it can be very, very blurry and
[5:26:31] it wouldn't look any much more different
[5:26:33] than a place with more pixels of colors.
[5:26:36] Not always, but you know, a lot of times
[5:26:38] it will be. Again, I kind of want to
[5:26:39] unwrap in the proper way in the event
[5:26:41] that you come back here and you want to
[5:26:44] export it to another 3D software to
[5:26:46] texture in or you want to apply a PBR
[5:26:48] material. So that means under object
[5:26:49] data properties, we can come over here
[5:26:51] to UV maps. If you applied PBR
[5:26:54] materials, you're by default using this
[5:26:56] default one that comes with every object
[5:26:58] called UV map. So this is the UV map for
[5:27:00] texturing. We want one for baking. So
[5:27:03] all we can do is just create a new one
[5:27:04] and call that baking. And it'll just
[5:27:06] clone your UV map. So, here I didn't use
[5:27:08] a PBR material. I didn't use UVs to
[5:27:11] match this either. But again, that
[5:27:13] doesn't matter because we used a solid
[5:27:15] color in here or quote unquote a
[5:27:16] procedural material that doesn't use UVs
[5:27:18] to determine how to texture on it. Now,
[5:27:21] something that did use the UV to
[5:27:23] determine how to map our image texture
[5:27:26] is something like this computer screen
[5:27:27] over here. So, if I hit home, this image
[5:27:29] here, if I go into UV map, I used the UV
[5:27:33] map. I used this UV map to map my image
[5:27:35] texture onto the screen perfectly. So
[5:27:37] here we have one UV map for mapping the
[5:27:39] texture to the 3D object. Now what we
[5:27:42] need is a second one called baking. And
[5:27:45] this one will be taking this 3D model
[5:27:48] and putting it on a texture to bake with
[5:27:51] all the other textures. So for example,
[5:27:53] if I have this one highlighted at
[5:27:54] baking, this one highlighted at baking
[5:27:57] as well, you can just go into edit mode,
[5:27:59] U, smart UV project together, and now
[5:28:01] they're sharing the same texture. Now,
[5:28:03] right now it looks messed up because I
[5:28:05] have baking highlighted. But you can see
[5:28:07] this render icon here, which means
[5:28:09] during baking process, it'll use this
[5:28:11] map for the image texture when it's
[5:28:14] baking on this active baking UV map. So,
[5:28:16] if you want, you can just leave it back
[5:28:18] there for now. We'll get to that when we
[5:28:19] get to that. Okay. So, when it comes to
[5:28:21] this piano, I'm going to hit all and
[5:28:25] clear seams. Let's just do it manually
[5:28:27] for us. Now, I made a sort of a small
[5:28:29] issue here because now if we were to do
[5:28:32] this manually, we would have to mark a
[5:28:34] seam on every single one of these.
[5:28:35] Whereas, if we did an array modifier,
[5:28:38] unwrapped one of these piano keys, and
[5:28:40] then used the array modifier and then
[5:28:42] applied the array modifier, then we
[5:28:43] would only have to unwrap one of these
[5:28:45] keys because they all have the same
[5:28:46] geometry here. Now, that's an easy fix
[5:28:48] because what we can do is just select
[5:28:51] all the keys, like one side on the keys.
[5:28:54] Well, actually, box select might be
[5:28:55] faster here. Oh, I don't want to select
[5:28:57] the piano. Maybe just in case, we just
[5:29:00] do something like this. And we can do
[5:29:02] Ctrl L and just delete those vertices.
[5:29:05] So now we have one here. We can do Ctrl
[5:29:07] L and P separate by selection after
[5:29:09] selecting it. So we can actually go into
[5:29:11] local view here. And I'm just going to
[5:29:14] be going for the UV unwrap method here.
[5:29:16] So quote unquote, the best of both
[5:29:18] worlds. I'm just going to pop one over
[5:29:20] here. Mark seam. Control E mark seam or
[5:29:22] Q mark seam if you have it. Quick
[5:29:24] favorites. Now, when it comes to slicing
[5:29:26] off the ring, I'm going to put it on the
[5:29:28] side because that'll be less visible
[5:29:30] than over here because all the piano
[5:29:32] keys are next to each other. So, what we
[5:29:34] can do is just do over here. And same
[5:29:36] thing on this side. We can just put it
[5:29:38] on the side because that'll be hidden.
[5:29:40] Again, we want to hide our seams as best
[5:29:42] as possible. So, that's why I'm deciding
[5:29:44] to put it on the side there. So, if I go
[5:29:46] in here, hit A, you can see we have a
[5:29:48] pretty great pretty good unwrap with
[5:29:50] even textile density. Now we can just do
[5:29:52] our array modifier stuff again. Oh, I
[5:29:55] forgot to mention, you might be
[5:29:56] wondering, okay, why didn't I put a seam
[5:29:57] at the bottom? Well, that's because I
[5:30:00] deleted all the faces at the bottom, so
[5:30:02] there's nothing to cut out there. If you
[5:30:03] left the faces in, yes, you would also
[5:30:05] have to add a seam on the bottom there.
[5:30:07] Yeah. So, I just redid the array
[5:30:08] modifier. By the way, if you did save
[5:30:10] your original piano in a modifiers
[5:30:12] collection, you could have just used
[5:30:14] that one. F3, convert to mesh. Applies
[5:30:16] that. And then we can join it with the
[5:30:18] piano or you can wait after we're done
[5:30:20] with the rest of the piano. So now if I
[5:30:21] go into edit mode, you can see all of
[5:30:23] them have the same exact unwrap, which
[5:30:25] is really, really nice. I'll also say if
[5:30:26] you go in here and you get a slightly
[5:30:29] different result when you're unwrapping,
[5:30:30] it's probably because you're using a
[5:30:33] different unwrapping method. You can see
[5:30:34] there's different kinds here. And if you
[5:30:36] take a look on the Blender
[5:30:38] documentation, you can actually read
[5:30:39] what each of these does. when it comes
[5:30:41] to hard surface models like the ones
[5:30:43] we're working with conformo generally
[5:30:44] work seems to work the best for us. So
[5:30:47] that's what the method that I'm going to
[5:30:49] be using at the moment. Now I will also
[5:30:51] say since all of these have the baking
[5:30:53] map when they're actively highlighted
[5:30:55] they will be sharing the same exact
[5:30:57] texture. So, as we unwrap more objects,
[5:31:00] like for example, this one, the piano
[5:31:02] and the key over here, since they're
[5:31:04] sharing the same UV map, they're going
[5:31:06] to be sharing. Since we have both of
[5:31:08] them on the baking UV map highlighted,
[5:31:11] they're going to be overlapping each
[5:31:12] other. Take a look what happens when I
[5:31:13] switch this to UV map. Now, we only see
[5:31:15] the one of the texture sets. If you want
[5:31:17] to do manual packing with your baked
[5:31:19] texture, what I recommend you do after
[5:31:21] you're done unwrapping something is just
[5:31:23] to scale it down and just move it off
[5:31:26] somewhere into oblivion. That way when
[5:31:28] you revisit it and do like enter tab
[5:31:30] mode here. Now is it that big of a deal?
[5:31:32] Honestly, no. Because you can always
[5:31:33] just move it later. You don't have to
[5:31:34] select both of them. You can just select
[5:31:36] one and then move it out later. Or
[5:31:38] depending on your method, if you unwrap
[5:31:40] them together, let's say we just go
[5:31:42] conformal, then Blender will try and
[5:31:44] pack it by default for you with the
[5:31:46] objects that you selected. So if that's
[5:31:48] your workflow, then you don't really
[5:31:49] have to move things outside. But if you
[5:31:52] want to manually pack things, you might
[5:31:53] as well just move things outside
[5:31:55] beforehand. That way you don't have to
[5:31:56] do it later. But again, not really a big
[5:31:58] deal for us. So let's focus on each of
[5:32:00] these individual parts. Like ideally we
[5:32:03] probably should not have joined these
[5:32:04] objects until after baking. That way we
[5:32:07] can quickly enter local view, but that's
[5:32:08] totally fine because what we can do is
[5:32:10] always just select something and then
[5:32:12] Ctrl I to invert our selection and hide
[5:32:14] everything else. And then now we can
[5:32:16] just enter local view. And now you can
[5:32:17] see we just have this. So here you can
[5:32:19] see that we already have some sharp
[5:32:21] edges here. And honestly, there is a
[5:32:24] really really common workflow where you
[5:32:26] use sharp edges as your seams because
[5:32:28] oftent times it works perfectly fine.
[5:32:30] But again, I'm also trying to minimize
[5:32:31] the amount of seams. So for a model like
[5:32:33] this, I'm actually going to take the
[5:32:35] center bevel and unwrap it like that. So
[5:32:37] here you can see that we have a loop
[5:32:39] over here over here. So I'm just going
[5:32:41] to continue that across the model.
[5:32:44] Hopefully that gets everything like so.
[5:32:48] Let's do over here as well.
[5:32:50] Just holding shift alt shift alt. Let's
[5:32:54] continue over here. And that should get
[5:32:56] everything. We can mark our first seam
[5:32:58] over there. All right. And remember now
[5:33:00] we have an inset cube here and an inset
[5:33:02] cube here. So what we want to do is cut
[5:33:04] it out. So here we can have a we can put
[5:33:08] our cutout over here just like we did
[5:33:10] when we had an inside cube. Now this
[5:33:12] just says bevels. Ctrl + E mark seam. So
[5:33:14] this is cut out. And then of course we
[5:33:16] need one here. E mark seam. Right? You
[5:33:18] can just imagine this is like the box
[5:33:20] that we did earlier. And of course, now
[5:33:22] we have a ring, right? It's just spread
[5:33:24] across several bevels instead of just
[5:33:26] one continuous uh sort of loop instead
[5:33:30] of just one continuous face. So again,
[5:33:32] if you want to break this ring,
[5:33:33] honestly, this ring is probably not that
[5:33:35] problematic, but again, probably cut it
[5:33:37] over here, like over here, and then one
[5:33:40] over here. Again, if you want to
[5:33:43] minimize the amount of seams, then you
[5:33:45] can just have one and that would be it
[5:33:47] for the entire loop. Again, you also
[5:33:49] want to take into consideration how
[5:33:51] effective your unwrap is when you're
[5:33:53] packing. And generally, what we want to
[5:33:55] go for is everything to be kind of like
[5:33:57] a square because those are going to be
[5:33:58] easier to pack with a lot of objects
[5:34:01] compared to something like this, if that
[5:34:03] makes sense. Because at the end of the
[5:34:05] day, the entire texture is a square. So
[5:34:07] working with like rectangles and squares
[5:34:08] will pack better than some sort of
[5:34:11] distorted shape like this. So here you
[5:34:14] can see I'm combining methods this time.
[5:34:15] This time instead of just using one seam
[5:34:17] for the entire ring like we did earlier,
[5:34:19] I'm using two and then on each corner
[5:34:22] just to flatten out things a little bit.
[5:34:24] Is this overkill? Possibly. But does it
[5:34:27] matter? Honestly not. For us it does
[5:34:29] not. So same thing over here. Just like
[5:34:32] this. And now you can see the result is
[5:34:35] very few distortion, definitely more
[5:34:38] seams, but you know, we also have things
[5:34:40] that are easier to pack. And now we just
[5:34:42] have this inside piano, right? So let's
[5:34:44] cut that out. So we can do the same
[5:34:46] thing maybe around here. Hold control.
[5:34:50] I'm just going around the center bevel.
[5:34:51] Whoops. Let's make sure I don't get that
[5:34:54] over there. Just holding control.
[5:34:56] Slicing over. Wait, actually, I think I
[5:34:58] can hit alt and get this entire loop.
[5:35:01] Yeah. And then I can hit alt and get
[5:35:03] this entire loop. Cool. Ctrl + E mark
[5:35:06] seam. I don't want to continue along
[5:35:08] this edge. Again, if you wanted to do
[5:35:09] the two faces, you could totally do
[5:35:11] that, but I'm just going along the
[5:35:13] center bevel. So, I'm just going to
[5:35:15] continue over here down to this seam.
[5:35:18] And we can clear these two. So, Q clear
[5:35:21] seam. And then we can continue this on
[5:35:23] here. So, Ctrl + E mark seam. And let's
[5:35:26] just make sure. Yeah. Okay. I can clear
[5:35:28] these two out as well. Now, are there
[5:35:30] add-ons that if your geometry is
[5:35:32] symmetrical, you can just copy one half
[5:35:34] to the other? Yes, they are, I believe,
[5:35:36] but most of them are paid. So, I'm not
[5:35:38] going to be using them in this video.
[5:35:40] So, again, we can just continue on here
[5:35:42] along the edge over here. So, control E,
[5:35:46] mark seam. We can just hold alt and
[5:35:48] hopefully get everything here. Mark
[5:35:49] seam.
[5:35:51] Seems to look pretty good here. We can
[5:35:53] continue over on this side as well.
[5:35:56] Again, it's just symmetrical. Hold alt
[5:35:58] control e mark seam. So let's make sure
[5:36:01] it's also getting the back but it's not.
[5:36:02] So that's okay. So control E mark seam.
[5:36:06] Sorry I keep doing control E when I
[5:36:08] should be doing Q. So there's an over
[5:36:11] there. And I think this is going to be
[5:36:14] the last one. So just over here and
[5:36:17] connect down there. So if you take a
[5:36:21] look at our piano and let me just go
[5:36:23] control spacebar. We did a fairly fairly
[5:36:26] good job. Again, we cut this out. So,
[5:36:29] this can just imagine it's just like a
[5:36:31] face. Then we cut this out with our UV
[5:36:33] unwrap. So, the entire thing is just a
[5:36:35] rectangle. UV unwrap method to have six
[5:36:38] individual faces, right? Like here and
[5:36:41] here, quote unquote individual faces,
[5:36:43] but you kind of get what I'm talking
[5:36:45] about. That way, we maximize texture
[5:36:47] space and minimize distortions. Yes, we
[5:36:49] had more seams, but for us, this is
[5:36:52] going to be a good unwrap. Now, we can
[5:36:54] alt H to unhide our stuff. We can come
[5:36:57] back here and just do Ctrl LR I H and
[5:37:00] hide. And now work on this over here.
[5:37:02] Okay. So, how would I unwrap something
[5:37:05] like this? Well, again, you could
[5:37:07] definitely go for the center bevel.
[5:37:09] Well, I guess in this case, it's not
[5:37:10] really a center bevel, but you could
[5:37:12] just, you know, do this on every single
[5:37:13] side, including the bottom side as well.
[5:37:16] And that would be a perfectly good
[5:37:17] unwrap. Given what we're going for, a
[5:37:19] baking texture and my background
[5:37:21] experience, I wouldn't invest more than
[5:37:23] 2 seconds on this. And what I would do
[5:37:25] is just select a face like this. Shift
[5:37:28] G, select similar area like so. It'll
[5:37:30] select both of them. Control E, mark
[5:37:32] seam, and just be done with it. And if I
[5:37:34] go into the UV, you can see that we get
[5:37:36] a pretty decent unwrap here. And here
[5:37:38] you can see that, you know, the textual
[5:37:40] density is very very uniform around
[5:37:42] here. And you know, we don't really have
[5:37:44] to touch anything. Now, if you want to
[5:37:46] optimize for baking, you probably want
[5:37:48] to straighten these out a little bit.
[5:37:50] But for texturing, you might actually
[5:37:51] want to leave them a little bit more
[5:37:52] distorted. So, if you want to straighten
[5:37:54] them out, I like using this plugin here
[5:37:56] called UV squares. And he's leaving it
[5:37:59] open source. So, you can just download
[5:38:00] the zip, come into edit, preferences,
[5:38:02] add-ons, install from disk, and you can
[5:38:04] see I have it over here, check mark. So,
[5:38:06] when I hit N, you can see that I have
[5:38:08] this thing here called UV squares. And
[5:38:11] to use it, you have to turn off UV sync
[5:38:12] selection. You can select one of these
[5:38:14] that was not square. And you just select
[5:38:17] it, do Ctrl L. Whoops. Do Ctrl L just to
[5:38:20] select the entire thing. Select one of
[5:38:22] these and then do Ctrl L over here and
[5:38:24] do two grid by shape and it will
[5:38:26] actually just make your UV look like a
[5:38:28] shape. Now, of course, it's distorting
[5:38:30] because we're definitely going to need
[5:38:31] more seams in order to counteract that
[5:38:34] distortion, but again, we're baking
[5:38:36] here, so this distortion actually
[5:38:38] doesn't really concern us at all. So,
[5:38:40] here we're maximizing for packing, but
[5:38:42] we are not optimizing for texturing. So,
[5:38:45] for us, again, I wouldn't spend more
[5:38:46] than 2 seconds on unwrapping this. So,
[5:38:48] I'm just going to leave it like this.
[5:38:50] And this is honestly good enough for a
[5:38:52] rectangular shape. Okay, so let's do Alt
[5:38:54] H to get back the stuff that we hid. So
[5:38:57] how would I unwrap this? Well, if you
[5:38:59] look at it, the entire thing is just a
[5:39:01] giant cylinder with some extrusions. So
[5:39:04] as long as we cut these out, then the
[5:39:06] rest is essentially just becomes a
[5:39:07] cylinder. But instead of marking the
[5:39:10] seams for every single one of these,
[5:39:11] that would be kind of tedious. I'm just
[5:39:12] going to trust that smart UV project
[5:39:15] will handle this for us. So ctr L U,
[5:39:17] smart UV project. Unwrap. It looks okay.
[5:39:20] Not much distortion. Hit A to select
[5:39:22] everything. Q. Seams from islands. And
[5:39:24] that did a pretty good job here. Now,
[5:39:26] it's definitely giving us probably some
[5:39:28] extra seams. And you can see this is an
[5:39:30] extra seam as well as here, right? We
[5:39:33] only have one ring. So, we don't need
[5:39:35] two seams here. And we actually don't
[5:39:37] need a seam at all because this deleted
[5:39:40] face on the bottom is acting like a seam
[5:39:42] of sorts. So, it's already flattened. It
[5:39:44] can already be flattened without a seam.
[5:39:46] So, we can actually just get rid of
[5:39:48] these seams over here and all the way
[5:39:52] back here as well. And again, you can
[5:39:53] see that it's still working perfectly
[5:39:55] fine because we have the top half which
[5:39:58] is being cut out through a seam. And
[5:40:00] this is the seam down the side and the
[5:40:02] back doesn't even have a back. So, we
[5:40:03] don't need anything to cut out there.
[5:40:05] So, we can fix this over here as well.
[5:40:09] Just like so.
[5:40:11] Don't need a seam here.
[5:40:13] And don't need a seam here as well. So
[5:40:15] everything looks good with our piano so
[5:40:17] far. Ideally, yes, over here I probably
[5:40:20] should not overlap them. There'll be
[5:40:22] like a black line over here and over
[5:40:24] here when I bake, but honestly, that
[5:40:26] might actually add a little bit more
[5:40:27] realism as well. So, is it worth
[5:40:30] spending the time to fix? Well, that's
[5:40:31] kind of up to you. So, the last thing
[5:40:33] for the piano then is just this top area
[5:40:35] over here. And then these, of course, so
[5:40:37] these are just cylinders. So, we can
[5:40:38] just select these. Ctrl + E, mark seam.
[5:40:41] And then over here in the back, we want
[5:40:43] to hide our seams. Q more seam. Okay.
[5:40:45] So, how do unwrap these? Again, you have
[5:40:47] multiple methods. If you think about it,
[5:40:50] this is just a raised version of this
[5:40:52] inset. So, you could just unwrap it the
[5:40:55] same way, right? Select these faces,
[5:40:57] control E, mark seam, and then now we
[5:40:59] have this loop. So, if you want to save
[5:41:01] time, you only need one. So, we could
[5:41:03] just put something over here. And this
[5:41:06] honestly would be perfectly fine for us.
[5:41:08] And you can see that yes, we have a ring
[5:41:09] here, but it's not really too much of an
[5:41:11] issue because it's not like a completely
[5:41:13] distorted ring. But, you know, if you
[5:41:15] want to
[5:41:16] cut it out, you can totally do that.
[5:41:18] But, you know, if you want to do the
[5:41:20] same thing we did for the inset one, you
[5:41:22] know, alternatively, if you want to just
[5:41:24] do something quick and dirty, you can
[5:41:27] clear seam. Just go along the inner edge
[5:41:30] like this, or sorry, the inner bevel,
[5:41:33] control E, mark seam. And this would be
[5:41:36] a perfectly valid unwrap as well,
[5:41:38] depending on your goal. Again, there is
[5:41:40] a ring here, but that's totally okay.
[5:41:42] And honestly, for what we're doing, you
[5:41:45] might not actually even need seams for
[5:41:47] this kind of object at all because it's
[5:41:49] only half of an object. And Blender can
[5:41:52] handle that very, very well. So, if I
[5:41:55] select this entire thing, you know,
[5:41:56] leaving the key as is with no seams is
[5:41:59] actually perfectly valid when it comes
[5:42:01] to baking. So, if you want to do that
[5:42:03] for the rest of these, you can totally
[5:42:04] do that. And I'll just leave that for
[5:42:06] the purpose of this tutorial. I'm
[5:42:07] actually just going to not have a seam
[5:42:10] there at all. Remember, we're
[5:42:11] highlighting baking when we're
[5:42:12] unwrapping here, not UV map. Now, if for
[5:42:15] some reason all of your scenes, never
[5:42:16] use UV map. You can just use UV map
[5:42:19] instead of having a second one, but I
[5:42:21] kind of like to have two separate ones
[5:42:23] just in case. Okay, so now we can just
[5:42:25] join these pianos, everything in the
[5:42:26] piano together like so. Again, make sure
[5:42:28] they both have the same UV maps and do
[5:42:31] Ctrl + J. And now we have a very well
[5:42:33] unwrapped piano. Just like that. So,
[5:42:36] right now they're all overlapping, but
[5:42:38] we can hit A to select everything and
[5:42:41] then just U and again conformal here
[5:42:43] just to see what it looks like. And it
[5:42:45] looks pretty good together. Super cool.
[5:42:47] So, if you want again, you can move that
[5:42:48] off into Oblivion. So, the fact that we
[5:42:50] did the piano, you generally have a good
[5:42:52] idea on how to pretty much do, you know,
[5:42:55] anything that's kind of similar to the
[5:42:58] piano. Now, anything that's like cubish
[5:43:00] and extruded and inset, that sort of
[5:43:02] stuff. So, for example, if I go in here
[5:43:04] and you have no idea where to start or
[5:43:06] you just want to save your time, you can
[5:43:07] just unwrap smart UV project unwrap and
[5:43:10] then Q seams from islands. And if you
[5:43:12] look at what they give you, you can see
[5:43:13] that they're prioritizing the center
[5:43:15] bevel. Again, it has some issues here.
[5:43:17] So, you probably want to continue this
[5:43:19] one up, right? And then you would
[5:43:20] continue this here and get rid of this
[5:43:22] seam. That way, it's more consistent
[5:43:24] along where it's cutting. Again, not
[5:43:26] really a big deal. Or you can continue
[5:43:28] this one and get rid of this one. Or
[5:43:31] like we did for some other ones, if you
[5:43:33] want, you can select the faces, right?
[5:43:35] And of course, all these other ones as
[5:43:36] well. And I deleted the back and the
[5:43:38] bottom so there's nothing to select. E
[5:43:40] mark seam. And then, of course, you have
[5:43:42] all these corners. So, you can cut them
[5:43:43] out like we did for the beveled cube.
[5:43:46] And you could just go around doing that
[5:43:47] for, you know, every single corner. So
[5:43:49] down here as well.
[5:43:51] So really up to your use case. And then
[5:43:53] of course we have a ring here. Of course
[5:43:55] we have a ring here. Do we have to fix
[5:43:57] this? Honestly, probably not, but might
[5:43:59] as well. So anything mark seam. You can
[5:44:02] have four seams if you want. This is a
[5:44:04] extra seam that doesn't contribute
[5:44:05] anything. So we can clear those. The
[5:44:08] issue there, same thing here. This is a
[5:44:10] flat face. So the seam doesn't actually
[5:44:12] provide any value here. Now maybe if it
[5:44:13] was like really too long, you know,
[5:44:15] having a seam will split it up a little
[5:44:17] bit. So you can see if I have Q here
[5:44:19] mark seam now they can be packed as
[5:44:22] individual faces like so. But at the
[5:44:24] same time, you know, now we have to line
[5:44:26] things up if we want to make it look
[5:44:28] seamless. So you can see I just went
[5:44:30] around and added a bunch of seams. But
[5:44:32] again, if you want to use other method,
[5:44:33] that's totally fine. All right. So let's
[5:44:35] do something a little bit different like
[5:44:37] Mr. Rabbit over here. So if I go into
[5:44:40] edit mode on Mr. rabbit. What prone
[5:44:42] object did we use to shape Mr. Rabbit?
[5:44:45] Well, I used a cube with a subdivision
[5:44:48] surface modifier. So, essentially, we
[5:44:49] can just treat this like a cube or, you
[5:44:51] know, same with the room at all. We can
[5:44:53] just So, we can just do the same thing.
[5:44:54] We can just uh come over here, select
[5:44:58] the round side at the top, control E,
[5:45:01] mark seam, and then on the corners, we
[5:45:04] can just slice it off like so. And
[5:45:06] honestly, if you want to just leave it
[5:45:08] like a cylinder and minimize seams, this
[5:45:10] is actually fairly fairly well. So you
[5:45:12] can see that this is actually not that
[5:45:14] bad at all. But again, if you want to
[5:45:18] make it very minimal stretching, you can
[5:45:21] just do it something like this. Now you
[5:45:24] can see that the stretching is a little
[5:45:25] bit better and this might be a little
[5:45:27] bit easier to pack than something else.
[5:45:30] Again, when you're modeling, don't
[5:45:31] forget to come over here to UV maps and
[5:45:35] add the baking UV map. Now, you might be
[5:45:36] asking, okay, why don't you just like
[5:45:39] place, let me just do this real quick.
[5:45:41] Clear seam. Why not just cut it in here
[5:45:43] and over here and over here and then
[5:45:46] just mark seam like that is similar
[5:45:47] stretching. That looks like equal
[5:45:49] textual density. Why you doing all that
[5:45:51] complicated fancy stuff? Well, on a
[5:45:54] simple model, yeah, it might not be a
[5:45:56] big deal. And when we're baking, this
[5:45:59] seems appropriate for baking as well.
[5:46:00] But again, when it comes to like
[5:46:02] texturing and things, your seams are
[5:46:03] going to cause some issues. And
[5:46:05] generally, I kind of like to follow the
[5:46:07] rule like, you know, treat everything
[5:46:09] like a primitive object. And that way,
[5:46:10] you know, you'll just be more consistent
[5:46:12] over time that way. So, yes, you would
[5:46:14] be right saying like, you know, in this
[5:46:16] case, okay. But generally, I like to
[5:46:19] just stick with with, you know, treating
[5:46:21] things like they're primitive objects.
[5:46:23] So, same thing with the ear. If I go in
[5:46:25] here, cube unwrap here. So, I just cut
[5:46:28] out the top, the top, and if you wanted
[5:46:30] to just do a cylinder one, you totally
[5:46:31] could just have one seam to get rid of
[5:46:33] the ring. The bottom face is deleted.
[5:46:35] So, no seam is necessary there. Same
[5:46:38] with the speaker over here. This we used
[5:46:39] a round cube, which is just a subdivided
[5:46:41] cube. You can see that I cut out the
[5:46:44] cylinder over here. There was a ring in
[5:46:46] here, and then I added a edge over
[5:46:48] there. And then, since I cut this out,
[5:46:51] everything the rest of everything else
[5:46:53] was just a round cube. So, I cut out the
[5:46:55] top just like Mr. Rabbit and then cut
[5:46:57] out the sides just like this. You'll
[5:46:58] notice that we do have some odd little
[5:47:02] shape here. Does it really matter? Not
[5:47:04] really. But if you wanted to, you know,
[5:47:05] you could like
[5:47:07] continue the seam down here and possibly
[5:47:10] this would be a little bit better for
[5:47:12] baking. Definitely not for texturing
[5:47:14] because we have more seams, but okay.
[5:47:16] So, let's take a look at something where
[5:47:18] we use a different method to unwrap like
[5:47:20] using sharp edges. So this will come in
[5:47:23] handy a lot like when on over here. Now
[5:47:26] this is something we probably should
[5:47:27] have unwrapped first before applying our
[5:47:30] array modifier. But the luckily thingy
[5:47:32] here is we can use that select sharp
[5:47:35] edges here. So we can do select and do
[5:47:37] sharp edges. And you can see it'll
[5:47:39] select all our sharp edges. And if we do
[5:47:41] control E mark seam, you can see that
[5:47:43] that actually works fairly well for us.
[5:47:45] Of course since we cut out all these
[5:47:47] cylinders, we do get a bunch of rings.
[5:47:50] Now, this isn't particularly a big issue
[5:47:52] for us, but again, we already know how
[5:47:55] to get rid of seams. Sorry, I mean, you
[5:47:58] know, rings.
[5:48:00] And this might be a little bit better to
[5:48:02] pack, but and then it seems like we
[5:48:03] still have rings back here. So, I must
[5:48:05] have forgot to delete these. So, shift
[5:48:07] G, select similar normal, and then we
[5:48:09] can just delete those faces there. It
[5:48:11] also seems we have like this really long
[5:48:12] thing, which probably could pack fine,
[5:48:15] but we might as well get rid of it. I
[5:48:17] think it's because of Yeah. So it's like
[5:48:19] continuing on over here. So we actually
[5:48:22] don't need to see that at all. So we can
[5:48:24] just hold control. Unfortunately, it's
[5:48:27] getting the entire edge loop and delete
[5:48:29] those faces. Same thing up here.
[5:48:33] Control delete those faces. So now's the
[5:48:35] good time if you forget to delete some
[5:48:36] of your faces to actually start deleting
[5:48:38] them.
[5:48:40] And delete those faces. Just like that.
[5:48:42] And there you can see that, you know, we
[5:48:44] have a fairly good unwrap here. So I
[5:48:47] just unwrapped with conformal and we can
[5:48:49] move that off into oblivion if we want
[5:48:50] to. So again let's take a look at
[5:48:52] something that's slightly different. So
[5:48:54] let's take a look at text for example.
[5:48:56] Now text is fairly similar to these logo
[5:48:59] SVG logos. At the end of the day they
[5:49:02] you can just think of them like
[5:49:04] cylinders. You have a face over here, a
[5:49:06] face over here. Well I deleted the back
[5:49:08] face here. So you just have a seam along
[5:49:10] this way. Now, for some reason, even
[5:49:12] though they're merged by distance, I
[5:49:15] can't select the edge loop here. So,
[5:49:17] what I'm going to do actually for this
[5:49:19] is use smart UV project and let it
[5:49:21] handle for us. Like so. And you can see
[5:49:23] it does a good job when it's like 90°
[5:49:25] angles. It does a good job finding them.
[5:49:27] So, we can just hit A just like
[5:49:29] everything. Q seams from islands. And
[5:49:30] you can see that it does a fairly good
[5:49:32] job. Now, it is giving us these extra
[5:49:35] seams along this along the ring here.
[5:49:37] But this might actually be good in some
[5:49:39] cases because you don't want it to be
[5:49:41] too long. If you want to spend the extra
[5:49:43] few seconds optimizing where to place
[5:49:45] these, you can totally do that. But, you
[5:49:47] know, time is money. So, if you're happy
[5:49:49] with that, then you can totally just
[5:49:50] leave it as is. You can also see here
[5:49:52] they kind of have issues as well. It's
[5:49:54] going like zigzag again. But, is it
[5:49:57] worth the time to fix? So, this text is
[5:49:59] going to be the same approach. When I do
[5:50:01] the logo again, you can just treat it
[5:50:03] like a cylinder. Select the outer loop.
[5:50:05] Ctrl E mark seam. And then one of the
[5:50:07] sides, control E mark seam. And this is
[5:50:10] kind of unnecessary over here. Clear
[5:50:11] seam. So the L is kind of unwrapped
[5:50:14] properly. If you want to add extra seams
[5:50:16] because it's too long, the ring is too
[5:50:18] long, you can totally do that. Again,
[5:50:20] you know, why spend the extra time when
[5:50:22] UV unwrap can do it properly. So you
[5:50:24] smart UV project wrap. This looks okay.
[5:50:28] Q seamst islands. So, if I look at it,
[5:50:30] you know, generally it looks okay, but
[5:50:32] there's definitely some things that
[5:50:34] would cause, you know, a little bit
[5:50:35] complicated packing issues like this
[5:50:37] thing over here or this L here. Yes, you
[5:50:41] can put stuff inside, but then it kind
[5:50:43] of looks a little bit weird that you
[5:50:44] have something wrapping some something
[5:50:46] that's unrelated. But again, it's not
[5:50:48] really a big deal. So, you can just
[5:50:51] leave it as is and save your time and
[5:50:52] move that into Oblivion.
[5:50:54] So, again, nothing really special here.
[5:50:57] You just select the edge loop. Hopefully
[5:50:59] this one you can get a complete one. So,
[5:51:02] and maybe like this. Control E mark
[5:51:03] seam. You can see that's going to work
[5:51:05] fairly well. But again, but you know,
[5:51:07] instead of just doing one at a time, we
[5:51:09] can just select all of them. Again, make
[5:51:11] sure for each of these baking is
[5:51:12] highlighted. Your second UV map UV
[5:51:15] unsmart UV project Q scenes from
[5:51:18] islands. Okay, cool. Good enough for us.
[5:51:21] So, we can start moving these into our
[5:51:22] unwrapped collection. And we can just
[5:51:24] uncheck unwrapped if we want to. So,
[5:51:26] let's take another example. We can
[5:51:28] review the rounded cube again or the
[5:51:30] subdivision cube, right? All of these
[5:51:32] were subdivided cubes. So, you can kind
[5:51:35] of already envision how we're going to
[5:51:36] unwrap. You know, take like one of these
[5:51:38] circles, right? Sorry, I guess they're
[5:51:39] not circles, but like one of these tops
[5:51:41] and then cut along the sides. Same with
[5:51:43] this one. We could do something like
[5:51:46] here, cut out the ring. And then maybe,
[5:51:49] you know, have one on four corners. And
[5:51:51] then for the top, it's like a elongated
[5:51:53] sort of curved cube. So in that case
[5:51:57] then it kind of makes sense to cut out
[5:51:59] the center part and a little bit of the
[5:52:01] sides. That way when it's flattened it
[5:52:04] can be flattened easily. So if I do
[5:52:05] smart UV project
[5:52:08] unwrap huge seams from islands you can
[5:52:10] see that's kind of exactly what we get.
[5:52:12] They're trying to cut off a little bit
[5:52:14] of the top. So it's easier to flat this
[5:52:16] than a completely bent piece of paper.
[5:52:18] And obviously the angles over here are
[5:52:20] going to be easier to bend. Then when it
[5:52:22] comes to the headphones, again, they do
[5:52:24] they mess up a little bit here with the
[5:52:26] with not being parallel. So if you want
[5:52:28] to fix that, you can do that. Mark seam
[5:52:31] and you can just clear out the seams
[5:52:32] over here
[5:52:35] and add, you know, more seams and then
[5:52:38] add seams over here. Control E, mark
[5:52:40] seam. Get rid of that. So that
[5:52:43] definitely looks a lot better. They
[5:52:44] actually seem to do the inner one
[5:52:46] consistently, which is nice. And then
[5:52:48] same if you want to polish up this side
[5:52:50] as well, you can totally do that. Is it
[5:52:53] necessary? You know, is it necessary?
[5:52:56] Again, probably not. But, you know, if
[5:52:59] you want to be clean, you can totally do
[5:53:01] that.
[5:53:04] Then maybe we can just clean it up just
[5:53:05] a little bit more. And then maybe we can
[5:53:08] clean this up just a little bit more.
[5:53:15] And then we can keep this consistent.
[5:53:18] And then we can keep this consistent
[5:53:19] along the outer edge.
[5:53:22] Mark seam
[5:53:24] Q clear seam. Q clear seam. You know,
[5:53:28] sometimes it might be better just to
[5:53:29] start from scratch then update the one
[5:53:31] that UV unwrap gives us, but sometimes
[5:53:34] it's just fun just to have some fun if
[5:53:36] that makes sense. So here I'm just
[5:53:38] polishing up the corners. Just holding
[5:53:41] control, getting rid of them. Ctrl + E,
[5:53:43] mark seam. Looks a little bit better
[5:53:45] here. This one is also not consistent.
[5:53:47] And then here you can see that this
[5:53:49] isn't consistent either. Yeah. So, if
[5:53:51] you want to polish them up, you totally
[5:53:52] can, but you know, not really a big deal
[5:53:54] for us. Now, it might be worth
[5:53:56] straightening these out with UV squares,
[5:53:58] but we can actually determine that later
[5:54:00] once we start baking. So, I did some a
[5:54:02] little bit more unwrapping, but
[5:54:04] honestly, there's nothing really new at
[5:54:05] this point that you can't already do on
[5:54:08] your own. So, I kind of just want to
[5:54:09] give you a little bit more tips and
[5:54:11] tricks and then let you go and unwrap
[5:54:13] your scene yourself. Now, if you have
[5:54:14] all the same UV map, so all of these
[5:54:17] objects have the simple bake here. I'm
[5:54:19] going to be using a simple bake add-on
[5:54:20] just because it's a lot faster. It's
[5:54:23] paid and it's $8, but when we bake, I'm
[5:54:26] going to be doing it the free way. I'm
[5:54:27] just doing it this because I'm going to
[5:54:29] be using this in the future. But don't
[5:54:31] worry, you know, when we do it, we're
[5:54:32] going to do it completely free natively
[5:54:34] in Blender. With this one, which is
[5:54:36] appropriately unwrapped, we can do Ctrl
[5:54:39] L and copy UV maps. And you can see even
[5:54:41] though these are distorted, they have
[5:54:42] the same geometry and the copying the UV
[5:54:46] map works. So instead, so we don't have
[5:54:49] to do anything. And now we can just hit
[5:54:50] A and then hit A here. Q seams from
[5:54:53] islands. And you can see all the seams
[5:54:55] are going to transfer from there. And uh
[5:54:57] yeah, definitely, you know, if you don't
[5:54:59] if you already applied your modifiers or
[5:55:00] don't have a modifier one, definitely
[5:55:02] definitely save your time with copy EV
[5:55:04] maps. You can see all these have
[5:55:05] different distortions and everything,
[5:55:06] but they have the same geometry, so they
[5:55:08] all work. Q seams from islands. You can
[5:55:11] see I just applied them all just like
[5:55:13] that. So I don't have to manually select
[5:55:14] every single one. I know there are
[5:55:16] add-ons that if you have the same
[5:55:18] geometry like this leaf, then you
[5:55:20] wouldn't have to select the geometry on
[5:55:23] this leaf as well, which speeds up your
[5:55:25] workflow even faster. But again, I'm not
[5:55:28] going to be using paid on. So the second
[5:55:30] tip I'll show you is that we talked
[5:55:33] about our subdivided cubes. You know how
[5:55:35] we unwrap Mr. Rabbit kind of like this?
[5:55:38] Well, that's kind of how I did almost
[5:55:39] every single thing that was a subdivided
[5:55:42] cube at one point. You can see I just
[5:55:44] take the top. I find where the middle
[5:55:46] comes to this diagonal sort of corner
[5:55:48] and then I just cut it there and I do it
[5:55:50] on both sides. Same thing over here. You
[5:55:53] can also see that for the microphone
[5:55:54] here. These were subdivided cubes. So, I
[5:55:56] just cut it like so. And of course, I
[5:55:58] deleted some extra faces over there. And
[5:56:00] every time I follow this method, I get
[5:56:02] very, very good unwraps, minimal
[5:56:04] distortion, and seemingly equal tixel
[5:56:06] density. So that even goes for these. So
[5:56:09] these were extruded cubes. Like I had a
[5:56:12] cube over here and I just extruded this
[5:56:14] way and extruded this way and then added
[5:56:16] a subdivision surface. So applied it.
[5:56:19] You can see that we kind of have the
[5:56:21] same pattern over here. So what I did is
[5:56:24] I just find these find where they
[5:56:26] connect to their to the other one. For
[5:56:29] example, on this side, let me just go
[5:56:31] into local view here like so. And
[5:56:34] basically I'm just finding the areas
[5:56:36] that have the diagonal and connecting
[5:56:38] those up
[5:56:43] right here. So we got square square over
[5:56:45] there. Control E mark seam. And now if I
[5:56:49] just give this a material that we can
[5:56:50] see that thing on. You can see that we
[5:56:53] get a great unwrap here. Minimal
[5:56:54] distortion and equal texo density all
[5:56:57] just by following the same exact method.
[5:57:00] And that's exactly the same method
[5:57:01] actually when we used our iPhone. Same
[5:57:04] thing when I used my flower, the flower
[5:57:06] center over here. Same thing with the
[5:57:08] basket itself. This is also a subdivided
[5:57:10] cube. I did cut out these extrudes, but
[5:57:12] you can see the general shape of the
[5:57:14] subdivided cube is still the same. I
[5:57:15] just found that edge, found the corner,
[5:57:17] and cut it out just like that. So,
[5:57:19] another really quick tip and trick and I
[5:57:21] guess intuitive idea is in instead of
[5:57:24] cutting it like this for subdivision
[5:57:26] surface cubes because they're so quick
[5:57:28] together, you could easily just get
[5:57:30] array with a slice down the middle like
[5:57:33] here or here. Control E mark seam. And
[5:57:36] if you take a look, that is actually
[5:57:37] very very good for what we're going for.
[5:57:39] It maximizes texture space and there's
[5:57:41] minimal distortion. You can ignore that
[5:57:43] because I didn't put seams on those.
[5:57:44] Now, logically, how does this make any
[5:57:46] sense? Well, think about if you had a
[5:57:48] regular cylinder. So, let me just add a
[5:57:51] cylinder real quick and just let me add
[5:57:53] a loop cut here and then unwrap it. And
[5:57:55] I'm just going to use conformal. And let
[5:57:57] me just delete the top and bottom faces
[5:57:59] and only focus on this area right here.
[5:58:01] So, if you can imagine this, this and
[5:58:04] this is exactly just like the cylinder.
[5:58:07] Then that means we can just add a seam
[5:58:08] down the center. So, let's just do that.
[5:58:10] Ctrl E mark seam. And now take a look at
[5:58:13] how we are unwrapping. So essentially
[5:58:14] what it's doing is taking all these
[5:58:16] faces and pressing them down. Now in
[5:58:18] real life that would be impossible
[5:58:19] without ripping the paper. So there's a
[5:58:21] lot of stretching here. But because we
[5:58:23] subdivided something so many times like
[5:58:26] this, there's actually so many faces
[5:58:28] that when you push it down, it doesn't
[5:58:30] actually really matter anymore. Look how
[5:58:32] squashed it is together. So imagine if
[5:58:34] you had one piece of paper or one half
[5:58:36] of paper that kind of looked like this
[5:58:37] and they just asked you to push it down
[5:58:39] flat on the ground. Well, it would
[5:58:40] actually be really easy, right? You can
[5:58:41] imagine like this would scale up this
[5:58:43] way until it goes flat. And this one
[5:58:45] would also scale up until it goes flat
[5:58:47] as well if you like push from this side
[5:58:48] downwards. And we can visualize that
[5:58:50] with the cylinder. If I add let's say I
[5:58:54] don't know like five loop cuts, I don't
[5:58:55] know that might have been six. I'll just
[5:58:56] type six like so. And now I hit you
[5:59:00] conformal. Take a look at what happens.
[5:59:02] The ring becomes less of an issue. So if
[5:59:04] I do it again, I'm going to subdivide
[5:59:06] and again and then I do conformal. So
[5:59:09] now take a look. You can actually see
[5:59:11] that we have solid blue faces along a
[5:59:13] lot portion of the cylinder. And that
[5:59:16] makes intuitive sense because if we push
[5:59:18] down on one of these, we have so many
[5:59:20] faces that the stretching is being
[5:59:22] miticated by all those faces. So that's
[5:59:25] kind of like the same idea that we have
[5:59:26] over here, which is why we can just cut
[5:59:28] over here and be perfectly fine. So you
[5:59:30] know, if you just want to be speedy, you
[5:59:32] can just, you know, do something like
[5:59:33] that. Same thing with here. Ctrl E mark
[5:59:36] seam just like that. And you'll get a
[5:59:37] pretty good unwrap for what you're going
[5:59:39] for. it'll pack well and it has even
[5:59:42] texo density. So that's exactly what I
[5:59:44] did for the plants here, these are also
[5:59:46] subdivided cubes, but instead of cutting
[5:59:48] it with the diagonals, I just went with
[5:59:50] cutting it slight right down the center
[5:59:53] middle. Additionally, I'll also say when
[5:59:55] it comes to subdivided cubes, I did make
[5:59:57] quite a few topology errors here. So
[6:00:00] generally, you know, you don't want you
[6:00:02] want to work in quads, yes, but you also
[6:00:04] want to work in things that kind of have
[6:00:06] the same size across your object unless
[6:00:09] there's like more detail in certain
[6:00:10] areas. But in this case, you can see
[6:00:12] that I have multiple faces that are very
[6:00:14] different sizes across the object and
[6:00:16] it's not very ideal. So because the
[6:00:18] topology is not really ideal, the unwrap
[6:00:21] isn't really ideal either. You know,
[6:00:22] these seams, while they are, you know, a
[6:00:25] subdivided cube, they're in really
[6:00:26] awkward sort of positions. So in this
[6:00:29] case, the bad modeling led to a bad
[6:00:31] unwrap. For us, it doesn't really
[6:00:32] matter. So I'm not going to bother
[6:00:33] fixing it. But just something to note.
[6:00:36] That is also why I made this over here.
[6:00:38] And here I changed this to arc, right?
[6:00:40] So if I apply this, you can see that the
[6:00:42] topology here definitely looks a lot
[6:00:44] better than what we did than what I
[6:00:47] accidentally did over here. Here I
[6:00:49] didn't use arc. So you can see that the
[6:00:51] bevel looks like this. And it's a little
[6:00:53] bit messy here. Now, it didn't really
[6:00:55] end up affecting the unwrap, but you
[6:00:57] know, going for the arc would have been
[6:00:59] definitely easier to unwrap and it
[6:01:01] wouldn't have been as distorted along
[6:01:03] the corners, but again, not really a big
[6:01:04] deal. You can see that I also for the
[6:01:07] legs here, I didn't use arc. So, we also
[6:01:11] have that messed up topology here.
[6:01:12] Again, not really a big deal, but you
[6:01:14] know, ideally, you would want to use arc
[6:01:16] in the future. So, when it comes to the
[6:01:18] wheels, you can see I also did that half
[6:01:20] cut method here, just like on the
[6:01:22] leaves. For the wheels, they're just
[6:01:23] cylinders. So, I cut them like
[6:01:24] cylinders, right? I just cut them over
[6:01:26] here and then just slashed on the edge
[6:01:28] there. So, you can see decent unwrap
[6:01:30] over here. For this middle thing, you
[6:01:31] can see, oh, it's just a cylinder. So, I
[6:01:33] just gave it one slash over there. For
[6:01:34] the computer, I just used smart UV
[6:01:36] project. It did a fairly decent job for
[6:01:38] me, so I didn't really touch that at
[6:01:40] all. It's a little bit messed up as you
[6:01:42] can see, but, you know, I just wanted to
[6:01:44] save some time there. Again, this is all
[6:01:46] subdivision cube. So, it's all all of
[6:01:49] these unwraps were identical just in
[6:01:51] different shapes and things like that.
[6:01:52] Another quick tip is if you can't select
[6:01:55] by area like we did for the piano, you
[6:01:57] can just go into local view, go into
[6:01:59] wireframe, and just box select like
[6:02:01] this. Hold shift box select like this.
[6:02:03] And then you have, you know, those faces
[6:02:05] selected if you want them. And then
[6:02:06] control E mark just like that. Another
[6:02:08] trick, definitely use ctr L, cr I and H
[6:02:12] very, very frequently, especially if
[6:02:14] your objects are joined. Like here, I
[6:02:16] accidentally joined them early. So it's
[6:02:17] like, okay, how do I even see what I'm
[6:02:19] looking at? You could probably do like
[6:02:20] something like this, you know, and just
[6:02:22] like select it, Ctrl+, hide this, or,
[6:02:26] you know, instead what you can do is
[6:02:27] just like we did for the piano, select
[6:02:30] the individual object, Ctrl L. So now I
[6:02:32] have seams. So just it would select the
[6:02:34] entire thing without seams. But I just
[6:02:36] do Ctrl+ instead, then Ctrl I, then
[6:02:38] hide. And now you can just have these
[6:02:40] two unwrap yourself. And then of course,
[6:02:42] Alt H to get them back, just like so. So
[6:02:45] for all the hanging wires and those
[6:02:47] curves that we converted to meshes, all
[6:02:50] of them are just cylinders basically. So
[6:02:53] that's kind of all I did. I just deleted
[6:02:56] the two caps and then sliced it down
[6:02:58] along the center. So just using control.
[6:03:01] And if you accidentally mis select the
[6:03:03] control and see like a zigzag, just undo
[6:03:06] and just do it again until you get it
[6:03:07] right. And then if it's a little bit too
[6:03:09] long, I just cut it in half over here.
[6:03:11] So that's why I have this seam here. And
[6:03:13] you can see just like that, it cut the
[6:03:15] wire into half and it packs fairly well.
[6:03:17] It looks really good. Another tip, if
[6:03:19] you are selecting a bunch of things, I
[6:03:21] guess I should have mentioned it way
[6:03:22] earlier in the video, even modeling, if
[6:03:24] you select a bunch of things and
[6:03:25] accidentally mess up your selection,
[6:03:27] just hit Ctrl +- Z. And if you
[6:03:29] accidentally get rid of your selection,
[6:03:30] just hit Z. It will go back to your
[6:03:32] original selection, so you don't have to
[6:03:34] select everything over again. So,
[6:03:36] another quick tip for copying your UV
[6:03:38] maps. Instead of typing this every
[6:03:40] single time, double clicking and typing
[6:03:42] it for every single object. All you have
[6:03:44] to do is just Ctrl + C and then on the
[6:03:48] new object, just create a new one and do
[6:03:50] Ctrl +V and it will just paste the name
[6:03:52] right there. You don't even have to
[6:03:54] double click. It'll just rename it for
[6:03:55] you and it won't replace your original
[6:03:57] one. So, it'll just change the name
[6:03:59] itself. So, you can see I still have
[6:04:01] everything retained there. So before we
[6:04:02] move on to baking, why don't we render
[6:04:04] out an image that we can share with our
[6:04:06] friends. So again, if you don't have a
[6:04:08] camera, so if you don't have a camera,
[6:04:09] just add a camera and then find a place
[6:04:12] you like and then Ctrl Alt numpad zero
[6:04:14] just to snap your camera to view. And
[6:04:17] then you can make sure to select your
[6:04:18] camera and then just GG to move it into
[6:04:20] position. You can see that on my camera
[6:04:23] I'm using orthographic. You know, feel
[6:04:24] free to use perspective and, you know,
[6:04:27] do multiple angle renders if you want to
[6:04:29] as well. I'm just going to be doing an
[6:04:31] orthographic view. Just frame it like
[6:04:33] so. Let's go into rendered view. And
[6:04:35] let's find our unwrap collection and
[6:04:37] just turn that back on. All right, cool.
[6:04:40] So, now we can just frame this up. By
[6:04:42] the way, if you want a render region,
[6:04:44] you can do Ctrl +B. And that's why mine
[6:04:46] is limited. And if you also want to see
[6:04:47] that, you can come over into scene and
[6:04:50] you can click render region and things
[6:04:51] like that. So, in here, I'm going to
[6:04:53] keep it at 20480 by 2480. But, you know,
[6:04:56] if you want to change your picture
[6:04:58] resolution, you can totally do that.
[6:04:59] Like 10 1920 x 1080, you know, refframe,
[6:05:02] whatever you want to do. I'm just going
[6:05:03] to go for 20480. The render settings.
[6:05:06] Now, we can come over here. Again, make
[6:05:08] sure you're in cycles. Then, under
[6:05:11] render, we want a very low noise. So,
[6:05:13] this should be good. 256 might be a
[6:05:16] little bit overkill, so we can just
[6:05:17] divide by two. We probably wouldn't
[6:05:19] notice anything as well. And then we
[6:05:21] want to d noiseise the image. So, D
[6:05:23] noiseis, I'm putting it high. And then
[6:05:25] I'm using my GPU. If you want to
[6:05:27] optimize it a little bit, you can come
[6:05:28] into light pass and then change the
[6:05:30] amount of how many bounces for lights.
[6:05:32] So you can put that down like eight.
[6:05:34] Honestly, you can probably put it down
[6:05:35] to six and have it work fine. And for
[6:05:37] performance here, you can also come down
[6:05:39] to memory and do use tiling. And
[6:05:41] basically what use tiling will do is
[6:05:43] it'll render your image in chunks. So
[6:05:46] instead of going like one at a time, and
[6:05:48] this will usually be faster. So I like
[6:05:51] to do 256 x 256 chunks. But, you know,
[6:05:54] if your computer's good, you probably
[6:05:55] don't have to do that anyway. So, now
[6:05:57] that it's good, let's just go into
[6:05:59] wireframe. It's quote unquote supposed
[6:06:01] to make your computer a little bit less
[6:06:04] taxing when you render if you have your
[6:06:06] viewport in wireframe. That's probably a
[6:06:08] marginally minuscule amount, but you
[6:06:10] know, whatever. So, we're just going to
[6:06:11] hit F12. And now you can see it's going
[6:06:13] in 256 chunks across my 20480x 20480
[6:06:17] picture. Seems like it's done. We can
[6:06:19] just do image, save as, and save it
[6:06:22] whatever you want to do it. All right.
[6:06:23] When it comes to baking, like I showed
[6:06:25] earlier when we were looking at some
[6:06:27] award-winning websites, we need to put
[6:06:29] our shared UV map onto a single image
[6:06:31] texture. So, we can actually create
[6:06:32] that. So, just like this texture over
[6:06:35] here, we can actually start deleting
[6:06:36] these if you don't want them anymore.
[6:06:37] And also, when I go back in solid view,
[6:06:40] I'm going to go over here and instead of
[6:06:42] using texture, I'm going to go to
[6:06:44] material again. Back to default.
[6:06:46] Everything seems a little bit weird now
[6:06:48] cuz we've been looking at grids for so
[6:06:49] long. So now what we want to do is you
[6:06:51] can create it in the material, any
[6:06:53] material you want, or you can come into
[6:06:55] the UV editor and just create it here.
[6:06:57] So I'm going to create it over here in
[6:06:58] the UV editor. We're going to go for 4K.
[6:07:00] Click and drag my mouse down. 1024 * 4
[6:07:04] 4K texture. And we'll just call this
[6:07:06] texture set one, but you know, name it
[6:07:09] whatever you want. I honestly don't
[6:07:10] know. And then we want to do 32-bit
[6:07:12] float. This will just make a more high
[6:07:14] dynamic range image so we get better
[6:07:16] colors. We're not going to be baking
[6:07:18] anything with transparency because I
[6:07:20] don't have transparency anyway here
[6:07:21] except the glass, but we're replacing
[6:07:23] the glass, which I'll talk about just in
[6:07:25] a little bit. So, let's uncheck alpha.
[6:07:26] Now, when you're baking with color,
[6:07:28] sometimes the image texture color bleeds
[6:07:30] into the model itself. Not always, and
[6:07:33] honestly, it doesn't really matter that
[6:07:35] much, but I like to go for white. And
[6:07:37] I'm just going to create a new image
[6:07:39] just like that. Make sure to alt s and
[6:07:41] save this somewhere. And when you save
[6:07:43] it, save it as a radiance HDR image. And
[6:07:46] this will just be an image format that
[6:07:48] captures a wider range amount of colors.
[6:07:50] If we bake in like PNG or JPEG or some
[6:07:54] other lower bit image format, it won't
[6:07:57] capture as many good colors. Now, it
[6:07:58] might not be noticeable, but typically
[6:08:00] if you want the best result, you'll go
[6:08:02] for like a high dynamic range and then
[6:08:04] later you can convert it down here. So,
[6:08:06] basically, you have more information and
[6:08:08] then you go to lower information, which
[6:08:10] is a much better result than, you know,
[6:08:12] starting at lower information if that
[6:08:14] makes sense. So we're going to start
[6:08:15] with this. We can just save this image.
[6:08:17] Okay. So this is going to be our first
[6:08:19] texture set that we bake to. So we can
[6:08:21] select I don't know any random object
[6:08:23] maybe like these or something. Again
[6:08:26] make sure they all have simple bake and
[6:08:27] all those ones that are highlighted. It
[6:08:29] doesn't really matter which one is being
[6:08:30] rendered because we don't use the UV map
[6:08:32] for anything. But as just make sure that
[6:08:34] this is highlighted like so. So now what
[6:08:36] we can do is again you can select each
[6:08:40] individual one. So you can just do the
[6:08:42] Ctrl+ select all these set of UVs and
[6:08:44] just see what that looks like here.
[6:08:46] Now's the time where you move around.
[6:08:48] You know, you can select all UVs and
[6:08:50] just kind of move them around. See what
[6:08:52] it gets you. Just like so. And now what
[6:08:55] your goal is to do is to pack your
[6:08:57] islands. So adjust them how you need and
[6:09:01] optimize them to in your island. And
[6:09:04] it's kind of just like that. And it's
[6:09:06] just like that. So if you want, you can
[6:09:08] move individual faces if you want. You
[6:09:10] know, you can move individual faces.
[6:09:12] Ctrl L move individual things and just
[6:09:15] pack it to the best that you can. And of
[6:09:17] course, you don't want overlapping UVs
[6:09:19] because we're trying to bake lighting
[6:09:21] information. And if you have overlapping
[6:09:22] UVs, you know, it's going to bake twice
[6:09:25] over the same spot and kind of glitch
[6:09:26] out. The entire goal now is just to pack
[6:09:29] the island. Now, obviously, if you do
[6:09:30] this manually, it will take a really
[6:09:32] long time for our scene. So generally
[6:09:34] what you like to do is assuming you all
[6:09:37] use the same UV mapping method. If you
[6:09:40] did anglebased for some, conformal for
[6:09:42] others or minimum stretch for others,
[6:09:44] just make sure you remember that when
[6:09:45] you're unwrapping. Again, I used
[6:09:47] conformal for everything. But for these
[6:09:49] more organic models, like these for
[6:09:52] example, you might get slightly better
[6:09:54] results with like minimum stretch, but
[6:09:56] honestly, they haven't been noticeable
[6:09:57] for me. Anyway, let's go here and we can
[6:10:00] just do U unwrap and do conformal. and
[6:10:03] I'll try and pack it for us. Now, what
[6:10:05] this suggests is that, okay, we can add
[6:10:07] a lot more objects to the scene, which
[6:10:09] is great. And if you want to actually
[6:10:10] pack it a little bit better, you can go
[6:10:12] into UV and see this thing here called
[6:10:14] pack islands. And then if you hit pack,
[6:10:16] you can see it definitely uses a lot
[6:10:18] more texture space now, you know,
[6:10:19] maximizing the amount of resolution for
[6:10:21] each area. And then, of course, the
[6:10:23] sizing is relative to how big it is
[6:10:25] relative to all the other objects on the
[6:10:27] scene. So, the larger objects are
[6:10:29] definitely taking up more area on the
[6:10:31] space. Now, this is also the time to
[6:10:33] determine how much texo density you
[6:10:34] actually want on each face. So, this
[6:10:36] might be more clear on like this piano
[6:10:38] for example. So, if I just take it, move
[6:10:40] it over here like so. Right now, if I
[6:10:44] select this side of the face, it has the
[6:10:47] same sort of mapping as this side of the
[6:10:50] face. But the issue is this side of the
[6:10:53] face will rarely be looked at, if looked
[6:10:56] at at all. I don't know. Maybe I could
[6:10:58] delete that. I don't know. But assuming
[6:11:00] you'll see a little bit of it, you could
[6:11:02] actually make this face a lot smaller on
[6:11:04] the UV map and then repack it. You lower
[6:11:07] the resolution of that face. Well, that
[6:11:08] means you can actually increase the
[6:11:10] resolution of this place because now you
[6:11:12] have more space on your texture.
[6:11:14] Obviously, you'd have to move things
[6:11:15] around, but you get the idea. So, here's
[6:11:17] also the time where you can like
[6:11:19] determine that. Now, obviously, that
[6:11:20] takes a lot of time. So, would I even
[6:11:22] bother for this scene? Probably not
[6:11:24] because we're working with solid colors.
[6:11:26] But if you do notice an issue and you do
[6:11:28] want to make that trade-off, you can
[6:11:30] totally do that. Also, a lot of other
[6:11:31] options here, but they haven't been
[6:11:33] working really great for me. In some
[6:11:35] cases, they might work like average
[6:11:37] island scale and minimize stretch. You
[6:11:39] could totally try these out, but
[6:11:40] typically paid add-ons do this a lot
[6:11:42] better than Blender natively. So, one
[6:11:45] that I really recommend, it's $39, but
[6:11:47] it saves you a lot of time, is UV
[6:11:50] Packmaster. So, you can see if I do, let
[6:11:53] me just do the Blender pack first. So
[6:11:56] here you can see I did the blender pack
[6:11:58] and honestly it did a fairly good job.
[6:12:01] Now you can see there's still some extra
[6:12:02] stuff over here. But look what happens
[6:12:04] when I do the UV packmaster pack. It
[6:12:07] gets very very much more texture space
[6:12:10] out of there. You'll see that it also
[6:12:12] has a lot of lot of other options here.
[6:12:14] One of them is important is margin which
[6:12:17] is also in Blender by the way and that's
[6:12:19] how much space is between your islands.
[6:12:23] And you need space between there because
[6:12:24] when you bake, sometimes it bleeds
[6:12:26] outside of these lines. So those can
[6:12:28] overlap. And additionally, if they're
[6:12:30] like touching each other or on top of
[6:12:31] each other, your colors are going to
[6:12:33] start mixing and one texture might
[6:12:35] appear on a different area of the model
[6:12:37] that isn't intending to have that color
[6:12:39] at all. So let's go back to these over
[6:12:41] here and let's just go into edit mode
[6:12:44] and let's just bake these. So the way to
[6:12:46] bake them is for every single material
[6:12:48] you have to create an image texture and
[6:12:51] you have to make sure it's the active
[6:12:52] one for the texture that you're baking
[6:12:54] to. So here we can just search for
[6:12:55] texture set one and we don't have to do
[6:12:58] anything you know just make sure it's
[6:13:00] highlighted outline. So now it's in this
[6:13:02] room here. So it's going to bake onto
[6:13:04] this texture like so. Then we come into
[6:13:07] render properties like we did before.
[6:13:09] And we can leave all of these the same
[6:13:10] as our image. Low noise 128 samples.
[6:13:14] However, we want to uncheck D noiseis
[6:13:16] here. The reason we want to uncheck D
[6:13:18] noiseis here is because Blender has a
[6:13:20] baking issue in cycles when you have D
[6:13:22] noiseis on. And you can see over here
[6:13:24] when you are baking, you might get like
[6:13:26] these black sort of lines here. And
[6:13:28] that's caused by if you have D noiseis
[6:13:30] activated. And this was open 4 years ago
[6:13:33] and it's still open, which means they're
[6:13:34] working on it. And you can kind of see
[6:13:36] like someone suggested something 3
[6:13:38] months ago. It's still an ongoing issue.
[6:13:41] So if you bake in cycles with D noiseis
[6:13:43] on, you might get some black lines along
[6:13:45] your seams. So I'm going to check here
[6:13:46] and we'll use the Blender compositor to
[6:13:49] D noiseis our image instead. So under
[6:13:51] bake, you know, we can do everything. So
[6:13:53] combined takes into consideration
[6:13:55] everything. So we're just going to leave
[6:13:57] everything here, all the lightings, all
[6:13:59] the contributions, everything like so.
[6:14:00] Now, we don't want to clear the image
[6:14:02] before every bake. If you do, then you
[6:14:04] can just attach that, but we don't
[6:14:06] because we're going to be baking
[6:14:07] multiple things to it. But if you mess
[6:14:08] up a bake and you want to clear the
[6:14:10] image, you know, you can totally just do
[6:14:11] clear image. And here, this by default
[6:14:14] is just like how much it bleeds across
[6:14:16] the seams of your UV islands. That way
[6:14:19] it'll kind of help, you know, minimize
[6:14:20] how visible your seams are. And
[6:14:22] generally 16, the default, works
[6:14:24] perfectly fine. I don't think I've ever
[6:14:26] had to change that in in a long time.
[6:14:28] Again, make sure this is active. And
[6:14:30] make sure that simple bake is and make
[6:14:33] sure your baking UV map is the one
[6:14:35] that's highlighted. Mine's called simple
[6:14:36] bake. yours is just called whatever. Oh,
[6:14:39] and I also forgot to mention like in
[6:14:41] every single material that your room
[6:14:44] has, you want to copy and paste the
[6:14:46] image texture. So, in wood, also paste
[6:14:49] this here. Make sure it's active. In
[6:14:51] outlet, also post it here. Anywhere,
[6:14:54] make sure it's active with the white
[6:14:56] outline. Okay. Now that each of the
[6:14:59] rooms materials has this active image
[6:15:01] texture, we should be able to good and
[6:15:04] just bake.
[6:15:06] Awesome. So, just make sure to hit alt s
[6:15:08] to save it. And you hit alt r to refresh
[6:15:11] your image. Just like so. And now if I
[6:15:13] go into rendered view and then if I go
[6:15:15] here and put this into my principled
[6:15:17] BSDF, we see completely black. And
[6:15:20] that's because what we're doing is
[6:15:21] rendering with this one. So switch the
[6:15:23] render to here. And now you can see what
[6:15:26] we get if I go into render view is our
[6:15:30] image texture mapping to this. So let's
[6:15:32] just go into local view. And you can see
[6:15:34] that we see here. And take a look. All
[6:15:36] those seams that we thought were going
[6:15:39] to be concerns are actually not really
[6:15:41] visible in the final output, which is
[6:15:43] amazing. Now you can see all that grain.
[6:15:45] So that's the noise on the texture,
[6:15:47] which we can d noiseise with the
[6:15:48] compositor later. For all intended
[6:15:50] purposes, this is actually looking like
[6:15:52] a pretty decent result. Now, because
[6:15:54] it's in the principled BSDF, the world
[6:15:56] lighting is also going to affect this
[6:15:58] lighting. So pretty pretty cool. So
[6:16:00] let's move on to the roof then. So, I'm
[6:16:03] just going to unhook that. Put this back
[6:16:04] in here. Switch this back to UV map. Not
[6:16:07] that that actually affected anything
[6:16:09] because we didn't use our UV map for
[6:16:11] anything. And now I'm just going to go
[6:16:12] out of local view. And we do the same
[6:16:14] exact thing for this. Just make sure for
[6:16:16] all the materials in this object, which
[6:16:18] is just wood. This is active. And it's
[6:16:21] already unwrapped and mapped to our
[6:16:23] texture right here. Just like this. So,
[6:16:26] we can just go here and then we can hit
[6:16:28] bake. And then let's go into wireframe.
[6:16:30] Now here you can see when I baked I made
[6:16:32] two issues. First I had clear image on
[6:16:34] for some reason. I thought I unchecked
[6:16:36] that. Oh well. So it cleared my other
[6:16:38] bake. The second issue is that
[6:16:40] everything on my texture is black which
[6:16:42] suggests that my normals are incorrect.
[6:16:45] So if I go here indeed this is
[6:16:47] incorrect. So I just have to select
[6:16:49] everything al flip. And now everything
[6:16:52] should be okay. And we should be able to
[6:16:54] bake two things at once just by
[6:16:55] selecting them. So we can just do that
[6:16:58] and just do bake. Awesome. And you can
[6:16:59] see that everything baked properly.
[6:17:01] That's super super cool. And again, if
[6:17:03] you want to preview it, you kind of
[6:17:04] already know how to do that. So, I'm not
[6:17:06] going to show you anymore. Again, always
[6:17:08] make sure to hit alt s to save it. Or if
[6:17:11] you want to version, you can do image
[6:17:12] and save as or save a copy, whatever.
[6:17:14] You'll also notice now again, we get
[6:17:16] some things like here. So, this kind of
[6:17:18] suggests that something is blocking the
[6:17:20] light and we have probably an extra face
[6:17:22] that we don't need somewhere. So, if I
[6:17:24] go into my room, it kind of looks like
[6:17:26] there's some sort of light leaking in
[6:17:28] here. And that kind of suggests that
[6:17:30] it's right here. So, if I go into
[6:17:32] rendered view and just hide this,
[6:17:34] indeed, we kind of have like this face
[6:17:36] here that no one really sees and it
[6:17:38] takes a huge portion of our texture. So,
[6:17:43] what are we going to do? Are we going to
[6:17:44] lower it and then re-ake it so it takes
[6:17:46] less resolution, but it still exists? Or
[6:17:48] are we just going to delete it and hope
[6:17:50] no one can tell? Okay, so let's take a
[6:17:52] look at what it would look like if we
[6:17:54] didn't have this. So, let's go into
[6:17:55] render view. Now, this is what it looks
[6:17:57] like if the floor is there. Now, let's
[6:18:00] hide this and let's go into edit mode
[6:18:01] and let's delete this face. Now, let's
[6:18:03] alt h just to get this back. Will people
[6:18:06] notice from a distance? From close, they
[6:18:09] can definitely tell that there is
[6:18:11] nothing there. But from far away, can
[6:18:13] people tell? And the answer is probably
[6:18:16] no. Which means we don't actually need
[6:18:19] that face taking up this sort of texture
[6:18:22] space here. We can actually just leave
[6:18:23] it deleted. So, if you unwrap and pack
[6:18:25] again, it'll probably be different now
[6:18:27] that this face is gone. So, if you have
[6:18:29] a different packing, you'd have to clear
[6:18:31] your image or create a new image texture
[6:18:33] if you wanted to do that way. But, if
[6:18:34] you had the same UV mapping on your
[6:18:36] texture, you could just bake right over
[6:18:38] the existing colors and it would just
[6:18:39] replace them. But since our unwrap is
[6:18:42] likely going to be different now, if I
[6:18:44] do UV unwrap conformal UV packs,
[6:18:49] you can see the pack is definitely
[6:18:51] different here. And of course, if you're
[6:18:53] packing manually, you know, it's
[6:18:54] definitely going to look different. So
[6:18:56] here you can see this takes a larger
[6:18:58] portion now. Same with over here because
[6:19:00] we have more texture space to pack. So
[6:19:02] you can bake in portions like you can
[6:19:04] bake these two first and then with your
[6:19:06] remaining texture space, you can maybe
[6:19:08] tack this on over here and then like put
[6:19:10] it over here and kind of just see, you
[6:19:13] know, where you can fit it. Like here
[6:19:15] for example, you're like, "Oh, okay. I'm
[6:19:17] just going to select this, you know,
[6:19:19] Ctrl+, select all these, move it over
[6:19:21] here, like here. And then with this
[6:19:24] material, you know, you have your stone
[6:19:28] wall material. You just make sure this
[6:19:30] is active in your stone wall as well,
[6:19:32] like over here. Make sure it's active.
[6:19:36] And then with this selected, you can
[6:19:38] just bake it onto your pre-existing map,
[6:19:41] assuming you know you baked these
[6:19:43] already and they're in this format. So
[6:19:45] you can bake multiple at a time. You can
[6:19:46] bake one at a time. You can pack
[6:19:48] manually or you can pack with UV
[6:19:50] packmaster. So again, I'll show you
[6:19:52] that. And you can see it definitely
[6:19:54] packs a lot better. So you kind of have
[6:19:55] a lot of options here. Don't worry about
[6:19:57] getting perfect packs. Don't worry about
[6:19:59] anything, honestly. As long as it looks
[6:20:01] good, that's all you kind of have to
[6:20:02] worry about, you know, when you're just
[6:20:04] starting out, you know, just have fun.
[6:20:05] Okay. Now, I kind of just want to talk
[6:20:07] about a few more concepts when it comes
[6:20:09] to baking. So the first thing is if you
[6:20:12] plan to animate something for example
[6:20:14] like this coffee and have it grow from a
[6:20:18] scale of zero to a scale of one like so.
[6:20:20] If you bake with the coffee mug active
[6:20:23] like this all the objects that you're
[6:20:25] baking will have the coffee mug shadow
[6:20:27] here. So that would look really awkward
[6:20:29] when you're animating from zero because
[6:20:32] the coffee mug doesn't exist yet but
[6:20:33] there's still a shadow appearing because
[6:20:35] the image is baked on there. So that
[6:20:38] means when you're baking like this or
[6:20:39] this, what you want to do when you're
[6:20:42] baking these objects specifically is
[6:20:45] hide the coffee mug during render. You
[6:20:48] can see this icon right here. If you
[6:20:49] hide it, it will still appear in your
[6:20:51] render. So if you want, you can just do
[6:20:53] both of them so it's clear like that.
[6:20:55] But definitely make sure the camera is
[6:20:56] off. So when you bake, you want to
[6:20:58] disable the render here. Now obviously
[6:20:59] the downside for that is then you don't
[6:21:01] have a shadow there. So when the coffee
[6:21:04] mug comes back, there is no shadow here
[6:21:06] on the texture. So, you wouldn't have a
[6:21:07] shadow there. Now, again, like we looked
[6:21:09] at the other award-winning websites,
[6:21:11] that might not be noticeable. Even
[6:21:13] though everything else has a shadow,
[6:21:14] this might not have a shadow, but you
[6:21:16] know, people might not actually even pay
[6:21:18] attention to that. So, here you kind of
[6:21:19] have those trade-offs. Of course, you
[6:21:21] can always use a light with a bake
[6:21:24] texture to cast a shadow, but we are
[6:21:26] trying to avoid real-time lighting. And
[6:21:28] you might be saying, well, that kind of
[6:21:29] defeats the purpose of why we're baking.
[6:21:31] But, but sometimes, a lot of times, you
[6:21:32] combine real-time lighting in 3GS with
[6:21:35] baked textures. for us. Yes, I feel like
[6:21:37] that would be defeating the purpose of
[6:21:39] why we're baking in the first place. So,
[6:21:41] you could definitely do that approach if
[6:21:42] you wanted to. Or what you could do is
[6:21:44] like simulate a shadow, not necessarily
[6:21:47] the same shape as this mug, but like a
[6:21:49] plane that looks like that has like a
[6:21:51] shadow image texture. And this is a
[6:21:52] really common method for faking shadows
[6:21:54] because here here you can see it's kind
[6:21:56] of like a oval. So, if you like have an
[6:21:57] oval plane with a shadow texture, you
[6:22:00] could simulate a shadow for it as it
[6:22:01] grows up. You could like scale up the
[6:22:03] plane as well. That's just something to
[6:22:05] consider if you are planning to animate
[6:22:07] your individual objects. Another thing I
[6:22:09] want to mention is with the glass, these
[6:22:11] are also targets. So I I moved this into
[6:22:14] my targets here. Same thing with this.
[6:22:16] Actually, I haven't split this one up
[6:22:18] yet. So let me do that real quick. I'm
[6:22:20] going to select the glass of here of
[6:22:22] this computer. I'm going to P separate
[6:22:23] by selection and I'm going to move this
[6:22:26] into my targets. Again, these are the
[6:22:28] things that we're going to target. Same
[6:22:30] thing with here. We can also move this
[6:22:32] to target. So the screen I'll target
[6:22:35] this is computer glass. Computer glass.
[6:22:39] And this is fish bowl glass. So these
[6:22:43] are things that we're not going to be
[6:22:45] baking. So when you unwrap, you know,
[6:22:47] don't put these UVs inside your image
[6:22:49] texture. It'll just take up space. If
[6:22:51] you accidentally do it, it's fine. I
[6:22:53] mean, it'll just waste texture space,
[6:22:56] but whatever. Now, when you're baking,
[6:22:57] do you want to disable them from render?
[6:22:59] So when you're baking, should you get
[6:23:01] rid of them? Well, you can see they
[6:23:02] actually contribute a lot of things to
[6:23:05] your scene, like the shadow here. So, if
[6:23:07] I disabled this in render view, you can
[6:23:10] see I would lose some of the shadow that
[6:23:11] the bowl's giving and the reflection on
[6:23:13] the glass might adjust the light in
[6:23:15] subtle ways along your scene. It might
[6:23:18] honestly it might not be noticeable at
[6:23:20] all, but yeah. So, I would probably
[6:23:22] render with the glass still enabled.
[6:23:24] Just don't put that on your unwrapped
[6:23:26] texture. And then this water is just a
[6:23:29] transparent color. So, I'm actually also
[6:23:32] going to move that to targets. All
[6:23:33] right. So, now you can just organize
[6:23:35] things. If you want to categorize your
[6:23:37] textures, like one is room elements, if
[6:23:39] one is desktop items, you know, you do
[6:23:41] you. And I will see you on the other
[6:23:44] side. All right. So, I finished baking
[6:23:46] and I got rid of all my collections and
[6:23:48] just put them into into four different
[6:23:50] collections. Each of these collections
[6:23:52] are associated with their own specific
[6:23:54] texture. So, I had four, but after
[6:23:56] baking, I realized I only I only needed
[6:23:58] two. But oh well, you know, four is
[6:24:01] fine. You live and learn. It's
[6:24:02] definitely going to increase the load
[6:24:03] time, but you know, it's fine. So now
[6:24:06] what you should have is a bunch of baked
[6:24:08] textures. So I have eight here because I
[6:24:10] also changed my lighting and baked
[6:24:11] nighttime as well. So you can do that as
[6:24:13] well if you want to. So now what we need
[6:24:15] to do is go to the compositing tab and
[6:24:17] dn noiseise our image. So if I shift A
[6:24:19] and search for an image texture and we
[6:24:22] want to and we want to navigate to one
[6:24:23] of these like this one right here, you
[6:24:25] can see it's got really a bunch of noise
[6:24:27] and grain on there. So we can do the d
[6:24:29] noiseise like so. Plug our image into
[6:24:32] the dinoiser our dino noiser into the
[6:24:34] compositor and over here just hit mute
[6:24:37] this. This is the thing that renders our
[6:24:40] camera. So we want to render an image
[6:24:42] instead which you can come over here
[6:24:44] render render image or just hit f12. But
[6:24:46] before you do that you need to make sure
[6:24:48] that under output properties your
[6:24:50] resolution is the same as your image
[6:24:52] texture. So if you did a 2K make sure to
[6:24:54] change this to 2040. I did 4K, so I'm
[6:24:58] going to leave it at 4096. And
[6:25:00] everything should be good to go. And
[6:25:02] I'll just hit F12. And you can see all
[6:25:04] that noise is gone. And the color space
[6:25:07] has adjusted to the one that we see in
[6:25:09] Blender. Cool. We'll just use image,
[6:25:11] save as, and I'll just leave it as PNG.
[6:25:14] We don't have any alpha channels, so we
[6:25:15] can just do RGB. We will be changing
[6:25:17] this format later anyway, so we can just
[6:25:19] save as this for now. Okay. Just repeat
[6:25:22] the process with all your other
[6:25:23] textures, and I'll see you on the other
[6:25:25] side. Okay, now's the time to save
[6:25:28] incremental. Save a completely new file
[6:25:31] or duplicate everything, you know, up to
[6:25:33] you. I like to just file, save
[6:25:35] incremental. So, I have a completely new
[6:25:36] file in case I mess something up. And we
[6:25:38] don't need the UV editor anymore. And
[6:25:41] we'll leave the shader tab open for a
[6:25:43] little bit. Okay. So, the first thing I
[6:25:45] want to do is adjust origin points and
[6:25:47] join objects together if you haven't
[6:25:49] done that already. So, for example, I
[6:25:51] don't really plan on animating any of
[6:25:53] these because I baked them baked the
[6:25:56] shadow in with them. So, I'm just going
[6:25:58] to join everything that I'm not planning
[6:26:00] to animate. I'm just going to be joining
[6:26:02] them all together just because it'll
[6:26:03] save on draw calls. If you don't know
[6:26:06] what those are, that's totally okay. It
[6:26:07] doesn't really matter. I'm just going to
[6:26:08] join it with the room itself. So, you
[6:26:10] can see I just call that cube. Now is
[6:26:13] also the time if you want to rename
[6:26:14] stuff, you can also rename stuff as
[6:26:15] well. So, I'm just going to go here. I'm
[6:26:17] going to Ctrl J. I'm just doing Ctrl +
[6:26:19] J. And maybe it's better if I do this in
[6:26:21] solid view. So, let's just see. I'm not
[6:26:23] animating this. I'm not going to animate
[6:26:25] this. I'm not going to animate this. I'm
[6:26:27] not going to animate this. Uh, I'm not
[6:26:30] going to animate this. And not going to
[6:26:32] animate this. So, I'll just join that
[6:26:34] all. So, I'll just join everything with
[6:26:36] the rim here. Just like this. Ctrl J.
[6:26:40] And then what is this? Okay, I'll also
[6:26:42] just Ctrl J and join with the room. So,
[6:26:44] my first texture set is actually just
[6:26:46] one object because I'm not animating any
[6:26:48] of these, which is awesome. So, now what
[6:26:50] we can do is get rid of the original UV
[6:26:52] map because remember simple bake is the
[6:26:54] UV map that's mapping to our texture.
[6:26:56] So, we can get rid of this and then we
[6:26:58] can create a new one called first
[6:27:00] texture set.
[6:27:02] And let's just make sure this works. So,
[6:27:04] so we'll just search for an image
[6:27:06] texture just like so. Open it up.
[6:27:08] Navigate to your first one or whatever
[6:27:10] one you created. And you can just plug
[6:27:12] it in just like that. It'll look a
[6:27:13] little bit off, but you know that's
[6:27:14] fine. Just make sure just make sure
[6:27:16] nothing looks suspicious. So you can go
[6:27:18] in local view, of course, and just
[6:27:20] inspect it. Look for seams. Look for
[6:27:22] lines that don't really make any sense.
[6:27:24] And if you have to re-ake things, you
[6:27:26] know, you can totally do that if you
[6:27:29] want. So I don't see anything
[6:27:31] particularly noticeable, but you know,
[6:27:33] if you do see some sort of line or some
[6:27:36] sort of issue, you know, don't be afraid
[6:27:38] to just go back into the UV editor.
[6:27:41] Let's see. a UV editor and open your
[6:27:45] image texture. So, this one is called
[6:27:47] first texture set day. And let's say you
[6:27:50] have like a small black line, you know,
[6:27:52] don't be afraid to just like move it
[6:27:54] just a little bit. And like I showed
[6:27:57] earlier in the video, it might mess up
[6:27:58] the colors, but a lot of times it might
[6:28:00] not mess up the colors. So, don't be
[6:28:01] afraid to do that if you notice
[6:28:03] something. Again, if you are familiar
[6:28:06] with Photoshop or some other photo
[6:28:08] editing software, yes, you can like
[6:28:09] paint on here or fix up the color. Use
[6:28:12] like AI autocorrection to fix up, you
[6:28:14] know, certain lines and areas like that
[6:28:16] if you want to. But for the most part,
[6:28:18] this looks good to me. So, we don't
[6:28:19] really have to touch anything. And yes,
[6:28:21] I forgot to delete the faces back there,
[6:28:23] which I can actually do now before we
[6:28:25] export. Like, yeah, I'm wasting space on
[6:28:28] my image texture, but we could also
[6:28:30] delete the geometry, but honestly, I'll
[6:28:31] just leave it in there because it's
[6:28:32] there. disable deselect for first
[6:28:35] texture set and reenable for the second
[6:28:37] texture set. And I don't think I'm going
[6:28:40] to animate any of these. So I'm just
[6:28:42] going to hit Ctrl + J to join them
[6:28:44] statically. Okay. So in this second
[6:28:46] texture set, you'll notice that I have
[6:28:47] three spheres here. And these I just
[6:28:50] added and I did not put them as part of
[6:28:52] the bake, but these are targets that I
[6:28:54] will be targeting. So I'm going to
[6:28:56] actually just move them into our targets
[6:28:59] class and rename them to like fish and
[6:29:01] then rename it to like fish. fish bubble
[6:29:04] one or something like that and fish
[6:29:06] bubble two and so on and so forth. That
[6:29:08] way I can easily target it in code and
[6:29:09] you know know what it is later. So I
[6:29:12] guess in the end my second texture set
[6:29:14] is only one of these. If you want to you
[6:29:17] can create you know get rid of all these
[6:29:19] materials and you know create a second
[6:29:21] texture set and hook it up just if you
[6:29:24] want to validate that it works. So we
[6:29:26] just did that. So second texture set. Of
[6:29:28] course, this is optional or if your
[6:29:30] workflow wants you to import the image
[6:29:32] with the model, but again, we're keeping
[6:29:34] it separate. So, here, actually, this
[6:29:36] actually kind of saved me a little bit
[6:29:38] because I forgot to remove the UV map on
[6:29:41] all of them. So, we get rid of it and
[6:29:43] okay, everything works again. So, it's
[6:29:45] really important that when you export,
[6:29:47] this is the only one that you have when
[6:29:49] you export. Continuing on in this
[6:29:52] texture set, what I'm going to do is
[6:29:53] animating the scale of these. So, I'm
[6:29:56] actually going to leave them separate.
[6:29:57] So, what I'm going to do is select all
[6:29:58] of these. Hit Ctrl I, I believe, and hit
[6:30:02] control I. And that'll select everything
[6:30:03] else in my texture set that but nothing
[6:30:06] else because I disabled the selection
[6:30:08] for all my other collections, which is
[6:30:09] great. And I don't plan on animating any
[6:30:12] of these other ones. So, what I'm going
[6:30:14] to do is just come over here and Ctrl J
[6:30:17] and join them just together like that.
[6:30:19] Now, the materials messed up because I
[6:30:21] use generated coordinates, but again, we
[6:30:23] don't even need materials at all. We
[6:30:25] just need to get rid of the UV map here.
[6:30:28] Leave simple bake. And we can just
[6:30:30] actually get rid of all the materials.
[6:30:32] Just like this. Again, we can do first
[6:30:34] texture set. We can copy this. Change
[6:30:37] this to third. This to third texture set
[6:30:41] and just open our third texture. Same
[6:30:44] thing for these. We can just get rid of
[6:30:46] everything. We can change this to third
[6:30:48] texture set. And then with this active,
[6:30:50] we'll do CR Link materials. Now, it's
[6:30:54] messed up because we still have UV map
[6:30:56] here. So, let's get rid of UV map like
[6:30:58] so.
[6:31:03] And we still need to get rid of light
[6:31:05] wooden on all of these as well.
[6:31:09] And this one is
[6:31:12] I didn't get I didn't get rid of the UV
[6:31:14] map on that one. And this one I
[6:31:17] accidentally got rid of the texture
[6:31:19] instead of Okay, cool. So, everything
[6:31:22] seems to be good. If I right click,
[6:31:24] select objects. Yeah, everything seems
[6:31:26] to be good in this one right here. So,
[6:31:28] it seems like I still have smooth
[6:31:30] shading modifiers, which is fine. I can
[6:31:32] just convert that to mesh. I don't think
[6:31:33] that'll actually make any difference.
[6:31:35] So, anyway, I just converted it like so.
[6:31:37] So, let's move on to the fourth texture
[6:31:39] set. Now, since I'm going to be
[6:31:40] animating these later, I'm going to move
[6:31:42] that into my targets. So, I'm going to
[6:31:44] call this my work button. This one I'm
[6:31:48] going to call about button. About
[6:31:51] button. This one I'll call contact
[6:31:54] button. Contact button. And I'm going to
[6:31:57] move these into my targets. And then I'm
[6:32:00] also animating these. I don't really
[6:32:02] know what to call this. So I'll just
[6:32:04] call it hanging
[6:32:06] blank one. Actually, let's use a number.
[6:32:10] Hanging plank one. And then I'll call
[6:32:12] this one hanging blank_2.
[6:32:17] So I'll just move that into targets as
[6:32:19] well. So, so far it seems like I moved
[6:32:22] all my targets into targets and then
[6:32:23] everything that I'm not targeting I just
[6:32:26] joined together as a single object. So,
[6:32:28] honestly, I'll just call this first and
[6:32:30] I'll just call this second. If you want
[6:32:31] semantic name, if you want semantic
[6:32:33] names, you can totally do that. I'm just
[6:32:35] going to do first, second, third. Okay,
[6:32:37] for the fourth texture, let's see. I'm
[6:32:40] going to probably animate the boba. So,
[6:32:43] I'm just going to change that right now
[6:32:45] with an underscore add plushy. put that
[6:32:48] into targets. Let's see. I do plan to
[6:32:52] animate these as well. So, I'm just
[6:32:53] going to move that into targets as well.
[6:32:56] Uh, actually, I do think I want to
[6:32:57] animate this. So, I'm going to move that
[6:32:59] into my targets collection. Cool. Just
[6:33:02] like that. I don't think I'm animating
[6:33:03] anything else. Again, if you do, then
[6:33:05] you can leave them separate and move it
[6:33:07] to targets. So, I'm just going to select
[6:33:09] everything here. And I don't know, it
[6:33:11] doesn't really matter which one. I'm
[6:33:12] just going to select one of them, make
[6:33:15] it active, and just Ctrl J and join
[6:33:17] them. And then I'll just call this
[6:33:19] fourth. Fourth like so. And if you want
[6:33:22] to, you can get rid of all the
[6:33:23] materials. So let's just for the sake of
[6:33:26] completeness, let's just get rid of all
[6:33:28] the materials on fourth. And let's just
[6:33:30] do texture set.
[6:33:34] Fourth. Of course, we can hook up our
[6:33:37] fourth texture set just to see how it
[6:33:38] looks.
[6:33:40] Cool. And let's just get rid of our UV
[6:33:42] map.
[6:33:44] And again, you know, go and inspect it
[6:33:46] for any flaws and any issues and to see
[6:33:49] if you need to re-ake or delete
[6:33:51] something and whatnot. Cool. Okay. So,
[6:33:55] this is all I have. And then for my
[6:33:57] targets, these are the things that I'm
[6:33:58] going to be animating in code. So, if
[6:34:02] you have a lot of them and you want to
[6:34:03] do them in order, what I recommend is
[6:34:05] giving some sort of ID like 1 2 3 4 5.
[6:34:08] That way, you can just use like a loop
[6:34:10] in Gap rather than having to manually
[6:34:12] target each one. If you don't have an
[6:34:14] ID, I mean you could probably select by
[6:34:16] computer fan. So that is also
[6:34:19] technically quote conet ID. You know,
[6:34:21] you have a lot of different variety
[6:34:22] methods, but you know, your naming
[6:34:24] convention now kind of determines how
[6:34:26] easy it will be for you to code later.
[6:34:28] So, do you need a naming convention? No.
[6:34:30] But it definitely speeds up your process
[6:34:32] here. I think for me specifically for
[6:34:34] this project, I don't think I will be
[6:34:36] animating anything in specifically in
[6:34:38] order. maybe the computer fans, but for
[6:34:41] the rest of them, I think I'm just going
[6:34:42] to do it manually. All right. And yes,
[6:34:45] all the objects here still have their
[6:34:47] materials. If you want to replace them
[6:34:48] with their appropriate textures just to
[6:34:51] check, you totally can. Again, just make
[6:34:53] sure for the ones that are baked, you
[6:34:55] get rid of UV map and just leave your
[6:34:57] baking one. So, you might have named it
[6:34:59] baking. I called it simple bake. Um, so
[6:35:01] up to you. So, I'm just checking that
[6:35:03] right now. So, screen, I didn't bake it,
[6:35:06] so that's why it's just leaving that.
[6:35:07] That's totally fine.
[6:35:09] Twitter, I baked, so I'm going to get
[6:35:11] rid of this. YouTube, I baked. I'm going
[6:35:12] to get rid of this. So, let's see.
[6:35:15] Screen, I didn't bake. GitHub, I baked.
[6:35:18] Fishbubble, I didn't bake. Fishbowl
[6:35:20] water, I did not bake. That's also going
[6:35:21] to be a target. Glass, I did not bake.
[6:35:23] Contact button, I already replaced. Uh,
[6:35:26] so these are all baked. Cool. All of
[6:35:30] those are baked. And then the ones that
[6:35:32] I didn't bake, I just left the original
[6:35:34] UV map there. And I almost forgot, but
[6:35:36] now we want to check our origin points.
[6:35:38] So this one, I think I'm going to scale
[6:35:40] like this. So I'm just going to go into
[6:35:43] edit mode and probably just move the
[6:35:45] origin point here. So shift S, cursor to
[6:35:47] selected, right click, right click, set
[6:35:48] origin, origin to 3D cursor, just like
[6:35:50] that. So this is kind of what I like
[6:35:52] here. Let's see. This one, this one can
[6:35:56] scale from this origin point, which is
[6:35:58] okay. These
[6:36:01] share the same origin point. These also
[6:36:04] have their origin points in the center.
[6:36:06] Let's see if that looks okay. So, scale
[6:36:08] here. So, what I'm kind of envisioning
[6:36:10] is this comes out, this comes down, and
[6:36:12] then these kind of stagger and come out
[6:36:14] a little bit delayed, but almost at the
[6:36:16] same time. Same thing with these. So, I
[6:36:21] wonder if I scale from here or if I
[6:36:24] scale from the bottom instead. I think I
[6:36:28] don't Let me check. What I can do is
[6:36:30] just shift right click just to try it.
[6:36:32] Hit period on my num key 3D cursor. It
[6:36:34] would just go up here. And then we can
[6:36:36] just see.
[6:36:38] Yeah, I think I like the scaling coming
[6:36:40] down from here instead of the center for
[6:36:42] these. Again, that's kind of up to you.
[6:36:44] If you want, we can probably just select
[6:36:46] this. Shift S cursor to selected and
[6:36:48] then right click, set origin origin to
[6:36:50] 3D cursor if you wanted to do that. Or
[6:36:52] you can just eyeball it, honestly. Shift
[6:36:53] right click somewhere. Right click, set
[6:36:55] origin origin to 3D cursor. You know,
[6:36:57] it'll probably be close enough. Same
[6:36:59] thing over here. I'm just going to shift
[6:37:01] right click arbitrarily. Let's go back
[6:37:02] to bounty box center. Let's see.
[6:37:06] Yeah, bow plushy is a little to the
[6:37:07] left. So, I want to fix that. Let's go
[6:37:09] into edit mode. This time I'm going to
[6:37:11] Oh, I accidentally did not. Okay, this
[6:37:15] is an issue. So, this just took up space
[6:37:17] on my image texture. Could I rebake?
[6:37:19] Absolutely. But then I have to repack
[6:37:21] everything and bake everything again.
[6:37:23] So, whoops. Oh well. But at least I can
[6:37:25] delete the geometry. So, I'll save a
[6:37:27] little bit of memory there. Anyway, uh
[6:37:29] sorry. The reason I went in here is to
[6:37:32] set the origin point. So, select that
[6:37:33] edge loop there. Shift S cursor to
[6:37:35] selected. Right. Go into object mode,
[6:37:37] right click, set origin origin to 3D
[6:37:40] cursor. Just like that. Cool. And that
[6:37:43] looks nice. It's scaling just like that.
[6:37:45] Cool. Cool. Cool. Now, actually, one
[6:37:46] thing I want to do is honestly,
[6:37:50] we probably should have done this before
[6:37:51] I was moving things around, but I want
[6:37:54] to give them the names for the textures
[6:37:56] that they have right now. That way we
[6:37:57] don't have to like manually set it
[6:37:59] later.
[6:38:00] Honestly, this is kind of optional step,
[6:38:02] but you know, whatever. So, like you
[6:38:04] know how these separate components are
[6:38:06] all mapping to the third texture set?
[6:38:08] Well, instead of like typing them in,
[6:38:10] I'm just going to like filter in code
[6:38:12] all the ones with the name of underscore
[6:38:14] third. So, I'm just going to tack this
[6:38:16] on to the end of everything that has
[6:38:18] that maps to the third texture set. So,
[6:38:21] I'm just going to go down and oh, I got
[6:38:24] the rid of the material here. I think
[6:38:26] this is texture set four. Okay, so this
[6:38:29] is texture set four. So I'm just going
[6:38:31] to call this fourth. So this is called
[6:38:35] fourth, third, second, first. So I'm
[6:38:37] just going to check if this exists in
[6:38:39] the string because you know it's just a
[6:38:40] string. So chair top this is over here.
[6:38:43] And let's just take a guess. Maybe
[6:38:45] texture set three. Okay, it's sorry I
[6:38:48] said three but it's four. So it's going
[6:38:50] to be fourth. Then YouTube, Twitter,
[6:38:52] GitHub should be the same as Bobo
[6:38:54] plushy. So I'm just going to confirm
[6:38:56] that with CR Link materials. Yes, they
[6:38:59] are. So I can just copy forth for these.
[6:39:04] So for these I can do that Twitter,
[6:39:08] YouTube. Okay. So So it seems like just
[6:39:10] by coincidence the ones that I am
[6:39:13] animating or interacting with like
[6:39:15] having clickable just happen to be from
[6:39:17] my third and fourth textures. I guess
[6:39:20] that was just a coincidence. the ones
[6:39:21] that aren't baked like my bubble or my
[6:39:24] computer screen, I didn't have any sort
[6:39:26] of ID for them underscore because there
[6:39:29] is no texture to map to. So, I'll also
[6:39:31] say if you want to create like hitbox
[6:39:34] zones for objects, like let's say this
[6:39:36] is your about me section and you want to
[6:39:38] be able to click on there. If you don't
[6:39:40] want to use the complicated mesh itself,
[6:39:42] you can always make like a hitbox
[6:39:44] geometry like this. Just make sure you
[6:39:46] name it something like hitbox_about_me
[6:39:49] or something like that. And you can just
[6:39:51] make this invisible in 3GS, but still
[6:39:54] clickable. So that means you would have
[6:39:56] like a click zone over here. For the
[6:39:58] navigation itself, I'm just going to use
[6:40:00] their own original mesh. Yes, if you use
[6:40:02] a less complicated mesh, performance
[6:40:05] increases. However, this is a very
[6:40:06] simple mesh. So the the difference in
[6:40:09] performance is probably very very small.
[6:40:11] So it's not worth creating hitboxes
[6:40:13] here. But if you want to create hitboxes
[6:40:14] for your things to ray cast and hit to
[6:40:17] select later, you can totally do that.
[6:40:18] Otherwise, I'm just going to be using
[6:40:20] like the actual objects themselves to be
[6:40:22] clicked on. All right. So, when you're
[6:40:24] ready, you can just hit A to select
[6:40:27] everything. This shows that these are
[6:40:28] selected, but they're not because I
[6:40:30] disabled selection for them. So, you
[6:40:32] know, make sure you got everything. Be
[6:40:34] super cool. Now, we can just do file
[6:40:36] export glTF/GB.
[6:40:39] Remember export settings so you don't
[6:40:41] have to change it every single time.
[6:40:42] Only limit to selected objects, right?
[6:40:44] We don't want to export the lightning
[6:40:46] camera and things like that. In our
[6:40:48] mesh, UVs and normals, great. Material,
[6:40:50] no export. We are not going to be
[6:40:52] exporting our materials with our model.
[6:40:54] Shape keys, we don't have any of those.
[6:40:56] Armatures, none of those. Skinning, none
[6:40:57] of those. This is okay. And we have no
[6:40:59] animations. So, I'll just call it
[6:41:01] room_folio,
[6:41:03] but name it whatever you want. And I'm
[6:41:04] just going to hit enter and enter. Just
[6:41:06] like that, and save that. But if you are
[6:41:08] curious and you just want to see how
[6:41:09] things are, you can just hit A and
[6:41:11] export it with the PNG materials. So,
[6:41:13] all of these I have them with their PNG
[6:41:15] materials. So, I can just do file export
[6:41:18] like so. And then include what? Let's go
[6:41:21] to data. Let's go to materials. Let's do
[6:41:24] export. And I'm just going to export
[6:41:26] this with materials underscore with
[6:41:29] materials. Then we can just navigate to
[6:41:31] gltf report. You can see it's right
[6:41:33] here. Room profiler with materials. It's
[6:41:35] really large. Now you can see what we
[6:41:37] get. And everything seems to look good
[6:41:40] except the ones that I'm replacing
[6:41:42] later, like the glass and the water. But
[6:41:44] for the most part, this looks pretty
[6:41:46] good. So we can continue on with the
[6:41:48] coding. All right. So I'm going to be
[6:41:50] using Vit as our bundler. If you don't
[6:41:52] know what a bundler is, basically it
[6:41:54] just takes all our development sort of
[6:41:56] things and compiles it down and
[6:41:58] optimizes it for browser because the
[6:42:00] browser can only read like HTML, CSS,
[6:42:03] JavaScript, and web assembly. And
[6:42:04] there's all these other different kinds
[6:42:06] of development tools that help speed up
[6:42:07] our development process. Bundlers do a
[6:42:09] lot of other things as well, but that's
[6:42:11] kind of like the general idea of why
[6:42:12] we're using a bundler. So, I'm going to
[6:42:14] use Vit because it's very, very quick to
[6:42:16] set up and it works well for these kinds
[6:42:18] of projects. So, here I just navigated
[6:42:20] to my path. I'm just going to copy that.
[6:42:21] I'm just going to CD just to go in
[6:42:23] there. And then with this copied, let me
[6:42:26] just copy that real quick. I'm just
[6:42:27] going to paste it in here just like so.
[6:42:28] So, I'm going to assume that you already
[6:42:30] have Node installed or one of these like
[6:42:31] bun or Yarn, you know, some sort of
[6:42:33] package manager. I'm just going to be
[6:42:35] using Node.js. Honestly, that doesn't
[6:42:38] really matter for this tutorial as long
[6:42:39] as you have some sort of package
[6:42:40] manager. I'm going to call this room
[6:42:41] portfolio, but name it whatever you
[6:42:43] want. I'm just going to go for vanilla
[6:42:45] JavaScript in this video and I'm just
[6:42:47] going to go with vanilla JavaScript like
[6:42:49] that. So, I'm going to go into that
[6:42:51] directory or that folder that they
[6:42:52] called me. I'm going to do npmi, which
[6:42:55] will just install the dependencies
[6:42:56] listed in the package.json, which we
[6:42:58] can't see yet. And I'll just do code
[6:43:00] dot. And if you have VS Code installed,
[6:43:01] it will open your directory into VS
[6:43:04] Code. So, here you can see that. And
[6:43:06] then package.json. I just installed this
[6:43:09] because this is the only thing in
[6:43:11] package.json. So let's just run mpm
[6:43:13] rundev to make sure this works. And
[6:43:15] indeed it is working. Super super cool.
[6:43:17] Just like that. Okay. So let's install
[6:43:19] some dependencies that we definitely
[6:43:21] need. So we might come back to this. So
[6:43:23] I'm just going to do mpmi install for
[6:43:26] SAS Gap and definitely 3GS. So I'm just
[6:43:29] going to do all of them just like so.
[6:43:31] Now let's get rid of counter. We don't
[6:43:33] need this. Get rid of it. Actually we
[6:43:34] can just delete it. I'm just going to
[6:43:36] delete that. don't need this or this.
[6:43:38] So, we can delete those. In main.js, we
[6:43:42] can just get rid of everything here
[6:43:45] except the import. We can leave this as
[6:43:47] SCSS. And then we can rename this with
[6:43:50] SCSS. So, I just hit F2. Same hotkey in
[6:43:53] Blender as VS Code. And your folder
[6:43:55] system actually, well, at least for
[6:43:57] Windows here, we can just get rid of
[6:44:00] everything. I don't think we really need
[6:44:02] to touch anything here. So, let's just
[6:44:03] get rid of that. Let's also do our
[6:44:06] default reset. So,
[6:44:09] so box sizing border box like so. M0 for
[6:44:13] margin zero, P 0 for padding zero, just
[6:44:16] like so. And we can just get rid of this
[6:44:18] stuff. We'll come back to this in a
[6:44:19] little bit. Now, in index.html, so I'm
[6:44:21] just doing Ctrl P to quickly navigate to
[6:44:23] search for files. And you don't actually
[6:44:25] have to type it. You can just like type
[6:44:27] arbitrary characters that you know are
[6:44:28] inside. So, you don't even have to spell
[6:44:30] it correctly. And you'll just jump to
[6:44:31] that file. And here we want to create
[6:44:33] our experience that just wraps our
[6:44:36] canvas in case you know we need to work
[6:44:38] with that. So, and inside we want our
[6:44:40] canvas where our 3GS scene lives. And
[6:44:42] I'll just call that experience canvas
[6:44:45] just like so. Okay, let's set up our
[6:44:48] folders. So, I like to do models. And I
[6:44:51] also like to do well now since we have
[6:44:53] textures, I'll do textures as well. So
[6:44:56] basically the public folder is the
[6:44:58] static folder asset that Vit will use to
[6:45:00] know where to find their static assets.
[6:45:03] If you change this from the root
[6:45:05] directory or you change the name, you
[6:45:06] will have to create a vit.config file
[6:45:09] and adjust it there. But you know we
[6:45:11] don't have to do that. So we can just
[6:45:12] leave it as is. And then one I have like
[6:45:14] one for images as well. We might come
[6:45:16] back and add to this anyway. All right.
[6:45:18] So before we put my our model in here
[6:45:21] and our textures, I want to compress
[6:45:23] them. That way it'll reduce on the load
[6:45:25] time. So, one thing I like to do with my
[6:45:28] model is go put it through Draco
[6:45:30] compression, which is a really common
[6:45:32] compression method. In the past, when
[6:45:33] you export it from Blender, there used
[6:45:35] to be a compression thing you could
[6:45:36] check and it would do Draco compression
[6:45:38] automatically, but for some reason, it's
[6:45:40] been removed and I never bothered to
[6:45:42] look up why. Anyway, that's fine because
[6:45:43] we can use gltf report to compress our
[6:45:46] model. There's a lot of other methods
[6:45:47] which I cover in my Minecraft video
[6:45:49] which you can check if you want to, but
[6:45:51] we're just going to use this one. And
[6:45:53] what we're going to do is come over down
[6:45:54] under export here and change this to
[6:45:56] Draco just like so. And then we don't
[6:45:58] have to touch anything here. We can just
[6:46:00] hit export and it'll download it for us.
[6:46:02] And you can see it's only 1 megabyte
[6:46:04] compared to our original one which is
[6:46:06] 12.5 kilobyt or sorry or 12 megabytes.
[6:46:10] And you can see that, you know, it looks
[6:46:12] identical. Super super cool. So we
[6:46:14] should just be able to drag that in
[6:46:15] there. I'm going to actually change this
[6:46:17] to old. So, I'm just going to hit F2.
[6:46:19] And I just want this one called room
[6:46:21] portfolio. Cool. And I would just put
[6:46:22] that into models. To compress our image
[6:46:25] textures, I'm going to be using this
[6:46:27] squish, which is made by Google. And
[6:46:29] we're going to convert it to WEBP
[6:46:30] because WEBP is optimized for the
[6:46:32] browser. And it typically has the best
[6:46:35] image quality to file size ratio. Not
[6:46:39] always, but you know, typically. And we
[6:46:41] don't need any other sort of format for
[6:46:43] us. So, we're just going to be going for
[6:46:44] WEBP. So, I'm just going to click and
[6:46:46] drag there. I'm going to change this to
[6:46:48] webp just like so. And then on the left,
[6:46:51] you can see before and then on the right
[6:46:53] you can see after. So, you can see it
[6:46:55] definitely gets blurry over here. So,
[6:46:58] make sure to just be aware of that. So,
[6:47:01] I think I'm going to increase the
[6:47:02] quality a little bit. Okay. Seems like
[6:47:04] 90% quality seems pretty good. From far
[6:47:07] away, no changes, but like close away
[6:47:10] even there was no changes. So, let's
[6:47:12] just download that. You can see this is
[6:47:14] only 732 kilobytes, whereas our original
[6:47:17] one was 19 megabytes, which is kind of
[6:47:19] crazy. All right, so just repeat that
[6:47:22] with the other textures. I'm just going
[6:47:23] to click and drag this here. If you want
[6:47:25] to adjust the quality slider, or if you
[6:47:27] just want to leave it at 90 and just do
[6:47:29] it and be done with it, that's totally
[6:47:30] fine as well. All right, so when you're
[6:47:32] done compressing, you can just click and
[6:47:34] drag your textures into textures right
[6:47:37] here. And then maybe we can be a little
[6:47:38] bit more organized. And I'll call this
[6:47:40] room. Inside room, I'll do night. And
[6:47:43] then I'll also click over here and do
[6:47:45] day. And then all the day ones, I'm just
[6:47:47] holding control to select every single
[6:47:49] opposite one. Move it into day. And then
[6:47:52] hold shift to select everything in
[6:47:53] between. And then just move it into
[6:47:55] night. And then additionally in
[6:47:56] textures, we probably want a video
[6:47:59] texture. So I'm just going to create a
[6:48:00] video texture there. Sorry, a video
[6:48:02] folder. And we'll put a video there in a
[6:48:05] little bit. I know Blender also has this
[6:48:07] option here called create WEBP when you
[6:48:09] export. Honestly, I've never used it
[6:48:11] before, but maybe that's like an
[6:48:13] alternative if you want to. We could
[6:48:14] have also saved our image instead of it
[6:48:16] as PNG as a WEBP, but honestly, I've
[6:48:18] never had the chance or bothered to try
[6:48:20] it out. So, that actually might be a
[6:48:21] faster solution if you wanted to look
[6:48:23] into that. Okay, let's start going into
[6:48:26] main.js and start setting up our 3GS
[6:48:29] experience. So, I kind of explained it
[6:48:31] really really in detail in my previous
[6:48:32] video, so I'm going to try and rush
[6:48:34] through this part of the setup, but you
[6:48:36] know, more of just a refresher. So the
[6:48:37] first thing I need is a canvas for my
[6:48:39] renderer to target. So again, I'm just
[6:48:41] going to use document duckquery
[6:48:43] selector. And I'll just get my
[6:48:45] experience canvas just like so. And it
[6:48:49] was a class. So I'm going to put a dot
[6:48:50] there. So semantically, it would make
[6:48:52] sense if we also gave this an ID. So I'm
[6:48:54] also going to do ID hashtag. Oh, sorry.
[6:48:57] Not that's not a hashtag. That's a
[6:48:58] quote. And then I'll just copy and paste
[6:49:00] this in here just like so. And then we
[6:49:03] can just do hashtag here now. Cool. Then
[6:49:06] I'm going to just copy all of this stuff
[6:49:08] to make it speed up a little bit. This
[6:49:11] is from the getting started docs.
[6:49:13] Creating a scene. So we can just paste
[6:49:15] that in here just like so. Hold alt to
[6:49:18] move this up. I want it at the top like
[6:49:20] so. So we're just creating a scene that
[6:49:22] we add stuff to. We're creating a
[6:49:23] camera. Adding a cube and then animating
[6:49:25] it. So this function I want to and I'll
[6:49:28] be changing this one just because I like
[6:49:30] looking at an arrow function better. So
[6:49:32] I'll do const render equals arrow
[6:49:35] function and let's move all this logic
[6:49:38] into render and then let's just call
[6:49:40] render down here. Then we need our
[6:49:42] window.request animation frame so it
[6:49:44] loops on every single frame and we just
[6:49:46] want to pass in the render function. So
[6:49:48] we call it once and then this will keep
[6:49:50] on calling itself over and over again.
[6:49:52] Okay, so let's update. We don't need to
[6:49:54] append anything here. We don't need to
[6:49:56] set the animation loop. And then I want
[6:49:58] to store the sizes of the inner width
[6:50:00] and inner height into a variable that we
[6:50:02] update. So in the event that I want to
[6:50:05] change it later. So I'm just going to
[6:50:06] call that con sizes equals. And we'll
[6:50:08] set the height height equals to
[6:50:10] window.in
[6:50:12] height inner height. And we'll set the
[6:50:15] width equal to window.in width just like
[6:50:19] so. Put a comma there. So now what we
[6:50:21] can do is just control D select the next
[6:50:23] instance of that. Backspace this out.
[6:50:25] Let's call this width. And we need
[6:50:28] sizes. So I'll do sizes do width. So
[6:50:31] same thing with the height. Ctrl + D to
[6:50:33] select the next instance height. And
[6:50:35] let's just change this to sizes.ight.
[6:50:37] Just like that. All right. So let's go
[6:50:40] to style.css and let's make our canvas
[6:50:42] full screen. So what I'm going to do is
[6:50:44] go into my index.html folder just to
[6:50:46] make sure. Okay. I caught it. We can I
[6:50:49] guess we can also just change this to an
[6:50:50] ID. And let's just Crl X to quickly
[6:50:53] delete lines or cut lines. So I just do
[6:50:56] experience like so. And I'll just do #
[6:50:59] experience which is my div wrapper. I'll
[6:51:02] make it fixed. I don't know if I want to
[6:51:04] change that later at the time being. So
[6:51:06] I'm just going to position fixed just
[6:51:08] like so. Make its height take up the
[6:51:10] full and the take up the full page just
[6:51:14] like that. Top zero, left zero, doesn't
[6:51:16] really matter here. And then we can just
[6:51:18] overflow hidden everything just like so.
[6:51:21] Now, if you're using normal CSS, yes, we
[6:51:24] would put this outside like here and
[6:51:27] target this experience dash canvas like
[6:51:29] so. Now, since we're using SCSS, we can
[6:51:33] actually have some visual idea. And it
[6:51:35] can follow the same sort of hierarchy as
[6:51:37] it does in our index HTML. And you can
[6:51:40] leave it inside instead of outside. If
[6:51:42] you want to leave it outside, that's
[6:51:43] totally fine as well. I'm just going to
[6:51:45] put it inside # experience. And then we
[6:51:47] just want height and width 100% as well.
[6:51:50] Okay, let's uh control W to close those
[6:51:52] real quick. Let's go back to main.js.
[6:51:54] And let's set up our renderer. So, it
[6:51:56] needs our canvas that we passed in. So,
[6:51:58] I'm just going to set that canvas to our
[6:52:00] canvas that we created over here. And
[6:52:02] then anti-alias to get rid of those
[6:52:04] jaggedy lines. We're just going to set
[6:52:05] that to true right now. Then, let's
[6:52:07] adjust the pixel ratio. So, renderer set
[6:52:10] pixel ratio math.mmin. So, I explained
[6:52:13] this in my previous video. If you need
[6:52:16] to look that up, you can totally do
[6:52:18] that. But basically, it's just how many
[6:52:20] pixels it takes to represent a certain
[6:52:23] CSS pixel. And you generally don't need
[6:52:25] more than two. Anything more would
[6:52:26] probably be overkill and you know, take
[6:52:29] performance when there's not much
[6:52:31] difference. So, and of course, we need
[6:52:32] to make it responsive because right now,
[6:52:34] if I resize, nothing's going to adjust.
[6:52:37] So, we know how to do that. But just a
[6:52:38] refresher this time, we can add our
[6:52:42] event listeners over here. event
[6:52:44] listeners and I'll just do window
[6:52:46] addeventlister and I'll call it
[6:52:48] onresize. So every time this resizes
[6:52:50] we're going to get an event. So what we
[6:52:52] want to do is highlight sizes wwidth and
[6:52:55] we want to update this to the new window
[6:52:57] inner width and height. So I can post
[6:52:59] that left arrow key to go there. Enter.
[6:53:02] Backspace this out. Hold alt for two
[6:53:05] cursors equals and window.in
[6:53:07] oops inner width. And we can just change
[6:53:10] this one over here to height just like
[6:53:12] so. So we adjust to the new one every
[6:53:14] single time. We need to update the
[6:53:17] camera. So update camera. We need to
[6:53:20] update the aspect ratio which is this
[6:53:21] second parameter right here. So camera
[6:53:24] aspect equals sizewidth divided by size
[6:53:27] by height. Let's get rid of this right
[6:53:28] here. And we need to update the
[6:53:30] renderer. So let's just update the
[6:53:32] render as well. Update renderer. We need
[6:53:35] to update this. And yep, I almost
[6:53:37] forgot. We need to call update
[6:53:38] projection matrix in order for it to
[6:53:41] actually update. And now you can see
[6:53:42] that if I go back here, it's fully
[6:53:44] responsive. Just like that. Super super
[6:53:46] cool. Okay. So now I want orbit controls
[6:53:49] so we can move around our scene.
[6:53:51] Remember it's right click to pan, left
[6:53:52] click to rotate around. So if we come to
[6:53:55] the docs, we can see how to import orbit
[6:53:56] controls. So I'm just going to import
[6:53:58] that. I'm just going to go to the top of
[6:53:59] my documentation. Just paste that there.
[6:54:02] Sorry, I said documentation. I meant
[6:54:03] doc. Then let's just copy this const
[6:54:06] controls equals new orbit controls. And
[6:54:08] let's just place that under our camera
[6:54:10] over here. Just like so. Like so. We
[6:54:13] don't need to place it here. We can just
[6:54:14] put it over somewhere over here. Cool.
[6:54:16] Let's just place our camera position
[6:54:18] over here just so it's kind of grouped a
[6:54:20] little bit. We'll move things around so
[6:54:22] it's not that big of a deal. Like here.
[6:54:24] Controls.date. And now you can see it
[6:54:26] works. I can move around and so on so
[6:54:28] forth. But this time I actually want
[6:54:29] damping. I think in my previous video I
[6:54:31] didn't use it. damping just makes it so
[6:54:33] when you when you release your mouse it
[6:54:34] still moves a little bit after it kind
[6:54:36] of gives this smooth sort of effect. So
[6:54:38] you can come to their code here you can
[6:54:39] see it's just controls enamel damping
[6:54:41] true and then some sort of damping
[6:54:42] factor there that you can adjust to your
[6:54:44] liking. So I'm just going to place that
[6:54:46] right over here E just get rid of that
[6:54:49] and that's also why we have
[6:54:50] controls.update update in the render
[6:54:52] loop this time as you can see from their
[6:54:54] comment. And if you want to get here,
[6:54:55] you can go to the GitHub open source
[6:54:57] repos or in 3JS examples and then just
[6:54:59] hit the code icon right here and I'll
[6:55:01] navigate to this right here. Okay, let's
[6:55:03] load our model. So, we're going to use a
[6:55:05] gltf loader. But before that, we need to
[6:55:07] set up a Draco loader which is located
[6:55:09] in node modules under three. So, again,
[6:55:13] this is just the entire GitHub repo
[6:55:14] pretty much three. It should be under
[6:55:16] examples JSM and then under libs you can
[6:55:20] see this thing here called Draco. We
[6:55:22] just want to Ctrl + C to copy this
[6:55:25] entire folder. Close node modules folder
[6:55:28] and right in public folder just paste it
[6:55:30] right there. So here in the Draco folder
[6:55:32] you can see that it's got like some
[6:55:33] decoders encoders. So let's create our
[6:55:36] loaders. I guess we can just put up here
[6:55:38] with everything else. So I just call
[6:55:39] this loaders. But before we create them
[6:55:42] we need to import them. So if you come
[6:55:43] to 3GS documentation, you can see how to
[6:55:45] import them right here. So we're just
[6:55:46] going to copy that for the Draco loader.
[6:55:48] We can just import it just like that.
[6:55:50] Texture loader by default seems to come
[6:55:52] with the three node modules folder. So
[6:55:54] we don't actually have to import
[6:55:55] anything special there. However, for the
[6:55:57] glTF loader, yes, we also have to import
[6:55:59] something here. So we're just going to
[6:56:00] import that just like so. Cool. So let's
[6:56:02] create it. Again, we have our textures
[6:56:04] that we need to load. So let's create
[6:56:06] our const texture loader. texture loader
[6:56:09] equals new 3 texture loader like so. And
[6:56:13] this should be new. Sorry. Now, in order
[6:56:16] to use the Draco loader, we need to set
[6:56:18] the decoder path to that path that we
[6:56:20] just created. So, we can just copy all
[6:56:23] this stuff right here.
[6:56:25] And let's just paste that in here. Get
[6:56:28] rid of this. Now, we don't have to path
[6:56:30] to it like so because we moved it into
[6:56:33] our public folder. So, what we can do is
[6:56:35] just do / draco slash just like so. We
[6:56:38] need to use our gltf loader. So you can
[6:56:40] see actually they showed us here as well
[6:56:42] to set the Draco loader here. So let's
[6:56:44] do it again. Const loader. So actually
[6:56:47] let's do camelc case here. And I'm just
[6:56:49] going to call this Draco loader like so.
[6:56:51] And I'm just going to double click copy
[6:56:52] and paste that like so. And then for
[6:56:55] this one we can just leave I guess this
[6:56:57] one as loader. So here I'm just going to
[6:56:59] copy this. I guess we could have just
[6:57:00] used this doc instead. Oh well whatever.
[6:57:02] Uh let's just copy this. Crl X like
[6:57:06] here. And then we're just setting the
[6:57:08] Draco loader to the Draco loader that we
[6:57:10] created. Model loaded loaders. Whoop. I
[6:57:13] also misspelled this. So, let's just fix
[6:57:15] that real quick. So, let's create some
[6:57:18] uh let's create like a map. That way, we
[6:57:20] have keys set to each of these because I
[6:57:22] don't want to do the same thing twice.
[6:57:24] So, let's just con texture map. And I'm
[6:57:28] going to give the keys the same as the
[6:57:30] ones in Blender, right? Underscore
[6:57:32] third. So, it'll be third, fourth, and
[6:57:34] then first, second, third, so on, and so
[6:57:35] forth. So, we'll just do the same thing.
[6:57:37] So, the keys for this object will be
[6:57:39] first. And I'll have a day and night
[6:57:41] version. If you don't have a night
[6:57:42] version, that's fine. I'm just going to
[6:57:44] have a night version as well. And then
[6:57:45] we need our path pass into our texture
[6:57:47] loader. So, we'll just navigate to the
[6:57:49] path of this right here. Again, it's in
[6:57:51] the public folder. So, we should just be
[6:57:53] able to do texture/ room/day.
[6:57:56] And we'll just call it first texture set
[6:57:59] day.p.
[6:58:01] I forgot a slash here. Copy and paste
[6:58:04] this over here as well. Let's put some
[6:58:06] quotes. And let's just change this to
[6:58:08] night like so. And now let's just shift
[6:58:11] alt down arrow. Let's change this to
[6:58:13] second. Like so. We forgot the comma.
[6:58:15] Whoops. Let's add a comma here. And
[6:58:17] let's do that for third and fourth as
[6:58:19] well. Third. Of course, organize it how
[6:58:23] you split up your textures, but this is
[6:58:24] how I did. And then I'll just select
[6:58:26] this and do Ctrl D and change this to
[6:58:29] second.
[6:58:30] Do this same thing here. Crl + D. Change
[6:58:32] this to third. Over here, change this to
[6:58:36] fourth. Like so. Just the name of my
[6:58:38] textures over here. I forgot to change
[6:58:40] this one to night first. Whoops. That's
[6:58:42] totally okay. We can just select that
[6:58:44] and paste night. There we have an object
[6:58:48] with all our paths that we can pass into
[6:58:50] our texture loader. Now, let's store
[6:58:52] them in another object when we're
[6:58:54] loading them. So, let's create that
[6:58:55] right now. This way, we can just easily
[6:58:57] access them later. So, textures equals
[6:59:00] day. And this will just be an object as
[6:59:02] well. And night. So we can have an
[6:59:05] object here. So this is the one for the
[6:59:07] loader. And then this is the one after
[6:59:09] they're done loading, we're going to put
[6:59:10] it into this object here. Okay. So all
[6:59:12] the 3JS texture loader really needs is
[6:59:15] just a path. So that's all we're going
[6:59:16] to do. And the way we're going to do
[6:59:18] that is with object.ent entries. Just,
[6:59:20] you know, some built-in JavaScript
[6:59:21] function. Here you can see what it does.
[6:59:23] It will split up each of these entries
[6:59:25] into their key and to value. And here
[6:59:28] they're just printing it out as a string
[6:59:30] using a string literal which is why it's
[6:59:32] appearing like this. But that means we
[6:59:33] have a key. So what we would do instead
[6:59:36] is our key would just be like first,
[6:59:37] second, fourth and then our value would
[6:59:39] just be our path. So let's go. We'll
[6:59:40] just do object. entries entries and
[6:59:43] we'll pass our texture map in there. And
[6:59:46] then for each for each of the keys and
[6:59:49] path of the keys and we can just call it
[6:59:52] pass. Whoops. We can just call it pass.
[6:59:54] They called it values. We'll just call
[6:59:55] it pass. We're going to we're going to
[6:59:57] load that specific texture. So, let's
[6:59:59] see. I forgot a parenthesy here. And I
[7:00:02] need another one over here just like so.
[7:00:05] Okay, that's good. So, let's create
[7:00:07] context texture equal to our texture
[7:00:10] loader. And we just want to load pass
[7:00:13] day. So, remember pass is the value. So,
[7:00:16] so essentially what we get is this,
[7:00:18] right? And then we're just doing dot
[7:00:19] notation to access the day path. And
[7:00:21] then we want to put in this. Oh, let's
[7:00:23] call it loaded textures. Sorry. So
[7:00:25] loaded textures day. So we're targeting
[7:00:28] this object right here. And we want its
[7:00:30] key and then we're going to create a key
[7:00:32] and we're just going to set it equal to
[7:00:35] day texture like so. Okay. So let's see
[7:00:37] what we're doing with one iteration. Oh,
[7:00:39] sorry. This should be key, not keys.
[7:00:41] Let's see when we go through one
[7:00:42] iteration what happens. So we come over
[7:00:45] here, we target day, we get the path, we
[7:00:47] pass it in, we load it up, and then we
[7:00:48] set it into over here. And now if the
[7:00:51] key does not exist in over here in this
[7:00:54] object, it will create it for us. So
[7:00:56] what happens through one first iteration
[7:00:58] is they will have something like this
[7:01:00] first and it will just be our day
[7:01:03] texture like so. So this is our first
[7:01:06] iteration what we get and then of course
[7:01:08] you know as we repeat it's just going to
[7:01:09] continue on. So this would be like first
[7:01:11] day texture. This would be second day
[7:01:13] texture and then this would be and then
[7:01:15] this would be second and so on so forth.
[7:01:16] And then we also want to do it for the
[7:01:18] night as well. So if you want to if if
[7:01:21] you want to confirm that you can just
[7:01:22] print it out. Okay. So let's just do the
[7:01:23] same thing for night as well. So let's
[7:01:25] come over here. The same thing here.
[7:01:27] Let's just do control d and just change
[7:01:29] this to night. And now let's load the
[7:01:31] gob model. So we can do loader.load. It
[7:01:34] takes a path in the first you can see
[7:01:37] right there URL. So again we just do
[7:01:39] models. It should just be in /models.
[7:01:41] Yeah. Okay. So /models
[7:01:43] /roomportfolio.gb.
[7:01:46] Let's grab that GB. So we'll just call
[7:01:48] it GB. And on load, what are we going to
[7:01:50] do? So this is the second parameter
[7:01:51] here. So when once it's completed done
[7:01:53] loading, this callback is going to be
[7:01:55] triggered. So the first thing we want to
[7:01:57] do then is to assign our objects those
[7:01:59] image textures. The way to do that is
[7:02:01] using GB is using the traverse method,
[7:02:04] which we covered in the previous video,
[7:02:05] but it just goes through your entire
[7:02:07] GB's children and their childrens of
[7:02:08] children. So let's just do GB scene dot
[7:02:11] scene.t traverse and we'll just do child
[7:02:15] like so. And if the child is a mesh, we
[7:02:17] want to update its material. So is mesh
[7:02:20] like so. And if it is, then we want to
[7:02:23] loop through all our keys for the
[7:02:25] texture map and check if the child name
[7:02:27] contains that key because we named it in
[7:02:29] Blender that way. So we can do that with
[7:02:32] object.key keys. Again, this is a
[7:02:34] built-in JavaScript function that
[7:02:36] returns the keys of your object. So I
[7:02:38] just do picture map. And then same thing
[7:02:41] here for each of these keys. We're going
[7:02:43] to check if the child.name doinccludes
[7:02:48] includes the key inside the string and
[7:02:51] if it does then we'll do create a new
[7:02:53] material. So I'll just call it con
[7:02:54] material new three dot mesh. We are not
[7:02:57] we don't need any real-time lighting. So
[7:02:58] we can use a mesh basic material and we
[7:03:01] just map our loaded textures. So the
[7:03:03] object that we created up here and by
[7:03:05] default I want the day. So I'm just
[7:03:07] going to hardcode day here. And then we
[7:03:09] can just pass in the key which will be
[7:03:10] first, second, third. And then we can
[7:03:12] just set child domaterial
[7:03:15] equal to that material.
[7:03:17] Now, you don't have to create a variable
[7:03:19] if you don't want to. I'm just doing it
[7:03:20] for organizational purposes. And then,
[7:03:22] of course, the last thing we have to do
[7:03:24] when it's done loading. So, let's make
[7:03:26] sure I get in here is to add it to the
[7:03:28] scene. So, I'll just do scene add and GB
[7:03:32] scene of our GB file. And then, whoops.
[7:03:34] This should be key, not keys. If I go
[7:03:37] back to the browser, this is what we
[7:03:38] have. And it looks messed up, but it's
[7:03:40] because Blender and 3GS uses a slightly
[7:03:43] different coordinate system on terms of
[7:03:45] their starting point of 0 0. So what we
[7:03:48] need to do is for the textures
[7:03:50] themselves, we'll just set them equal to
[7:03:53] flip Y. Just do flip Y equal to false
[7:03:57] like so. And then we can also do that
[7:03:59] the night one. Again, if you don't have
[7:04:00] a night one, that's totally okay as
[7:04:01] well. Cool. Now it looks a little bit
[7:04:04] washed off, and that's because we need
[7:04:05] to set the color space of our texture.
[7:04:07] So now what we can do is the texture
[7:04:10] color space equals 3 sRGB color space
[7:04:15] just like so. Same thing for the night
[7:04:16] as well. And now you can see that it
[7:04:18] looks exactly like it does in Blender.
[7:04:20] So if you take a look at the
[7:04:22] documentation by default the output
[7:04:24] color space is 3 sRGB color space. So we
[7:04:26] don't actually have to touch the
[7:04:28] renderers one. Cool. Now, one thing you
[7:04:30] will notice is take a look at Kirby over
[7:04:33] here, or actually any any any seam that
[7:04:36] you have on your on your object. You can
[7:04:39] see that as I get farther and farther
[7:04:41] away, the seams are becoming more and
[7:04:43] more noticeable. Even though they don't
[7:04:45] appear on my image texture at all, the
[7:04:48] seams are still appearing. Now, that's
[7:04:49] because of this thing called mip
[7:04:51] mapping, which basically, you know,
[7:04:52] tries to improve performance by reducing
[7:04:54] image resolution, right? Because if
[7:04:56] you're really far away, it's like why do
[7:04:58] you need all that resolution? So, it'll
[7:05:00] sample areas around your seams, right?
[7:05:01] And since you have like since you have
[7:05:03] like gaps between your seams, sometimes
[7:05:05] it's just completely black, which is why
[7:05:06] the seams will start appearing because
[7:05:08] it's like sampling that black color
[7:05:10] instead. So, what we can do to fix that
[7:05:12] is actually change the way that 3GS
[7:05:15] handles things. So, if you go into the
[7:05:17] 3GS documentation, you can see here that
[7:05:19] it's about how the texture is sampled.
[7:05:21] This is a little more complicating and
[7:05:23] getting into the weeds of stuff, but
[7:05:25] just to know that we're changing it to
[7:05:27] the same thing that the mag filter has,
[7:05:28] which is three dot linear filter. And
[7:05:30] basically, instead of just like taking
[7:05:32] the sampled color that they got, they're
[7:05:34] just going to linearly interpolate
[7:05:35] between the colors. So that's all we're
[7:05:37] going to do to hide those seams. So
[7:05:39] we'll just do if child do material. We
[7:05:41] can check if it has a baked texture by
[7:05:43] checking if it has a map. So right, we
[7:05:45] attached the image texture to the map
[7:05:47] property of the mesh basic material. So
[7:05:49] if it exists, it means it has a baked
[7:05:51] texture to it. And then we can just set
[7:05:53] child.material dominar
[7:05:58] filter linear filter just like so. All
[7:06:01] right. And this should be sorry, this
[7:06:02] should be inside our traverse function.
[7:06:05] So let me put this in up over here like
[7:06:08] so. And then scene should be outside of
[7:06:10] our traverse function. We don't need
[7:06:12] that in there. And then okay, I
[7:06:14] misspelled this. This should be map.m
[7:06:16] minfilter. Now, if I go back, take a
[7:06:18] look. We don't see the seams when we go
[7:06:20] far away anymore. I also want to change
[7:06:22] the field of view. 75 seems a little bit
[7:06:24] too high for this. So, I'm going to go
[7:06:27] to camera, wherever we created this, and
[7:06:29] I'm probably going to put it at like 45
[7:06:31] or something like that.
[7:06:34] Yeah. Cool. So, this feels a little bit
[7:06:36] better. I think in Blender it was 35,
[7:06:39] but yeah. So, just adjust it how you
[7:06:41] want, but I think 45. Or maybe we can
[7:06:44] try 35.
[7:06:47] So yeah, so 35 45 doesn't really matter.
[7:06:50] Seems okay to me. And everything seems
[7:06:53] to be working, which is great. Okay. So
[7:06:55] now what I want to do is if the child
[7:06:58] material includes glass. So this one
[7:07:01] includes a map. So now we just want to
[7:07:04] check if child.name that includes glass.
[7:07:07] So this time I'll just do glass. And I
[7:07:09] capitalized the G. We could just do two
[7:07:11] lowercase if we wanted to. Oh well, it
[7:07:13] doesn't really matter. And if it does,
[7:07:14] then we want to set child domaterial. We
[7:07:17] do. We want to set that child domaterial
[7:07:19] equal to a new glass material. So you
[7:07:22] can separate it if you want. And this
[7:07:23] time I'm just going to hardcode it. So
[7:07:25] physical material like so. And we'll set
[7:07:28] some properties like transparent. We'll
[7:07:30] set it equal to true. And I'm kind of
[7:07:32] just basing it off the parameters here.
[7:07:35] So it's in 3GS examples. If you look up
[7:07:37] material/physical/transmission,
[7:07:39] you can see what we have here. I think
[7:07:41] I'm just going to copy and paste this
[7:07:43] honestly. Just uh right in here because
[7:07:46] it looks good to me. Like so. I don't
[7:07:49] think we need a lot of this. So,
[7:07:52] probably don't need color. Don't need
[7:07:54] this specular color. Probably don't need
[7:07:55] to touch that. And then I'm going to use
[7:07:58] this HDR as the reflections. So, I'm
[7:08:01] just going to go for I don't know like
[7:08:02] 1K honestly and just download this here.
[7:08:05] So, I'll just do HDRI to cube map and
[7:08:07] convert it through here. And I'm just
[7:08:09] going to add the HDR here. And then I'll
[7:08:11] just convert it to cute map like so. And
[7:08:14] save it. We want them split up. So let's
[7:08:16] select this one right here. 256
[7:08:19] resolution. Yeah, I think 512 will be
[7:08:22] okay. Then we can just hit process just
[7:08:25] like so. And we can just save that. And
[7:08:27] then here we'll get a Q map. Let's
[7:08:29] convert all of these to WEBP using
[7:08:31] Squish. So let's go back to Squish and
[7:08:33] just compress all of these to WEBP.
[7:08:36] Cool. So, they're all compressed and you
[7:08:38] can see I reduced the file size a lot.
[7:08:40] So, let's come over here and we can call
[7:08:43] it skybox. I think we can just call it
[7:08:45] environment map. Well, I'll call it
[7:08:47] skybox because that's kind of what it is
[7:08:49] as well. This will just be useful once
[7:08:51] we have reflections. So, I'm just going
[7:08:52] to click and drag those in there. So,
[7:08:54] you can see they're a little bit blurry,
[7:08:56] but that's totally okay. Now, in order
[7:08:57] to load a cube texture, we need to use
[7:09:00] the pre cube texture loader. Let's place
[7:09:03] it with the rest of our loaders. So,
[7:09:05] probably up here. And let's just do
[7:09:07] const environment map like so equals and
[7:09:11] whoops I misspelled this environment
[7:09:13] map. And this is under slash textures/
[7:09:16] skybox skybox. And then we can just do
[7:09:20] ctrl d to select the next instance. And
[7:09:22] let's just change this to webp because
[7:09:23] all of ours are webp. Now in our glass
[7:09:26] material we can set the environment map.
[7:09:28] So we can just do in environment map
[7:09:30] equals environment map just like so. Now
[7:09:33] if I go back we should see some sort of
[7:09:35] reflection.
[7:09:36] Yeah. So, we do see some sort of
[7:09:38] reflection along the glass, which makes
[7:09:40] it a little bit more realistic. Just
[7:09:42] like that. Cool. The next thing I want
[7:09:44] to do is do the fishbowl water, which
[7:09:47] has a little bit of an alpha.
[7:09:50] So, we can do the same thing here. If
[7:09:52] childname includes water, water water,
[7:09:57] then we want to create a new mesh basic
[7:09:59] material. Yeah, I'm just going to set it
[7:10:01] equal to the child material. I don't
[7:10:03] feel the need to separate them anymore.
[7:10:05] I was planning to do that originally,
[7:10:07] but not for this. Let's go back. So,
[7:10:10] let's go back in Blender and just copy
[7:10:11] this hexodimal. The last two are the
[7:10:14] alpha channel. So, we don't need that.
[7:10:16] We just need the color. So, what we can
[7:10:18] do is change this to color. Let's do
[7:10:20] Ctrl + E to delete. All right. By the
[7:10:22] way, I'm saying control E, but that's
[7:10:24] like a custom shortcut that I created
[7:10:26] myself. So, if you do delete all right,
[7:10:29] you can see that I set it to control E.
[7:10:31] So, we can just do 0x and paste our
[7:10:33] hexodimal there. And we can set
[7:10:35] transparency equal to true. And then we
[7:10:37] can put the opacity at like 0.6.
[7:10:40] I think it was 0.66 in Blender. It
[7:10:42] doesn't really matter, but we can just
[7:10:43] check. So now if I go back here, you can
[7:10:46] see that we do have the water material,
[7:10:47] and it looks nice, but we can't see it
[7:10:49] behind here. And that's kind of the
[7:10:51] issue with transparency. But that's fine
[7:10:53] because we can fix that simply by
[7:10:56] setting this equal to false depth,
[7:10:58] right? So this way, you know, the
[7:10:59] renderer doesn't determine which one is
[7:11:01] blocking the other one. You know, they
[7:11:02] just blend together. So, what we can do
[7:11:05] then is just set depth right depth right
[7:11:08] equal to false. Whoops, sorry, not a
[7:11:11] semicolon. And then we can just copy and
[7:11:12] paste this in here somewhere just like
[7:11:14] so. And whoops, I forgot the comma. And
[7:11:17] I just realized that this is also inside
[7:11:20] of our object keys, which doesn't make
[7:11:23] sense because these are separate. So,
[7:11:25] what we can do is just move them out.
[7:11:28] So, I'm going to let's see glass. Let's
[7:11:30] just get this parenthesy out here. We
[7:11:33] want it outside but still inside if
[7:11:35] child.m mesh. We just want it outside of
[7:11:37] our texture mapping loop. And then we
[7:11:40] can change this to else. If just to make
[7:11:42] it a little bit more explicit. Save it
[7:11:44] like so. And then here we can just do an
[7:11:46] else like so. And then let's just move
[7:11:48] our object keys function inside of that
[7:11:52] bracket up there. Just using alt up
[7:11:54] arrow to move it up a line. So now if I
[7:11:57] go back you can see that we can see the
[7:12:00] water and the glass. Okay. Let's check
[7:12:02] for any errors in the console that we
[7:12:04] might not light intensity is an
[7:12:06] exposure. It's not a property. Okay,
[7:12:08] let's just get rid of light intensity
[7:12:09] and exposure then. Cool. Those are gone.
[7:12:12] This is from one of my plugins. So, you
[7:12:14] can just ignore that. I also just
[7:12:15] realized we have two objects that are
[7:12:18] using the glass material. So, we're
[7:12:19] creating a new material for each object,
[7:12:21] which is bad. We just want to use the
[7:12:23] same exact material. You know, it's like
[7:12:25] creating two materials in Blender, but
[7:12:27] not changing a single parameter in each
[7:12:28] one of them. So, it just takes up
[7:12:30] unnecessary space. So let's come over
[7:12:32] here. Let's just do con glass material
[7:12:34] like so. And let's just set it equal to
[7:12:36] the material that we created. And then
[7:12:38] we can set the glass material equal to
[7:12:40] this sorry the child material equal to
[7:12:43] the glass material. And then we can just
[7:12:45] copy this else if and just paste it over
[7:12:47] here. And then we want to check for
[7:12:48] bubble. And then I'll call this white
[7:12:51] material. And I will just create a new
[7:12:54] mesh basic material like so. So, I'm
[7:12:57] just going to call this const white
[7:12:58] white material equals Whoops. Let's get
[7:13:01] rid of this. And I'll just do # FF FF
[7:13:06] FFF. Don't need transparency. Don't need
[7:13:08] this. Don't need this. Just like so. And
[7:13:10] now you can see I have my little bubbles
[7:13:13] there. Okay. Now, we just need to set
[7:13:15] our screen. So, I'm just going to do
[7:13:16] else if. And I'm just going to change
[7:13:19] this to screen.
[7:13:22] So, in order for this to work, let's
[7:13:24] change this to a new mesh basic
[7:13:26] material. So, this time we only have one
[7:13:27] screen, so we don't have to split it
[7:13:29] out. We can just do equals new basic
[7:13:32] material. And then for the map, we can
[7:13:34] just put it to a video texture that we
[7:13:36] will create in just a few seconds. So,
[7:13:38] let's see. Okay, we just need to get rid
[7:13:40] of that equals. Let's just create this
[7:13:42] video texture with our other material
[7:13:44] kind of areas. So, we need to create a
[7:13:47] video element first. If you want to put
[7:13:49] it in your HTML directly, you can
[7:13:51] totally do that. I'm just going to do it
[7:13:52] in JavaScript. So, everything's in a
[7:13:54] single place. So, I'm just going to do
[7:13:56] document.createelement.
[7:13:58] Create uh and it'll be a video HTML
[7:14:01] element. And we'll set it source video.
[7:14:06] Let's see. Equal to let's see where do
[7:14:08] we put it? Okay. Slash textures
[7:14:10] /extures/room
[7:14:13] uh slash video. So, it should be in
[7:14:15] here. So, I have a small video here that
[7:14:17] I'm going to be using. So, you know, use
[7:14:20] whatever video you want. Just make sure
[7:14:21] the file size is kind of small. Cool.
[7:14:23] So, this is called screen.mpp4. So, I'll
[7:14:25] just call it screen.mpp4. Just like so.
[7:14:28] I want it to loop. So, I'm just going to
[7:14:30] shift alt down arrow. I want it to loop.
[7:14:32] So, I'm going to set this to we're going
[7:14:34] to set this to true. Just like so. We
[7:14:36] have to mute it if we want to autoplay
[7:14:39] it. And I don't have any audio anyway.
[7:14:40] So, I'm just going to set it to true.
[7:14:43] Then we can set then autoplay to true.
[7:14:45] It will if you don't set sorry this
[7:14:48] should be muted. If you don't set muted
[7:14:49] equal to true autoplay won't work. That
[7:14:51] way they just prevent you from like if
[7:14:53] someone loads on a site it'll just like
[7:14:55] bombard you with extremely loud noise
[7:14:56] and things like that. So the same thing
[7:14:58] is true for with audio. And then we can
[7:15:00] just tell it to play. So we can do video
[7:15:03] element.play
[7:15:05] like so. And typically if you just want
[7:15:08] it constrained to its own space rather
[7:15:10] than full screen, you just do plays in
[7:15:12] line and also set that to true. For us,
[7:15:14] I don't think that will actually really
[7:15:16] matter. And then to use video texture in
[7:15:19] 3GS, you can just see that it's built in
[7:15:21] into the 3xport by itself. So we can
[7:15:24] just get the video element and create it
[7:15:26] there. But again, we don't have the HTML
[7:15:28] element. We're creating it with
[7:15:29] JavaScript. So we can just use that
[7:15:31] instead. So, let's just do const video
[7:15:33] texture equal equals new 3 dot video
[7:15:37] texture. And we just grab the video
[7:15:39] element right here because it's just an
[7:15:41] HTML element stored in this variable
[7:15:43] right here. And let's just make sure the
[7:15:44] color space is the same. I don't
[7:15:46] actually know if we need this or not,
[7:15:47] but it's better safe than sorry. So, I'm
[7:15:49] just going to 3 sRGB color space just
[7:15:52] like so. And then we can just place the
[7:15:54] video texture. Well, actually, we
[7:15:55] already did that. All right, this should
[7:15:57] be good. Let's go take a look and see.
[7:16:00] Okay, let's see. Failed to load. No
[7:16:02] supported source was found. Okay, it's
[7:16:04] probably a glitch somewhere. Let's see.
[7:16:06] I mean, the path is probably wrong. /ext
[7:16:08] rooms slash room slash Oh, video
[7:16:12] separate. So, whoops, my bad. Cool. Take
[7:16:15] a look. Now, our video is on top of our
[7:16:18] computer screen. Super super cool. Just
[7:16:19] like that. So, of course, we also need
[7:16:22] to do video texture flip y and set that
[7:16:25] to false as well. And sweet. Now, it's
[7:16:28] upright just like that. Oh, by the way,
[7:16:30] if this if you feel like the screen is a
[7:16:32] little too stand outish given that it's
[7:16:34] under the shadow and whatnot, you can
[7:16:36] totally like probably reduce the opacity
[7:16:39] with the mesh basic material or if you
[7:16:41] want reflections as well, you can
[7:16:42] totally change this to a mesh physical
[7:16:44] material just like our glass material
[7:16:46] and then play around with some of those
[7:16:48] settings as well. So, you could totally
[7:16:50] do that if you wanted to. Additionally,
[7:16:51] if you want, you can put a plane around
[7:16:54] here. You can either create that plane
[7:16:55] in 3GS or you can create it in Blender
[7:16:57] and reexport your model. You know,
[7:16:59] really up to you. I might do that a
[7:17:01] little bit later, but for now, I'm just
[7:17:02] going to move on. Okay, the next thing I
[7:17:04] want to do is set like a default camera
[7:17:06] position because right now, every time I
[7:17:08] refresh, I start here and then I have to
[7:17:09] like zoom out and then pan just to get
[7:17:12] like a decent view. Come into my render
[7:17:14] function over here and I'm going to do
[7:17:16] thing. I'm going to log the camera
[7:17:18] position. So, I'll do camera
[7:17:20] sorry.position and let me put that in a
[7:17:23] console.log. log sorry console log
[7:17:25] camera position and I also want to log
[7:17:28] the orbit controls target which by
[7:17:30] default this vector 3 of orbit controls
[7:17:34] it starts at it looks at 0000 so we also
[7:17:37] want to change the target as well so we
[7:17:39] can do controls controls we called it
[7:17:43] controls and we'll just log out the
[7:17:44] target there and we'll just do
[7:17:46] console.log vlog. I just want to split
[7:17:48] it up. So, I'm just going to put like
[7:17:49] something there. Okay. Now, we just find
[7:17:52] a good camera position that we like.
[7:17:54] This seems pretty good. So, I'm just
[7:17:56] going to scroll up once on my mouse
[7:17:58] wheel, just like so. And I'm just going
[7:18:00] to copy all this. So, let's open this.
[7:18:02] And let's open this. All right. So,
[7:18:04] let's just make sure to copy these
[7:18:06] values. So, I'm just going to copy this
[7:18:07] over here. And I'm going to go into
[7:18:10] perspective camera. And I'm going to do
[7:18:12] set and just paste this in here.
[7:18:15] Now, I don't want to save my file yet
[7:18:17] because it'll hot module reload and I'll
[7:18:18] lose these values. So, I'm just going to
[7:18:20] copy these now. And for controls over
[7:18:23] here, I'll do controls.target
[7:18:26] set. And I'll just paste this in here.
[7:18:28] Okay. Now, we can get rid of all this
[7:18:30] other stuff. And then we can just place
[7:18:32] some commas here. Let's get rid of all
[7:18:34] this stuff as well. Cool. Let's get rid
[7:18:38] of that. Alt for two cursors. Save like
[7:18:41] so. Let's get rid of these. Cool. Now
[7:18:44] both position and controls.target
[7:18:48] they're both vector 3es. You can see
[7:18:50] right here target is a vector 3. If you
[7:18:52] go to vector 3 all vector 3s have set
[7:18:55] which just sets the xyz components of
[7:18:57] this vector. So that's kind of all we're
[7:18:58] doing instead of using dot notation like
[7:18:59] I had earlier. Now you can see every
[7:19:01] time I refresh my page I'll just start
[7:19:03] with this camera angle which is really
[7:19:04] nice. And we can just uh comment this
[7:19:08] out for now. We might revisit that in a
[7:19:09] little bit. Okay. Okay, so the next
[7:19:11] thing I want to do is make the things
[7:19:12] that I uh want to interact to actually
[7:19:15] be interactable in the 3GS scene like
[7:19:17] these buttons over here and this and
[7:19:19] this and this. And the way to do that is
[7:19:21] using the 3GS ray caster, which which I
[7:19:23] covered in my previous video, but
[7:19:25] basically it shoots a ray from your
[7:19:27] cursor. Well, for us it will be our
[7:19:29] cursor through our simulated camera, you
[7:19:31] know, directly forward ahead and if
[7:19:33] anything is intersecting with that ray,
[7:19:35] it'll it'll find out and and then you
[7:19:37] can sort of listen to that intersection
[7:19:39] event and then, you know, handle events.
[7:19:41] So, it takes intersect objects which is
[7:19:43] just an array of objects. And since our
[7:19:46] GB file has a bunch of objects in there,
[7:19:49] the only way we would be able to prepare
[7:19:52] our raycaster for that is if we manually
[7:19:54] typed each name because unfortunately
[7:19:56] even though we put all our interactable
[7:19:58] targets into our targets collection,
[7:20:00] that doesn't really translate to 3GS. So
[7:20:02] what I should have done before
[7:20:03] exporting, which is fine, is just
[7:20:05] honestly add a underscore target here.
[7:20:08] So then we can just check that
[7:20:09] everything that is indeed a target will
[7:20:12] be hit into our raycast cer. So only
[7:20:15] give the underscore target ID, whatever
[7:20:18] you want to call it. If you want to call
[7:20:19] it like raycaster and just check if the
[7:20:21] name includes raycaster, you can totally
[7:20:23] do that as well. And actually, I feel
[7:20:24] like that might be a little more clear
[7:20:26] because we have these other targets that
[7:20:27] are also targets, but they're not being
[7:20:29] raycasted. So maybe what I'm going to do
[7:20:32] is select all these. We're going to do
[7:20:33] that battery name again. Just out of the
[7:20:35] selected ones under target, I'm just
[7:20:37] going to replace it with raycaster.
[7:20:41] Whoops. I guess I didn't need to do the
[7:20:42] underscore, but anyway. Yeah. And now
[7:20:44] what I'm going to do is just copy ray
[7:20:47] caster for everything that I want
[7:20:49] raycaster. So yeah, see these I don't
[7:20:51] want ray casters. So I'm not going to
[7:20:52] give those to neither the fish bubbles.
[7:20:55] But these ones I definitely want to give
[7:20:57] the raycaster. So anything that you want
[7:21:00] to be clickable or like hoverable or
[7:21:03] listen to some sort of event, you know,
[7:21:04] definitely give it a raycaster for sure.
[7:21:06] Now, I left this in here originally, but
[7:21:08] now looking back in the browser, I will
[7:21:10] never see that back face ever because
[7:21:12] I'm capping the rotation to like this
[7:21:13] and this. So, there's no point of
[7:21:15] keeping that there. It's just taking up
[7:21:17] file size inner geometry. Yes, ideally
[7:21:20] you would re-ake because it took up
[7:21:23] because it took up a huge portion of the
[7:21:25] texture which you could fit other
[7:21:26] objects in there. So, yes, it's a
[7:21:28] complete waste, but but oh well, at
[7:21:30] least uh we can save on some file space.
[7:21:32] But if you want to re-ake, you totally
[7:21:33] can. But that takes a lot of time. So I
[7:21:36] just I'm just going to not do that.
[7:21:39] Let's just make sure we we can delete
[7:21:42] these as well. So I just want to make
[7:21:44] sure that I'm getting only that. Let's
[7:21:46] just delete those vertices. Cool. Yeah.
[7:21:49] So we'll never see those back ones.
[7:21:51] Okay. Cool. We could cut this as well
[7:21:54] and then just save up on that amount as
[7:21:56] well, but you know, it's not really too
[7:21:58] much of a big deal. You know, we don't
[7:22:00] have to be too perfect about it. Oh,
[7:22:03] here I guess for this back we can do
[7:22:05] that. So, we can add like a loop cut.
[7:22:07] Uh, let's just leave it halfway just to
[7:22:09] be safe. And then let's just delete
[7:22:11] these vertices here. Again, we're
[7:22:14] wasting texture space cuz we have bake
[7:22:16] the full length rather than just a
[7:22:18] little bit. But that's totally okay. So,
[7:22:21] again, I'm capping it to here so they'll
[7:22:23] never notice. Another thing I'll say is
[7:22:25] if you accidentally messed up a baking
[7:22:27] and you don't want to bake again, you
[7:22:29] still have sort of, you know, ways to
[7:22:31] get around that. But for example, this
[7:22:33] lamp here, I kind of want it to be its
[7:22:37] own target that I animate in and bounce
[7:22:38] in. So what I can do is select
[7:22:40] everything plus just to increase my
[7:22:43] selection more. Get everything there.
[7:22:45] Again, if you don't have that, you can
[7:22:47] do select more less right here. And then
[7:22:49] I can do P separate by selection. And I
[7:22:52] can rename this to lamp and underscore
[7:22:54] first and then move this into targets.
[7:22:58] Now obviously if I go from a scale of
[7:23:00] zero. Well actually let's reset its
[7:23:02] origin point for first. So I'm going to
[7:23:04] right click set origin origin to
[7:23:05] geometry and then control period gz and
[7:23:09] just snap it down to the bottom here.
[7:23:10] Crl+ just to confirm that. Okay. So if I
[7:23:13] scale it like this if the scale is zero,
[7:23:15] let me just hide it with h real quick.
[7:23:17] You can see that this place is black and
[7:23:19] that would look kind of awkward from far
[7:23:20] away. Actually, for luckily for this,
[7:23:22] you know, no one can really tell, but we
[7:23:24] can possibly get away with is texture
[7:23:27] painting a color over here. So, you can
[7:23:29] do this in Photoshop. Normally, what I
[7:23:31] would do is in Photoshop, I would like
[7:23:34] circle this area, select this area, and
[7:23:35] do content aware fill. And then it'll
[7:23:37] kind of fill in that area really, really
[7:23:39] nicely. But, you know, Photoshop is
[7:23:41] paid, so I'm not going to be doing that.
[7:23:42] So, you kind of have like two options
[7:23:43] here. You can hit period key just to
[7:23:45] jump to your UV where it is. And you can
[7:23:47] see over there what it's highlighting is
[7:23:49] that sort of thing there. But since this
[7:23:51] is roughly the same shadow area, we can
[7:23:53] actually just move this and map it over
[7:23:55] somewhere here. And now you can see well
[7:23:58] now the color is a little bit off
[7:23:59] because that area is darker than over
[7:24:01] here. So but from far away you can see
[7:24:04] that actually no one can tell
[7:24:06] whatsoever.
[7:24:08] So if you want to do that, you can do
[7:24:10] that or you can try and get away with
[7:24:12] just scaling it down. It might look a
[7:24:14] little more blurry, but it might be
[7:24:16] better, more seamless this way. Now, you
[7:24:17] can see it definitely looks a little bit
[7:24:19] more seamless. So, you might want to
[7:24:21] grab some of these edges just to move
[7:24:23] them a little bit, you know, make them a
[7:24:25] little bit darker as well, just move it
[7:24:27] back over here. Yeah. So, from far away
[7:24:31] now, you know, no one can tell that
[7:24:33] there's anything messed up there. So, if
[7:24:35] you don't want to use that sort of hacky
[7:24:36] method, what you can do instead is
[7:24:38] actually paint right over these. So
[7:24:41] again, you can also do this in
[7:24:42] Photoshop, but let's see. Okay, it's
[7:24:44] right here on the image texture. If we
[7:24:45] go to texture paint and we navigate to
[7:24:48] Okay, we're already on here. Let's just
[7:24:50] see where it is. So this giant bulb
[7:24:51] right here. So what we can do is
[7:24:53] probably sample some sort of thing here
[7:24:55] and just like repaint it. So if you have
[7:24:57] Photoshop, you'd do the same thing in
[7:24:59] Photoshop as well. So we can like sample
[7:25:01] a color from there and like just paint
[7:25:02] over there like so. And of course, you
[7:25:04] have options to adjust your brush, which
[7:25:07] I'm not going to be covering in this
[7:25:08] video, but that's something you can do
[7:25:09] as well. And you can see I'm just going
[7:25:11] over there. You can adjust your strength
[7:25:13] if necessary. And of course, you can
[7:25:15] always resample your colors to like get
[7:25:17] a darker place. And then hit F to make
[7:25:19] your cursor a little bit smaller. Shift
[7:25:20] F to control the strength. And then you
[7:25:23] can just like paint, you know, the the
[7:25:25] details back in there. And you can see
[7:25:27] I'm just like painting the lines back
[7:25:28] there. So, if you want to sample a color
[7:25:30] really quickly, you can just hold shift
[7:25:32] X and you can see my color is updating
[7:25:34] up there. And I don't have to hit
[7:25:36] anything after shift X. I just do shift
[7:25:38] X and it'll sample the color. So, here
[7:25:40] maybe I want a little more of this color
[7:25:42] over here. So, I'm just texture painting
[7:25:44] back. And then what you can do then is
[7:25:47] you can see that asterisk means it's not
[7:25:48] saved. Is do Alt S and save it. And then
[7:25:51] let's go back into your shader editor or
[7:25:53] anywhere that you have a shader editor.
[7:25:55] So somewhere over here like so. I have
[7:25:58] first texture set just hit alt R just to
[7:26:01] reload images. And now if I go into
[7:26:03] solid. Let's go back to rendered. You
[7:26:06] can see we kind of patched up that hole.
[7:26:07] Yeah, it definitely looks a little bit
[7:26:09] messy. But you know if you had good
[7:26:11] texture painting, you could polish that
[7:26:13] up and make it look nice. Typically
[7:26:14] though, again what I do is like I go in
[7:26:16] Photoshop, I just select that area. I do
[7:26:18] content aware fill or generative AI. Now
[7:26:21] you can just do like remove background
[7:26:22] and it'll like do the effectively the
[7:26:24] same thing. I'll also say yeah don't
[7:26:27] accidentally delete things that Whoops.
[7:26:29] I accidentally deleted something. And I
[7:26:31] don't have undo available because it's
[7:26:33] so far deep which is a little bit tragic
[7:26:35] but that's fine. And this is why we do
[7:26:37] file save incremental because I can just
[7:26:39] go to let's say this one. Might as well
[7:26:43] just save this file. And here luckily we
[7:26:45] still have this here. So let's see
[7:26:48] cube.00001.
[7:26:49] Cool. We can just shift duplicate this.
[7:26:52] Move it to a new collection just called
[7:26:54] messed up.
[7:26:56] That's totally okay. We don't care about
[7:26:58] the name here. Let's just do go back to
[7:27:01] baking tutorial. Save for sure. Okay.
[7:27:04] Now, with this all this messed up, what
[7:27:07] we can do is just select these. We could
[7:27:10] join them if we wanted to. I feel like
[7:27:12] I'm just going to select all these and
[7:27:14] just delete these vertices like so.
[7:27:16] Let's come here to file, append. Let's
[7:27:19] search for that one that we had
[7:27:21] collection. Let's see. Where's our
[7:27:23] messed up one? Okay, we just added it.
[7:27:25] Cool. Now it's here.
[7:27:28] So, we could we can just get rid of the
[7:27:30] UV map. And it should be fine if we just
[7:27:33] have simple bake here. And then this was
[7:27:35] with texture set one. So, we can change
[7:27:37] the material for first texture set.
[7:27:40] Cool. Works. And now we can just delete
[7:27:42] this bottom face over here. Let's go
[7:27:44] into local view just to make sure that
[7:27:46] yeah, back face is deleted as well.
[7:27:48] Okay, now we can just join this back
[7:27:50] with the first texture set because I'm
[7:27:52] not going to be animating it. Cool. So,
[7:27:55] there is the power of saving versions.
[7:27:58] You know, that would have been
[7:27:59] catastrophic to fix otherwise. Well,
[7:28:02] maybe not that bad. We would just fill
[7:28:03] in the top and then find it on here and
[7:28:06] just map it again, but whatever. So,
[7:28:09] when you're done with everything that
[7:28:11] needs to be done, you can just hit A to
[7:28:13] select everything. File, export, glTF.
[7:28:16] We shouldn't have to touch any of this
[7:28:17] because we kept it. Remember export
[7:28:19] settings. Yep. No export in the
[7:28:21] material. I'm going to version this into
[7:28:23] V1. That way we have a fallback in case
[7:28:25] we messed up something.
[7:28:28] Again, don't forget if you have made any
[7:28:30] edits in Blender to your texture, make
[7:28:32] sure to compress it again. And then for
[7:28:34] your GB file, make sure to put it into
[7:28:37] gltf report and again change this to
[7:28:39] Draco and just export and download it
[7:28:41] somewhere. So that's all I did. And then
[7:28:43] I just changed the original one to
[7:28:44] underscore V1. I just replaced the
[7:28:46] textures over here. And then the new one
[7:28:48] that I just created, I called it
[7:28:50] underscore v2. And then I just changed
[7:28:52] the path to underscore vv2. If you want
[7:28:54] to just replace the old one and keep it
[7:28:56] as room_folio or just delete that one,
[7:28:59] that's totally fine as well. Okay, the
[7:29:00] next thing I want to do is go to GitHub
[7:29:02] and create a new repository. Typically
[7:29:04] in my previous videos, I would just push
[7:29:06] at the end, but that's typically not my
[7:29:08] workflow at all. I set up get, you know,
[7:29:10] right from the get- go, so we might as
[7:29:12] well just do it now. So, I'm just going
[7:29:13] to name it Sue a Kimfolio,
[7:29:17] but you know, name it whatever you want
[7:29:18] it. Uh, just leave it public. And I'll
[7:29:21] create the repository for now. Then I'm
[7:29:23] going to assume you have git installed.
[7:29:24] So, I'm just going to do this real
[7:29:25] quick. Get init
[7:29:28] origin right here. Then, let's uh let's
[7:29:31] change it to main. I think by default I
[7:29:32] already have it to main, but I might as
[7:29:34] well just in case. If you want to leave
[7:29:35] it at master, that's totally fine as
[7:29:37] well. Let's just get add everything.
[7:29:40] Cool. And then let's do get commit just
[7:29:42] like so.
[7:29:44] And let's just get push- origin
[7:29:55] in Verscell. And if you connect to your
[7:29:58] GitHub account, it should automatically
[7:30:00] find your latest repository push. So you
[7:30:02] can just hit import just like so. And it
[7:30:04] should automatically detect your Vit
[7:30:06] with no issues. Here you can see that it
[7:30:08] finds our upper directory you know v
[7:30:10] build everything seems to be fine here
[7:30:12] we don't have to edit anything and we
[7:30:14] can just deploy it and now every time
[7:30:15] you push by default it will
[7:30:17] automatically make another push so if
[7:30:19] you wait about 2 or 3 minutes you should
[7:30:22] be able to see it when you visit this
[7:30:24] URL every time you make a new push and
[7:30:27] yeah you can just already share this
[7:30:28] with the world which is just your
[7:30:29] initial one but every time you push it
[7:30:31] should be updating super super cool okay
[7:30:33] why don't we do something simple first
[7:30:35] and let's make the fans hands rotate.
[7:30:37] So, I'll say that these two are number
[7:30:41] two and four, which means it has to
[7:30:43] rotate, I think, along the Z-axis. I'm
[7:30:46] not sure. And then these will have to do
[7:30:48] along the Y-axis given my intuition. So,
[7:30:51] we can have const Zaxis fans like so.
[7:30:55] And we'll just have an array of fans
[7:30:57] that we want to target. And then and
[7:30:59] then here we can have like ISIS fans.
[7:31:02] Now, let's just go to our loader.load
[7:31:04] function. So over here our fans are
[7:31:07] baked. So we want to come into this else
[7:31:09] statement over here. And we can just
[7:31:11] check if child.name includes we want to
[7:31:15] check for fan because I have that name
[7:31:17] in blender just like so. And if
[7:31:19] child.name includes let's see we can
[7:31:22] just do fan_2 which is kind of overkill
[7:31:25] but whatever you know it works. It
[7:31:27] works. And then we can just do or fan_4.
[7:31:31] Then we'll do Z-axis fans and we'll just
[7:31:34] push the child there to that. Otherwise,
[7:31:38] what we want to do is push to the Y-axis
[7:31:40] like so. And just like the default
[7:31:43] rotating cube that they give us in the
[7:31:45] getting started, we can animate our
[7:31:47] fans. So, animate fans, we can do Z-axis
[7:31:50] fans like so. And then for each of these
[7:31:53] fans, we can just add to their rotation.
[7:31:55] So, whoops, sorry, I should call this
[7:31:57] fan. And then fan.rotation.z
[7:32:00] Z plus equals. We can just do 01. I
[7:32:03] think that was like fast enough with the
[7:32:05] default rotating cube and it might look
[7:32:07] good for the fans. Shift alt down arrow
[7:32:10] change this to Y-axis. And then this one
[7:32:12] can be Y instead. And now if I go back
[7:32:14] here, you can see I have some rotating
[7:32:16] fans. Looks like Z-axis is not the right
[7:32:18] call. It should be X-axis. So let's just
[7:32:21] control shift L for Z-axis with a
[7:32:23] highlighted. It will select all the
[7:32:24] instances. And we can just type X-axis
[7:32:26] here. And then we can change this to X.
[7:32:28] And now you can see we have some
[7:32:30] rotating fans just like that. And if
[7:32:32] your rotation is really wonky, again,
[7:32:35] make sure that your origin point is in
[7:32:36] the center of your fans. All right. Now,
[7:32:38] we need to create a ray caster and then
[7:32:41] normalize our device coordinates such
[7:32:44] that the ray caster can calculate
[7:32:46] appropriately. I explained this in my
[7:32:47] previous video, but basically in the
[7:32:49] browser in JavaScript, it starts 0, 0 in
[7:32:51] the corner and it goes to like whatever
[7:32:53] like 1,000 comma 10,000 in your browser
[7:32:55] window or whatever resolution it is. And
[7:32:57] basically what this does is it makes
[7:32:58] your center 0 0. And if you go to the
[7:33:01] left it's negative 1. If you go to the
[7:33:02] right it's one. If you go up it's going
[7:33:03] to be one. If you go down it's going to
[7:33:05] be negative 1. So I'm we can just
[7:33:07] reorganize everything later but I'm just
[7:33:08] going to do it here. Window add event
[7:33:10] listener like so. And this one's going
[7:33:13] to be mouse move. They use onpointer
[7:33:15] move and this works but it has issues
[7:33:18] with iOS devices which means you have to
[7:33:20] use like touch move instead. So I'm just
[7:33:22] going to split it out into mouse move
[7:33:24] and touch events rather than just using
[7:33:26] pointer. All right, let's just come over
[7:33:28] here. Create an arrow function and we
[7:33:30] want that event object that comes in
[7:33:32] there. So, so let's come over here as
[7:33:34] well. And of course, we need these to
[7:33:36] update. So, I'm actually just going to
[7:33:39] leave it as pointer because why not the
[7:33:42] variable name as least, but we will be
[7:33:44] updating it in the mouse move. So, let's
[7:33:47] just take a look at can just type
[7:33:49] pointer.x equals. And now the event
[7:33:52] object should be similar to on pointer
[7:33:54] move as for mouse move. So we should
[7:33:57] just be able to copy and paste this and
[7:33:58] have it work. Let's control D and change
[7:34:00] this to E because we call it E. If you
[7:34:02] want to call it event, you can totally
[7:34:03] do that as well. All right, let's come
[7:34:05] into our render function now. So let's
[7:34:09] go back up. Shift shift enter to go back
[7:34:13] up one instead of down one. So you can
[7:34:16] see that if I go shift enter, it'll go
[7:34:18] up to 11. So I just went up from one
[7:34:20] down to 13 to quickly jump to it. And
[7:34:22] now we can just copy this stuff. So
[7:34:24] raycast caster set from camera check if
[7:34:27] the intersect objects and then do
[7:34:28] something with it for each of the
[7:34:31] intersected objects. So we can just copy
[7:34:33] that anywhere here. Let's just do ray
[7:34:35] cer ray cer. And of course we want to
[7:34:38] pass in our intersect objects. And I
[7:34:40] believe we called it ray cer objects.
[7:34:42] Maybe we could have called it intersect
[7:34:43] objects. Oh well. Now also when I am
[7:34:45] hovering or I have an intersection I
[7:34:48] want to show that the pointer is
[7:34:50] clickable. So I'm going to change the
[7:34:51] cursor if intersects. If there's some
[7:34:54] sort of intersection it doesn't matter
[7:34:56] what it is. So if it's greater than zero
[7:34:57] it means we're intersecting with
[7:34:58] something. We're going to set the
[7:35:00] document.body.style.cursor
[7:35:03] and we're going to set that to pointer.
[7:35:04] Otherwise we're just going to set it to
[7:35:06] default. So we can just leave it at
[7:35:08] default like so. And this should be
[7:35:10] working like so. So, if I go back and
[7:35:12] hover over here, you can see I my mouse
[7:35:14] moves to pointer. And when I get off,
[7:35:15] it's not. And everything's turning red.
[7:35:17] Super super cool. There's some things
[7:35:19] that I don't want clickable, but are
[7:35:21] still showing the pointer icon. So,
[7:35:23] these are going to be an issue here. And
[7:35:25] then these are not showing up either as
[7:35:28] red, even though they should be. So, if
[7:35:29] I go back into Blender, it becomes clear
[7:35:31] why these are not highlighting because I
[7:35:33] didn't give the raycaster ID to it. So,
[7:35:36] I would just give raycaster ID to them
[7:35:39] right now. So I'm going to put it into
[7:35:40] raycaster under raycaster. And I
[7:35:42] accidentally gave it to fishbowl glass
[7:35:44] which I'm going to get rid of. And then
[7:35:46] I also gave it to computer glass by
[7:35:47] accident. And now let's just give it to
[7:35:49] GitHub. We'll just attach ray caster
[7:35:51] over there. Now another thing we should
[7:35:53] add for the UI is everything that we
[7:35:57] want to show the pointer when we hover
[7:35:59] over it. We can do that. So this one we
[7:36:02] can do uh underscore hover or underscore
[7:36:05] pointer, you know, whatever you want to
[7:36:07] call it. And if you have if you want
[7:36:09] like different effects for each one,
[7:36:11] then you can actually tag on multiple
[7:36:13] IDs and then depending on that you can
[7:36:15] adjust it accordingly. Exporting and
[7:36:17] compressing only takes like 5 minutes
[7:36:19] each time. So, you know, it's not a big
[7:36:21] deal if you have to come back here
[7:36:22] later. So, my work button I wanted to
[7:36:24] show pointer. Cool. So, I would I'll
[7:36:27] just So, let me just copy that. And then
[7:36:30] for about I'm just going to hit period
[7:36:31] to jump to there. I'm going to attach
[7:36:33] the pointer ID to that one. Same with
[7:36:36] contact and whoops. I guess I should
[7:36:38] have done it for these at the same time
[7:36:39] that I added ray caster. So these are
[7:36:42] ones that I definitely want to show that
[7:36:44] you can click on them again. Do it for
[7:36:47] whatever you want on your scene that can
[7:36:48] be clickable. And if you don't know, you
[7:36:50] know, you can always come back here
[7:36:51] later and do it another time. Okay. So
[7:36:54] let's just hit A to export again. File,
[7:36:56] export glTF. Let's do room portfolio.
[7:37:00] room portfolio
[7:37:02] version 3 v3. Again, you know the drill.
[7:37:05] I'm just going to export it. So, same
[7:37:07] deal. I put it into gltf report,
[7:37:08] downloaded it, put it into models, and
[7:37:10] just change my path right here. Okay,
[7:37:13] let's come back up here and let's create
[7:37:15] a let current intersect. So, all the
[7:37:17] current intersected objects. We'll just
[7:37:20] do current intersects
[7:37:23] like so. Like here. And let's just come
[7:37:25] back down over here. And instead of
[7:37:27] setting const intersects here, we can
[7:37:29] set our current intersects over here.
[7:37:31] And then we can control D changes to
[7:37:33] current intersects. If current
[7:37:34] intersects, there is a current
[7:37:36] intersect. That means it will return
[7:37:38] some sort of thing. So greater than
[7:37:39] zero, we can we can just set like some
[7:37:42] const value here called current
[7:37:43] intersect object. And we'll just set it
[7:37:46] to the first intersection. So whatever
[7:37:48] is in front, we're just grabbing the
[7:37:50] first intersecting of the array. So
[7:37:52] basically just what's in front and it
[7:37:54] should just be dot object. And then we
[7:37:56] can just check if current intersect
[7:37:59] object name.inccludes
[7:38:02] our pointer ID that we gave it to. Then
[7:38:04] we can show the pointer otherwise we
[7:38:07] just won't. So let's just make sure I
[7:38:10] have this inside of this. Cool. Let's
[7:38:14] see. Do I have one here? Cool. Now in
[7:38:16] the event that there's no intersect
[7:38:18] object, we still want to be able to
[7:38:20] reset the cursor. So, we want to also
[7:38:23] put the else on the outside of the if
[7:38:25] statement for this one as well. So,
[7:38:27] we'll just set that back to default as
[7:38:28] well. Now, if I go back, I should hover
[7:38:30] over the ones with pointer ID. They
[7:38:32] should show the pointer. And then the
[7:38:33] ones that don't, like this boa t here
[7:38:36] and these light bulbs that I made them
[7:38:38] like so. But all of these show the
[7:38:39] pointer, which is awesome. These are the
[7:38:41] ones that I gave the pointer ID. And
[7:38:43] then these ones don't. By the way, if
[7:38:45] you have no idea what I'm logging here,
[7:38:47] you know, it's just a bunch of objects
[7:38:48] and I'm just accessing a bunch of object
[7:38:51] data. So that's all that is. At any
[7:38:53] point of the time, you can just log it
[7:38:54] out and you'll see all the object and
[7:38:56] what I'm selecting. Okay, let's get rid
[7:38:58] of this color thing. We'll revisit this
[7:39:00] in a little bit. Now, let's create our
[7:39:02] social links so we can just get those
[7:39:04] working right now. So, I'm just going to
[7:39:05] put it up here. Let's just do con social
[7:39:08] links. And I'll make this an object. So,
[7:39:11] we have GitHub. And I'll just set that
[7:39:14] to So, I'm just going to set that to
[7:39:16] github.com like so. And I'm going to set
[7:39:18] YouTube just equal to youtube.com. So
[7:39:21] I'm just going to paste that there.
[7:39:23] Shift alt down arrow. And let's control
[7:39:25] D and change this to Twitter. Now let's
[7:39:28] take a look at our under. So what we
[7:39:30] need is an on click event listener. So
[7:39:33] we can just do window.addeventlister
[7:39:36] and we'll do click. So once we click on
[7:39:39] something, we can check if our current
[7:39:41] intersects object sorry array has a
[7:39:44] length of zero. That means we're
[7:39:45] intersecting something. Honestly, we
[7:39:47] could use a current intersect object
[7:39:49] global variable if we wanted to, but you
[7:39:51] know, we can just do this anyway. And
[7:39:53] then we'll just do con object equal
[7:39:55] current intersect. Again, we'll just get
[7:39:57] the first one like so. And then for each
[7:40:00] of the social links, again, we're going
[7:40:01] to use object. entries. So, the key and
[7:40:04] the value. So, object entries. Go for
[7:40:07] the social links, we'll do for each of
[7:40:10] the social links, we'll get the key,
[7:40:12] which is GitHub, Twitter, YouTube, that
[7:40:14] sort of stuff. And then I'll just call
[7:40:16] it URL. They call it value in the docs,
[7:40:18] but we'll just call it URL. And whoops,
[7:40:20] I want need to do it like so. Create a
[7:40:22] function here. And whoops, I'm missing a
[7:40:25] another parenthesy over here and one
[7:40:27] over here. So if objectname
[7:40:30] doccludes includes the key that we're
[7:40:33] looking for, right? Which is just
[7:40:35] GitHub, YouTube, that sort of stuff.
[7:40:37] Then let's just do const new window
[7:40:39] equals window.open
[7:40:43] open. So, we're opening a new window
[7:40:45] here, and we want to set some things for
[7:40:47] this new window open. For example, the
[7:40:49] opener, we're going to set it equal to
[7:40:51] null. These are just security things
[7:40:53] that are best practices. Very, very
[7:40:55] common. If you've ever worked with links
[7:40:56] before, you've definitely seen this
[7:40:57] done. So, we're just doing it in
[7:40:59] JavaScript instead. Window.loation.
[7:41:01] We're just going to set it to the URL
[7:41:03] associated with that key. And then just
[7:41:04] more stuff. Window.target equals blank.
[7:41:08] Whoops. Target. And then, just more
[7:41:11] security stuff here. No opener. No
[7:41:14] referer.
[7:41:16] Whoops. That should just be E2. Like so.
[7:41:18] So now when I click on these, it should
[7:41:20] work. Well, okay. YouTube works, Twitter
[7:41:24] works, GitHub does not work. GitHub does
[7:41:26] not work, which means I probably
[7:41:27] misspelled. I probably had a capital H
[7:41:29] in Blender. I don't actually know, but
[7:41:31] this probably because of that. Yeah.
[7:41:33] Okay. It's because of that. Sweet. All
[7:41:35] right. Now, we just need to display our
[7:41:37] modals when we select our navigation
[7:41:40] buttons. So, let's go into index.html
[7:41:42] and set those up. So, I'm just going to
[7:41:44] place it here. I want three modals. So,
[7:41:46] I'm just going to do times three. And
[7:41:48] then we can have like an about and then
[7:41:50] we can have like a contact. And then I
[7:41:53] think my last one was work. Let's just
[7:41:54] put in the same order. It honestly
[7:41:56] doesn't really matter, but I'm just
[7:41:57] going to keep it the same order. Now,
[7:41:59] what we can do in style.css is just
[7:42:01] target these modals. So, I'm just going
[7:42:04] to do the generic stuff for the modals.
[7:42:07] So, I'm just going to make all of them
[7:42:08] the same style for now. So, I'll just do
[7:42:10] modal. And I'm just going to do the
[7:42:12] generic position. Uh, whoops. Absolute
[7:42:15] like so. Just to center it real quickly.
[7:42:17] Top 50%.
[7:42:19] Left 50%. Just like so. And then
[7:42:22] transform. Transform. Translate
[7:42:26] 50%. Com, 50%, just like so. And let's
[7:42:30] just make the font size really big. So,
[7:42:31] like 32 pixels, like so. Let's go back
[7:42:33] to index.html. Control P index.html.
[7:42:36] Let's put some stuff in here. So, I'll
[7:42:38] do work and we'll just copy and paste
[7:42:41] that a bunch. And then I'll do about
[7:42:43] here. And then for contact, we can write
[7:42:45] contact and a bunch of other random
[7:42:47] characters after that. And then let's
[7:42:49] just set their zindex to like 999 so
[7:42:51] they're in front of everything just like
[7:42:53] so. Cool. And you can see that they're
[7:42:55] all there right now. Now, I want to hide
[7:42:57] them and then display them. So, what we
[7:43:00] can do is just like let's just set
[7:43:01] display equal none for now. And later
[7:43:03] we'll fix that. Also, inside of index
[7:43:06] html, what I want first is an exit
[7:43:09] button. I'm going to create another HTML
[7:43:11] element here. And I'll just call it
[7:43:12] modal exit button. Exit button like so.
[7:43:15] And I'll just type exit modal here.
[7:43:19] Something really large and noticeable.
[7:43:21] And then I guess I should have just done
[7:43:22] it appropriately, but whatever. We can
[7:43:24] just do it now. And then I'll just do
[7:43:26] like H1 modal title. And then let's just
[7:43:29] move our random spam inside of model
[7:43:33] title. I don't actually know what format
[7:43:35] I'm going for yet. So, I'm just doing
[7:43:37] some dummy content for now. So, cool. We
[7:43:40] have a bunch of modals with a title and
[7:43:42] an exit modal. And these should be a
[7:43:44] button. Sorry. Hold alt, double click,
[7:43:46] and let's just place button there. All
[7:43:48] right. Let's go back to main.js. And
[7:43:51] let's do control W just to quickly close
[7:43:53] that. And in main.js, we want to select
[7:43:56] all our modals. So, we can create an
[7:43:58] object for that. That way, we can just
[7:44:00] loop through them later. So const modals
[7:44:02] equals just like so we have work and we
[7:44:05] have let's see about and contact as
[7:44:07] well. So we can just do something like
[7:44:09] so and let's just place three cursors
[7:44:11] here and documentquery selector like so
[7:44:14] and all of them have the modal class. So
[7:44:16] we can do dot modal and then just the
[7:44:17] appropriate thing. So this way oops zero
[7:44:20] out there sorry backspace I mean and
[7:44:23] then we just selecting both their class
[7:44:24] names. So it says so I'm going to be
[7:44:26] using gap the animation library to
[7:44:29] animate these modals coming in. So we
[7:44:31] need to import that. So what I'm going
[7:44:32] to do is come up here just import gap
[7:44:35] from gap and gap and then we can create
[7:44:38] our functions that animate our modal. So
[7:44:40] we'll do the first one con show model.
[7:44:43] And we'll pass in a model here like so.
[7:44:46] And let's see what the issue. Oh, it
[7:44:47] didn't recognize a spacer. Okay, that's
[7:44:49] fine. And then we can just immediately
[7:44:51] set the model.style display equal from
[7:44:54] hidden to block. So as as soon as we
[7:44:56] click on one of our bottom options, it
[7:44:58] will click show model. It'll pass in the
[7:45:00] modal and we'll just set it to block.
[7:45:02] And then when it comes to Gab
[7:45:04] animations, you have to set your initial
[7:45:06] states with Gab itself, otherwise it
[7:45:09] might glitch out. Not always, but
[7:45:10] sometimes you do. So in this case, I
[7:45:12] want to set I just I'm just going to go
[7:45:14] for a basic opacity animation for now.
[7:45:16] So I just do set modal and I'm just
[7:45:19] going to target the opacity of the CSS
[7:45:22] property. And I'm just going to set that
[7:45:23] as default as zero. And then I'm just
[7:45:25] going to do gab.2. Take the model again.
[7:45:29] And this time I'm just going to set its
[7:45:30] opacity equal to one. And whoops, sorry,
[7:45:33] this should be a semicolon like so. And
[7:45:35] we can just make the duration really
[7:45:36] quick. I think by default it is 1
[7:45:39] second. So now I'm just setting it to
[7:45:40] 0.5 seconds. And then we can have one
[7:45:42] for hide model as well. So let's just
[7:45:44] come over here and let's just change
[7:45:45] this to hide modal. So we're going to
[7:45:48] come over here and we'll just set this
[7:45:51] opacity to zero now. And sorry opacity
[7:45:53] is misspelled here. It should be opacity
[7:45:55] like this. Cool. And then on complete,
[7:45:58] we want to display none. So it'll be
[7:46:01] opacity zero, but we still can click on
[7:46:03] it. So afterwards, we want to once the
[7:46:06] animation is done playing, we want to
[7:46:07] set it back to none. Display none. So
[7:46:10] we'll just copy this right here. And
[7:46:12] let's add a carrot over here. And then
[7:46:15] just set this back to none. Just like
[7:46:17] so. Okay. Now we should just be able to
[7:46:19] go to our click. So in here, our buttons
[7:46:22] already have underscore raycaster
[7:46:24] associated with it. So it should already
[7:46:26] be a part of our intersect objects that
[7:46:28] we are checking for here. So let's just
[7:46:30] come here and now we should just be able
[7:46:32] to check for those. So let's make sure
[7:46:34] I'm out of the entries. That's cool. We
[7:46:36] already have this. So I'm just going to
[7:46:38] copy this right here actually. And we
[7:46:40] want to check for work button. If it is,
[7:46:42] then we can show our model and pass in
[7:46:44] that model. So we'll just pass in
[7:46:46] modals.work.
[7:46:48] So remember this is the object that we
[7:46:49] created up there and we're just
[7:46:51] accessing the work which was selecting
[7:46:53] the document query selected the modal.
[7:46:56] Then we can do else if and let's just
[7:46:59] copy and paste this cuz why not? Whoops.
[7:47:03] Let's just copy and paste this cuz why
[7:47:04] not? Let's change this to about. Let's
[7:47:08] place some parentheses here. And then
[7:47:10] let's just copy and paste this one more
[7:47:11] time. You could use else if you wanted
[7:47:13] to but you know no reason to do that.
[7:47:16] And then let's just change this over
[7:47:18] here. Let's change this to about. Let's
[7:47:20] change this to contact. Like so. All
[7:47:22] right. So, if I go back, these should
[7:47:24] work. Let's see. Child is not defined.
[7:47:26] Okay. That's probably because
[7:47:30] yeah, down here I was traversing child
[7:47:32] for mesh name, but now we called it
[7:47:33] object. So, sorry. This should be
[7:47:35] object. So, control D. Select next
[7:47:37] instance. Change that to object. Oh,
[7:47:39] random. But I did give it a background
[7:47:41] color of black. So, if I go back, it
[7:47:43] should be working now. Let me click
[7:47:44] here. So yeah, it's working. But okay, I
[7:47:47] forgot to do the exit button. So invalid
[7:47:50] property duration. Uh yeah, I misspelled
[7:47:52] that. Okay, so let's just we can just
[7:47:54] fix that real quick. Let's just control
[7:47:56] D duration like so. And then now we can
[7:47:59] select all our buttons. So we can
[7:48:02] documentquery selector all and I forgot
[7:48:05] what I called it in index.html modal
[7:48:08] exit button. So I'll do alt left arrow
[7:48:10] just to jump back to where I go. By the
[7:48:12] way, if you want to jump to where your
[7:48:13] previous cursor location, you can just
[7:48:15] use your alt, left, and right arrow
[7:48:17] keys. Or you can just come up here and
[7:48:19] click here. We're going to select all
[7:48:21] our modal exit buttons. Exit buttons.
[7:48:24] Sorry, I keep saying buttons and then
[7:48:25] adding the S in in there. And then for
[7:48:28] each of these buttons, button. And for
[7:48:30] each of these buttons, what we're going
[7:48:31] to do is add an eventlister. So
[7:48:33] button.addeventlister. And it'll just be
[7:48:35] a simple click. Let's grab that
[7:48:37] eventlister. I mean, sorry, that event
[7:48:39] object. And we need to find the modal.
[7:48:41] We could pass in the model if we wanted
[7:48:42] to, but I'm just going to find it. So,
[7:48:45] we can do e target closest and we can
[7:48:49] pass in the class nameal. And then we of
[7:48:51] course we can just hide modal and then
[7:48:53] use the modal that we found to hide and
[7:48:55] play the animation over here. So, if you
[7:48:58] don't know what closest is, basically
[7:49:00] what so basically what it does is your
[7:49:02] click events happens at this button.
[7:49:04] It's going to search up your hierarchy
[7:49:05] for that class. So, basically like
[7:49:07] searching for the parent. In this case,
[7:49:09] we the parent itself is just dot model.
[7:49:11] But if you had a deeper nested thing, it
[7:49:13] would go up one level and keep going
[7:49:15] until it find it. So if I have my click
[7:49:18] event on this button, well, it's going
[7:49:20] to find this model because I'm going up
[7:49:22] up and then I get this parent here. So
[7:49:24] that's just kind of like a neat trick to
[7:49:25] speed things up. So now if I go back and
[7:49:27] hit my work, hit exit model. You can see
[7:49:29] everything is working just like so.
[7:49:32] Super super cool. I also think now's a
[7:49:34] good time to push because we started
[7:49:36] getting something. So we can just do get
[7:49:37] add everything get commit dashm and
[7:49:40] let's just say uh I don't know starting
[7:49:42] modals working basic or we or and we can
[7:49:46] do something like we're you know
[7:49:48] something random just like so and we can
[7:49:50] just do get push just like so. All right
[7:49:52] we're getting somewhere. Okay now what I
[7:49:54] want to do is fix the touch events
[7:49:56] because right now when I click on it I
[7:49:59] have to click twice for this to activate
[7:50:00] and when I click on this exit button
[7:50:02] sometimes it glitches out and it will
[7:50:04] like flicker. You can see it'll flicker
[7:50:06] there. And this is probably because we
[7:50:08] have so many concurrent events. We have
[7:50:09] orbit controls which takes a bunch of
[7:50:11] touch events. Then we have our ray cer
[7:50:13] that's detecting a click event, I
[7:50:15] believe. And also the HTML element. So
[7:50:17] there's kind of all these conflicting
[7:50:18] events. So let's try and manage that and
[7:50:20] fix that right now. So what I'm going to
[7:50:22] do is add a touch start and touch end.
[7:50:24] Unfortunately, like I said earlier,
[7:50:26] pointer move, it'll work on Android and
[7:50:30] PC, but there's issues with iOS devices
[7:50:33] with pointer move. So we are splitting
[7:50:35] them up. So I'm going to do touch start
[7:50:36] like so. And then once I hit my finger
[7:50:40] on the screen, sorry, tap the surface.
[7:50:42] That triggers a touch start event. So
[7:50:44] that's when I want to update my pointer
[7:50:46] for the raycast caster camera. So I
[7:50:48] should just copy and paste this over
[7:50:50] here. Now instead of this event object,
[7:50:52] we need to grab event object.ouches
[7:50:55] touches and we want to just grab the
[7:50:57] first finger that you get client X. So
[7:51:00] basically the event object has this
[7:51:02] thing here. If you want, you can just
[7:51:03] console.log e, but it has this thing
[7:51:05] here called touches. And let's say you
[7:51:07] put three fingers on your screen. Zero
[7:51:09] just gets the first finger that landed
[7:51:10] on your screen. So that's kind of all we
[7:51:12] need. So we're going to do the same
[7:51:13] thing over here. Y. And this calculation
[7:51:16] should work. If I messed up something,
[7:51:18] we'll find out later. Now, we also want
[7:51:20] to do e.prevent default because we have
[7:51:22] like scrolling behaviors on mobile and
[7:51:24] things like that. So prevent those
[7:51:25] default behaviors. And then we have to
[7:51:27] change this into a active event listener
[7:51:31] by setting the second parameter over
[7:51:33] here. And then we want a touch end event
[7:51:35] listener. And this will so when they
[7:51:37] release their finger from the screen,
[7:51:40] this is going to trigger. So let's
[7:51:42] change this to touch end like here. Also
[7:51:45] e.prevent default. And let's create a
[7:51:47] new function here called handle
[7:51:49] raycaster interaction. That way we don't
[7:51:52] have to do it for the click as well as
[7:51:55] the touch start. By default, click is
[7:51:57] supposed to convert to touch events on
[7:51:59] mobile. But again, we have so many we
[7:52:00] have so many conflicting events that I
[7:52:02] feel like it's glitching out. So, let's
[7:52:04] just create a function here. And I'll
[7:52:05] just call it handle. Whoops. Handle ray
[7:52:08] caster interaction like so. And let's
[7:52:10] make sure I put parenthesis here. So,
[7:52:12] I'm calling it fine. And let's just grab
[7:52:15] this if statement here. Ctrl X to cut
[7:52:17] it. Ctrl +V to paste it in there. And
[7:52:21] then here, we can just pass in the
[7:52:24] function instead. So handle recaster
[7:52:26] interaction. All right. So this should
[7:52:27] be working. And now if I go back here,
[7:52:29] let's hope this is working. And yeah,
[7:52:32] you can see now when I go here, it's
[7:52:34] working when I click. And then let's
[7:52:35] just make sure in desktop. Yeah. Okay.
[7:52:37] So it's still working in desktop. Great.
[7:52:39] And we don't get any errors. Cool. Now
[7:52:41] you will notice there is one issue. I
[7:52:42] can't click this exit button anymore.
[7:52:45] Honestly, that's probably again with a
[7:52:46] bunch of overlapping events. I don't
[7:52:49] actually know, but I'm just going to
[7:52:50] assume that that's the issue because
[7:52:52] click should convert to touch. So what
[7:52:54] we can do is add a separate touch event
[7:52:57] using the same exact thing. So we can
[7:52:59] just copy this over here like so. I also
[7:53:02] forgot passive equals false here. So
[7:53:04] passive equals false. Well, not equals
[7:53:06] false, but passive false. And we can
[7:53:08] just change this to touch end. We don't
[7:53:10] need touch start, right? Because if they
[7:53:11] tap down, there's no event, but as soon
[7:53:13] as they release their their finger,
[7:53:15] there will be an event there anyway. So
[7:53:16] touch end will be fine. So because click
[7:53:19] might also accidentally trigger on the
[7:53:20] mobile device. What we can do is add a
[7:53:23] flag variable and that checks if it's a
[7:53:25] touch then don't fire the click one. So
[7:53:28] we can just do let touch happened or
[7:53:30] something like that and we'll set it to
[7:53:32] false. And then if this one is triggered
[7:53:34] we'll just set this equal to true. So
[7:53:37] we'll set this to true. And then if
[7:53:39] touch happened over here if touch
[7:53:41] happened if touch happened
[7:53:44] just guard clause return and don't do
[7:53:46] anything. So, if I go back here, let's
[7:53:48] just take a look and check. Cool. That
[7:53:50] seems to be working. Now, let's go to
[7:53:52] desktop. Okay, exit model is no longer
[7:53:55] working. And that makes sense because
[7:53:56] once we have a touch event, then we go
[7:53:58] to desktop. This is still true. And it's
[7:54:00] just constantly returning that guard
[7:54:02] clause. So, it's not executing anything
[7:54:04] here. So, let's actually just move this
[7:54:06] up above here. And then once they mouse
[7:54:08] move, we can just like set touch
[7:54:10] happened back equal to false. That feels
[7:54:13] a little bit hacky, but honestly, you
[7:54:16] know, I feel like that. Okay, let's go
[7:54:18] from desktop to mobile contact. Let's go
[7:54:21] back to desktop still. Great. It works.
[7:54:25] Yeah, seems like a sort of a hacky
[7:54:27] solution, but I feel like so if I figure
[7:54:29] out something, you know, make sure to
[7:54:30] check the code for updates. But for now,
[7:54:33] that seems to be working for us. So,
[7:54:35] I'll just leave it as is. All right. So,
[7:54:37] let's come into source and let's create
[7:54:39] a styles folder. And this will kind of
[7:54:40] just like hold everything in here. So,
[7:54:42] let's do fonts. SCSS, which I want to do
[7:54:45] right now. So, we can have a custom font
[7:54:47] for our model design. I'm not going to
[7:54:49] go into too much of the modal styles in
[7:54:51] this video because I kind of just want
[7:54:53] to focus on the Blender and 3JS part
[7:54:55] rather than the styling, but you can
[7:54:57] style it however you want. Once you have
[7:54:58] your fonts that you want, just click and
[7:55:02] drag them into transfer. So, here I just
[7:55:04] have my font file that I downloaded
[7:55:07] online called Multi Forces and the other
[7:55:09] one is shifty notes. Both of them are
[7:55:12] public licensed and created by Niscala
[7:55:15] Huruff. So, so definitely check them
[7:55:17] out. Definitely check the artists out
[7:55:19] there to support them. And what we want
[7:55:21] to do is convert it to WA and WA 2 files
[7:55:23] which are the web fonts and fix vertical
[7:55:26] base metrics. Sometimes the fonts will
[7:55:28] have and basically what it'll try and do
[7:55:30] is like match up your font alignment
[7:55:32] because sometimes
[7:55:34] depending on how you made your font,
[7:55:36] your font can appear in line but like
[7:55:38] the actual spacing will be a little bit
[7:55:39] different. For the most part though, if
[7:55:41] you make your font correctly, this won't
[7:55:42] really do anything whether you leave it
[7:55:43] on or off. So, I'm just going to leave
[7:55:45] it on and I'm just going to hit convert
[7:55:47] again. W and W 2, just like so. And then
[7:55:49] we can just download our font face kit.
[7:55:51] So, here you can see that we have our
[7:55:53] fonts. And then we also have this
[7:55:54] stylesheet thing here, which we can open
[7:55:56] in VS Code. Let's just copy that and
[7:55:58] paste that into our fonts.css.
[7:56:01] And then let's take what else they gave
[7:56:02] us over here. And let's just drag that.
[7:56:04] Well, actually, let's create a new
[7:56:05] folder here first. And let's just call
[7:56:07] it fonts. Let's just click and drag that
[7:56:09] into fonts. Cool. So, we have our fonts
[7:56:12] right there. Now, we need to go back to
[7:56:14] fonts.scss and update the path. So, we
[7:56:16] can just come over here and navigate
[7:56:18] control shift L to select all the
[7:56:20] instances and just do /font slash like
[7:56:22] so. Then, let's just go to style.scss
[7:56:25] and import it so we can use it. So, we
[7:56:27] can come over here and we'll just do at@
[7:56:30] use and we'll dot /styles/styles/fonts.
[7:56:35] SCSS just like so. Let's add our
[7:56:37] semicolon there. Another thing I like to
[7:56:39] do is have a reset. So, we can do a
[7:56:42] reset. SCSS. Now, the idea behind a
[7:56:44] reset is that different browsers have
[7:56:46] like different paddings and margins and
[7:56:48] defaults and things like that. So,
[7:56:49] resets.css will just keep everything
[7:56:51] consistent. If you look up CSS resets
[7:56:53] online, you'll probably find a lot of
[7:56:55] different ones, but this one seems to
[7:56:57] work really well. So, I'll just use this
[7:56:59] one. Credits to my web. And I'm just
[7:57:01] going to paste that into reset. SCSS.
[7:57:03] Honestly, for what we're doing, it
[7:57:05] probably doesn't really matter. Uh, but,
[7:57:07] you know, might as well. I just wanted
[7:57:08] to let you know that I do typically, you
[7:57:10] know, use a reset. SCCSS. And then
[7:57:13] another thing I like to do is definitely
[7:57:15] have a variables.CSS file. All right,
[7:57:18] let's get our first variable. Um, we
[7:57:20] could go back to Blender to get the
[7:57:22] color or we can use this thing here,
[7:57:24] which I use a lot. It's a color picker
[7:57:25] add-on. I totally recommend it. And you
[7:57:28] can just like grab a color anywhere on
[7:57:29] your screen. So, that looks pretty good.
[7:57:32] And you can just copy that. And then in
[7:57:34] variables, we can create a variable
[7:57:35] here. And I'll just call it base purple.
[7:57:39] But you know, if you want to give it a
[7:57:41] actual proper naming convention, totally
[7:57:43] go for it. And we can go back and maybe
[7:57:45] get like a like a base pink or
[7:57:47] something. And then I'll just shift alt
[7:57:48] down arrow, call this base pink. Well,
[7:57:51] it's actually really cool because my VS
[7:57:54] Code theme is also kind of following the
[7:57:56] same theme that we have for portfolio.
[7:57:58] What a coincidence. Base black. And we
[7:58:01] can just do #00000000.
[7:58:04] And then let's just select a color here.
[7:58:06] So I don't want it to be completely
[7:58:07] black. Maybe just like something
[7:58:09] slightly black. And then we can do the
[7:58:11] same thing for white. You know, maybe
[7:58:14] maybe instead of # fff, we can do
[7:58:16] something that's uh whoops, I forgot
[7:58:18] semicolon here. A little bit less white.
[7:58:21] I don't know. It's it's really up to
[7:58:23] you, though. So back in style. SCSS.
[7:58:25] Let's also just import variables. SCSS.
[7:58:28] And we have to give it a name space. So
[7:58:30] I'll just call it as varss but you know
[7:58:32] call it whatever you want to call it.
[7:58:34] And now what we should be able to do
[7:58:36] let's just for the model itself let's
[7:58:38] just do a max width of like 700 pixels.
[7:58:42] And then we'll we'll just take 100% of
[7:58:44] the width just like so. Then for the
[7:58:46] background color let's just do varss dot
[7:58:49] and then let's get our variable. So I
[7:58:51] forgot what I call it already which is
[7:58:52] embarrassing. Um so let's see. Yeah we
[7:58:55] can just do base white for now. And if
[7:58:57] we you know you can always change it.
[7:58:58] So, I'm just getting this variable over
[7:59:00] here. And let's get rid of display none
[7:59:02] for the time being. So, here you can
[7:59:03] see, okay, we see it now. And yeah, we
[7:59:05] have the hashtag FDF FDF FD, which is
[7:59:08] what we're seeing right here. Super
[7:59:09] super cool. I actually don't like how
[7:59:11] it's white. Maybe we can get like
[7:59:12] something that's over here or something
[7:59:14] like so. Let's just create that. And
[7:59:16] let's just do base light purple. Purple
[7:59:21] like so. And then let's just change this
[7:59:23] to base light purple. You know, if you
[7:59:25] want to set the font family up here or
[7:59:27] wherever you want to use it, you can now
[7:59:29] access it. So, you just do it whatever
[7:59:32] you want to call it. So, maybe call it
[7:59:34] this like so. And then you can have a
[7:59:37] fallback to like enter or whatever you
[7:59:39] want to do. System UI,
[7:59:41] you know, same thing. Whatever you want
[7:59:43] to do there for the fallbacks. Yeah. So,
[7:59:45] you kind of have all the general idea
[7:59:47] when it comes to styling. Yeah. So, now
[7:59:50] just have some fun styling your model.
[7:59:52] or if you don't want to use a model, you
[7:59:54] can do something else like a full screen
[7:59:55] overlay or some other canvas transition
[7:59:57] or whatnot. But you kind of have the
[7:59:59] general workflow now that I typically
[8:00:01] use. I also like to when I'm working
[8:00:04] with SCSS use at include media. And this
[8:00:06] is a really easy way to make break
[8:00:09] points in SCSS. Of course, you could
[8:00:11] also just do it in native SCSS as well,
[8:00:13] but include media kind of makes it a lot
[8:00:15] simpler. And then every time that you
[8:00:18] have like a breakpoint, basically you
[8:00:19] make like a object of break points. So
[8:00:21] like mobile is like 20 pixels or
[8:00:24] whatever and then desktop is like 787
[8:00:27] pixels or whatnot. And then you have
[8:00:29] these break points and then in here you
[8:00:31] just do add include add include and then
[8:00:34] your breakpoint. I think it's like less
[8:00:37] than or equal to your breakpoint over
[8:00:39] here. And then it'll just pretty much
[8:00:41] look like this. You don't have to type
[8:00:43] all the media screens and everything
[8:00:44] every single time. So that's kind of
[8:00:46] just a really nice way to make it
[8:00:48] responsive. So you'll probably also see
[8:00:50] me use mixins which is part of SCSS but
[8:00:54] basically they're reusable styles. So
[8:00:56] like display flex and justify content
[8:01:00] justify content center all this sort of
[8:01:03] stuff is very very repetitive and
[8:01:06] appears in multiple places. So basically
[8:01:08] you just create the style once.
[8:01:10] Basically you just create it once and
[8:01:12] then you can just use it in multiple
[8:01:14] places just like so. That way you don't
[8:01:16] have to copy and paste a bunch. Of
[8:01:17] course, you could also just add that
[8:01:19] class to the HTML element as well. Or,
[8:01:21] you know, you could just do it in SCSS
[8:01:23] as well. And of course, you know, feel
[8:01:24] free around to play with the Gap here.
[8:01:26] If you need a timeline, you can totally
[8:01:28] do that as well. So now what I want to
[8:01:30] do is when I hover over these, I want
[8:01:32] some sort of user feedback in terms of
[8:01:34] like scaling or whatnot. So yes, you
[8:01:36] could again check for name, but I'm
[8:01:38] going to come back here again. Uh,
[8:01:40] sorry. And I'm going to have one more.
[8:01:42] So I'm going to call hover. So every
[8:01:44] item that has a hover, I'm going to add
[8:01:46] a hover effect for it. And then for the
[8:01:49] ones that I want different hover
[8:01:50] effects, I can do like for example over
[8:01:52] here, I can do like hover_2
[8:01:55] or hover v2, you know, whatever you want
[8:01:57] to do it. Just give it some sort of ID
[8:01:59] that you can easily check for later.
[8:02:00] That's what I'm going to do for all of
[8:02:02] these. I'm definitely going to give it
[8:02:03] underscore hover. That way when I hover
[8:02:06] it, I can apply like a small like a
[8:02:09] scale effect. And see, we'll just add
[8:02:11] hover effects to all of these.
[8:02:14] Yep. So, just give hover to whatever
[8:02:16] that you want. And make sure everything
[8:02:18] that you have a hover effect, you also
[8:02:19] have the raycast cer ID for as well. And
[8:02:22] of course, order doesn't really matter
[8:02:24] because we're just checking if the name
[8:02:25] includes that. So, you know the drill. I
[8:02:28] put it in gltf report, downloaded it,
[8:02:30] changed it to_v4, and then just change
[8:02:32] the path here. All right. So, now we
[8:02:34] need to track the hovered objects. So,
[8:02:38] let's just come up somewhere. Honestly,
[8:02:40] I don't know where. or we can just put
[8:02:42] it over here. And let's just do let
[8:02:44] current hovered object. So, this will
[8:02:47] keep track of whatever we're hovering.
[8:02:49] And we're just going to set it to null.
[8:02:51] Then, of course, we need to go to our
[8:02:53] room portfolio in here and check if the
[8:02:56] child name includes hover.
[8:02:58] So, yeah, we'll just come over here and
[8:03:00] do hover. If you have another one like
[8:03:03] hover_2, you can also do that here as
[8:03:05] well. I'm just going to do one initially
[8:03:08] here. And then in here, what we need to
[8:03:10] do is because when I hover over
[8:03:12] something, we're going to change it from
[8:03:13] an initial scale and rotation or
[8:03:15] whatever parameter you want if you want
[8:03:17] to change position too as well. You'll
[8:03:18] need like an initial position. So in
[8:03:20] order to store that, we could attach it
[8:03:22] to a custom object or we can just use
[8:03:24] this thing here called dot user data as
[8:03:27] part of all object 3Ds which includes
[8:03:29] our mesh where it stores some user data
[8:03:31] that you can put in yourself. So we can
[8:03:32] just use this instead. So, since I'm
[8:03:34] going to be adjusting the scale,
[8:03:35] rotation, and maybe position, we might
[8:03:38] as well just do all of them, we'll do
[8:03:40] child user data initial scale. Just
[8:03:43] create a new three vector 3 to store
[8:03:45] that in. So, 3 dove vector 3 like so.
[8:03:48] And then again, another built-in method
[8:03:50] here. By the way, I'm just telling you
[8:03:51] this stuff, but like there it's listed
[8:03:54] in the documentation if you don't know
[8:03:55] what they do. So, here you can say just
[8:03:57] copies the past values into that that
[8:03:59] vector that you're calling on on. So,
[8:04:01] we'll just copy the child.scale scale
[8:04:03] and then for rotation we can do initial
[8:04:06] rotation like so and we'll do
[8:04:07] child.rotation. Now this can't be this
[8:04:10] should be a uler angle rather than a
[8:04:12] vector 3 and then we can also do
[8:04:14] position here. So we can change this to
[8:04:16] initial position and we can change this
[8:04:18] to child.position and then we need an is
[8:04:21] animating flag because when we're
[8:04:23] hovering over it it's going to keep
[8:04:24] triggering the play animation. So we
[8:04:27] need some sort of flag to say okay only
[8:04:29] play it once. So that's what we're going
[8:04:31] to be doing now. So just child do user
[8:04:33] data is animating animating and I'm just
[8:04:36] going to set that to false because it's
[8:04:38] not animating by default. Okay, in our
[8:04:40] render function. So here we already
[8:04:43] check for the current intersected object
[8:04:45] or the currently hovered object right
[8:04:47] right over here. So we can just check if
[8:04:50] the current intersect object current
[8:04:52] intersect object its name includes hover
[8:04:56] like so. If it does then we can play the
[8:04:58] hover animation. So let's just do play
[8:05:00] hover animation. And I think if you have
[8:05:05] different kinds of hover then you might
[8:05:07] want to have an additional parameter
[8:05:09] here. But what I want to is definitely
[8:05:11] the current hovered object which I we
[8:05:14] created up there. And then the second
[8:05:16] parameter will be if we are still
[8:05:18] hovering that or not. So let's just set
[8:05:20] that to true because we are by default
[8:05:23] hovering. If this is true if it's
[8:05:25] intersecting something and it has the
[8:05:27] name of hovering means we're hovering
[8:05:28] it. So, we set it to true. And let's
[8:05:30] just come up here and create that
[8:05:32] function now. So, I completely forgot
[8:05:34] what I just called it. Play hover
[8:05:35] animation. Okay, cool. So, play hover
[8:05:38] animation function. Whoops. We want to
[8:05:41] take in that object that we are passing
[8:05:43] in that we're hovering and is hovering.
[8:05:45] So, if we're hovering it or not. Now, we
[8:05:48] don't want to play this if the object is
[8:05:51] animating. So, we can just have a guard
[8:05:53] clause already. Object dot user data.
[8:05:56] So, we created this earlier. We haven't
[8:05:58] set this yet, but it's just in advance
[8:05:59] is animating. So if you know the object
[8:06:02] is animating, we don't want to animate
[8:06:04] it again. So we'll just return it and
[8:06:06] like so. So nothing will execute. So if
[8:06:09] this is false, well then once we're
[8:06:11] hovering, then that means we want it to
[8:06:13] set to true. So object user data user
[8:06:16] data is hovering is animating and we
[8:06:18] want to set that to true because now
[8:06:20] it's animating. So if we're hovering,
[8:06:23] let's play our hovering animation. So we
[8:06:26] can just do something arbitrary. I don't
[8:06:27] know if we need a timeline yet. So I'm
[8:06:29] just going to do gap.2
[8:06:32] and then object.cale. So we just get the
[8:06:34] object scale. We can set it x to object
[8:06:37] do user data user data that initial
[8:06:41] scale that we had originally dox. And
[8:06:43] then we can just multiply it by like
[8:06:46] some sort of random factor here. And I'm
[8:06:48] missing a comma here. And then we can
[8:06:50] just shift alt down arrow twice. And
[8:06:52] then do the same thing for y and z. But,
[8:06:55] you know, if you want to give them
[8:06:56] different scalings or if you only want
[8:06:58] to do X and Y, I honestly don't know yet
[8:07:00] cuz I haven't done it yet. So, I'm just
[8:07:03] going to do all of them and see what
[8:07:04] that gives me. We can set like a
[8:07:05] duration of like 0.5 seconds. And then I
[8:07:08] definitely want to ease in for like some
[8:07:10] stylistic effect. So, I think what I
[8:07:12] want to do is bounce in possibly. I
[8:07:15] don't know. And then we can set how how
[8:07:18] strong that is. And I'm just taking a
[8:07:20] wild guess here. But if you want to like
[8:07:22] actually look at it, you can actually
[8:07:24] see the ease visualizer on GSAP over
[8:07:26] here. And you can see, you know, how the
[8:07:28] ease would appear on like your scale and
[8:07:31] things like that. And then you can also
[8:07:33] make like your own custom ease. So right
[8:07:35] now I'm doing bounce out. So it's kind
[8:07:37] of like so. And then you can like adjust
[8:07:38] this over here. And then you can just
[8:07:41] copy it and then use it yourself. So
[8:07:43] that's really really cool. And actually
[8:07:44] looking at this, I think I want to do
[8:07:46] bounce out, not bounce in. So let's just
[8:07:47] do bounce out.
[8:07:50] And then we can do the same thing except
[8:07:52] for rotation. So let's just do
[8:07:54] object.rotation.
[8:07:57] And then let's just change this to uh
[8:07:59] initial rotation like so. And I forgot
[8:08:02] what axis it is. I only want to do it on
[8:08:06] I think it was x-axis because for our
[8:08:08] fans that were oriented the same way it
[8:08:10] was on the x-axis. So I'm going to take
[8:08:12] a guess x and I'm going to add like I
[8:08:15] don't know math.pi pi pi and then maybe
[8:08:18] like divided by 8 or something like
[8:08:20] that. This might be a little bit too
[8:08:21] much rotation, but we'll see. And by the
[8:08:23] way, if you don't want to use like unit
[8:08:25] circle values, that's totally okay. You
[8:08:26] can just like multiply it by like 01 and
[8:08:28] then just go trial and error from there.
[8:08:30] So since both of these have the same
[8:08:32] duration, we can just put the onmplete
[8:08:34] in either one of them. So once this is
[8:08:36] done completing, that means is animating
[8:08:38] is back to false. So let's just put in
[8:08:41] that call back on complete like so. What
[8:08:44] we what do we want to do? We just want
[8:08:47] to Whoops. This should be equals. We
[8:08:49] just want to set object do user data is
[8:08:52] animating. And we just want to set that
[8:08:53] back to false because it's no longer
[8:08:55] animating. Also, sorry, I just realized
[8:08:57] this should be is hovering, not just
[8:08:59] hovering. Sorry. Okay. So, if we're no
[8:09:02] longer hovering that thing, then what we
[8:09:05] can do is play the reverse of it. So,
[8:09:07] let's just copy and paste this right
[8:09:09] here over here. And then we can just get
[8:09:12] rid of the things that we created here.
[8:09:14] So, I'm just going to three cursors with
[8:09:16] alt controll x. Get rid of that. And
[8:09:19] then we can make it faster on the way
[8:09:21] back. So, we can just do something like
[8:09:22] this. Okay. So, yeah. Okay. Now, we need
[8:09:26] to make some adjustments to the render
[8:09:27] function. Here, I messed up. We don't
[8:09:29] want to play the the animation on the
[8:09:32] current hovered object. We want to play
[8:09:34] it for the current intersect object. So,
[8:09:36] every time we intersect the new object,
[8:09:38] that's when we're going to play the
[8:09:39] animation. The current hovered object
[8:09:41] will be the object that is in a hover
[8:09:43] state and this will keep track of when
[8:09:45] our mouse leaves and when it does we'll
[8:09:47] play it but we'll play the go back to
[8:09:49] original scale and set this second
[8:09:51] parameter to false. So what we want to
[8:09:53] do is current intersect object and then
[8:09:55] let's check if current intersect object
[8:09:59] does not equal equal the current hovered
[8:10:01] object which means we changed objects.
[8:10:04] So then we can move this in over here.
[8:10:06] Then we want to play the new animation
[8:10:08] for the new currently intersecting
[8:10:10] object. If that makes sense. Now we also
[8:10:13] need to update the current hovered
[8:10:15] object after we play the hovered
[8:10:16] animation to the current intersected
[8:10:19] object that we're then for the current
[8:10:20] hovered object. If we're playing this
[8:10:22] new one, then we can set the old one to
[8:10:26] play back to its original scale stuff.
[8:10:28] So then we'll just check if current. So,
[8:10:30] if current hovered object like so, and
[8:10:33] we'll just do play hover animation.
[8:10:34] Maybe that's not the best function name.
[8:10:36] Whoops. Anyway, we'll pass in the
[8:10:38] current hovered object this time and
[8:10:40] we'll set it to false. So, trigger that
[8:10:42] else statement and play this one going
[8:10:44] back to its initial state. And then in
[8:10:46] the event that there is no current
[8:10:49] intersect object and no current hovered
[8:10:51] object means we're not hovering
[8:10:52] anything, we want to set everything back
[8:10:54] to null. So again, just like over here
[8:10:57] with our else statement with the
[8:10:58] document body style doc cursor default,
[8:11:00] we just want to paste if current hovered
[8:11:02] object here. Then we'll set it play
[8:11:04] again. And then we this time we want to
[8:11:06] set the current hovered object equal to
[8:11:08] null. Just like so. Okay. So if I go
[8:11:10] back and take a look, it seems to be
[8:11:14] partially working. If I leave before the
[8:11:16] animation continues, it's not playing.
[8:11:18] And that makes sense because of this
[8:11:20] guard clause right here with is
[8:11:22] animating. it's just going to remain
[8:11:24] true and then it's just going to cancel
[8:11:25] it out. So what we can do instead is
[8:11:28] actually do gap.kill
[8:11:30] twins. So we can do gap.kill twins twins
[8:11:35] twins of and we'll do object.scale
[8:11:37] object.scale cuz we're we're attaching
[8:11:40] twins to object.scale. Right? This is
[8:11:42] what we're targeting right here. As well
[8:11:44] as object rotation. And if you have
[8:11:45] position, you can do that as well. I'm
[8:11:47] actually going to do that for position
[8:11:48] as well because I feel like I'm going to
[8:11:50] plan to do that in the future. uh just
[8:11:52] probably off camera or something. And
[8:11:54] then we actually don't need this user
[8:11:56] data thing here at all. And let me just
[8:11:58] so let's also get rid of child user data
[8:12:00] right there as well. Okay. So basically
[8:12:02] what's happening here is once this is
[8:12:04] playing if we leave our mouse initially
[8:12:07] g it's going to trigger this play hover
[8:12:09] animation and it's going to kill that
[8:12:11] tween. So it'll take whatever partial it
[8:12:13] is. Let's say like we start at scale of
[8:12:15] one and it's at like 1.1 when our mouse
[8:12:18] leaves. Gab is just going to kill this
[8:12:20] tween and then play this tween instead,
[8:12:22] right? Because we're no longer hovering
[8:12:24] it. And it'll just take that scale that
[8:12:26] it paused at and then immediately just
[8:12:28] go to the initial scale. So, this should
[8:12:30] be working now. So, now if I go back,
[8:12:32] you can see I can hover over everything
[8:12:33] and it'll it'll work perfectly fine just
[8:12:36] like so. So, here you can actually see
[8:12:38] this is why you probably need different
[8:12:41] versions for rotations because some of
[8:12:42] these, you know, they don't see they
[8:12:45] don't feel good with the same animation
[8:12:47] here. So here you can see I also have an
[8:12:49] issue because I had overlap. Those areas
[8:12:50] are black. So that's something I'm going
[8:12:52] to be fixing in Blender. We already know
[8:12:54] how to fix that. You can adjust your UVs
[8:12:56] or you can paint over it. And let's just
[8:12:58] go into local view over here. Let's just
[8:13:01] see. So it's just the top face over
[8:13:04] here. It's just the top few faces over
[8:13:06] here. Let's just hit period key just to
[8:13:07] see where that is. And I feel like we
[8:13:10] can just possibly bring it forward just
[8:13:12] like that. That actually looks pretty
[8:13:14] nice. Also, if you want to add two loop
[8:13:15] cuts here and just move that section,
[8:13:17] you could totally do that as well. But I
[8:13:19] don't think I need to do that. And I
[8:13:21] don't want to add that extra geometry.
[8:13:23] So, let's just see where this is. So,
[8:13:26] people are barely going to look at the
[8:13:28] back here. We could probably use like a
[8:13:29] knife tool and slice through it. If you
[8:13:31] don't know what a knife tool is, that's
[8:13:32] totally fine. Um, but I think what I'm
[8:13:35] going to do is just honestly just maybe
[8:13:38] uh I think I'm just I don't know what
[8:13:39] this is. I think that's the roof, but
[8:13:40] I'm just going to use the roof back
[8:13:42] instead. And yeah, that solves our issue
[8:13:44] as well. Of course, it's not seamless,
[8:13:47] but very, very few people are going to
[8:13:49] be paying that much attention here. I
[8:13:51] don't know if this is an issue or if we
[8:13:52] even see the bottom, but let's just hit
[8:13:55] period key to jump to it. And if you
[8:13:57] can't jump to it, it likely means that
[8:13:59] these are not on the same area on the UV
[8:14:01] map. So, these probably are. So, these
[8:14:04] are not. So, let's see. Where is this
[8:14:06] one? Oh, this one is also part. So, we
[8:14:08] can move that here. And then this one.
[8:14:10] And this one. And this one. Hopefully
[8:14:12] these are in the same area. Yes, they
[8:14:14] are. So here. So for this one, I can
[8:14:16] also just move it to like our
[8:14:19] wherever that is there. So yeah, again,
[8:14:23] we're wasting texture space by baking
[8:14:25] that area because we're not even using
[8:14:27] it anymore. But oh well, fast solutions.
[8:14:30] And honestly, we could probably only
[8:14:32] have baked one sign and then just use
[8:14:34] that sign's texture and not bake any of
[8:14:37] the other ones. that would have probably
[8:14:38] saved up a lot of texture space and we
[8:14:40] could have put like a lot of stuff. So
[8:14:42] yeah, just do it for the other signs and
[8:14:43] I'll see you on the other side. And then
[8:14:45] again, now is the time to add your other
[8:14:48] hover effects and you can just check for
[8:14:50] that. Basically what what I'm probably
[8:14:52] going to do off camera is like do scale
[8:14:54] factor scale factor and have a lot of
[8:14:57] other things like want scaling equal
[8:15:00] true and then if I want scaling then
[8:15:02] I'll do the scaling and if I want
[8:15:05] rotation then I'll also do the rotation
[8:15:07] and then this value will be determined
[8:15:09] like if object.name name contains v2
[8:15:13] like we already know converge contains
[8:15:14] hover so does it contain v2 if it does
[8:15:17] then scale factor equals like 1.5 and
[8:15:21] then scale factor would just be here and
[8:15:23] then I'll just update scale factor based
[8:15:25] on the object name or ID or whatever you
[8:15:28] want so I'm not going to show that
[8:15:29] because it's mainly just if statement
[8:15:31] checks but that's what I'm going to be
[8:15:33] doing off camera there. All right, let's
[8:15:35] disable orbit controls and raycaster
[8:15:37] when the model is open. So what I'm
[8:15:39] going to do is just have some sort of
[8:15:41] state variable. So probably honestly it
[8:15:43] doesn't really matter where and just do
[8:15:45] let is modal open is model open and
[8:15:49] we'll set that to false by default. And
[8:15:51] then if it is in show model what we can
[8:15:53] do actually let's just put it above the
[8:15:55] show and hide stuff. We can set is modal
[8:15:58] equal to true and we can just
[8:16:00] controls.enabled and set that to true.
[8:16:02] Again those are the orbit controls that
[8:16:04] we had. Sorry I mean false. We should
[8:16:06] set that to false because we want to
[8:16:07] disable it. And then we can just copy
[8:16:09] and paste this into hide model as well.
[8:16:11] But this time we're going to set this to
[8:16:13] true. And we're going to set this to
[8:16:15] false. And now in our render function,
[8:16:18] all we have to do is just have a guard
[8:16:19] clause or an if statement for our
[8:16:22] raycaster. So let's see where is our
[8:16:24] raycaster stuff. It's right here. So if
[8:16:28] does not equal. So if it's false means
[8:16:31] that we can do this. We can check for
[8:16:33] the ray cer and we should just be able
[8:16:35] to place it right. Now, this seems to
[8:16:37] start glitching out everything, and
[8:16:39] that's probably because when we bypass
[8:16:41] the raycast caster logic, none of this
[8:16:43] stuff is being set. So, it's like
[8:16:44] messing up. So, what we can do is come
[8:16:47] over back into show model and update all
[8:16:50] this stuff.
[8:16:51] So, if current hovered object, then we
[8:16:55] can just do the raycast caster stuff
[8:16:56] here. Play hover animation current
[8:16:58] hovered object, and we'll set that to
[8:17:00] false. And then we'll just set the
[8:17:02] current hovered object equal to null.
[8:17:05] And then we can also just set
[8:17:06] document.body
[8:17:08] style cursor. And we can set that back
[8:17:11] to default. And we can set that back to
[8:17:13] default. And then we can also clear all
[8:17:15] the current intersect objects. And we
[8:17:17] just set that equal to an empty array.
[8:17:19] And now if I go back. Cool. It works.
[8:17:22] Now, if you want to wait to enable
[8:17:25] controls, you can put it on on here.
[8:17:28] Like if you had some extra animation or
[8:17:30] something that you wanted to like wait
[8:17:32] until you went back to your original
[8:17:34] position and then you enable controls
[8:17:36] again, you could totally do that here as
[8:17:38] well. Also forgot to mention, don't
[8:17:40] forget that we need to also put is model
[8:17:43] open here. Whoops, sorry. Is model open?
[8:17:46] And if it is, then we just want to
[8:17:47] return guard clause for touch start and
[8:17:49] touch end. Because if you have like an
[8:17:51] overflow on your model that's open, it
[8:17:54] will prevent that default scrolling
[8:17:56] behavior where you like touch and drag
[8:17:57] to scroll. So that would require you to
[8:18:00] use the scroll bar instead of just
[8:18:01] touching. And the scroll bar might
[8:18:03] glitch out a little bit. So make sure to
[8:18:04] have this guard clause here as well for
[8:18:06] the touch start and touch end event
[8:18:08] listeners. All right. Now, let's limit
[8:18:10] our controls so they don't see the back
[8:18:12] of this area. So if you remember when we
[8:18:14] first started our camera started like
[8:18:16] smack dab right over here. So that means
[8:18:19] if if our camera spawned over somewhere
[8:18:21] over here over there. So the origin is
[8:18:23] somewhere over there which means we want
[8:18:25] a maximum of 90° in this way. By default
[8:18:28] a maximum of 90° this way is already in
[8:18:31] place. But we can also go underneath the
[8:18:34] surface. So here we actually want a
[8:18:36] minimum of 0°.
[8:18:38] So we just have to set this and this.
[8:18:40] And if you want to be explicit, you can
[8:18:41] set the top one as well. So the polar
[8:18:43] angles, you know, just like north pole,
[8:18:45] south pole, if you want to be explicit
[8:18:47] about it, you can set it. So for
[8:18:49] definitely the min angle, we can do
[8:18:50] controls dominar angle. Min polar angle.
[8:18:54] And we're going to set that to zero. So
[8:18:56] now we can't go below the floor. And
[8:18:58] then we can set the max. So like when we
[8:19:00] drag down instead, we can set it to math
[8:19:04] pi / 2
[8:19:07] or 90°. Right? Just like on the unit
[8:19:09] circle over here, pi / by two, like so.
[8:19:12] And then again, if you don't know where
[8:19:14] these properties are, you can go to the
[8:19:15] orbit controls documentation, and it'll
[8:19:17] tell you what these actually stand for.
[8:19:19] And then I want to set the left. Oh
[8:19:21] yeah, I forgot to mention, but when we
[8:19:23] go left, we don't want to go any
[8:19:25] rotation. So we're also going to set
[8:19:26] that to zero. So we'll call that minumth
[8:19:30] angle. That's what they call it. And
[8:19:31] we're going to set that to zero. So we
[8:19:33] can't go any further left. And then
[8:19:35] controls domax, a zero angle. And again
[8:19:38] that will also be math.py / two. So now
[8:19:42] if I go back you can see I can't go left
[8:19:44] anymore beyond this. And over here yes
[8:19:47] our camera starts here but those
[8:19:49] properties are relative to the camera
[8:19:51] starting position. So you can see that
[8:19:55] we can't go below and we can't go above
[8:19:56] and we can't go to the right. Super
[8:19:58] cool. So we're kind of constrained here.
[8:19:59] Now, another thing I want to limit is
[8:20:01] the distance that they can go in and out
[8:20:04] because if they keep going too far, you
[8:20:06] know, then they'll see emptiness. So, we
[8:20:08] can change that. We can also prevent how
[8:20:10] close they get. Again, these are also
[8:20:12] properties in the documentation. And
[8:20:14] I'll set this to like five. And then
[8:20:16] controls domax distance. I don't know.
[8:20:18] I'm just going to take a wild guess and
[8:20:20] say like 50 or something. So, now you
[8:20:22] can see if I dolly in, I can't go any
[8:20:25] for closer beyond this point. So, maybe
[8:20:27] you want them to go closer. I don't
[8:20:29] know, kind of up to you. And then when I
[8:20:31] go farther away, this is going to be the
[8:20:32] maximum that I'm looking for. And then
[8:20:34] on mobile, this seems to be okay for
[8:20:37] mobile as well. So the next thing I want
[8:20:38] to do is limit how much they pan because
[8:20:40] I don't want them to like pan off over
[8:20:42] here, you know, into oblivion. Now, the
[8:20:44] way we do that is by limiting the
[8:20:46] target. So by default, orbit controls
[8:20:49] has, you know, well, we have a camera,
[8:20:51] right? And then orbit controls has this
[8:20:54] thing called a target that it looks at.
[8:20:56] So if we constrain the target to a
[8:20:58] certain location and the target only can
[8:21:00] move within this location then we
[8:21:03] essentially also limit you know how much
[8:21:05] a user can pan. Okay. So in order to do
[8:21:07] that it's easier just to edit orbit
[8:21:09] controls. So hold control and just like
[8:21:12] click here just to quickly jump to orbit
[8:21:14] controls code. And you can see here this
[8:21:18] is all the orbit controls code. So let's
[8:21:20] just copy this and let's come into our
[8:21:22] own area source. Over here, we can
[8:21:24] create a new folder called utils. And
[8:21:27] then we'll just call this orbit
[8:21:28] controls.js.
[8:21:30] Let's just paste this in here. And then
[8:21:32] for our main.js, instead of importing it
[8:21:35] from our node modules package, we'll
[8:21:38] just do slash
[8:21:40] utils/orbit
[8:21:42] controls.js
[8:21:44] just like so. And you can see it still
[8:21:45] works. Cool. Let's go to the orbit
[8:21:48] controls that we created. Make sure
[8:21:49] you're not in the node modules one.
[8:21:51] Okay. So in our orbit controls, let's
[8:21:53] just you can put it anywhere. We're
[8:21:55] going to create a min and max pan. So
[8:21:58] let's do const min pan and we'll just
[8:22:01] set it equal to a new vector 3. This
[8:22:04] time we're not using dot notation
[8:22:06] because they imported it with object
[8:22:08] deconstruction. When we did it, we did
[8:22:10] import everything as three. So that's
[8:22:12] why we're doing three dot vector 3 in
[8:22:14] here. But here they deconstructed it. So
[8:22:17] now we don't have to do three dot. So
[8:22:18] now we can just set some stuff. I don't
[8:22:21] know, maybe I'm just going to guess
[8:22:22] maybe likegative 1gative 1gative -2
[8:22:26] something like so. And then here I want
[8:22:28] them to be able to go up in the y- axis
[8:22:30] like 5 units and then you know maybe a
[8:22:33] little bit on you know this will just be
[8:22:35] the other corner pretty much. So we can
[8:22:37] try something like this and let's change
[8:22:38] this to max pan. And now what we want to
[8:22:41] do is find the area where the pan is
[8:22:45] being set. So there's probably some sort
[8:22:49] of this.target area or something.
[8:22:53] So if we look for target.
[8:22:56] Yeah, we have this.target. So this is
[8:22:58] where at some point they're probably
[8:23:01] setting this somewhere. So we can just
[8:23:02] search for that. Let's see
[8:23:05] this dot move target to pan location.
[8:23:08] Cool. So okay. So we should be able to
[8:23:10] just clamp over here. So now we can just
[8:23:13] do this.target.clamp clamp and we'll put
[8:23:16] our min pan and our max pan in here like
[8:23:20] so. And again, a clamp is a vector 3
[8:23:22] method as you can see that I'm hovering
[8:23:24] over there, which you can also find in
[8:23:25] the documentation if you need to. So now
[8:23:27] if I go back here, you can see that my
[8:23:30] pan is limited. I can go a little bit to
[8:23:32] the right and then over here I can't go
[8:23:35] any more below that. Cool. And I can't
[8:23:38] go any more above five. So if you want
[8:23:41] to increase that, I feel like I want to
[8:23:43] increase that. You can definitely play
[8:23:44] around with this. I definitely want to
[8:23:46] be and I can see I can go much higher.
[8:23:48] So yeah, just play around with it until
[8:23:50] you get something that you like. Okay,
[8:23:52] so now what I want to do is have some
[8:23:54] intro animations. So basically, you
[8:23:57] know, once we load on the page, you
[8:23:58] know, things animate in like this over
[8:24:00] here, just to catch the user intention,
[8:24:02] you know, areas that they can click on
[8:24:04] later. So before I talk about that, I
[8:24:06] just want to talk about you'll notice a
[8:24:08] few things like the fish going up and
[8:24:10] down and the chair going left and right
[8:24:11] and why I didn't show that. And the
[8:24:13] reason I'm not covering that in this
[8:24:15] video is primarily because it's very
[8:24:17] very similar to when we were doing the
[8:24:20] fans. Basically, I created a variable
[8:24:22] and then I checked for the name and then
[8:24:24] I just set that child and then I just
[8:24:26] set that variable equal to the child if
[8:24:28] they find it. And then in my render
[8:24:29] function, I just animated like so.
[8:24:31] There's not much different than what we
[8:24:33] did with the X and Yaxis fans. Now, you
[8:24:35] might be looking at this and thinking
[8:24:37] like, wow, this is extremely tedious.
[8:24:39] You have to check for the chair name
[8:24:41] every time. You have to check for the
[8:24:42] chair. You have to assign a variable.
[8:24:44] You have to do all this thing. That's
[8:24:46] kind of extremely tedious. Is there a
[8:24:47] better way to do that? And the answer is
[8:24:49] actually yes. And the reason I didn't do
[8:24:51] it in this video is probably because I
[8:24:53] wasn't planning to animate so many
[8:24:55] things, honestly. Um, but the the
[8:24:57] general idea is when it comes to your
[8:24:59] naming convention, what you can do is,
[8:25:01] you know, like our names, they're like
[8:25:03] really long like ray caster and then
[8:25:05] like third and so on so forth. The the
[8:25:07] idea instead of having to always check
[8:25:09] the name and always creating a variable
[8:25:11] and all that sort of stuff is you just
[8:25:14] create like an object and you'll just
[8:25:16] call it like const items, you know,
[8:25:18] whatever you want to call it. And then
[8:25:20] you can use like a split string or
[8:25:23] regress, you know, however you want to
[8:25:24] split up your string. And this like
[8:25:27] first part can be like your key or your
[8:25:30] object. So it'll just automatically
[8:25:32] generate a key called chair top for you.
[8:25:35] And then you can also check what other
[8:25:36] things are included that string like ray
[8:25:38] caster third so on so forth and then
[8:25:41] associated with that you can have those
[8:25:43] specific properties. So here you can
[8:25:45] have like the mesh which would just be
[8:25:46] the child itself. So you would
[8:25:48] automatically generate the child. So
[8:25:50] instead of having to always create a
[8:25:52] variable and accessing it you can just
[8:25:54] do items you know chair top chair top
[8:25:57] mesh. That way you don't have to you
[8:25:59] know create so many variables and then
[8:26:00] any any item you want to do you can do
[8:26:02] that. And then have other properties
[8:26:04] like raycaster and then maybe true. It
[8:26:07] doesn't have to be boolean. It could
[8:26:08] just be a string too like raycaster
[8:26:10] raycaster. Otherwise it'll be like null
[8:26:13] or something if it doesn't have the
[8:26:14] hover effect. And then when you check if
[8:26:16] it has raycaster you don't have to check
[8:26:18] if you know check for the name again. So
[8:26:20] on so forth. You can just do items.
[8:26:22] Chair top does you know. Raycaster. And
[8:26:25] if it's null honestly just don't even
[8:26:27] put it in the object. That way it would
[8:26:28] just then you just go through the list
[8:26:30] of items and then check if and then you
[8:26:32] just check you know like does chair top
[8:26:34] have the property of raycast like if you
[8:26:36] know if items do chairtop raycaster and
[8:26:40] then if it doesn't then it's like oh
[8:26:42] okay it doesn't have raycaster so don't
[8:26:43] do anything about it and obviously you
[8:26:45] know when you have a loop this wouldn't
[8:26:47] be manual this would just be you know
[8:26:48] whatever item you put in here this would
[8:26:50] just be the key that's going through the
[8:26:52] loop right so this way you don't have to
[8:26:53] create so many variables and check for
[8:26:55] it and do all that stuff over and over
[8:26:57] in. And honestly, if I knew I was going
[8:27:00] to animate this these many things, I
[8:27:02] probably would have done that in the
[8:27:03] first place. But I just thought that,
[8:27:05] hey, we just doing it one time, it's not
[8:27:07] a big deal. But, you know, now it's
[8:27:09] becoming a little bit of a big deal. But
[8:27:11] that's totally okay. And it's kind of
[8:27:12] too late to change it because we would
[8:27:14] have to change a lot of things. So,
[8:27:15] we're just going to finish out this
[8:27:17] video just by creating more variables
[8:27:19] for our final animated objects. Yes,
[8:27:22] it'll be a little bit tedious, but, you
[8:27:23] know, copy and pasting helps a little
[8:27:25] bit. So, one thing I definitely want to
[8:27:26] animate, like I said earlier, is these
[8:27:28] planks in here and then these coming in
[8:27:30] here. And then I guess everything else
[8:27:32] is kind of a little bit more optional,
[8:27:34] but the reason particularly not only for
[8:27:37] visual appearance, but also to, you
[8:27:40] know, let the user know what are going
[8:27:41] to be the more primary areas for you to
[8:27:44] click on. So, in order to animate these
[8:27:46] to a scale of one, well, then we have to
[8:27:48] set an initial scale for all of them to
[8:27:50] be zero or however you want to animate
[8:27:53] it. So it could be a rotation that you
[8:27:55] set initially as well. So I'm not going
[8:27:57] to bore you with typing that out. But
[8:27:58] here you can see that I just found my
[8:28:00] name and then I set the child scale and
[8:28:03] then I set all the variables here equal
[8:28:05] to the child as I go through there. If
[8:28:07] we find it now again you'll see a lot of
[8:28:11] redundant code here. And yes, this isn't
[8:28:13] great. You could also go back into your
[8:28:15] Blender file and for each of the things
[8:28:17] you want to animate, you can do
[8:28:18] underscorean animate, you know, and then
[8:28:21] check for that and then set all the
[8:28:22] scales with animate to 00 or whatever
[8:28:24] you want, you know, like if animate and
[8:28:28] hanging plank_1,
[8:28:30] then do this instead. Otherwise, you
[8:28:32] know, just set 000 here. You know, it's
[8:28:35] like we're just hard coding everything.
[8:28:37] And again, and yeah, like like I said
[8:28:39] earlier, you know, I would definitely go
[8:28:40] for a more automatic approach than what
[8:28:42] we're looking at right here, but you
[8:28:44] know, it's totally okay because at least
[8:28:46] at least uh at least you know, people
[8:28:48] know what we're doing here. So, it's a
[8:28:50] little bit crazy and you know, people
[8:28:52] are going to judge you for it, but you
[8:28:53] know, it works and um you know, at least
[8:28:56] it's it's it's readable in a sense.
[8:28:58] Okay. So, now what I want to do is
[8:29:00] create a function like play intro
[8:29:02] animation. So, I'm just going to do play
[8:29:04] intro animation, but name it whatever
[8:29:06] you want. And I'll play it as soon as we
[8:29:08] add our GB scene or scene. We're going
[8:29:10] to later move this after our custom
[8:29:13] loading screen is done. So, I'll just
[8:29:15] come over here and do function play
[8:29:16] intro animation like so. And I want the
[8:29:19] side over here to play at the same time
[8:29:21] as my Boba stuff over here. So, what we
[8:29:24] can do is create two GSAP timelines. One
[8:29:27] for the set over here and one set for
[8:29:29] over here. If you want to, you don't
[8:29:32] have to use Gap timelines at all and you
[8:29:34] can just like hardcode when it animates
[8:29:36] in and that would work perfectly fine as
[8:29:38] well. Additionally, you could use one
[8:29:39] Gap timeline rather than two different
[8:29:41] ones and then adjust the timing factors
[8:29:43] on the single one rather than two.
[8:29:45] Again, that's really up to you. I'll be
[8:29:46] doing two timelines, one for here, one
[8:29:49] for here. Now, you might be asking,
[8:29:50] okay, if you have three different ways
[8:29:52] to approach this when it comes with
[8:29:55] GSAP, which one's best? And for this
[8:29:58] specific idea, for this specific
[8:30:00] project, all three of them are perfectly
[8:30:02] valid and they're probably equal in
[8:30:04] terms of complexity. Honestly, it's
[8:30:05] probably just your up to your preference
[8:30:07] at this point. If you wanted to, again,
[8:30:09] you could also go back into Blender and
[8:30:10] give them IDs and names to automatically
[8:30:14] generate a timeline for you in a
[8:30:15] specific order rather than hard- coding
[8:30:17] it yourself. However, I will be hard
[8:30:19] coding it just so it's a little bit
[8:30:20] clear. So, the first thing I'm going to
[8:30:22] be doing is creating a const T1 gap
[8:30:25] timeline. These have timeline like so.
[8:30:28] And I want to set some defaults which
[8:30:30] means every time we play an animation,
[8:30:32] it has these certain animation features.
[8:30:35] So one is probably duration and I'll set
[8:30:37] that to 0.8. So every time one of the
[8:30:40] meshes scale, it'll take about it'll
[8:30:42] take 0.8 seconds. I also want to do the
[8:30:44] same thing with their ease. All the
[8:30:46] eases will be back dot out. And I want
[8:30:49] to probably probably put in a intensity
[8:30:52] of like 1.8. Again, if you don't want a
[8:30:55] consistent ease, you can actually just
[8:30:57] replace the ease in the timeline itself
[8:30:59] and it will override the default. Cool.
[8:31:00] So now what we can do is use T1.2. So 2
[8:31:04] and GB just takes your original value
[8:31:05] and goes to the new value. So we'll do
[8:31:08] plank one scale, which is what I call
[8:31:11] hanging plank one. And I'm going to set
[8:31:13] its Z to one and its X to one as well.
[8:31:18] You can see that that's exactly what we
[8:31:20] get. And now we can just do method
[8:31:22] chaining. So we can just do two. Again,
[8:31:24] if you want to split it up to T1.2,
[8:31:26] T1.2, so on and so forth, you could
[8:31:28] totally do that. But I'm just going to
[8:31:29] be using method chaining. Okay. So let's
[8:31:31] do plank 2.cale
[8:31:34] like so. Come over here. And this time I
[8:31:37] want to set all X, Y, and Z to one. So
[8:31:40] let's just go in order X and then Y and
[8:31:42] then set it to one. And then we might as
[8:31:44] well finish it up right now. So I'm just
[8:31:46] going to paste that. Paste it again.
[8:31:48] Paste it again. This one will be work
[8:31:50] button. This one will be I think it's a
[8:31:53] bad button. Yes. Cool.
[8:31:56] And then this one will be contact
[8:31:58] button. So if I go back it should play
[8:31:59] in. It comes in goes down up like so.
[8:32:02] And you can see that comes just like
[8:32:04] that. And uh we have an issue. And
[8:32:07] that's makes sense because we are saving
[8:32:10] in our user data the initial scale
[8:32:12] position and rotation. So that means all
[8:32:15] we have to do is just move this below
[8:32:18] that. So let's see. Hopefully that is
[8:32:20] outside of
[8:32:23] this ray caster. Let's see. It's right
[8:32:25] here. Yeah. So, we should just be able
[8:32:27] to move it below this and everything
[8:32:29] should be fine. Yep. And now everything
[8:32:32] is back to working. Cool. So, it copies
[8:32:34] So, it copies the original scale before
[8:32:37] we set it back to 0 0. Super cool. Now,
[8:32:40] I don't like how it goes one at a time.
[8:32:41] I want them to sort of overlap with each
[8:32:44] other. And the way to do that is by
[8:32:45] using relative values related to your
[8:32:48] previous animation or your forward
[8:32:49] animation. And you also have absolute
[8:32:51] values as well that you can use of if
[8:32:53] you want to as well. But for us, we're
[8:32:54] going to be using relative values, which
[8:32:56] means it's going to be relative to
[8:32:58] something. In this case, it'll be to our
[8:33:00] previous animation in the timeline line.
[8:33:02] And here you can see there's a lot of
[8:33:04] different ways to do that. And then
[8:33:06] maybe for plank 2, I want to start a
[8:33:08] little bit early at plank one scaling.
[8:33:12] So we can do like minus= 0.5 seconds. So
[8:33:17] essentially this should start at 0.3
[8:33:20] seconds in plank 1.scale and then we can
[8:33:23] just copy that for these other ones. I
[8:33:25] don't know if so I don't know if I want
[8:33:27] to offset it any differently. So we can
[8:33:29] just copy it to the other ones as well.
[8:33:31] So now if I go back it should play.
[8:33:35] It seems like the easing is not working.
[8:33:38] So let's take a look if I messed up
[8:33:40] somewhere. And indeed I did. I don't
[8:33:42] have the defaults object that we need to
[8:33:44] put our defaults in. Whoops. So let's
[8:33:47] just move that into our defaults object.
[8:33:49] And now you can see it works
[8:33:50] appropriately.
[8:33:54] Cool. Now I want these to play a little
[8:33:56] bit faster on their own animations cuz
[8:33:59] right now it seems a little bit too
[8:34:00] slow. So we can just change this to like
[8:34:03] 0.6 like so.
[8:34:07] And now you can see we kind of get a
[8:34:09] more nice effect. Now for the boba and
[8:34:11] the work items, we can actually do the
[8:34:13] same exact thing. So we can just copy
[8:34:15] and paste this. Again, I would probably
[8:34:18] automate this in the future rather than
[8:34:20] what we're doing, but you know, it's
[8:34:21] totally okay. So here we can change this
[8:34:23] to T2. And then we can change this one
[8:34:25] to T2 as well. And we can change this to
[8:34:27] Boba. And Boba also has a scale uh this
[8:34:30] time of Y as well of zero. So we're
[8:34:32] going to set that to one. Then we can
[8:34:34] change plank 2 to GitHub YouTube like
[8:34:38] so. and then Twitter.
[8:34:41] Twitter and then we don't have anything
[8:34:42] after that. So, we can just get rid of
[8:34:44] this. So, now if I go back and refresh
[8:34:46] the page, you can see they're playing at
[8:34:48] the same exact time. Super super cool.
[8:34:51] Super cute. Super awesome. Also, by the
[8:34:53] way, if you get something that you
[8:34:56] really like, except it goes a little bit
[8:34:57] too fast. You don't have to, you know,
[8:35:00] hate your life and then go back and
[8:35:02] change every single value. There's
[8:35:04] actually this thing in Gap called time
[8:35:07] scale where you can just like set the
[8:35:08] time scale for it. So here you can just
[8:35:10] see after every time I created the
[8:35:12] timeline, I just gave it a scale of 80%.
[8:35:14] So 80% speed. Of course you can change
[8:35:16] that per your timeline. Here you can see
[8:35:18] it plays 20% slower. Super super cool,
[8:35:21] just how I like it. Okay, so now I just
[8:35:24] want to talk about my loading screen
[8:35:25] here. So if I refresh the page, you can
[8:35:27] see loading and then I can hit this
[8:35:29] enter button and then I'll enter and
[8:35:31] just like so. So I want to briefly talk
[8:35:34] about how I did that. So the first thing
[8:35:36] is I needed some styles here. So what I
[8:35:39] did was I made the entire loading screen
[8:35:41] a little bit larger than the screen
[8:35:44] itself. And that's because I wanted the
[8:35:46] border to not be visible initially from
[8:35:49] the start. Especially because I have a
[8:35:50] border radius. And if you have a border
[8:35:52] radius, the tiny little corners there
[8:35:55] would show. So I made it expand a little
[8:35:57] bit out of the viewport. Additionally, I
[8:35:59] kind of like the style better when the
[8:36:01] loading screen didn't have a border
[8:36:03] around it, which is why I don't have a
[8:36:05] border here. And yes, I know I'm mixing
[8:36:07] pixels and rims and things like that.
[8:36:09] It's not the prettiest code, but I am uh
[8:36:12] my prototyping habits die hard. For the
[8:36:15] intro stuff, I used the loading manager.
[8:36:18] So, here you can see that in 3GS.
[8:36:21] Basically, you just attach it to your
[8:36:23] con loader. So I created my manager
[8:36:25] loader and I just attached it to the
[8:36:28] gltf loader. So here you can see I just
[8:36:30] passed in my manager to that glTF loader
[8:36:32] and that's pretty much all you did. And
[8:36:34] then just like the gltf loader then
[8:36:36] we're loading our models. This also has
[8:36:38] a onload callback function that you can
[8:36:41] do something you know once the loading
[8:36:42] is completed. So that's all I did here.
[8:36:44] I just set once everything was done
[8:36:46] loading I just set a bunch of styles and
[8:36:49] then also you know when it's done
[8:36:50] loading what I did was I add some event
[8:36:52] listeners to loading screen button so
[8:36:55] that way I can click on it and then it
[8:36:56] triggers this handle enter event which
[8:36:59] sets some more styles it also changes
[8:37:01] the favi icon and then play some music
[8:37:04] which I didn't talk about but I will get
[8:37:06] to in a little bit and then it plays
[8:37:08] this another function here called play
[8:37:10] reveal and this just is another timeline
[8:37:12] where I take loading screen, do some
[8:37:15] animations to it. You might be
[8:37:16] wondering, okay, how did I know this
[8:37:18] looked good? How do you know what that
[8:37:20] is at all? And honestly, I don't know,
[8:37:22] honestly. I was just trying things until
[8:37:23] I got something that I like. These are
[8:37:25] just 3D CSS properties. You know, you
[8:37:27] might just go for a basic opacity. You
[8:37:29] might go for a reveal effect, you know,
[8:37:31] a clip path animation. It's it's really
[8:37:33] up to you. But one thing that's
[8:37:34] important here is when it's done
[8:37:36] animating, you want to remove the
[8:37:37] loading screen from your DOM, not just
[8:37:40] hide it. So that's why when the
[8:37:42] animation is done I am loading screen
[8:37:44] over here and now you can see instead of
[8:37:46] adding it after this scene.gb sorry
[8:37:49] scene.add
[8:37:51] I removed that and then I put play intro
[8:37:53] animation on complete of the play reveal
[8:37:56] animation. So just again you can see I
[8:37:58] just changed the button styles here and
[8:38:01] then as soon as it's done playing it
[8:38:03] plays the intro animations with all the
[8:38:05] meshes animating in. So when it comes to
[8:38:07] audio uh I like to use how.js JS because
[8:38:11] it helps you know standardize things
[8:38:12] across different devices and browsers.
[8:38:14] It's fairly simple. You just create like
[8:38:16] a how and then there's a lot of things
[8:38:18] that you can do with it like yeah you
[8:38:20] just navigate there and then you can use
[8:38:22] you know like play so it should be play.
[8:38:25] Yeah here you can see play when I click
[8:38:26] it starts playing the music and here you
[8:38:28] can also see I have like volume so you
[8:38:30] can set the volume. Uh yeah that's
[8:38:32] pretty much it. I feel like I'm going to
[8:38:34] clean up some of the code, you know,
[8:38:36] hopefully by the time this video is
[8:38:38] released and then but for the rest of
[8:38:41] it, it's mainly just CSS styling and
[8:38:43] then a lot of bunch of other Gap stuff
[8:38:45] that we already know how to do. It just,
[8:38:48] you know, it's just a bunch of time
[8:38:50] consuming stuff. Oh, actually, sorry,
[8:38:51] one last thing that I didn't mention is
[8:38:54] to make the starting responsive. What I
[8:38:56] did is I just had one initial check, you
[8:38:59] know, just below my controls on
[8:39:01] window.in width. If it's less than 768
[8:39:04] pixels, then I'm setting this target in
[8:39:06] position. Otherwise, I kept our same
[8:39:09] desktop one over here with some slight
[8:39:11] modifications. That way, when they're on
[8:39:12] mobile, the entire room is in frame
[8:39:15] because if you leave this by default,
[8:39:17] it'll be too close. Maybe whatever your
[8:39:19] scene is going for, your desktop also
[8:39:21] works for your mobile version, but mine
[8:39:23] didn't. So, I set my camera a little bit
[8:39:25] farther back. And this only runs once
[8:39:26] and it only checks once. This is not a
[8:39:29] on resize sort of thing. Okay. So now
[8:39:31] what we can do is just push. So as like
[8:39:36] set starting just so I have a camera
[8:39:39] here. I mean a comment that I can push
[8:39:41] or something. So we can just make well I
[8:39:43] was pushing off camera but we can just
[8:39:44] make one last push here and just do
[8:39:48] let's go epicio. Let's do this. Woo.
[8:39:54] Woo. All right. That's awesome. And then
[8:39:56] we can just get push. Get push. And then
[8:39:59] since we already deployed it earlier in
[8:40:02] the video, it should automatically
[8:40:03] deploy to Verscell. Yeah. So that's
[8:40:05] pretty much it for the video. I guess I
[8:40:07] just wanted to some final comments and
[8:40:09] shout out to my Patreon supporter. Shout
[8:40:11] out to Jason L. Thank you for supporting
[8:40:14] me on Patreon. If you'd like to support
[8:40:16] the videos that I do, you know,
[8:40:18] definitely please check me out. Maybe
[8:40:20] I'll post some more extra tips and
[8:40:22] tricks here or something like that. Of
[8:40:24] course, if you need help, you can always
[8:40:25] email me. I am most active on Discord.
[8:40:28] So if you need help, you know,
[8:40:29] definitely reach out to me through
[8:40:31] Discord. That would be my preferred
[8:40:32] communication method. Email is totally
[8:40:34] fine as well. So, you know, some future
[8:40:37] challenges you could probably do like
[8:40:39] this piano or like these fish and these
[8:40:41] other things that I didn't cover in this
[8:40:43] video, like we know how to target the
[8:40:45] fish. And then we also know about the
[8:40:47] sign function and things like that. So,
[8:40:49] you could consider how to do that. Same
[8:40:52] thing with the piano. You can imagine
[8:40:53] that the origin points are over there.
[8:40:55] When you download the blend roof file,
[8:40:56] you'll notice that all the origin points
[8:40:58] for the black keys are at their top over
[8:41:00] there. So, all I did in Gab was just
[8:41:02] rotate it and scale it when I clicked on
[8:41:04] there, just like so. Yeah. So,
[8:41:06] definitely share what you create. It
[8:41:08] doesn't have to be a room. You know, tag
[8:41:09] me. I'd love to see it. And um I guess I
[8:41:13] will also mention that there's a lot of
[8:41:15] things that you see that I did not
[8:41:17] cover, like this coffee steam. This is
[8:41:19] actually from Bruno Simon, a very very
[8:41:22] popular, he's one of the most, if not
[8:41:24] the most popular 3JS developer, and he
[8:41:26] has this really awesome course that I
[8:41:27] highly recommend. I'm not sponsored by
[8:41:29] him in any way. I just really really
[8:41:31] recommend it. And even if you don't
[8:41:32] learn anything from the lessons, the
[8:41:34] community that you get is well worth the
[8:41:37] price. So, you know, if you have some
[8:41:39] money, you know, definitely purchase it.
[8:41:41] And it it goes on sale often for like
[8:41:43] Easter and uh a lot of really big
[8:41:46] holidays. So, you know, definitely keep
[8:41:48] a lookout for that. I just mentioned
[8:41:50] Easter because I feel like that's the
[8:41:51] closest holiday here in the United
[8:41:53] States. You also noticed that I have
[8:41:55] night and theme toggle between switching
[8:41:57] between day and night textures. This is
[8:41:59] also a shader. You can see it over in
[8:42:02] here theme. I was planning to cover in
[8:42:04] this video, but I decided not to, but
[8:42:06] the code is there if you want to take a
[8:42:08] look. However, I do plan in my next
[8:42:10] video to cover shaders. So, yeah. Thanks
[8:42:13] so much for watching. Hopefully, you
[8:42:14] enjoyed. Hopefully, you learned
[8:42:15] something. uh you know definitely tag me
[8:42:17] when you create something and post it on
[8:42:19] social media. I'd love to see it and I'm
[8:42:21] sure a lot of other people would really
[8:42:23] love to see it as well. Again, thanks so
[8:42:25] much for watching and I hope to see you
[8:42:26] in my next video. Take care. Peace out.
[8:42:29] Bye.
