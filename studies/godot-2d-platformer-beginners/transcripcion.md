# Transcripción — Godot Game Development for Beginners

- Fuente: https://www.youtube.com/watch?v=MiPkcTaRbfQ
- Canal: freeCodeCamp.org
- Expositoras: Sarah y Reem (Hack Club)
- Publicado: 2025-09-10
- Duración: 00:57:59 (3,479 s)
- Idioma: inglés · Motor: **Godot** (instalación de la última versión estable en godotengine.org)
- Subtítulos: automáticos de YouTube, pista `en-orig`, **1,394 bloques** normalizados y deduplicados
- Último cue: 00:57:55 (cobertura hasta el final del video)
- Formato: `[h:mm:ss]` al inicio de cada bloque. La cita en el outline usa el inicio del bloque que contiene el fragmento.

## Glosario de errores del ASR

Los subtítulos automáticos deforman los nombres propios, los nodos de Godot y varios términos. Los cues **no** se editan: la corrección vive acá.

| Como aparece en el cue | Lectura correcta |
|---|---|
| «Beam», «Reem», «Mayne», «S-path», «my S-path» | **Reem** (la segunda expositora) |
| «tile map layer», «tile map» | **TileMapLayer** (nodo de Godot 4). En 4.3+ reemplazó al `TileMap` único |
| «terrain zero», «terrains» | **Terrain Set** / **Terrain** dentro del *TileSet* (autotiling) |
| «character 2D», «character body 2D» | **CharacterBody2D** |
| «area 2D», «animated ball», «animated ball body 2D» | **Area2D** / **AnimatableBody2D** (el ASR dice «animated ball body»: es *animatable*) |
| «path follow 2D», «remote transform 2D» | **PathFollow2D** / **RemoteTransform2D** |
| «animat- animated sprite», «animation player» | **AnimatedSprite2D** / **AnimationPlayer** |
| «parallax 2D», «pair of waxing», «sketch» | **Parallax2D** (4.3+) / *ParallaxBackground*. El ASR de «parallax» sale como «pair of waxing» |
| «sketch parallax» | Nombre que la expositora empieza a escribir y corrige |
| «AppClipSlack» | Handle de Hack Club (Slack) — el ASR lo parte; no es un servicio llamado así |
| «good dough», «Godot» | **Godot** (el ASR deletrea la marca) |
| «my S-path» / «oopsies» / «my bad» | Muletillas de la expositora; no son comandos |
| «at on ready» | **`@onready`** (anotación de GDScript) |
| «time.get_fixed in the second by then thousand» | **`Time.get_ticks_msec()`** y luego `Time.get_ticks_msec() / 1000.0` |
| «tile size 32 by 32», «texture region» | `tile_size = 32×32` y el *texture region* del atlas |
| «local to scene» | `resource_local_to_scene` en el `PathFollow2D` |
| «body enter signal» / «body entered» | Señal **`body_entered`** de `Area2D` |
| «queue free» | **`queue_free()`** |
| «get tree . get current scene» | **`get_tree().current_scene`** / `scene_file_path` |
| «it's a little janky», «super cute» | Registro coloquial de las expositoras; no es terminología |
| «Hack Clubber» | Miembro de Hack Club |
| «control S or command S» | Atajo de guardado de escena |
| «itch.io», «export templates» | Correctos: plataforma de publicación y plantillas de exportación |

El video es de **2025-09-10**; la UI de referencia es Godot 4.x (los nodos citados son los de 4.3+, con `TileMapLayer` y `Parallax2D` ya separados del `TileMap`/`ParallaxBackground` viejos).

---

[00:00:00] This course will guide you step-by-step
[00:00:02] through building your very own first
[00:00:04] game using the Godot game engine. You'll
[00:00:07] start by setting up Godot and getting
[00:00:09] comfortable with the editor. From there,
[00:00:11] you'll create levels, design tile sets,
[00:00:14] and add a player character. The lessons
[00:00:16] also cover checkpoints, scoring, and
[00:00:18] adding enemies to make the game more
[00:00:20] engaging. Each concept is introduced in
[00:00:23] a simple and approachable way, perfect
[00:00:26] for beginners. By the end, you'll have a
[00:00:28] complete playable game that you can
[00:00:31] customize and expand further.
[00:00:33] This course was developed by Sarah and
[00:00:35] Reem. They are both students who are
[00:00:38] part of Hack Club. Hack Club is a global
[00:00:41] nonprofit organization that creates a
[00:00:43] community for high school students
[00:00:46] interested in coding and making things
[00:00:48] with technology.
[00:00:50] >> Ever wanted to make your own game, but
[00:00:51] didn't know how?
[00:00:52] >> In this tutorial, you'll learn how to
[00:00:54] make your own game with the Godot game
[00:00:55] engine. I'm Sarah, and I'm a 16-year-old
[00:00:57] Hack Clubber from California.
[00:00:59] >> And I'm Reem, a 17-year-old Hack Clubber
[00:01:00] from New York.
[00:01:01] >> Let's get started.
[00:01:04] For those of you who don't know, Godot
[00:01:05] is a free open-source game engine that
[00:01:07] helps you build 2D and 3D games. So, the
[00:01:10] first step of building with Godot is
[00:01:12] downloading the Godot engine. So, I'll
[00:01:14] head to godotengine.org
[00:01:16] and just download the latest version. I
[00:01:18] already have it installed for time's
[00:01:20] sake. So, after you finish your install,
[00:01:22] you should be able to find a .zip
[00:01:25] folder. So, you want to extract this.
[00:01:33] And this should take you to a new folder
[00:01:35] with your two .exe files. So, run the
[00:01:37] first one, and this will take you to the
[00:01:39] Godot project manager, where you can
[00:01:41] create your first game.
[00:01:47] So, I'm going to create a new game. I'll
[00:01:49] just call it Godot game one.
[00:01:51] Or maybe Godot game demo.
[00:01:56] And this is going to run and take you to
[00:01:59] the Godot engine where you can start
[00:02:01] building your game. And now Beam is
[00:02:03] going to show you how to build tile sets
[00:02:05] in your first game.
[00:02:07] >> Head over to this repository to get the
[00:02:09] art that we'll be using for your game.
[00:02:12] Click on code,
[00:02:13] local, and download as zip to download
[00:02:16] the art files that you'll be using on
[00:02:18] your tile set.
[00:02:28] Once that's downloaded, unzip the file.
[00:02:37] Head back over to your Godot project and
[00:02:39] click on the file manager.
[00:02:41] Right click and click on open in file
[00:02:44] manager.
[00:02:57] And take the file that you just unzipped
[00:02:59] and drag it into either the editor or
[00:03:01] your file manager for your game.
[00:03:11] Great. That file should now appear in
[00:03:13] your editor.
[00:03:15] Let's get started on your game.
[00:03:17] Create a new 2D scene.
[00:03:20] Click the add button to add a child
[00:03:22] node.
[00:03:23] Add tile map layer.
[00:03:33] And then open tile map at the bottom of
[00:03:35] your screen. This is where we'll be
[00:03:37] importing our tile set for your game.
[00:03:40] If you look at the inspector, your tile
[00:03:42] set currently says empty. Let's change
[00:03:45] that.
[00:03:46] On the down button next to empty, click
[00:03:48] on new tile set.
[00:03:51] You should have a new button that up on
[00:03:53] your bottom of your screen saying tile
[00:03:55] set.
[00:03:58] Click on the add button, add an atlas,
[00:04:01] open your Godot folder, and open the art
[00:04:04] folder.
[00:04:07] We'll be using this Aurora tile set PNG
[00:04:10] file for the background of our game.
[00:04:13] Click open, and this atlas texture will
[00:04:16] automatically modified by the Godot
[00:04:19] editor.
[00:04:23] Currently, our tiles are a little too
[00:04:25] small. Let's open up tile set,
[00:04:29] tile size, and change it to 32
[00:04:33] by 32 pixels
[00:04:35] to increase the size of our tiles.
[00:04:40] However, how do we actually get the tile
[00:04:42] set from here onto the background of our
[00:04:45] game?
[00:04:47] This is where the tile set comes in
[00:04:49] handy.
[00:04:51] Let's change the texture region to 32 by
[00:04:54] 32.
[00:04:59] By modifying the tile map layer in the
[00:05:01] inspector, this will allow your player
[00:05:03] to actually interact with the tiles that
[00:05:05] we add.
[00:05:08] To make some tiles solid, we're going to
[00:05:10] assign them physics layers.
[00:05:12] Head over to your tile map layer
[00:05:13] inspector and click on physics layers.
[00:05:16] Add an element,
[00:05:18] add a new physics material,
[00:05:21] and then in the drop-down menu of your
[00:05:22] select page on tile set, you'll see a
[00:05:25] new physics tab pop up.
[00:05:27] Click on it, click on it again,
[00:05:30] and then press F on your keyboard.
[00:05:33] When it's shaded in red, you'll know
[00:05:34] that your tile has officially become a
[00:05:36] solid.
[00:05:38] I could individually go and press F on
[00:05:41] each and every single one of these
[00:05:43] tiles, but that will take a lot of work,
[00:05:46] especially as we move into larger and
[00:05:48] larger tile sets.
[00:05:50] So, to select multiple tiles, I'll hold
[00:05:53] shift
[00:05:55] and drag my mouse over all of the tiles
[00:05:58] that we currently have.
[00:06:01] I'll click on F, and now when I click on
[00:06:04] each and every single one of them,
[00:06:06] they've each become individual solid
[00:06:08] tiles that the player can officially
[00:06:10] interact with.
[00:06:12] >> So, we've created our tiles, and if we
[00:06:14] go to tile map, and then we go to draw,
[00:06:15] we can see that we are able to draw with
[00:06:17] them, and they look great. But, one
[00:06:20] thing that you'll quickly notice is that
[00:06:22] if I just want to create a basic shape,
[00:06:23] I have to keep going back and keep
[00:06:25] selecting the tiles, and this can get
[00:06:27] really tedious really quickly. So, let's
[00:06:30] fix this. So, let's go to our terrain
[00:06:33] sets, add element, and under terrains
[00:06:36] again, add element. And this will create
[00:06:38] a new terrain called terrain zero. Let's
[00:06:40] go back to our tile sets, go to feet,
[00:06:44] and go to terrains.
[00:06:48] So, we're going to select terrain set
[00:06:49] zero, and again, terrain zero.
[00:06:52] And we're just going to be able to draw
[00:06:55] on this. So, if you double click on
[00:06:56] this, you can see that this allows you
[00:06:58] to draw.
[00:06:59] And for each tile, you're going to
[00:07:02] create
[00:07:04] you're going to draw on them, and you're
[00:07:05] going to create a grid-like pattern that
[00:07:07] looks like this. Where it's like two
[00:07:09] It's like a bunch of squares inside of
[00:07:10] each other.
[00:07:14] So, yeah, this is our terrain. And when
[00:07:17] we go to our tile map and go to
[00:07:19] terrains, we'll see the terrain set
[00:07:21] zero, and now we can see that when we
[00:07:23] draw,
[00:07:24] it'll just fill it in for itself. So,
[00:07:26] this makes building our game way easier.
[00:07:28] And when we run it,
[00:07:32] oh, first, let's select our main scene.
[00:07:34] So, first of all, you want to save this
[00:07:37] as your main scene,
[00:07:40] and you want to rename node to the main.
[00:07:44] And when we try to run our game, it'll
[00:07:46] ask us to select a main scene, so we'll
[00:07:48] just select current.
[00:07:51] And yeah, you can see our tiles, but one
[00:07:54] thing you'll notice pretty quickly is we
[00:07:55] don't have a player, so let's get on
[00:07:56] that. So, let's create a new node and
[00:08:00] we'll make a tile map layer.
[00:08:04] Oh, sorry, not a tile map layer. We're
[00:08:05] going to create a character 2D.
[00:08:08] So, let's name this player.
[00:08:12] Let's create a area 2D.
[00:08:14] Under that, we'll create a collision
[00:08:16] shape 2D. Under collision shape,
[00:08:20] we're going to make a rectangle.
[00:08:25] There you go.
[00:08:26] Um let's drag in our icon.svg.
[00:08:30] We can replace this with our art
[00:08:34] So, let's make sure that our icon is a
[00:08:36] child of player and not area 2D.
[00:08:40] Um
[00:08:42] Yeah, so let's attach our script to our
[00:08:44] player.
[00:08:47] So,
[00:08:49] generally this has template code, but it
[00:08:51] looks like it doesn't, so let me go grab
[00:08:52] that.
[00:08:56] Okay, cool. So, this is the template
[00:08:57] code. You should have this in your
[00:08:59] repository.
[00:09:00] Um not sure why it wasn't there. But, if
[00:09:03] we save this as player.tscn
[00:09:06] and we go back to our main in the 2D
[00:09:08] viewer,
[00:09:10] and let's import our player.
[00:09:16] Let's start it wherever you want, maybe
[00:09:17] down here.
[00:09:19] And we run our game.
[00:09:22] Oh, we can see that our player fell
[00:09:24] through. So, let's see why.
[00:09:27] Oh, yeah. So, you can see that our
[00:09:29] player does not have a shape.
[00:09:31] Okay, so we're just going to add a
[00:09:33] collision shape 2D and no area 2D, my
[00:09:35] bad.
[00:09:37] So, when you save this and when I run
[00:09:39] our game again, our player should be
[00:09:40] able to interact with the tile sets.
[00:09:42] And one thing that you can see is that
[00:09:44] my player isn't moving. So, to solve
[00:09:46] this, let's go to our project and
[00:09:49] project settings.
[00:09:50] And we have to make an input map. So,
[00:09:52] this is basically telling the computer
[00:09:54] what we want um
[00:09:57] our input keys to be. So, I would like
[00:09:59] to use WASD. So, under UI left, I'm just
[00:10:02] going to type in A. And it's going to
[00:10:04] listen for that input. I'll add it.
[00:10:07] Under right, I'm going to add D.
[00:10:10] We don't For up, I'm just going to use
[00:10:12] space.
[00:10:14] And we don't need a down. So, let's go
[00:10:16] back to our game.
[00:10:19] And you can see our character moves, and
[00:10:20] that is great.
[00:10:22] But one thing you might notice is the
[00:10:24] camera's in kind of an awkward position.
[00:10:26] So, let's add a new camera node under
[00:10:29] our player.
[00:10:31] And we're going to attach a script.
[00:10:33] And again, this has template code, but
[00:10:35] it's not there.
[00:10:37] And we want this to follow our player.
[00:10:39] So, we're going to declare a variable at
[00:10:41] on ready for our player.
[00:10:44] Just equal to we'll just drag this in,
[00:10:47] our player.
[00:10:49] Um we don't need the ready function.
[00:10:51] So, for our process function, again,
[00:10:54] this just runs every frame. So, we're
[00:10:56] going to say our global position, which
[00:10:58] refers to the global position of our
[00:11:00] camera, is equal to our
[00:11:02] player.global_position.
[00:11:04] So, when you run this,
[00:11:08] you can see that our camera now follows
[00:11:09] our player. That is great. Um one thing
[00:11:11] you might notice is that maybe you want
[00:11:13] to adjust the player um height.
[00:11:16] So, to do that, I'm sorry, not player
[00:11:18] height, the player movement, like how
[00:11:19] fast it moves, how high it jumps.
[00:11:22] So, if I want this to jump If I want
[00:11:24] this to jump higher, I'll just increase
[00:11:25] this number.
[00:11:27] And we run our game.
[00:11:30] Oopsie. Wait, I'm really bad to this.
[00:11:33] Um
[00:11:34] Let's go. Yeah, you can see that our
[00:11:36] player will jump higher. But anyways,
[00:11:38] um
[00:11:40] this is great. This can show you what
[00:11:42] our next issue is. So, we do have a game
[00:11:45] and our player can jump around, but our
[00:11:47] player can also just like fall into the
[00:11:49] abyss and nothing will happen. So,
[00:11:53] we have to create a checkpoint and death
[00:11:55] system so that when the player falls,
[00:11:57] they'll die
[00:11:58] and the game can move on and we can keep
[00:12:01] going.
[00:12:02] So, first things first, let's create a
[00:12:06] Let's create a new node in our main
[00:12:07] scene and we're going to make it node
[00:12:10] 2D.
[00:12:13] And we're just going to name this
[00:12:14] checkpoint
[00:12:16] manager.
[00:12:18] Let's attach a new script to it.
[00:12:21] Player variable last location.
[00:12:24] And then again,
[00:12:27] we're going to declare our variable
[00:12:29] player
[00:12:30] is equal to
[00:12:32] player.
[00:12:37] So, let's add a new function. This is
[00:12:39] the built-in Godot function um
[00:12:42] checking.
[00:12:48] This is the built-in Godot function that
[00:12:50] runs the first time your game loads up.
[00:12:54] So, when this is ready, we're going to
[00:12:56] say our last location is equal to our
[00:12:59] player global position.
[00:13:02] So, yeah, this is our checkpoint
[00:13:03] manager. And now let's create a new
[00:13:06] node. We're going to create a area 2D.
[00:13:10] Um under this, let's add a collision
[00:13:13] shape 2D,
[00:13:15] a marker 2D,
[00:13:17] and let's rename our area 2D checkpoint.
[00:13:23] And let's create a shape for our
[00:13:25] collision shape.
[00:13:28] Let's go to and this a whole rectangle.
[00:13:30] And let's draw our marker 2D over here.
[00:13:34] To the right.
[00:13:35] So, let's attach a new script to our
[00:13:38] checkpoint.
[00:13:39] I'm going to declare our variable
[00:13:41] checkpoint manager.
[00:13:45] And we're going to take our ready
[00:13:47] function.
[00:13:49] And when this runs, we're going to say
[00:13:51] checkpoint manager is equal to get
[00:13:54] parent
[00:13:56] dot get parent
[00:13:58] dot get node
[00:14:02] checkpoint manager.
[00:14:06] Cool.
[00:14:07] And then we're going to say
[00:14:11] So, for our Yeah, for our area 2D, we're
[00:14:14] going to go up to our node. And this is
[00:14:16] a signal, and this is just code that
[00:14:18] will run when an event is triggered. So,
[00:14:21] click on body entered and attach that
[00:14:23] signal to our checkpoint. And we'll see
[00:14:25] a new function appeared called on body
[00:14:27] entered. So, when body is entered, we're
[00:14:31] going to say
[00:14:36] Um first of all, we're going to check if
[00:14:39] the body is equal to our player. So,
[00:14:41] we're going to say body {dot} name is
[00:14:43] equal to player.
[00:14:45] And if that's true If that is true, then
[00:14:47] that means our player passed through our
[00:14:48] checkpoint. So, we're going to say in
[00:14:50] our checkpoint manager
[00:14:52] our checkpoint manager {dot} last
[00:14:54] location
[00:14:55] is equal to our global
[00:14:59] position.
[00:15:03] Let's
[00:15:05] We're going to say our checkpoint
[00:15:07] manager
[00:15:08] {dot} last location
[00:15:11] is equal to our marker 2D
[00:15:14] global position.
[00:15:17] So, this is our checkpoint script, and
[00:15:18] we're just going to save it as
[00:15:19] checkpoint.tscn.
[00:15:21] And now for our death zone, so let's
[00:15:23] create another area 2D.
[00:15:26] And, a collision shape 2D, and that's
[00:15:29] it.
[00:15:30] So, let's go over to our 2D viewer.
[00:15:34] And, just make a rectangle.
[00:15:37] Let's rename this death zone.
[00:15:41] Add a script.
[00:15:44] So,
[00:15:47] uh when our area 2D is entered,
[00:15:51] we want to uh signal.
[00:15:54] So, select this, add a body entered.
[00:15:58] And, that's our function.
[00:16:00] Um we also have to declare our
[00:16:03] variables. So, we're going to say var
[00:16:05] player,
[00:16:06] um var
[00:16:14] and our checkpoint manager. Oopsies.
[00:16:19] So, again, for our ready function, we're
[00:16:22] going to say our player is equal to
[00:16:27] get parent.
[00:16:33] Get
[00:16:34] parent.
[00:16:35] dot
[00:16:36] get node player.
[00:16:39] We're going to say
[00:16:41] checkpoint manager.
[00:16:43] Oopsies.
[00:16:44] Let's get parent.
[00:16:47] dot
[00:16:48] get parent.
[00:16:51] dot get node checkpoint
[00:16:54] manager.
[00:16:55] So, yeah.
[00:16:57] This is us declaring our variables, and
[00:16:59] this is what's actually going to run.
[00:17:01] So, again, we need to check if the body
[00:17:03] that passed through, if its name is
[00:17:04] equal to player.
[00:17:08] And, if so, we want to kill player. So,
[00:17:11] right now I'm just going to pass, but
[00:17:12] let's create a new function called kill
[00:17:14] player.
[00:17:17] And, what we want this to do is we want
[00:17:19] to set our player's global position. So,
[00:17:22] player.global
[00:17:24] position
[00:17:26] is equal to checkpoint manager.last
[00:17:30] location.
[00:17:32] And we're going to call this in our
[00:17:35] on body entered.
[00:17:37] And it should kill our player. So, let's
[00:17:39] test it. So, first of all, you need to
[00:17:41] save your death zone script and then go
[00:17:44] back to your main scene.
[00:17:46] And let's just end point our Oopsies, I
[00:17:49] didn't name it.
[00:17:51] Yeah, so you need to save your scene.
[00:17:55] And then link it in your added
[00:17:58] checkpoints. Oopsies. Checkpoint.
[00:18:02] So, there's your checkpoint.
[00:18:04] So, I'll set and add a scene collection
[00:18:08] and we're just going to
[00:18:10] drag our death zone in here.
[00:18:15] And if you go to tile map
[00:18:17] and
[00:18:18] go to tiles, you should be able to draw
[00:18:22] with your death scene. And it is a
[00:18:24] little weird shape, but we'll fix that
[00:18:26] in a second.
[00:18:27] So, let's just test this.
[00:18:29] And yeah, you can see that when you go
[00:18:31] over here, it'll kill you.
[00:18:33] So, let's fix our shape. You can see
[00:18:35] that's a little bit um not the correct
[00:18:37] size.
[00:18:46] That looks about right. And yeah, when
[00:18:48] we fall over there, it'll kill us. Let's
[00:18:50] go through our checkpoint.
[00:18:52] And we go over there, it'll kill us. So,
[00:18:54] yeah, we have our death zones and
[00:18:56] checkpoints set up.
[00:18:58] And our death zones are also really easy
[00:19:00] to reuse because we can just go to our
[00:19:02] tile map and start drawing with them.
[00:19:04] So, now Mayne is going to show you how
[00:19:06] to make obstacles. A new scene,
[00:19:09] add a static body 2D to as the root
[00:19:11] node.
[00:19:13] A collision shape so that your character
[00:19:15] can interact with the obstacle.
[00:19:20] Define your collision shape. For me, I
[00:19:23] want my collision shape to be the same
[00:19:25] size as my sun, so I'm going to add a
[00:19:27] circular collision shape.
[00:19:30] I'll drag this down here.
[00:19:33] And I'll increase the size like I want.
[00:19:39] To import the sun's texture into the
[00:19:40] scene, I'll add another child node named
[00:19:44] Sprite 2D.
[00:19:47] And then, I'll load in the texture
[00:19:50] as my sun.png.
[00:19:56] Then,
[00:19:57] I'll adjust the size of this collision
[00:19:59] shape
[00:20:01] to fit the size of the sun.
[00:20:07] Rename this to say obstacle.
[00:20:12] And click hit control S or command S to
[00:20:15] save this as an obstacle scene.
[00:20:19] Import my obstacle to the main scene as
[00:20:22] a child node.
[00:20:27] And I'll drag it where I want the player
[00:20:30] to have an obstacle against.
[00:20:33] Now, when I play the scene,
[00:20:38] my character cannot go past the
[00:20:40] obstacle.
[00:20:43] >> An immediate thing about our game is
[00:20:45] that it's kind of ugly. So, let's make
[00:20:47] it pretty.
[00:20:48] So, let's start off by adding a
[00:20:50] background. So, let's create a new node,
[00:20:52] and we're going to make a parallax.
[00:20:55] Let's call it sketch.
[00:20:57] Parallax.
[00:20:58] Parallax background.
[00:21:00] My bad.
[00:21:01] Um and we're going to add
[00:21:04] parallax
[00:21:06] uh
[00:21:07] 2D.
[00:21:11] Now, we're going to add a pair of waxing
[00:21:13] there.
[00:21:14] Okay, cool.
[00:21:15] So, in our new 2D, let's go to our
[00:21:19] motion.
[00:21:20] Uh, we're just going to set it to 1,600
[00:21:23] by 900 because that's the size of the
[00:21:26] art I made.
[00:21:27] So, we're going to go to our art and
[00:21:29] we're going to drag in
[00:21:33] background. There you go. Here's my
[00:21:35] background. So, let's drag it into our
[00:21:36] scene. And as you can see, he's a little
[00:21:39] big. So, let's just align him.
[00:21:42] I guess align her.
[00:21:44] Um, at the top and align it with that
[00:21:46] purple rectangle you see
[00:21:48] cuz that's how our screen's going to
[00:21:50] loop.
[00:21:51] So, this is our background
[00:21:54] and we have to make it child of
[00:21:55] parallax.
[00:21:57] Here, make it child of parallax there.
[00:22:00] And you can see that it's looping and it
[00:22:02] was actually the cut I did earlier. So,
[00:22:04] let me save
[00:22:05] like that.
[00:22:07] So, let's save this as background.
[00:22:09] And let's go to our main scene and
[00:22:11] import it.
[00:22:14] And you can move it around wherever you
[00:22:15] want. I would
[00:22:17] prefer it to be a little higher up. So.
[00:22:21] Um,
[00:22:22] oopsie. I guess you can't do that.
[00:22:25] Um, I'm just going to lift this whole
[00:22:26] thing up.
[00:22:31] So, when you run our game, you can see
[00:22:33] we have a background and it's moving.
[00:22:36] And oopsie, I just cut myself. Um.
[00:22:41] Okay, so let's expand our tile map
[00:22:42] layer. So, first of all, we want to draw
[00:22:45] more with it.
[00:22:46] Uh, because right now our tile set is
[00:22:48] very limited. So, let's just like draw
[00:22:50] over here.
[00:22:53] It's like
[00:22:54] all the way I guess.
[00:22:56] And let's include more of our tiles so
[00:22:58] that we have, you know, more gameplay.
[00:23:01] So, let's go going
[00:23:02] Let's add some over here.
[00:23:03] You can put them wherever you want. This
[00:23:05] is just like, you know, a sample.
[00:23:10] There you go. All right. So, let's run
[00:23:11] our game again.
[00:23:13] And you can jump and you can see our
[00:23:16] background.
[00:23:17] And you can see that it's continuing.
[00:23:20] Um
[00:23:21] So, yeah. Now, we have a looping
[00:23:22] background.
[00:23:23] You might want to move it up a little
[00:23:26] more just like
[00:23:28] so
[00:23:30] it fits the frame of your game.
[00:23:32] Kind of like this. I think this is
[00:23:33] great.
[00:23:34] Uh
[00:23:35] but, yeah. That's our background. Next
[00:23:38] thing So, next thing to do is let's add
[00:23:40] player animations. So, let's add under
[00:23:44] our player node a animation player.
[00:23:49] And a animat- animated sprite.
[00:23:53] So, under animation, we're going to add
[00:23:55] a new sprite frame.
[00:23:58] And we go to our animation bar.
[00:24:01] Under
[00:24:04] Yeah, under sprite frames,
[00:24:06] we have this new menu.
[00:24:08] So, over here, let's new sprite sheet.
[00:24:13] And we're going to be using this art
[00:24:15] folder I made.
[00:24:16] And let's just add in the idle animation
[00:24:18] first.
[00:24:20] So, you can see that's split up kind of
[00:24:21] weird, so
[00:24:23] these um
[00:24:25] sprites are 32 by 32.
[00:24:28] So, let's set them like that.
[00:24:30] And then select them and we're going to
[00:24:32] add two frames.
[00:24:34] And this is our default, so let's save
[00:24:36] this.
[00:24:37] And let's also get rid of this Godot
[00:24:40] icon cuz it's not very cute.
[00:24:42] Uh one thing you might notice is that
[00:24:44] the art is a little blurry, so
[00:24:47] under texture, you want to make it
[00:24:49] nearest and that'll make it clear again.
[00:24:51] Where is that?
[00:24:53] Auto play on load.
[00:24:55] So, let's run our game.
[00:24:58] And you can see he's bouncing. He's very
[00:24:59] cute, but he's not like moving or
[00:25:01] anything. So, let's fix that.
[00:25:04] So, under sprite frames, let's add in
[00:25:08] our run.png.
[00:25:09] So, again, you want to im-
[00:25:12] port the art from sprite sheet.
[00:25:15] Um
[00:25:16] the
[00:25:18] tile size is correct now, so we can just
[00:25:19] add it like this.
[00:25:21] And actually, we have to create a new
[00:25:22] animation. Let's call it run.
[00:25:26] Again, slice it.
[00:25:30] And these are our two animations, but
[00:25:32] they will not run without adding a code,
[00:25:35] so let's go there.
[00:25:37] So, over here in our process,
[00:25:41] let's
[00:25:44] All right.
[00:25:45] So, if there's direction,
[00:25:48] which would be if you have an input, we
[00:25:51] want to play our animation. So, first
[00:25:54] thing, we have to declare our animation
[00:25:56] player, so we'll say var
[00:25:58] animation player
[00:26:00] is equal to
[00:26:01] this guy.
[00:26:03] This guy.
[00:26:05] And then I'll say animation player
[00:26:08] .play
[00:26:10] run.
[00:26:12] So, let's see.
[00:26:15] Oh, oopsies. You also have to
[00:26:19] I think it should be good.
[00:26:21] Um
[00:26:23] Hm, maybe I should say var
[00:26:25] animated sprite
[00:26:28] Oopsies.
[00:26:29] It was equal to animated sprite 2D.
[00:26:32] And if there's direction, which
[00:26:34] basically means if there's an X or Y
[00:26:36] input,
[00:26:37] um we're going to
[00:26:40] play our animation. So, animated
[00:26:41] sprite.play
[00:26:44] run.
[00:26:47] So, let's run this.
[00:26:51] And you can see when we're running,
[00:26:52] running.
[00:26:53] Uh but we can also see he keeps running.
[00:26:56] So, if there's else, we're going to say
[00:26:59] run or idle or default.
[00:27:03] So, let's try that.
[00:27:06] And yeah, you can see when he's not
[00:27:07] running, he's not, you know, running.
[00:27:09] And when he's running, he's running. So,
[00:27:11] that's great. But what happens when you
[00:27:12] go left? He's still facing forward. So,
[00:27:15] let's change it. So, I'm just going to
[00:27:16] add another one more line and it's
[00:27:18] right.
[00:27:19] Uh okay.
[00:27:22] I mean
[00:27:23] So, let's just add another one more line
[00:27:25] and we'll see how that makes right.
[00:27:26] Uh flip.
[00:27:28] Um
[00:27:29] flip. Horizontal flip.
[00:27:31] If
[00:27:32] direction
[00:27:34] Let's check that. So, animated sprite
[00:27:36] dot flip horizontal is equal to
[00:27:39] direction is less than
[00:27:42] There we go.
[00:27:43] So, let's run this.
[00:27:46] And great. You can see that they're
[00:27:49] changing their direction based off of
[00:27:51] where you're running and
[00:27:53] um
[00:27:54] if you're actually running. So, that's
[00:27:55] super cute, super cool. And more stuff.
[00:27:58] So, right now our game is pretty cute.
[00:28:02] And
[00:28:04] you can jump around, but there's nothing
[00:28:06] that really makes it a game. There's no
[00:28:08] enemies and there's no like
[00:28:11] real movement. So, next thing is we want
[00:28:14] to add moving platforms and enemies.
[00:28:17] So, let's just start off with moving
[00:28:19] platforms. So, let's create a new node
[00:28:22] and we'll make it a
[00:28:23] path
[00:28:24] 2D.
[00:28:27] Under it, we're going to create a path
[00:28:29] follow 2D.
[00:28:38] Under that, we're going to add a remote
[00:28:41] transform 2D.
[00:28:44] I think it's going to add a animated
[00:28:45] ball.
[00:28:46] Animated
[00:28:47] ball.
[00:28:51] Animated ball body 2D.
[00:28:55] And add in our animated ball body 2D.
[00:28:57] And then that's our path collision shape
[00:28:58] 2D.
[00:29:00] And then over here, we're going to add
[00:29:02] in our art. It's just called platformer.
[00:29:06] Very original. Add a animation player.
[00:29:11] So, first thing let's add a shape.
[00:29:15] So,
[00:29:16] just make it fit your
[00:29:19] platformer.
[00:29:21] Again, you want to
[00:29:24] change the texture. So, that's
[00:29:26] clear love in the way.
[00:29:29] Um under our remote transform 2D, we're
[00:29:32] going to assign it animated ball body
[00:29:34] 2D.
[00:29:36] Um yeah, so under our path 2D, let's
[00:29:40] create
[00:29:44] Let's add element under points.
[00:29:47] And another
[00:29:48] element.
[00:29:49] And
[00:29:50] we're just going to move that Oopsies.
[00:29:53] Just going to move that around.
[00:29:55] And this is just changing where our This
[00:29:58] is just creating our path.
[00:30:01] Um it's a little janky.
[00:30:03] But yeah, so this is just going to move
[00:30:05] it that way.
[00:30:07] Uh let me add our platformer back.
[00:30:09] One thing that I like to do is under
[00:30:12] resource, I like to say local to scene.
[00:30:14] Because if you don't do that, then it's
[00:30:16] going to change all of the paths when
[00:30:19] you add up one path. Uh and while you're
[00:30:21] building your game, that can get really
[00:30:23] annoying.
[00:30:24] But yeah, that's our path follow 2D. Uh
[00:30:26] under our animation player,
[00:30:29] well, under our animation player, we're
[00:30:31] going to create an animation.
[00:30:33] And um
[00:30:35] I'll just name it like movement, I
[00:30:37] guess.
[00:30:39] So, let's add a
[00:30:43] Mhm.
[00:30:45] Now let's add a track go to your
[00:30:48] path follow 2D and under progress ratio
[00:30:52] let's make a keyframe.
[00:30:55] So this is just tracking the progress of
[00:30:58] our
[00:30:59] platformer along this path.
[00:31:02] And we have a keyframe right now at this
[00:31:03] current position.
[00:31:05] If you go to our path follow 2D
[00:31:07] now let's just move our progress ratio
[00:31:10] over to one.
[00:31:11] And we're going to add a new
[00:31:19] and move our time over here.
[00:31:22] Uh change our progress ratio and add a
[00:31:24] keyframe.
[00:31:25] So when you run this you can see our
[00:31:28] platform moving which is super cool.
[00:31:31] But it's um just staying there. So over
[00:31:35] here let's add a bounce back. Just click
[00:31:39] clicking.
[00:31:40] And this should
[00:31:42] bounce between it. So let's run our
[00:31:43] animation again.
[00:31:45] And yeah does that super cool.
[00:31:49] Um
[00:31:50] so let's save this as moving platform.
[00:31:56] And
[00:31:57] um
[00:32:00] Yeah so in our main node let's link a
[00:32:04] moving platform.
[00:32:06] Where is it?
[00:32:07] Oh oopsie it's over here.
[00:32:09] Oh my bad. Um for the export let's name
[00:32:12] this moving
[00:32:14] platform.
[00:32:16] Save.
[00:32:17] Link it.
[00:32:21] There you go.
[00:32:22] So it's over here and when you run our
[00:32:25] game we should be able to see it move.
[00:32:30] Oh we're not.
[00:32:31] Oh you can see our collision body works
[00:32:33] but you can also see it's not
[00:32:35] automatically running.
[00:32:36] So my S-path
[00:32:39] Okay, so under the moving platform,
[00:32:41] let's add a script.
[00:32:43] There you go.
[00:32:44] Uh function ready.
[00:32:48] Let's put a big bump.
[00:32:49] Um
[00:32:51] Yeah.
[00:32:53] So, first we have to save our
[00:32:56] uh
[00:32:57] on ready for animation.
[00:33:01] This is equal to
[00:33:03] animation player.
[00:33:05] And when the game loads up, then you can
[00:33:07] do the animation.play
[00:33:11] movement.
[00:33:12] So, let's save this. Let's go to our
[00:33:13] main node.
[00:33:16] Um I already imported it, but yeah, just
[00:33:18] do that.
[00:33:22] And yeah, now when you're in your main
[00:33:23] node, you can see the moving platform,
[00:33:25] which is pretty cool.
[00:33:27] So, the next thing is enemies, so that
[00:33:29] our player can actually interact with
[00:33:30] things, so just like jumping around.
[00:33:32] Okay, um my laptop may have just died,
[00:33:35] but anyways, let's create an enemy. So,
[00:33:38] um going over here, let's create our
[00:33:41] enemy Let's create a character body 2D.
[00:33:45] Let's create a collision shape.
[00:33:48] Create a area 2D.
[00:33:50] A collision shape.
[00:33:52] And in our 2D viewer, we're going to
[00:33:55] drag in our enemy.png.
[00:33:59] Again, we're going to make him not
[00:34:01] blurry cuz
[00:34:03] blurry is not good.
[00:34:06] Um
[00:34:08] Oh yeah, we're also going to link our
[00:34:10] death zone.
[00:34:13] So,
[00:34:14] yeah, just align that with your
[00:34:16] character.
[00:34:22] All right, there you go.
[00:34:25] For our collision shape, you want to
[00:34:27] make sure that it's a little smaller
[00:34:29] than
[00:34:31] uh the death zone, otherwise our player
[00:34:33] won't be able to interact with it.
[00:34:35] So, let's make that.
[00:34:40] Uh for our collision shape 2D, we're
[00:34:41] going to add a circle this time. And
[00:34:44] what this is is this is just like the
[00:34:46] enemy's vision zone, which is pretty
[00:34:47] cool. And basically, what we want this
[00:34:50] to do is
[00:34:52] if the player enters that vision zone,
[00:34:54] that our enemy follow them. So, let's
[00:34:56] name this as enemy.tscn.
[00:34:59] And really quickly, we're just going to
[00:35:00] import it.
[00:35:02] So, you can test the
[00:35:04] deathiness of our enemy.
[00:35:07] So, what I'm looking for right now is
[00:35:08] that when we go to our player,
[00:35:11] they'll die. And you see, they're dying.
[00:35:13] That's like great. Anyways,
[00:35:15] uh let's add in some movement for our
[00:35:17] enemy.
[00:35:18] So, first of all, let's name this enemy.
[00:35:22] And let's attach a new script.
[00:35:25] So, the key functions we need are
[00:35:27] function physics process, which is the
[00:35:30] built-in Godot process. Make it
[00:35:33] Put a pass in there cuz I don't need it
[00:35:34] right now.
[00:35:35] And for our area 2D, we're going to go
[00:35:38] to our node and we're going to add a
[00:35:40] body enter signal and a body exited
[00:35:43] signal.
[00:35:44] So,
[00:35:45] again, these just run whenever anything
[00:35:48] enters our area 2D.
[00:35:50] And we don't really want anything to
[00:35:53] make our enemy start chasing after the
[00:35:54] player. So, we have to check if the body
[00:35:57] is if the body.name equals to player.
[00:36:02] So, let's
[00:36:03] add a pass
[00:36:05] here.
[00:36:08] Um next thing is we need to add our
[00:36:11] speed variable, so I'll just say var
[00:36:13] speed is equal to like 200.
[00:36:17] Uh again,
[00:36:18] we have to declare our player, so I
[00:36:20] already var player is equal to
[00:36:23] our main player.
[00:36:25] There we go.
[00:36:27] So, if
[00:36:30] And last variable we have to add is a
[00:36:32] var follow. So, this is just going to be
[00:36:35] a boolean.
[00:36:36] And whenever the player enters, that
[00:36:38] boolean will be true. And whenever the
[00:36:40] player leaves, that boolean will be
[00:36:41] false.
[00:36:42] And depending on the volume that
[00:36:44] boolean,
[00:36:46] we're going to be, you know, chasing the
[00:36:47] player.
[00:36:48] So, if the player enters the scene, we
[00:36:51] say uh follow is equal to true.
[00:36:56] And if it's not, we say follow is false.
[00:37:00] And in a physics process, uh first thing
[00:37:03] you have to do is uh you have to add a
[00:37:05] move and slide function. This is just
[00:37:07] how Godot
[00:37:08] actually
[00:37:10] like runs the physics. So, just make
[00:37:12] sure you have that.
[00:37:13] Um
[00:37:15] var follow if follow
[00:37:20] So, basically,
[00:37:21] if our player is in the left of our
[00:37:23] enemy, we want our enemy to go left. If
[00:37:25] our player's to the right
[00:37:27] of our enemy, we want our enemy to go
[00:37:29] right. So, the way we do this is by
[00:37:31] looking at the X coordinates. So, if the
[00:37:34] player's X coordinates are more negative
[00:37:37] or less than our enemy coordinates, then
[00:37:39] our enemy will go left.
[00:37:41] And if our player coordinates player's X
[00:37:44] coordinates are more to the right, then
[00:37:46] our enemy will go right. So, let's
[00:37:48] implement that. So, if follow,
[00:37:51] um we add another if statement.
[00:37:53] If player.global_position.x
[00:37:56] is less than
[00:37:57] global_position.x,
[00:38:00] that means our player is in the left.
[00:38:02] So, we're going to say velocity.x is
[00:38:06] going to be negative speed.
[00:38:08] And else
[00:38:10] else if
[00:38:12] player.global_position.x
[00:38:14] is greater than global_position.x,
[00:38:17] then we say our velocity.x
[00:38:19] Oopsies.
[00:38:20] velocity.x
[00:38:22] is equal to speed. And I spelled
[00:38:25] velocity wrong cuz I'm silly.
[00:38:28] So, yeah, let's
[00:38:32] try that.
[00:38:35] Okay, cool. So, you can see our enemy's
[00:38:37] following our player.
[00:38:39] Cool.
[00:38:39] But one thing you can see is that our
[00:38:41] enemy is floating. So, what I want to do
[00:38:44] is add another if statement uh
[00:38:47] if not is
[00:38:49] on
[00:38:50] floor.
[00:38:52] Velocity less equal gravity
[00:38:56] gravity.
[00:38:58] And up up.
[00:39:00] I think that should work. Let's try
[00:39:01] this.
[00:39:02] Oh.
[00:39:04] Get gravity.
[00:39:07] Okay, let's try that.
[00:39:12] Okay, cool. Do you see our our player
[00:39:13] getting like hunted down by by our
[00:39:15] enemies? Actually,
[00:39:17] kind of annoying. But yeah, that's what
[00:39:19] enemies are for. Um you can lower the
[00:39:21] speed if you want, like if you're bad at
[00:39:23] video games like me.
[00:39:26] And they'll chase you slower and you can
[00:39:27] actually run away.
[00:39:29] So, yeah, now we have an enemy.
[00:39:31] So, um I want to create a scoring
[00:39:34] system. So, the way we're going to do
[00:39:35] that is we're going to create a new node
[00:39:38] and then create a canvas layer.
[00:39:40] Under that, we're going to add two
[00:39:42] labels.
[00:39:46] So, the first one is going to be score.
[00:39:50] The second one is going to be time.
[00:39:53] And in our text, we're going to say
[00:39:55] time.
[00:39:56] Uh leave it blank.
[00:39:59] Same thing for score.
[00:40:01] And let's name our canvas layer HUD.
[00:40:07] And then for our score, um
[00:40:09] for our labels, we can actually select
[00:40:10] where they sit on the screen. So, for
[00:40:12] our score, I want to say to the right.
[00:40:14] And for our time, I want it to be to be
[00:40:18] to the top.
[00:40:19] So, let's add a new script here.
[00:40:23] And I already have old code in here, but
[00:40:26] we're going to rewrite it, so don't
[00:40:27] worry.
[00:40:27] So, um
[00:40:29] for the variables we have, so we have
[00:40:30] our time is equal to zero, our score
[00:40:34] is equal to zero.
[00:40:35] Our um
[00:40:39] at on ready var time
[00:40:41] label is equal to
[00:40:45] Let me see something here. Time.
[00:40:47] at on ready var score label
[00:40:52] is equal to
[00:40:55] score.
[00:40:58] And
[00:41:00] so, for our process
[00:41:04] we basically want to be updating our
[00:41:06] time and label all the time. So, I'm
[00:41:08] going to put a pass here.
[00:41:09] And I'm going to create two new
[00:41:11] functions called show time
[00:41:13] or let's update time.
[00:41:16] pass
[00:41:18] at func update score
[00:41:21] pass.
[00:41:22] So,
[00:41:24] for our score,
[00:41:26] um we'll just say score label
[00:41:30] .text is equal to score colon comma plus
[00:41:36] uh string score. So, this is just taking
[00:41:40] our score variable and turning it to a
[00:41:42] string and
[00:41:43] um making this entire string and sending
[00:41:46] it to our text.
[00:41:48] And for our update time, we're going to
[00:41:50] have essentially the same thing.
[00:41:53] Uh except for you know, the time.
[00:42:02] Uh one thing I want to do is we have to
[00:42:04] actually update the time, so we say time
[00:42:06] is equal to
[00:42:07] time.get_ticks
[00:42:10] What's it?
[00:42:13] time.get
[00:42:15] fixed in the second by then thousand.
[00:42:19] Um
[00:42:21] Oh,
[00:42:22] oopsie. I have to like save this.
[00:42:24] Uh 2D
[00:42:27] Um yeah, we have to make it into our 18.
[00:42:32] And when we run this, we see that it's
[00:42:35] blank. Oh yeah, that's because I'm not
[00:42:37] actually updating it in the main
[00:42:38] functions. So, I did my update time
[00:42:41] and then update score. And that's my
[00:42:44] data again.
[00:42:46] And yeah, you can see our time going up
[00:42:49] and you can see our score increasing.
[00:42:51] The thing is, our score isn't actually
[00:42:53] updating. So, one way we can increase
[00:42:56] our player score is adding collectibles.
[00:42:59] So, let's create a
[00:43:02] um
[00:43:03] node.
[00:43:04] We're going to make this a static body
[00:43:07] 2D
[00:43:08] and a collision shape.
[00:43:11] Um oh wait, actually we're going to make
[00:43:13] it an area 2D.
[00:43:15] A collision shape.
[00:43:19] And in our node editor,
[00:43:21] um I'm just going to use this moon.png.
[00:43:25] Uh
[00:43:26] set the texture to
[00:43:28] nearest.
[00:43:30] For our collision shape,
[00:43:33] um add a rectangle.
[00:43:39] And get the moon in there.
[00:43:42] Let's name this collectible.
[00:43:46] And add a script to it.
[00:43:50] So, in our collectible, we need to add a
[00:43:54] uh body entered signal. So, we'll add
[00:43:56] that over here.
[00:43:58] And again, um
[00:44:01] we want to check if the body dot name
[00:44:06] is equal to player.
[00:44:09] And if so,
[00:44:10] then you want to one, increase the
[00:44:13] score, and two,
[00:44:15] um
[00:44:16] get rid of the object. So, let's say for
[00:44:21] player,
[00:44:22] um func on ready.
[00:44:27] Oh, I think it's called ready. All
[00:44:28] right.
[00:44:31] Um function ready.
[00:44:33] Um
[00:44:35] player is equal to get
[00:44:48] Uh
[00:44:48] let me try that.
[00:44:50] So, if body.name is equal to player,
[00:44:53] then
[00:44:54] Oh, we actually don't need player. So,
[00:44:55] let's say var HUD.
[00:44:58] Uh let's go ahead and
[00:45:00] D.
[00:45:01] So, if body.name is equal to player,
[00:45:03] then we increase our score. So,
[00:45:05] HUD.score
[00:45:07] plus equal like
[00:45:10] 50.
[00:45:10] There we go.
[00:45:12] So,
[00:45:13] plus other thing is to get rid of our
[00:45:18] art. So, we can do this by doing queue
[00:45:19] free.
[00:45:21] And let's save
[00:45:23] Let's save this as collectible.
[00:45:26] Import it to our main scene.
[00:45:33] I'm just going to put them over here.
[00:45:40] There we go.
[00:45:43] And yeah, you can see our collectible
[00:45:45] disappears and our score increases. So,
[00:45:48] that is very cool. Oh, last thing that I
[00:45:51] want to do to really take this to the
[00:45:53] next level is add in levels. Only one
[00:45:56] level.
[00:45:56] Um you can see that it's kind of just
[00:45:59] one scene,
[00:46:01] but adding levels can let you you know,
[00:46:04] have my levels and make it buildable
[00:46:06] games and this is really cool.
[00:46:07] And this will require a little bit of
[00:46:09] restructuring. It's not that bad, so
[00:46:11] don't worry.
[00:46:13] Um first thing I would like to do is
[00:46:16] in our folder, let's create a
[00:46:20] a new folder and name it levels.
[00:46:24] So in our levels, we're going to create
[00:46:26] two new scenes. We're just going to
[00:46:28] create level
[00:46:30] number one.
[00:46:33] Um
[00:46:35] level one
[00:46:37] and level two.
[00:46:39] Um generally when you have your games
[00:46:41] that go to the next level, you have some
[00:46:43] sort of icon that leads you there.
[00:46:45] So it could be like a door or like the
[00:46:47] flagpole in Mario.
[00:46:49] Um I don't think I need any more art.
[00:46:52] So it would be a very cool challenge for
[00:46:55] you guys to make your own art and um
[00:46:58] design your own door, but right now I'm
[00:47:00] just going to be using the sun PNG.
[00:47:03] So let's create a new scene. Create a
[00:47:06] new area 2D.
[00:47:08] Create a collision shape 2D.
[00:47:11] Uh in that we're going to drag in our
[00:47:13] sun.
[00:47:15] Again, change the texture
[00:47:18] to nearest.
[00:47:22] Collision shape 2D
[00:47:24] and then a rectangle.
[00:47:29] And we just want to match that to our
[00:47:31] shape.
[00:47:33] So let's name this next level.
[00:47:38] And we'll add in a script.
[00:47:42] And all we have to do here is we have to
[00:47:45] add a
[00:47:46] um body entered signal.
[00:47:51] And if body.name is equal to player
[00:47:58] then we're going to say that
[00:48:00] um
[00:48:01] I'm going to create a new variable for
[00:48:03] our current scene
[00:48:05] file this equal to get
[00:48:11] get_tree
[00:48:13] .get_
[00:48:15] current
[00:48:19] get_current_scene.scene_file_path.
[00:48:25] Um so this is going to return our file
[00:48:28] path. So if you want, you can see I
[00:48:30] print this
[00:48:32] and save it
[00:48:35] and import it into main
[00:48:39] uh next level.
[00:48:49] Okay.
[00:48:52] Yeah, that's going to print our current
[00:48:54] scene.
[00:48:56] So let's rename our main
[00:49:00] level one.
[00:49:03] And let's drag it
[00:49:06] into levels.
[00:49:08] So let's run that again.
[00:49:11] And um one thing is now that that is not
[00:49:15] our main scene, we have to run um our
[00:49:17] current scene.
[00:49:19] So
[00:49:21] uh we have to create a new level one
[00:49:23] and
[00:49:25] um
[00:49:27] let's open it.
[00:49:29] Uh it's over here.
[00:49:32] Let's open that.
[00:49:35] And we're just going to have to import
[00:49:36] our um
[00:49:38] stuff again. It's not a big deal. Um so
[00:49:40] import player, import
[00:49:44] um there. One thing that we do want to
[00:49:46] do is we want to move our tilesets into
[00:49:49] a new scene. So we're going to name uh
[00:49:51] tile map layer.
[00:49:54] And we're basically just going to do
[00:49:55] what we did in the new scene. It's not a
[00:49:57] big deal.
[00:49:58] So, uh if you remember, what we're going
[00:50:01] to do is create a new new tile set.
[00:50:04] And going to our tile set, we're going
[00:50:06] to add in a uh new atlas. Use a raw tile
[00:50:10] set.
[00:50:11] Um automatically create textures.
[00:50:14] Change the tile sizing
[00:50:18] in both this menu
[00:50:21] and um
[00:50:23] this menu.
[00:50:27] Let's create physics layers.
[00:50:32] Let's create a terrain set.
[00:50:35] And um
[00:50:37] let's select all of them.
[00:50:39] Add a physics layer.
[00:50:41] Uh go to paint. Add a terrain.
[00:50:47] Um
[00:50:52] Draw in your terrain.
[00:51:12] Um
[00:51:14] let's import our scenes out of scenes
[00:51:17] collection. Um we're going to import our
[00:51:19] test scene.
[00:51:21] Where is that?
[00:51:22] Test scene.
[00:51:24] And yeah, we can draw with it again.
[00:51:26] It's not a big deal. So, I'm just going
[00:51:28] to save this as
[00:51:30] tile map.
[00:51:37] And going back to our level one, we're
[00:51:41] going to import our tile map.
[00:51:44] Uh do a little drawing, I guess.
[00:51:50] Um
[00:51:52] I'm just going to save that.
[00:51:55] So,
[00:51:57] we also have to import a next level.
[00:52:02] So, I'm going to drag that over here.
[00:52:04] Uh
[00:52:05] move it around.
[00:52:07] Let's also import our HUD.
[00:52:10] And yeah, that's basically all we need
[00:52:12] for each level. So, you can just copy
[00:52:14] this over into level two. So, make your
[00:52:17] player,
[00:52:19] make your two key,
[00:52:22] uh
[00:52:22] make a tile map.
[00:52:25] And just draw like a little so your
[00:52:28] player won't like fall immediately into
[00:52:30] the void.
[00:52:31] So,
[00:52:32] um you save this and then going back to
[00:52:35] our next level, let's go to our script.
[00:52:39] So, if we run our level one,
[00:52:44] um you see this and let me go over here,
[00:52:47] it'll print our current file path. So,
[00:52:50] that's great. Um but we have to be able
[00:52:53] to increase the um digit over here to
[00:52:55] get to the next scene. So, what I'm
[00:52:57] going to do is I'm going to say var
[00:52:59] number
[00:53:01] is equal um current scene file to int
[00:53:05] plus one.
[00:53:06] And we can print that just you know
[00:53:08] pretty bugging purposes.
[00:53:11] Uh current scene scene file path, so try
[00:53:14] that again.
[00:53:18] Okay, so we can see that our number's at
[00:53:20] two. So, then I'm going to say var um
[00:53:24] next scene
[00:53:25] is equal to
[00:53:29] um
[00:53:31] I can't find it. I don't know where it
[00:53:32] is. Let me print it. So,
[00:53:34] uh print
[00:53:35] current scene file.
[00:53:42] All right.
[00:53:43] So, we want our next
[00:53:46] file to be at
[00:53:52] here.
[00:53:56] last number
[00:53:59] plus dot tscn
[00:54:02] And then, we want to change to it, so
[00:54:04] get tree
[00:54:08] dot get
[00:54:10] next.
[00:54:11] Um
[00:54:12] change into file next.
[00:54:16] scene
[00:54:18] Oh, yeah. So, you have to uh make this
[00:54:20] string, so you say
[00:54:24] to
[00:54:25] string.
[00:54:27] You have to wrap it in parentheses.
[00:54:30] And then, we're going to apply the
[00:54:30] string function.
[00:54:34] And we hop over there. We go to two.
[00:54:38] We're going to go to our next level.
[00:54:40] So, yeah, you just created your own game
[00:54:42] in Godot, and it has really cool art,
[00:54:45] really cool characters, and level
[00:54:48] switching, which is really awesome.
[00:54:50] But, yeah, everything in here is pretty
[00:54:52] modular, but this is
[00:54:54] a really cool base to scale things off
[00:54:56] of.
[00:54:57] And
[00:54:59] right now, I'm going to show you how to
[00:55:00] deploy a game, so everyone can see it.
[00:55:03] Okay. So, if we want to export a game
[00:55:06] onto itch.io, which is basically a free
[00:55:09] game platform.
[00:55:11] Um
[00:55:12] there's probably these steps, I guess.
[00:55:14] So, go to editor, go to manage export
[00:55:17] templates.
[00:55:19] And uh let me look.
[00:55:22] Oh.
[00:55:24] I think my Wi-Fi is really bad.
[00:55:26] Uh let's download and install.
[00:55:28] And this will take a hot minute.
[00:55:32] All right.
[00:55:33] So, export this. Export my your project
[00:55:37] and index.html.
[00:55:42] Um
[00:55:43] highlight all of these, send them to a
[00:55:46] zip.
[00:55:48] Does not matter what your zip is called.
[00:55:51] Uh
[00:55:52] go to your itch.io page.
[00:55:56] Oopsie.
[00:55:57] Uh click on this arrow, upload a new
[00:55:59] project.
[00:56:00] Good dough. Let's name it Name it
[00:56:02] whatever you want.
[00:56:03] Um make sure that the kind of project is
[00:56:05] HTML.
[00:56:07] And then upload your zip file.
[00:56:10] So, the zip file.
[00:56:12] Um this going to take a minute, but it's
[00:56:13] no big deal. One thing to know is that
[00:56:15] if you want your project to be public
[00:56:17] after um you first post it, you have to
[00:56:19] go back and edit it and make it public.
[00:56:21] Uh right now it's private. Uh there's
[00:56:24] nothing wrong with your computer, that's
[00:56:25] just how it works.
[00:56:27] Uh this takes a second to
[00:56:30] upload cuz your game gets pretty big.
[00:56:35] Uh it's got this file will be played in
[00:56:37] browser.
[00:56:38] And save that view paint.
[00:56:45] And
[00:56:46] run game.
[00:56:47] And your good dough and check my game
[00:56:49] up.
[00:56:55] And yeah, now your game is
[00:56:58] um
[00:56:59] on the internet and other people can
[00:57:00] play.
[00:57:01] And
[00:57:02] core functionalities are still there.
[00:57:04] Um so, yeah, that's where I'll be ending
[00:57:07] this tutorial.
[00:57:08] Um
[00:57:09] in part one and part two, you created
[00:57:11] your own tile sets, your own character,
[00:57:16] backgrounds, and obstacles.
[00:57:19] In part two, we added a lot of art to
[00:57:21] make our game prettier. So, we added our
[00:57:24] own backgrounds, we added character
[00:57:26] animations. Um we added this really cool
[00:57:29] um
[00:57:30] display of your points.
[00:57:32] And a bunch of extra functionalities
[00:57:34] like enemies,
[00:57:37] levels. So, yeah.
[00:57:39] You now have a pretty good base to build
[00:57:42] your own game
[00:57:43] and I'd love to see what you guys built.
[00:57:46] So, let me know in the comments DM me on
[00:57:50] AppClipSlack if you need any help
[00:57:53] or just comment and I'll try to respond.
[00:57:55] So, yeah, cool. Bye.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
