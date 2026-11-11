# Transcripción: Godot GameDev Tutorial – 3D RPG Game

- Fuente: https://www.youtube.com/watch?v=ouqgx1qKSdY
- Canal: freeCodeCamp.org
- Expositor: Omar (@CodingQuests); invitado: Lelu (@Le_x_Lu) en la sección de VFX
- Publicado: 2024-06-20
- Duración: 5:30:06 (19.806 s)
- Idioma: inglés
- Subtítulos automáticos de YouTube (`en-orig`), 7.239 cues deduplicados, ~52.900 palabras
- Cobertura: el último cue cae en 5:30:04, a 2 s del final del reproductor
- Curso original: https://www.codingquests.com/challenge-page/3drpgcourse
- Archivos del proyecto: [starter](https://codingquests.com/3dstarterfiles) · [final](https://codingquests.com/3drpgfiles)

## Glosario de errores del ASR (no se editan los cues)

| ASR escribe | Es | Nota |
|---|---|---|
| Gdau / gdau / Goot / Gau / Godot (bien) | **Godot** | nombre del motor |
| gdo engine | **Godot Engine** | |
| M root / am rout / Hamot | **CamRoot** | nodo raíz de la cámara |
| H / V | **H / V** | nodos de rotación horizontal y vertical |
| spring arm 3D | **SpringArm3D** | |
| State whoops / State controller | **StateController** | nodo de la state machine |
| animation tree | **AnimationTree** | |
| blend tree | **BlendTree** | |
| anim name | **anim_name** | señal `animation_finished(anim_name)` |
| on field | **on fill** | opción de Blender del cilindro |
| tony / tuny / toon | **toon / anime shading** | estilo del shader de nubes |
| frel | **Fresnel** | nodo del VisualShader |
| shader houra / Aura | **Aura** | efecto del level up |
| level of effect | **level up effect** | |
| pop effects / puff | **puff effect** | |
| row value | **raw value** | valor crudo del color (HDR) |
| item CMS / CMS | **custom_minimum_size** | |
| MK / MK item | **MISK** (misceláneo) | tipo de `ItemData` |
| dat / DAT / data | **data** | |
| do free / que free | **queue_free()** | |
| hell / hell be | **health** | |
| just hit | **just_hit** | |
| flor | **floor** | GridMap renombrado |
| wall arched | **WallArch** | índice de tile de pared |
| ad dative / aditive | **additive** | blend mode del glow |
| forward plus | **Forward+** | renderer |
| quing quest / coding quest | **CodingQuests** | canal del autor |
| leu / Leu / Lelu | **Lelu** | instructor invitado de VFX |
| Kay kit / Kut | **KayKit** | packs de assets |

## Transcript

[00:00:00] learn how to use gdau to build a 3D RPG
[00:00:02] game in this series Omar from coding
[00:00:05] Quest will guide you through four main
[00:00:07] components creating the player designing
[00:00:10] the AI skeleton monster building the
[00:00:12] guey with a profile and inventory system
[00:00:15] and adding stunning VFX to enhance your
[00:00:18] game by the end of this course you'll
[00:00:20] have the skills to create a dynamic and
[00:00:22] engaging 3D RPG game with gdau complete
[00:00:25] with Advanced features and interactive
[00:00:28] elements for skipping me just hold on
[00:00:30] real quick is I'm going to give you a
[00:00:31] quick overview of this course and what
[00:00:33] you'll get out of it my name is Omar and
[00:00:35] I run the channel coding Quest and if
[00:00:36] you guys enjoy this free course
[00:00:38] definitely check out my channel as well
[00:00:39] as my site as I'll also have this course
[00:00:41] up for free on there in a more
[00:00:43] comfortable format now the first thing
[00:00:46] that we're going to do in this course uh
[00:00:48] is understand that this course is split
[00:00:50] up into four sections the first section
[00:00:52] is going to be focusing on the player
[00:00:54] specifically the player will be able to
[00:00:56] have several different features like
[00:00:58] moving uh animating
[00:01:00] attacking uh stuff like that the next
[00:01:03] section we'll have a monster which will
[00:01:05] be a relatively simple AI that will just
[00:01:09] have some different state machines it'll
[00:01:11] be able to go from idle to run to attack
[00:01:13] Etc so it'll be able to detect all those
[00:01:16] different things in this course after
[00:01:19] the monster we'll be going into the GUI
[00:01:21] which will involve an inventory system
[00:01:24] with an equipment system with it a
[00:01:26] profile system to just represent and
[00:01:28] show our stats and finally a shop so
[00:01:31] this will allow us to buy items and
[00:01:33] stuff like that the last section of this
[00:01:36] course will have VFX this will kind of
[00:01:39] I'll kind of introduce you to what it
[00:01:42] how we do this with a very simple fire
[00:01:44] effect then we're going to have a guest
[00:01:46] instructor who's going to come in and
[00:01:48] he's much much more talented than I am
[00:01:50] with the shaders and particle effects
[00:01:53] inside of good he's going to kind of
[00:01:55] walk you through a lot of that
[00:01:57] stuff lastly as I mentioned short
[00:02:00] mentioned before if you guys don't
[00:02:01] prefer the YouTube format with one super
[00:02:03] long video I have this course up uh
[00:02:06] split up more comfortably on my site at
[00:02:08] quing quest.com we go check it out
[00:02:10] without but without further Ado good
[00:02:12] luck with this course and I hope to see
[00:02:13] you all at the end all right welcome
[00:02:15] everyone to our beginning uh part of
[00:02:18] this RPG course now in order to get
[00:02:21] started I'm going to assume that you
[00:02:23] have downloaded the starter project
[00:02:26] files now do keep in mind that if yours
[00:02:29] is zipped meaning it is a ZIP file and
[00:02:31] it ends with Z zip you need to unzip it
[00:02:36] here I have the unzipped version and now
[00:02:39] we can click the gdo engine and open it
[00:02:42] up here you will see the project manager
[00:02:45] now there is something to note at the
[00:02:47] moment of this recording the stable
[00:02:50] version is on 4.2 in fact I can open it
[00:02:53] up and you will see the version is
[00:02:55] 4.22 now the the version I'm going to be
[00:02:58] using is 4. three as this is kind of in
[00:03:01] beta or in Dev at the moment uh it is
[00:03:05] still not buggy per se but it is just
[00:03:08] not stable yet but um I'm going to be
[00:03:10] recording this and hopefully by the time
[00:03:12] you're watching this and following along
[00:03:14] it will be in 4.3 stable however just to
[00:03:18] basically note this if you are using a
[00:03:20] different version if you doubleclick the
[00:03:23] project you will see that it wants to
[00:03:25] upgrade it and it will do this
[00:03:27] automatically and it's very good at it
[00:03:29] it will upgrade whatever it needs to uh
[00:03:32] and it just does it all on its own now
[00:03:34] all I need to do to actually get started
[00:03:36] is I'm going to take my file here the 3D
[00:03:39] action RPG starter project files and
[00:03:41] drag it into my uh project
[00:03:44] manager now I will find it by finding
[00:03:47] the name of it 3D action RPG and if I
[00:03:50] double click it whether you needs to
[00:03:52] convert convert it or not you just open
[00:03:55] it and it might reort some assets if it
[00:03:58] needs to it will do whatever needs to do
[00:04:00] to get started so hopefully by the time
[00:04:04] it's done importing and whatever you see
[00:04:06] something like this you see no scenes
[00:04:08] you see a bunch of asset packs here you
[00:04:10] see a bunch of folders and let's just
[00:04:12] take a look at what we have first so we
[00:04:15] have a few asset packs that essentially
[00:04:17] here we have some uh 2D pixel
[00:04:20] art we have the kkit adventure which
[00:04:23] we'll be using for a character we have
[00:04:24] the Kut dungeon remastered which is
[00:04:27] going to be for a dungeon we have the
[00:04:29] skeleton which will be for our monsters
[00:04:31] and we have this sfx which will be for
[00:04:34] our sound we also have the VFX these are
[00:04:38] um these will be made outside of kind of
[00:04:40] the engine and and course but we'll have
[00:04:42] a introductory uh instructor kind of
[00:04:46] come in and you know do these on our own
[00:04:48] but here I have them just already
[00:04:50] finished as I'll be showing you how to
[00:04:51] actually Implement them into our game
[00:04:53] later we also have our default uh
[00:04:56] resource here or our theme and if I
[00:04:58] click it you will see it already kind of
[00:05:00] filled in but I will show you how to do
[00:05:02] this from scratch now kind of following
[00:05:04] that if I go to my 2D scene on the top
[00:05:08] you will see the UI that I'm using this
[00:05:10] is the UI template we're going to use
[00:05:13] some of these panels we're going to use
[00:05:14] some of these for armor stuff like that
[00:05:17] so this was something that we're going
[00:05:19] to use for a little later and then
[00:05:21] lastly of course we have our font this
[00:05:23] is going to be our font our custom font
[00:05:25] inside of the engine and that is already
[00:05:28] in the default function as font as well
[00:05:30] you can see here that I've already
[00:05:31] loaded it in all right so this is our
[00:05:34] starter project and now from here let's
[00:05:37] get started and create our grid map so
[00:05:39] we want to actually get started by going
[00:05:41] to the 3D part and we'll get started in
[00:05:44] here in just a
[00:05:46] second okay so let's get started with
[00:05:48] our grid map now our grid map is
[00:05:50] essentially Our World Builder it's our
[00:05:53] environment scene level to do this what
[00:05:55] we'll do is first we'll create two new
[00:05:58] folders we'll create a new folder called
[00:06:02] scenes and we'll create one more folder
[00:06:04] called scripts this is just to organize
[00:06:07] all our like scenes and scripts and
[00:06:09] things into these three main folders now
[00:06:11] one cool feature inside of gdau is if I
[00:06:14] rightclick one of these I can set the
[00:06:16] color folder of course you can kind of
[00:06:18] set it to whatever you'd like I'll just
[00:06:20] set it to random colors uh I'm not too
[00:06:22] picky about the colors so just kind of
[00:06:24] set them in order like this now in the
[00:06:27] scenes folder I'm going to create a new
[00:06:28] folder called levels and this is where
[00:06:32] you can create more than one level and
[00:06:34] anything level related I'll put it in
[00:06:36] here so first let's create our level so
[00:06:39] let's hit node 3D as our base scene I
[00:06:42] will save this in my scenes folder my
[00:06:45] levels I'm going to rename it right here
[00:06:49] I will rename this to level one and hit
[00:06:51] save and this will be our main scene at
[00:06:54] the moment if I hit play I can select
[00:06:57] current and you will see our game has
[00:07:00] launched this is our first game
[00:07:03] congratulations now let's rename this to
[00:07:05] level one on the top
[00:07:07] left and now I want to add something
[00:07:09] called a grid map this is going to be
[00:07:12] where I can actually put tiles down in a
[00:07:15] 3D environment now you can see that I
[00:07:17] can put stuff but there's nothing to put
[00:07:20] in order to put things in our game we
[00:07:23] need a mesh Library however in order to
[00:07:26] create a mesh Library I can't just
[00:07:27] create one like this I can't can't just
[00:07:29] click into this and do that this is
[00:07:31] something that you would you would do in
[00:07:33] a 2d scene or could do but in 3D
[00:07:36] unfortunately it's not that easy but
[00:07:38] don't worry it's still pretty easy just
[00:07:40] done a different way now to do this we
[00:07:42] will create a new scene here a 3D scene
[00:07:45] we'll rename this to mesh Library I'll
[00:07:50] contrl s to save this I'll put it in
[00:07:52] this level scene now what I'll do is I
[00:07:56] want to find a
[00:07:58] floor on uh our dungeon assets here so
[00:08:02] if I search up floor you will find some
[00:08:04] floors now do feel free to you know pick
[00:08:07] whatever you'd like I'm going to pick
[00:08:09] the
[00:08:11] floor P large I'm going to pick this guy
[00:08:16] and if I just drag it here and I turn on
[00:08:18] the pixel snap or the uh snap
[00:08:21] here it will snap to the next pixel now
[00:08:25] what I'm going to do is I'm going to
[00:08:26] reset the transform to 0
[00:08:29] and now I can snap it kind of nicely to
[00:08:33] this corner right here now don't worry
[00:08:35] it doesn't look beautiful and there is a
[00:08:37] reason for that but we'll get to that
[00:08:39] later at the moment all we need to do is
[00:08:41] hit make local I will drag this mesh out
[00:08:45] out of that thing I will delete this guy
[00:08:48] and now what I want to do is I want to
[00:08:50] click the mesh make sure the mesh is
[00:08:52] selected I'm going to go to mesh right
[00:08:54] here I'm going to create a collision
[00:08:58] shape and here we have a few uh options
[00:09:02] but I'm just going to leave it as it
[00:09:04] is and I will create and now you see
[00:09:07] here that I've created a collision shape
[00:09:10] now in my floor tile you want to make
[00:09:12] sure that it is the uh body where we
[00:09:16] have a static body 3D and then a
[00:09:18] collision shape now make sure it's in
[00:09:19] this order like so and now if we zoom in
[00:09:22] here you can actually kind of see that
[00:09:24] blue outline that is the Collision shape
[00:09:27] of our tiles now it's it's kind of hard
[00:09:29] to test this right now because we don't
[00:09:31] have a player yet but just trust me this
[00:09:33] will add Collision for our game now if
[00:09:35] you're using good 4.2 it is a similar
[00:09:38] process but I think it just has fewer
[00:09:41] options essentially and you will see
[00:09:42] something similar to this so if you're
[00:09:45] also using like 4.4 or whatever in the
[00:09:47] future it should relatively be the same
[00:09:50] if it's not search it up um for that
[00:09:53] respective version so if you're on 4.4
[00:09:55] or whatever version in the future just
[00:09:57] search it up on YouTube you might find a
[00:09:59] short 1 to 2 minute video explaining how
[00:10:01] to do that in fact I might actually
[00:10:03] update this in the future as well so
[00:10:06] okay now what we want to do is we want
[00:10:07] to repeat that process for one more of
[00:10:10] these I'm going to do this for this guy
[00:10:13] I will add a well I actually want to
[00:10:15] make this local first we'll drag this
[00:10:18] out I'm going to delete this node and
[00:10:21] I'm going to do the same thing at a
[00:10:23] static body click the mesh click create
[00:10:26] Collision shape and create and just drag
[00:10:28] that in
[00:10:30] and now you can see it's a little more
[00:10:32] accurate but yeah that's about it now
[00:10:35] all we want to do is we want to do two
[00:10:38] more things I'm going to add a wall now
[00:10:42] if you're wondering how to kind of
[00:10:44] navigate our 3D scene here all I need to
[00:10:46] do is hold shift and middle click and I
[00:10:49] can kind of drag my scene a little bit
[00:10:51] or my camera to the right or left now
[00:10:54] one other uh thing we'll add is a wall
[00:10:57] arched
[00:10:59] I'll drag this
[00:11:01] out I want this guy I want a wall
[00:11:07] doorway this is going to represent our
[00:11:09] door kind
[00:11:11] of and then I want a
[00:11:15] wall corner there we go and here you can
[00:11:19] see that it's just going to represent a
[00:11:21] corner now the last thing we'll have is
[00:11:24] a uh stairs this will be called uh
[00:11:27] stairs
[00:11:30] walled here we go and if I drag this out
[00:11:33] you will see it just has stairs or it is
[00:11:36] stairs okay so now we'll repeat the same
[00:11:39] process for each of these now a cool
[00:11:41] trick is if I select all of these and I
[00:11:43] right click and there should be a make
[00:11:47] local unless they took that
[00:11:48] out it seems like they took it out so
[00:11:51] we'll have to do it one by one that's
[00:11:53] okay so we'll make this local for each
[00:11:55] of these and again a cool trick is we'll
[00:11:59] control and select all the meshes and
[00:12:02] I'll simply drag them out of this now I
[00:12:04] can just delete all of
[00:12:06] these again I'll do the same
[00:12:09] thing now I have all these meshes I want
[00:12:12] to essentially add now for each of these
[00:12:15] I will just create a collision
[00:12:18] shape and you can see it's creating a
[00:12:21] pretty accurate Collision shape for each
[00:12:24] of
[00:12:25] these now we'll actually skip the uh
[00:12:29] stairwell and I'm going to delete the
[00:12:31] doorway door so here I don't want a door
[00:12:35] I'm just going to delete that now for
[00:12:37] each of these I'm going to just drag in
[00:12:38] the Collision
[00:12:40] shape but again I need a static body 3D
[00:12:43] for each of these to make sure we
[00:12:45] essentially add a static body 3D for
[00:12:48] each of these
[00:12:50] meshes and drag in the Collision shape
[00:12:52] for that corresponding mesh or static
[00:12:55] body now you might kind of Imagine an
[00:12:58] issue here for this stairs stairs don't
[00:13:02] exactly uh Collide well with our player
[00:13:05] and you'll see why later when we add our
[00:13:07] player but for now what we'll do is we
[00:13:10] will actually add a static body 3D I
[00:13:13] will add my own Collision shape a
[00:13:15] searching up Collision shape and I'm
[00:13:18] going to give it a shape
[00:13:20] of
[00:13:23] a to a box here we go and now I'm going
[00:13:27] to kind of just drag this box out and
[00:13:30] what I'll do is I'll rotate
[00:13:33] it and basically extend it to be the
[00:13:36] size of the stairwell and I'm going to
[00:13:38] turn off the snap so I can make this a
[00:13:40] little more accurate here and I'm going
[00:13:42] to just drag this up a tiny bit until I
[00:13:44] kind of see it pop out now I want to
[00:13:47] rotate it just slightly downwards like
[00:13:49] this and I'm going to just try to
[00:13:52] basically match it up with the stairs as
[00:13:55] much as I possibly can
[00:13:59] and this will allow us to basically
[00:14:01] smoothly run on the
[00:14:04] stairs all right so that looks kind of
[00:14:06] okay I'll just shorten this slightly so
[00:14:09] it doesn't pop out of the top there and
[00:14:11] now we'll save and finally we can go to
[00:14:14] our scene on the top left we can export
[00:14:17] as mesh Library we can go into our
[00:14:19] scenes levels all this
[00:14:23] Library hit save and now if we head over
[00:14:26] to a level one I will find the asset
[00:14:29] that I just found or just made I going
[00:14:32] into our levels and now here we have a
[00:14:34] mesh Library I can drag this in and now
[00:14:37] you can see that I have all my libraries
[00:14:39] or all my
[00:14:41] floors now what I can do here is I can
[00:14:45] hold shift drag and then
[00:14:48] crlf this will allow me to fill in my
[00:14:50] scene very quickly and very nicely now
[00:14:53] if I hit play nothing will happen or I
[00:14:56] won't see anything and that is for a
[00:14:57] very good reason that is because I do
[00:15:00] not have a camera 3D in order to make
[00:15:03] our 3D scene work I need a camera 3D
[00:15:05] inside of a 3D scene in order for it to
[00:15:08] play and so I can see our 3D environment
[00:15:12] now this does not look very well or very
[00:15:14] good in fact it looks horrible in fact
[00:15:16] we can't even see the outline of our
[00:15:18] files so uh in the next part we will
[00:15:21] look at adding our environment and
[00:15:23] seeing how we can add some light in
[00:15:25] World environment and stuff like that
[00:15:27] all right so I'll see you in the next
[00:15:30] part all right now that we have our
[00:15:33] scene here I want to add some World
[00:15:35] environments and stuff now let's take a
[00:15:37] look at what that even is if we add a
[00:15:39] new node here to our level one I'm going
[00:15:41] to add a world environment and
[00:15:43] immediately you can see man it looks so
[00:15:45] much better and if I hit
[00:15:47] play you will see no difference now why
[00:15:51] is that well we need to actually add an
[00:15:54] environment we need to add a new
[00:15:56] environment here when we do we will go
[00:15:58] into into this environment and we can
[00:16:00] start fiddling with its uh things here
[00:16:04] now let's take a look at a kind of short
[00:16:05] intro to what we can actually do here
[00:16:08] the first thing is the background now
[00:16:10] the background here this is where we can
[00:16:12] actually decide if we want a dungeon or
[00:16:14] a Overworld kind of a sky based thing
[00:16:17] let's take a look at the sky first so
[00:16:19] let's add a sky add a new sky over here
[00:16:23] we'll go to procedural Sky material and
[00:16:27] yeah that's kind of it in here you can
[00:16:29] of course adjust the colors but we're
[00:16:30] not going to do that we're going to hit
[00:16:33] play and now we can see a much nicer
[00:16:36] scene we can even see the tiles uh
[00:16:38] properly you know you can see the actual
[00:16:40] stuff of it now what we'll do is I'll
[00:16:43] add something called a directional light
[00:16:46] this allows me to add light that is
[00:16:48] directional and you can see by default
[00:16:50] it is pointing uh this way to my right I
[00:16:53] suppose for the negative Zed index now
[00:16:57] here I can point it downwards
[00:16:59] and if I hit play you will see now it's
[00:17:02] our scene is just more has more light
[00:17:05] now we're going to be making a dungeon
[00:17:07] so obviously we're not going to use any
[00:17:09] of this so let's reset all this as
[00:17:12] instead of mode or in our mode instead
[00:17:14] of color or Sky sorry we're going to use
[00:17:16] a custom color now in here when I click
[00:17:19] the custom color this is where it's kind
[00:17:21] of up to you be a little creative on
[00:17:23] this as I'm going to adjust the color
[00:17:27] 100 100 and 100 this will give my world
[00:17:31] kind of a grade out effect and when I
[00:17:34] hit play it looks a little dark but it's
[00:17:37] not completely black so if I were to
[00:17:39] reset the color here play again you'll
[00:17:42] see it's completely black which of
[00:17:44] course you probably don't want so it's
[00:17:46] kind of up to you you know be a little
[00:17:47] creative on the coloring um if you are
[00:17:50] creative I suppose um but I'm going to
[00:17:52] just do 100 100 100 and now I'm going to
[00:17:56] head over to the fog and volum metric
[00:17:59] fog now I'm going to just enable both of
[00:18:02] these now in order to play around with
[00:18:04] this I would kind of just suggest you
[00:18:07] know play around with some of these one
[00:18:08] by one and change the values and see
[00:18:11] what happens that is essentially the
[00:18:14] idea of this change some of the light
[00:18:16] energy values you know change the
[00:18:18] density Etc and see what your scene
[00:18:21] looks like for me what I'm going to do
[00:18:23] is in my volumetric
[00:18:26] fog I'm going to change the density to
[00:18:30] 0.02 and leave the rest as it is for the
[00:18:34] fog I'm going to change the density to
[00:18:39] 0.2 the light energy to
[00:18:42] 0.1 and that's it now if I hit play we
[00:18:46] get kind of a similar effect to what I
[00:18:48] have for my original kind of game all
[00:18:51] right so we're actually not going to
[00:18:53] enable glow just leave it off for now as
[00:18:55] we might actually come back to it um
[00:18:57] once we add more light and stuff to our
[00:18:59] world and scenes and stuff okay so now
[00:19:02] that we have our world scene set up here
[00:19:04] we want to actually start with our
[00:19:06] player so our player will be our next
[00:19:08] part and I will see you all in the next
[00:19:10] part where we actually get started with
[00:19:12] our player scene adding our player and
[00:19:14] you know making it work so see you in
[00:19:16] the next part all right so to get
[00:19:19] started here what we're going to do is
[00:19:20] create a new Scene by adding a new scene
[00:19:23] here we will add a new node called a
[00:19:27] sorry not static uh character body 3D
[00:19:31] I'm going to add a collision
[00:19:34] shape and what we're going to do now is
[00:19:37] add our character we add our character
[00:19:39] or the character that we'll add is
[00:19:41] inside of the assets folder in our K
[00:19:44] Adventures we'll find the fbx that we
[00:19:47] want and here if we find uh just one of
[00:19:52] these guys sorry not the assets the
[00:19:54] characters here we go we'll find these
[00:19:56] characters we will use a barbarian or no
[00:20:00] sorry we'll use a knight as our base and
[00:20:03] now we can drag our Knight here here we
[00:20:06] go I will make this
[00:20:08] local and now I can reset the Knight the
[00:20:12] position to 0 0 right there now the
[00:20:15] Collision shape I'm going to give it a
[00:20:17] collision shape of a capsule and just
[00:20:19] move this up to be around the same size
[00:20:22] as my player can make it a little
[00:20:25] smaller and just make it at the base of
[00:20:27] its feet
[00:20:29] all right so there we go there's our
[00:20:31] capsule for a player now we'll save this
[00:20:34] as player or lowercase maybe and I'll go
[00:20:37] up into my scenes folder create a new
[00:20:39] folder called player hit play and save
[00:20:44] and here we go now in here we'll rename
[00:20:47] our player to player I will now attach a
[00:20:50] script with the template character body
[00:20:53] 3D I will move this script into my
[00:20:56] scripts folder adding a new character
[00:20:59] uh script here called
[00:21:01] player open create and now we have our
[00:21:05] script now we'll just hit play uh
[00:21:08] actually before we hit play let's add
[00:21:09] our player to our scene here so let's
[00:21:12] add our player like
[00:21:14] so it might kind of lag out or it might
[00:21:17] just move it now that happens so I'll
[00:21:19] move it back into the uh player scen or
[00:21:22] player files sometimes that happens and
[00:21:24] it's kind of annoying but that's okay um
[00:21:26] it's just because the project files are
[00:21:28] so I might have to hold and drag it
[00:21:30] until I see the actual image there there
[00:21:33] we go so now I'll add my character body
[00:21:35] as a child of the level one I'll rename
[00:21:38] this to player hit save and now I'll hit
[00:21:43] play and when I hit play you will see my
[00:21:46] character body and in fact you can even
[00:21:48] start moving with your joystick or with
[00:21:50] your uh keyboard now obviously though
[00:21:53] you might notice that this doesn't
[00:21:56] actually really work the the way might
[00:21:58] want it to the arrow keys might not be
[00:22:01] the same way we actually need it to now
[00:22:04] that is because our uh camera is not
[00:22:08] attached to our player and we don't have
[00:22:11] Direction based movement well based on
[00:22:13] where our camera is looking so let's
[00:22:15] take a look at how we can do that inside
[00:22:17] of our player next but first to get this
[00:22:20] started though let's just close the mesh
[00:22:21] library and now I will actually get into
[00:22:24] my player and we'll take a look at how
[00:22:26] we can do this inside of our player
[00:22:29] all right to get started with our ler
[00:22:32] and camera control and movement and
[00:22:33] stuff what we're going to do is we'll
[00:22:35] set up the camera first and then we'll
[00:22:37] take a look at the script because we
[00:22:39] added a script but we don't know what
[00:22:40] any of it does yet so first what we'll
[00:22:42] do is I'm going to add a node
[00:22:44] 3D I'm going to add a new node called
[00:22:49] spring arm 3D I'll add one more node
[00:22:53] inside of the spring arm called camera
[00:22:56] 3D oops that's not camera 3D
[00:23:00] add a new node one more time M 3D and
[00:23:04] this guy I'm going to actually add one
[00:23:07] more node 3D and put all of this inside
[00:23:10] of that one now this one I'm going to
[00:23:12] rename it to M root this next one I will
[00:23:16] rename it to H and this one to V this
[00:23:21] essentially represents my horizontal
[00:23:23] movement and this represents my vertical
[00:23:25] movement and then this will be my actual
[00:23:27] camera right okay let's take a look
[00:23:29] though at what I want the setup to look
[00:23:32] like for the spring arm I'm going to
[00:23:34] take this and set it to negative five
[00:23:37] now you can change the length later but
[00:23:39] at the moment I'm just going to leave
[00:23:41] this as five now this is the actual
[00:23:43] length away from the camera the player
[00:23:46] you'll kind of see it will be away five
[00:23:49] uh pixels or meters away from the
[00:23:52] camera now the camera itself I'm going
[00:23:55] to rotate it in the transform
[00:23:59] on the Y AIS to 180 and on the X to -10
[00:24:04] this will just make it Point downwards
[00:24:06] ever so
[00:24:08] slightly next in my um am
[00:24:14] rout sorry no in my V right here we can
[00:24:17] now move this guy up uh a little bit
[00:24:20] kind of up to you I'm going to move it
[00:24:22] up to 2.9 this will be above my player's
[00:24:26] head all right now lastly we'll go back
[00:24:29] to our script and just a kind of tip
[00:24:31] here and this is what I will be doing
[00:24:33] for this series of course I'm going to
[00:24:35] be making my float or my script float
[00:24:38] this will make it come out of my actual
[00:24:40] scen or act out of gdau and into its own
[00:24:44] window this allows me to just show the
[00:24:46] code a little nicer and you can actually
[00:24:49] see everything without it being all
[00:24:50] crumpled up so I can zoom in and it
[00:24:52] might look a little nicer for you but of
[00:24:54] course you feel free to do whatever
[00:24:56] you'd like all right now in the code
[00:24:58] here we can see that we have a speed a
[00:25:00] jump velocity as our two variables now
[00:25:03] if you're using another version you
[00:25:04] might have gravity fact in vo 4.2 there
[00:25:08] was another one called variable gravity
[00:25:10] that might be what You' be using now
[00:25:13] don't worry it might yours might look
[00:25:15] slightly different but it's still the
[00:25:16] same the general idea here is first
[00:25:18] we're going to add gravity and we do
[00:25:20] that by adding the velocity on the Y AIS
[00:25:24] and here the gravity will add it to the
[00:25:26] y- axis times Delta here we'll jump the
[00:25:30] same idea so here we jump by clicking
[00:25:33] the UI accept which is actually spacebar
[00:25:35] or enter on by default inside of gdo
[00:25:38] we'll also use a function called is on
[00:25:40] floor to make sure we're actually on the
[00:25:42] floor and then we jump now here the jump
[00:25:45] velocity is actually positive and the
[00:25:47] reason is because the positive is
[00:25:50] upwards not NE uh the other way around
[00:25:54] now here we will get the input Direction
[00:25:57] by getting Vector between these four
[00:26:00] Keys it will give us a input Direction
[00:26:03] based on what I click with these four
[00:26:06] Keys next it will give us our Direction
[00:26:09] with the transform. basis and multiply
[00:26:12] it by the Direction X and Direction y
[00:26:15] now the reason we don't do the Zed is
[00:26:16] because that's we don't need that right
[00:26:18] we just need X and Y for the kind of Pop
[00:26:21] down movement if that makes sense now
[00:26:24] we'll normalize it this will kind of
[00:26:25] just essentially round our number to a
[00:26:27] nice number so it's not completely weird
[00:26:30] every time I click and then we'll check
[00:26:32] to see if direction is valid if it is
[00:26:34] this means I'm moving and if I am moving
[00:26:36] then I want to actually move I move by
[00:26:39] multiplying my velocity or making my
[00:26:41] velocity dox equal to Direction dox time
[00:26:44] speed which up here is 5.0 now here this
[00:26:48] is essentially the same as setting my
[00:26:50] velocity to zero but here it's just
[00:26:52] using a function called move towards uh
[00:26:55] it's just basically taking our current
[00:26:57] velocity and moving moving it to zero
[00:26:59] over the times of speed so don't worry
[00:27:01] too much about it it's pretty much the
[00:27:03] same as doing this now lastly we'll have
[00:27:05] a move and slide function this will
[00:27:07] allow us to actually move and slide or
[00:27:10] move our player so this allows us to
[00:27:13] actually utilize velocity now I do have
[00:27:15] a video on my channel uh explaining
[00:27:17] transform and basis and how General
[00:27:20] things inside of a 3D environment work
[00:27:23] at least in the simplistic manner so if
[00:27:25] you're curious about how the basis and
[00:27:27] transform works terms of our player do
[00:27:30] check out that video on my channel um it
[00:27:33] is on coding quests again that's so
[00:27:36] lastly let's close our script here as I
[00:27:38] want to set up my camera now in order to
[00:27:41] do this I'm going to create a new script
[00:27:42] here by going to scripts player and I'll
[00:27:45] actually add it through the cam rot here
[00:27:47] we'll add a new script by going to the
[00:27:49] top left by adding a new script I'll uh
[00:27:53] call this camera controller I'll add
[00:27:56] this script to my player scene for
[00:27:58] scripts here open create and here we go
[00:28:02] here's our script now in this script
[00:28:05] what I want to do is I'm going to delete
[00:28:07] all this and add some new variables the
[00:28:10] first variable will be cam
[00:28:12] root H this is going to be an
[00:28:16] integer this will be equal to zero we'll
[00:28:19] do the same thing but for the V we'll
[00:28:21] say cam root B and we'll say int equal
[00:28:27] Z next we want to get the or have a
[00:28:31] maximum and a minimum for both of these
[00:28:35] uh specifically for the V so what we'll
[00:28:37] do is I'm going to use something called
[00:28:39] export variable h v uh V root and this
[00:28:44] will be an integer and we'll make it
[00:28:47] equal to 75 by default now I'm going to
[00:28:51] duplicate this but I'm going to actually
[00:28:53] change this to be Max and this to be Min
[00:28:57] so the minimum value I want it to be 55
[00:29:00] at least for me and the max I want it to
[00:29:03] be 75 now you'll see what this kind of
[00:29:06] looks like in code when I actually start
[00:29:08] using it now what I'm going to do is I'm
[00:29:10] going to make two more variables for
[00:29:12] sensitivity to kind of adjust our
[00:29:14] sensitivity based on this variable I'll
[00:29:17] make one
[00:29:18] for
[00:29:21] sensitivity maybe I'll just copy this
[00:29:23] number right here or this word
[00:29:25] sensitivity this will be a float and
[00:29:28] I'll make this equal to
[00:29:29] 0.1 let me just copy paste this and
[00:29:33] we're going to change this to
[00:29:34] V one last thing we'll do is we will add
[00:29:38] a
[00:29:39] acceleration variable H acceleration
[00:29:42] this will be a float as well so we'll
[00:29:44] make it equal to
[00:29:46] .0 copy this one more
[00:29:49] time but this one will be for the V all
[00:29:53] right so now let's take a look at the
[00:29:54] actual logic of our code so the first
[00:29:56] thing we'll do is we'll create a
[00:29:58] function called input this will allow us
[00:30:01] to get a event input that essentially
[00:30:04] has things in it now what are these
[00:30:06] things well if I print event and I close
[00:30:10] this and hit my play
[00:30:13] button um we'll actually have to adjust
[00:30:15] something in a second but if I start
[00:30:17] moving my mouse around you'll see it
[00:30:19] says input event Mouse motion if I click
[00:30:22] you will
[00:30:24] see right above here it says event Mouse
[00:30:28] button this means I clicked right so
[00:30:31] this allows me to check to see if
[00:30:33] there's any sort of input with my mouse
[00:30:36] now what I need to do here just to make
[00:30:38] sure we set this up I need to delete my
[00:30:40] old camera 3D in my level one so now
[00:30:43] that this guy can actually take over and
[00:30:45] enable in this camera as this is the
[00:30:47] camera I want to look out of when I play
[00:30:50] Let's Open Up Our script here again and
[00:30:53] now let's take a look at what I can do
[00:30:55] to actually make this camera work what I
[00:30:57] can do is I can say if event is input
[00:31:01] event
[00:31:03] Mouse oops Mouse motion then I want to
[00:31:07] actually do something what do I want to
[00:31:09] do well I want to change my cam rot H
[00:31:13] and add the event the negative event uh
[00:31:18] do relative dox multiplied by the H
[00:31:24] sensitivity now I'll do the same thing
[00:31:26] but for the V oops
[00:31:29] copy paste this I'll change this to V
[00:31:32] I'm going to remove the negative here
[00:31:35] this will be do y and this of course
[00:31:38] will be V sensitivity this will allow us
[00:31:41] of course these AR the same number but
[00:31:42] this will allow us to you know adjust
[00:31:44] these movement based on
[00:31:47] sensitivity all right now this won't
[00:31:50] actually do anything so let's make this
[00:31:52] these numbers do something so we'll add
[00:31:54] a physics process function what we'll do
[00:31:57] here is we'll say cam root B is equal to
[00:32:01] clamp which is a math function we're
[00:32:04] going to clamp this form cam root V to
[00:32:09] degree to Radiance of our cam V
[00:32:14] Min to whoops outside of that to degree
[00:32:19] to radians one more time but this time
[00:32:21] we'll do the cam B
[00:32:24] Max all right so this will essentially
[00:32:27] clamp our vot between 55° and 75° you'll
[00:32:34] see what this looks like in just a
[00:32:35] second when we actually make this work
[00:32:37] so what we need to do to make this work
[00:32:39] is get node H and this will be our
[00:32:42] horizontal so we'll take the rotation of
[00:32:45] our Y and we'll make it equal to lur F
[00:32:49] the lur float from its float from so the
[00:32:54] float that we want it to rotate is going
[00:32:56] to be its current rotation so what I'll
[00:32:58] do is I'll copy
[00:33:00] this right here so I want to get its
[00:33:03] current rotation and then rotate it to
[00:33:08] mun H there we go over a time of
[00:33:13] Delta
[00:33:15] times H
[00:33:18] acceleration I think I spelled Delta
[00:33:20] wrong there so Delta there we go all
[00:33:24] right now that that's right now what I
[00:33:26] want to do is I want to actually copy
[00:33:27] paste this and now I'll do the same
[00:33:29] thing for the V but obviously the
[00:33:31] rotation for this will be on the X AIS
[00:33:34] because if I'm rotating the vertical I
[00:33:36] want to be doing the
[00:33:37] x-axis all right so here I'm going to do
[00:33:40] the same thing so instead of the H
[00:33:42] rotation I want the V rotation of course
[00:33:45] here I want the X rotation and then here
[00:33:47] I want the
[00:33:49] v v and then the V
[00:33:52] acceleration all right so now when I hit
[00:33:54] play Let's just test this out sometimes
[00:33:56] it can be buggy
[00:33:58] let's see if I can now move all right so
[00:34:01] now you can see when I move around my
[00:34:03] mouse not perfect but it is working
[00:34:07] slightly okay so let's take a look at
[00:34:09] what's going on as this doesn't seem to
[00:34:11] be working out 100% let's read through
[00:34:14] our code here and see if it makes
[00:34:16] sense first we're adding to our H
[00:34:18] rotation in the negative event. relative
[00:34:21] dox times H
[00:34:23] sensitivity next we're doing the same
[00:34:25] thing but on the y- axis which is right
[00:34:28] time the V sensitivity okay that looks
[00:34:31] right then we're taking our cam rot
[00:34:34] camot V and we're going to clamp it
[00:34:37] between its current uh count CL rot and
[00:34:40] between the minimum and the maximum okay
[00:34:43] that looks
[00:34:45] right okay now here we have the rotation
[00:34:48] doy we're going to lurp it from its H
[00:34:52] rotation so it's current rotation to cam
[00:34:55] root H right by the speed of Delta time
[00:35:00] acceleration and then same thing here
[00:35:02] but for the V this should be V that's
[00:35:05] right and then get node
[00:35:07] V okay so let's take a look at one more
[00:35:11] thing this all looks right but maybe one
[00:35:14] more thing that we can do is we can make
[00:35:16] our input here do set Mouse
[00:35:21] mode to input dot oops
[00:35:29] Mouse
[00:35:31] mode captured here we go we'll close
[00:35:34] this and this should capture our
[00:35:37] Mouse so now when I move it should allow
[00:35:40] us to move around smoothly but it's not
[00:35:43] I'll be right back and figure out why
[00:35:45] it's not letting us move all right so
[00:35:48] one small mistake I made actually is
[00:35:50] these two numbers are actually going to
[00:35:52] be floats not integers that is why we
[00:35:55] had that weird clunky sound is because
[00:35:57] it was trying to round our float number
[00:35:59] basically to a whole number and now we
[00:36:02] have a nice smooth motion there we go so
[00:36:04] now we have nice camera rotation now on
[00:36:08] the next part we're going to see how we
[00:36:09] can make our Player move in its
[00:36:12] corresponding well Direction because
[00:36:14] here you can see it's not exactly moving
[00:36:16] how we want it to Right Moving in well
[00:36:19] kind of this way or I guess this way as
[00:36:22] if it's looking this way but we need it
[00:36:24] to move whenever I move my camera in the
[00:36:27] corresponding Direction so let's take a
[00:36:29] look at the next part to see how we can
[00:36:30] do
[00:36:33] that all right so get started with our
[00:36:36] player what we're going to do is head
[00:36:37] over to the script I'm just going to
[00:36:38] stop the game here and this may seem
[00:36:41] annoying but what we're going to do is
[00:36:42] actually delete everything we're going
[00:36:44] to start everything completely from
[00:36:46] scratch the first thing we're going to
[00:36:47] do is we're going to start with um all
[00:36:50] the variables that we'll be adding
[00:36:51] eventually hopefully some of these will
[00:36:53] make sense uh right now and eventually
[00:36:55] some of them might not right now but
[00:36:57] some eventually they will make sense as
[00:36:59] we actually start to use them so let's
[00:37:01] just start with uh all the forces so the
[00:37:04] first thing on the forces is we'll
[00:37:06] export a few Val variables first we'll
[00:37:09] export a variable called gravity this
[00:37:11] will be a float equal to
[00:37:13] 9.8 next we'll
[00:37:16] export our jump Force this will be an
[00:37:20] integer equal to 9 will export a walk
[00:37:25] speed this will be an int equal to three
[00:37:29] and lastly we'll have a run speed as
[00:37:32] eventually we want to uh create a shift
[00:37:35] uh hold right where we can actually go
[00:37:37] from walking to running so this will be
[00:37:40] our speed that we actually run at now
[00:37:42] this will probably have to be greater
[00:37:43] than three so in my case I'm going to do
[00:37:46] 10 which may seem like a lot but you'll
[00:37:48] see notice or you'll notice later that
[00:37:50] it doesn't actually impact it that much
[00:37:53] you'll kind of uh play around with the
[00:37:54] values yourself hopefully next we're
[00:37:57] going to create a few um animation nodes
[00:38:00] so these are going to be the animation
[00:38:02] node
[00:38:04] names so what we'll do here is we'll say
[00:38:07] variable Idol node name which is a
[00:38:10] string will be equal to idle and what
[00:38:13] I'm going to do here is I'm just going
[00:38:14] to duplicate this a few times and now
[00:38:17] I'll just change the name of
[00:38:19] these this one will be walk this one
[00:38:21] will be run this one will be jump this
[00:38:24] one will be attack one and this one will
[00:38:27] be death now for each of these we'll say
[00:38:31] death or we kind of give it the
[00:38:33] corresponding one so walk here this one
[00:38:36] will be run this will be
[00:38:40] jump and attack one now you'll see what
[00:38:44] these kind of are for a little later but
[00:38:46] essentially they just represent the name
[00:38:48] of the animation that we'll be playing
[00:38:50] for each corresponding node all right so
[00:38:53] next we'll create some variables and
[00:38:55] these variables will be called our four
[00:38:57] for our state machine condition State
[00:39:00] whoops State machine conditions so what
[00:39:04] this will look like is is attacking and
[00:39:08] this will be a Boolean we'll also have a
[00:39:11] variable let's just duplicate this for
[00:39:14] now four times we'll have another one
[00:39:17] called is walking this will tell us if
[00:39:19] we're walking or not we'll have another
[00:39:21] one for is running and the last one for
[00:39:24] is dying each of these variables are
[00:39:27] going to true or false variables that
[00:39:29] will essentially tell us if we're dying
[00:39:30] or not if we're running or not if we're
[00:39:33] walking or not and if we're attacking or
[00:39:35] not all right so next up what we'll do
[00:39:38] is We'll add some Physics
[00:39:40] values so this will be the or the first
[00:39:43] one we have is Direction which will be a
[00:39:45] vector
[00:39:47] 3 next we'll have a
[00:39:49] horizontal
[00:39:52] velocity this will be a vector
[00:39:55] 3 next we'll have an aim turn and this
[00:39:59] will be a float this will allow us to
[00:40:02] aim uh for our
[00:40:04] turn when next we'll have a movement
[00:40:08] something called movement which will be
[00:40:09] a vector
[00:40:10] 3 next we'll have vertical
[00:40:15] velocity like so and this will be a
[00:40:19] vector
[00:40:20] 3 next we'll create a variable
[00:40:23] movement feed this will be an INT
[00:40:27] and last or not lastly we have two more
[00:40:30] we have an
[00:40:32] angular
[00:40:34] acceleration this will be an
[00:40:37] INT and next we'll have acceleration for
[00:40:41] actual movement will also be an INT and
[00:40:44] lastly we'll say
[00:40:46] variable uh there we go just hit and
[00:40:49] this will be a Boolean this is going to
[00:40:51] be for a little later uh in our series
[00:40:53] but this will allow us to detect if I
[00:40:55] just got hit or not so we kind of see
[00:40:58] what that's for much later but don't
[00:41:00] worry too much about it just now next
[00:41:02] I'm going to load or on ready load my
[00:41:05] cam rot or my cam rotation into as a
[00:41:09] variable or as a node and we'll do that
[00:41:12] by saying get node Hamot H I want to get
[00:41:16] access to the horizontal rotation of my
[00:41:18] node and I do that by saying get node uh
[00:41:21] rotation cam rot H and this will allow
[00:41:24] me to just get access to the node much
[00:41:26] quicker
[00:41:28] all right next what I want to do is I
[00:41:31] want to add a ready function and for now
[00:41:34] I'll just pass then I also want to add a
[00:41:37] physics process function this will allow
[00:41:40] me to actually Implement a lot of the
[00:41:42] physics process now in between this I'm
[00:41:45] going to add an input
[00:41:47] event and this will allow me to well
[00:41:49] input event just as we did in our camera
[00:41:52] rotation controller now in here is where
[00:41:55] we'll actually rotate or aim turn so
[00:41:58] here I'm going to say if event is input
[00:42:04] event uh Mouse motion then I'm going to
[00:42:09] whoops change my aim turn to be equal to
[00:42:14] negative event. relative dox time
[00:42:21] 0.015 all right now after this now we
[00:42:24] don't have this just yet but we'll write
[00:42:26] it anyways we're going to say if event
[00:42:29] is action pressed
[00:42:32] aim then I'm going to take my direction
[00:42:35] and make it equal to my cam
[00:42:38] rotation do Global transformation or
[00:42:42] transform basis. Z now this is going to
[00:42:46] actually allow me to change my direction
[00:42:48] that my player is looking at now this
[00:42:50] aim that I have that I don't have
[00:42:52] actually right now is going to be a left
[00:42:54] click or kind of whatever you want to be
[00:42:56] honest it might be control so if you
[00:42:58] want to aim your player in a certain
[00:43:00] direction whenever you hit this button
[00:43:02] this is how you do it so we'll add this
[00:43:04] a little later but don't worry too much
[00:43:06] about it right now but now we understand
[00:43:08] and see how we can kind of add this okay
[00:43:12] in our physics process function we want
[00:43:14] a few things the first thing we'll add
[00:43:17] is a variable called on floor this is
[00:43:21] going to be a variable that just checks
[00:43:23] to see is
[00:43:25] on floor
[00:43:27] so this will allow us to detect if we're
[00:43:29] on the floor or not but using a variable
[00:43:32] instead next what I'll do is I'll say if
[00:43:35] is not dying then I want to actually do
[00:43:38] the logic that I would do if I were not
[00:43:41] dying the first thing we'll do is we'll
[00:43:44] check to see or sorry not check but I'm
[00:43:46] going to actually uh add gravity now
[00:43:49] what I can say is if not on
[00:43:53] floor what I'll do here is I'm going to
[00:43:56] say Vertical Velocity plus equals Vector
[00:44:01] 3 dot
[00:44:04] down time
[00:44:06] gravity * 2 *
[00:44:11] Delta Delta so this will actually allow
[00:44:14] me to add our gravity now otherwise what
[00:44:17] I'm going to do here is I'm going to
[00:44:18] just copy
[00:44:20] this and I'm going to make this equal to
[00:44:23] a down time
[00:44:25] gravity instead of all this I'm just
[00:44:28] going to divide it by 10 and not
[00:44:30] multiply but divide by 10 all right okay
[00:44:34] so next what I want to do is I want to
[00:44:36] jump to jump similarly to what we had
[00:44:39] before I can say if input do is action
[00:44:43] just pressed I'm going to create a new
[00:44:45] variable or a new input called jump
[00:44:48] which we haven't added to our game yet
[00:44:50] but don't worry we'll add it soon and
[00:44:52] we'll say and is not is
[00:44:57] attacking because I don't want to jump
[00:45:00] while I'm attacking I also want to be
[00:45:02] able to jump when I'm also well you
[00:45:05] probably guessed it uh on floor so we'll
[00:45:08] use that variable that I just created to
[00:45:10] check if I'm on the floor or not now if
[00:45:13] I do what I'll do is very similar to the
[00:45:15] vertical velocity I can just take my
[00:45:17] Vertical Velocity and make it equal to
[00:45:20] Vector 3 dot up though this time times
[00:45:24] jump
[00:45:24] force all right so that is how I jump
[00:45:27] similar to what I had before next up I'm
[00:45:30] going to update my angular acceleration
[00:45:33] to 10 I'm going to update my movement
[00:45:36] speed to zero and then I'm going to
[00:45:39] update my acceleration to
[00:45:43] 15 all right next what we want to do is
[00:45:46] actually add our rotation so to do that
[00:45:48] or a camera rotation and apply it to do
[00:45:51] that what we'll do is we'll say h
[00:45:53] rotation is equal to cam rotation. h
[00:45:57] we'll get access to the node that we
[00:45:58] just created above we'll get its Global
[00:46:02] transformation
[00:46:04] transform basis and then oops basis and
[00:46:08] then we'll get
[00:46:13] .y hopefully this doesn't error there we
[00:46:16] go all right next what I want to do is I
[00:46:19] want to say direction is equal to its
[00:46:23] current direction rotated
[00:46:27] to our Vector oops Vector up Vector 3
[00:46:31] dot up with the H rotation as its angle
[00:46:35] then we'll normalize this this will
[00:46:37] essentially take its current direction
[00:46:39] take its current rotation and rotate it
[00:46:42] to the direction that I want it to be
[00:46:44] rotated to which is the AG
[00:46:46] rotation okay so now that we have that I
[00:46:49] want to actually get our Direction
[00:46:51] because this adjusts our Direction based
[00:46:53] on the rotation of our camera but what
[00:46:55] about the direction of our Mouse or not
[00:46:57] our Mouse but our keyboard well this
[00:46:59] isn't too hard what I can do is first
[00:47:02] I'll check to see if I'm actually
[00:47:03] pressing anything now to do that it's
[00:47:05] not too hard I can say if
[00:47:08] input is action pressed I can say
[00:47:13] forward or now in order to do the or
[00:47:16] command I can just do this which is
[00:47:18] shift and then the button right above
[00:47:20] your Enter key if you hold shift and
[00:47:23] press that weird straight button above
[00:47:26] your enter ke key that is how you do
[00:47:27] that now you can do or but I just prefer
[00:47:30] this way next what I'll do is I'm going
[00:47:33] to copy paste this right here and now
[00:47:37] what I'm going to do this might seem a
[00:47:38] little long but I'm going to now copy
[00:47:40] paste this two more
[00:47:42] times because now what I want to do is I
[00:47:45] want to check to see if I'm moving
[00:47:47] forward backwards I want to check to see
[00:47:50] if I'm moving left and you guessed it
[00:47:53] the last one is going to be to check if
[00:47:55] I'm moving right
[00:47:58] now if I'm doing any of these three
[00:47:59] actions or four actions sorry then what
[00:48:02] I'll do is I'll say direction is equal
[00:48:05] to in Vector
[00:48:08] 3 and then inside of this Vector 3 we're
[00:48:11] going to do something called input dot
[00:48:14] getaction strength this will allow me to
[00:48:17] essentially detect and get the action
[00:48:19] strength of a certain key now the key
[00:48:22] that I want here is going to be left for
[00:48:25] the X but here I'll sa left now what I
[00:48:28] want to do is I want to subtract so I'm
[00:48:30] going to copy this I want to subtract
[00:48:34] the
[00:48:34] right so here I'm going to subtract the
[00:48:37] left to the right and this will
[00:48:39] essentially allow me to see if I'm
[00:48:41] clicking left I will get one if I'm
[00:48:44] clicking right I will get negative 1 and
[00:48:47] that is what I want now here for the Z
[00:48:50] Axis or sorry for the Y I'll put zero
[00:48:52] and then for the Zed axis I want to just
[00:48:54] copy this
[00:48:57] right
[00:48:58] here this in the X uh or sorry the Zed
[00:49:01] axis then here I'm going to put
[00:49:05] forward and then for the last one I'm
[00:49:08] going to put
[00:49:09] backward and then lastly I need this guy
[00:49:13] on this line I
[00:49:14] believe and now we should not error
[00:49:18] unless I do because I probably have a
[00:49:21] missing thing
[00:49:25] somewhere so saying expected
[00:49:28] closing that right here we need to close
[00:49:31] this I
[00:49:32] believe nope that is not
[00:49:36] range but right here I need a comma
[00:49:39] that's why okay there we go so make sure
[00:49:41] there's a comma after each line except
[00:49:43] for the last one okay so this allows me
[00:49:46] to take my direction based on input so
[00:49:49] hopefully this kind of makes sense and
[00:49:51] if I zoom out here kind of get a full
[00:49:53] view of what the code should look like
[00:49:56] next I'm going to make sure that this
[00:49:57] direction is only updated if I'm
[00:49:59] clicking something all right so now I
[00:50:03] have my direction being updated on its
[00:50:06] current direction and rotating based on
[00:50:08] where I'm moving now the question is how
[00:50:11] do I actually
[00:50:12] move how do I actually rotate now the
[00:50:15] rotation that we're going to do is going
[00:50:17] to be rotation on the mesh not the
[00:50:20] actual player so on the very top of our
[00:50:24] script we're going to up here we're
[00:50:27] going to say on ready variable player
[00:50:29] mesh and we're going to load our mesh
[00:50:32] and we can do that by getting the KN so
[00:50:36] the Knight is going to be our player
[00:50:38] mesh all
[00:50:40] right next we'll head back to the bottom
[00:50:42] of our script here and in here uh sorry
[00:50:45] outside of this if check checking here
[00:50:48] we're going to check and now see if the
[00:50:53] input is action rest
[00:50:59] aim then what we'll do is I'll say
[00:51:01] player mesh. rotation doy is equal to
[00:51:05] lur angle to its current player mesh
[00:51:09] angle so what we'll do is we'll get its
[00:51:12] current
[00:51:12] rotation doy and we're going to rotate
[00:51:15] it to the cam
[00:51:18] rotation H or sorry cam rote H like that
[00:51:24] and we want to get that rotations
[00:51:27] y so we do that by saying rotation doy
[00:51:30] and lastly we'll do this at a speed of
[00:51:32] Delta time angular
[00:51:36] acceleration and that's
[00:51:38] it next we'll go down a little bit let
[00:51:41] me just go a few lines
[00:51:43] below next what I want to add here is an
[00:51:45] else statement and I'm going to actually
[00:51:47] copy this into this else statement but
[00:51:51] here what I'm going to do is I'm going
[00:51:52] to change this guy to the a tan
[00:51:57] two of its direction
[00:52:00] dox and
[00:52:02] direction do
[00:52:04] Z then I'm going to
[00:52:06] subtract it's rotation doy so this is
[00:52:11] the same as saying self. rotation
[00:52:14] okay and then the speed is also going to
[00:52:17] be Delta times
[00:52:18] acceleration all right this is how we do
[00:52:21] that now of course this isn't complete
[00:52:22] though because now we still have a few
[00:52:24] other things now the last parts we need
[00:52:28] are going to be right here I believe in
[00:52:32] this line so here we'll say velocity do
[00:52:36] Z is equal to horizontal velocity do Z
[00:52:41] Plus vertical velocity. Z and
[00:52:45] essentially we want to duplicate
[00:52:47] this three times we'll change this to Y
[00:52:51] this to Y and change this or sorry to x
[00:52:55] x and x
[00:52:58] now for the Y I'm going to change this
[00:53:00] to Y and change this by deleting this
[00:53:03] and only having the vertical
[00:53:06] doy lastly on the next line we'll move
[00:53:10] and slide this will allow us to actually
[00:53:12] use the
[00:53:13] velocity now the question is what if
[00:53:16] what about the horizontal velocity well
[00:53:18] here I can say if is
[00:53:22] attacking then what I want to do is I
[00:53:24] actually want to lurp my velocity
[00:53:27] to zero so I can do that by saying
[00:53:29] horizontal velocity is equal to
[00:53:32] horizontal velocity lurp and we'll lurp
[00:53:36] it to direction. normalized time
[00:53:41] 0.1 we'll do this at a speed of
[00:53:44] acceleration now I'll copy
[00:53:47] this now what if I'm not attacking which
[00:53:49] at the moment probably not going to be
[00:53:51] for a while well I'm going to copy paste
[00:53:54] it in the L statement but for this I'm
[00:53:56] going to remove the0 Z and instead I'll
[00:53:59] put movement speed uh movement
[00:54:03] speed and then that's it so now uh let's
[00:54:07] give this a try and see what we get well
[00:54:10] let's actually now import our
[00:54:12] functionalities here because I've added
[00:54:13] a few things but none of this actually
[00:54:15] does anything right now because well I
[00:54:17] haven't added it so let's close this go
[00:54:20] to our project settings our project
[00:54:22] settings here we'll go to input map and
[00:54:26] here where I want to add or can add new
[00:54:29] function input mapping now in the add
[00:54:32] action what I'll do is I'm going to add
[00:54:34] a new uh action called right left
[00:54:39] backward
[00:54:41] forward
[00:54:42] dump attack
[00:54:45] Sprint aim and pause these are all the
[00:54:49] inputs that we'll need eventually now
[00:54:51] for all of these you can add whatever
[00:54:52] you'd like for the right I'm going to
[00:54:54] add the left left I'm going to add a
[00:54:58] backwards I'm going to add s and forward
[00:55:01] I'm going to add a so ASW basically now
[00:55:05] for the jump I'm going to add the space
[00:55:06] bar attack I'm going to add the left
[00:55:09] button the left Mouse button and I can
[00:55:11] do that by going to Mouse buttons going
[00:55:13] up and selecting the M left Mouse
[00:55:16] button that's a attack now for Sprint I
[00:55:19] want shift for aim I want
[00:55:23] control for pause I'm going to add
[00:55:25] Escape
[00:55:26] now I can close this and now let's give
[00:55:28] it a try now most likely it probably
[00:55:31] won't work first try that's okay okay
[00:55:34] cool so we got something wrong right
[00:55:35] away because I spelled basis wrong so
[00:55:37] let's fix that right away and see what
[00:55:40] we
[00:55:41] get all right so we got a bunch of
[00:55:43] errors but we do have something working
[00:55:45] we do see that our mesh is working based
[00:55:48] on our rotation which is nice so we can
[00:55:50] see that some of these are actually
[00:55:53] working quite nicely and the aim is
[00:55:55] working so we now know that the aim is
[00:55:57] working we just aren't moving properly
[00:56:01] so let's take a look at what's happening
[00:56:02] and I'll be right back okay so one quick
[00:56:05] fix I think hopefully you probably
[00:56:06] realized this is on line 62 I spelled
[00:56:10] forward wrong but let's continue as uh
[00:56:13] we actually have a bit more to do
[00:56:14] because what was happening and the
[00:56:16] reasoning this wasn't working is because
[00:56:19] the is walking and is false we need to
[00:56:21] now have a way of keeping track of what
[00:56:24] is true and what is false so the first
[00:56:26] thing we'll do is when I'm not clicking
[00:56:28] anything here I'm going to add an else
[00:56:30] statement if I'm not moving forward
[00:56:32] backwards or whatever I'm going to now
[00:56:34] say is oops oh my gosh is walking that's
[00:56:40] not is walking is walking is equal to
[00:56:42] false I'll also say is running is also
[00:56:46] false now what I'm going to do is inside
[00:56:49] of the direction I'm going to check to
[00:56:51] see if
[00:56:53] input dot is action press
[00:56:57] hopefully you can guess I'm going to
[00:56:58] check to see if I'm sprinting I'm also
[00:57:01] going to check to see if is walking is
[00:57:04] true now if it is what I'll do is I'll
[00:57:07] say movement
[00:57:09] speed movement speed is equal to run
[00:57:13] speed and then I'll say is running is
[00:57:17] equal to True next I'll say else is
[00:57:21] walking is equal to true and movement
[00:57:27] speed is equal to walk speed there we go
[00:57:31] now the reason that we need this mostly
[00:57:34] specifically this is because here I was
[00:57:37] I had a movement speed of zero so that's
[00:57:39] why so now what I can do is if I hit
[00:57:41] close when I test this you will now see
[00:57:44] when I hit play I can now move around
[00:57:47] rotate my camera and see that my player
[00:57:49] is moving now I can even hit control to
[00:57:52] aim my player as I'm moving but
[00:57:55] obviously this still looks you know it
[00:57:57] looks okay but it's not perfect because
[00:58:00] well we need animation we have a lot of
[00:58:02] Swords of stuff as well let me actually
[00:58:05] what we'll do is we'll go to the rig
[00:58:06] here and I'm going to hide a few of
[00:58:08] these swords so what I'll do is I'll
[00:58:10] just hide the bone so I'll find just
[00:58:14] minimize
[00:58:16] these and you can of course hide
[00:58:18] whatever you'd like I'm going to show or
[00:58:20] hide everything except for the
[00:58:22] two-handed sword uh so this one hide
[00:58:25] everything above
[00:58:27] it and the
[00:58:29] shield where's the shield this guy right
[00:58:32] here find the shield and there we go so
[00:58:35] this is our two-handed sword I'll keep
[00:58:36] this guy in my hand as I'm going to use
[00:58:38] that as my sword later okay so now I
[00:58:41] actually have a nice equi uh night here
[00:58:45] okay in the next part we'll take a look
[00:58:48] at how we can start animating things all
[00:58:50] right so I'll see you in the next part
[00:58:53] okay so in this next part we're going to
[00:58:54] set up our animation now to get started
[00:58:57] we need to start with our animation tree
[00:58:59] so let's add a new node here called
[00:59:01] animation tree we'll go to the tree root
[00:59:04] on the top right and we will add a state
[00:59:07] machine we'll assign the animation
[00:59:09] player right here by clicking it and we
[00:59:12] can assign the animation player we'll
[00:59:15] hit okay and now what we can do is we
[00:59:17] can start adding some states now in our
[00:59:21] tree route here we'll click this and on
[00:59:23] the bottom you should see animation tree
[00:59:26] let's click into this as this is our
[00:59:27] actual State
[00:59:29] machine next what we want to do is
[00:59:31] rightclick and start adding things now
[00:59:34] we could add a either the animation
[00:59:37] itself or a blend tree now let's add
[00:59:40] some animations and then we go for blent
[00:59:43] tree in the attack so first We'll add a
[00:59:45] idle
[00:59:46] animation and if you're wondering you
[00:59:48] can just click the first letter so for
[00:59:50] example I will give you the idol um but
[00:59:54] now we'll add a blend tree
[00:59:57] and we'll rename this to attack
[01:00:00] one this will click into this and now
[01:00:03] you can see a blend tree now the cool
[01:00:05] part about this and the reason we might
[01:00:07] do this is because now I can add an
[01:00:10] animation and this would work similarly
[01:00:12] and I can connect this and it would
[01:00:14] output that animation but the cool part
[01:00:16] is that I can rightclick go to time
[01:00:19] scale and this will allow me to adjust
[01:00:23] the scale of the time depending on what
[01:00:25] I want want so if I want it to be two
[01:00:27] times as fast I can click two and this
[01:00:30] will animate the attack that I want two
[01:00:33] times as fast now I'm going to find the
[01:00:35] two-handed melee attack spinning and use
[01:00:38] that as my attack we head back here and
[01:00:41] I'm going to put my attack on the
[01:00:43] top just do it like this now I'm going
[01:00:47] to organize the rest of my notes I'm
[01:00:49] going to add a death
[01:00:51] animation a walk
[01:00:53] animation a run animation
[01:00:56] so you can pick whichever one you'd like
[01:00:58] and lastly a jump animation we'll do the
[01:01:03] jump full long do that
[01:01:06] one next I will connect all of these
[01:01:09] with a uh transition now the first thing
[01:01:12] we'll do is connect start to idle we'll
[01:01:14] connect idle to walk walk to run run to
[01:01:18] jump and idle to jump jump back to
[01:01:21] walking and walking back to jump now you
[01:01:25] might notice that all of these are
[01:01:26] automatic and that's okay because right
[01:01:29] now what we're going to do is we're
[01:01:30] going to add conditions for each of
[01:01:32] these now for each of these so the first
[01:01:35] one that we can add um well actually
[01:01:37] first let's finish the transition so
[01:01:39] here we can go from walking to death
[01:01:41] running to death and idle to death we
[01:01:44] should also be able to go from idle to
[01:01:46] attack and attack back to idle now let's
[01:01:49] take a look at what I meant by
[01:01:51] conditions okay now in each of these
[01:01:54] transitions let's take a look at our
[01:01:56] idle first idle to jump in this you can
[01:02:00] see the switch and the advanced the
[01:02:03] switch mode is on immediate the mode is
[01:02:05] automatic now I do want it on automatic
[01:02:09] however I want a condition with this and
[01:02:11] that condition is going to be called is
[01:02:13] in
[01:02:14] air now what I can do is start adding
[01:02:17] these conditions for whatever I want so
[01:02:20] for example the jump we'll actually
[01:02:22] rename this to jump
[01:02:26] from jump to walking I want the advanced
[01:02:29] condition to be is on
[01:02:34] floor from walking to Jump we're going
[01:02:37] to do the same thing as here so I'm
[01:02:39] going to copy this go into my Advan and
[01:02:43] sometimes it doesn't actually copy so
[01:02:44] I'm just going to be having type it in
[01:02:46] okay and we'll just go from each of
[01:02:49] these transitions to jump will be
[01:02:53] is is in here
[01:02:56] from walking to running the condition to
[01:02:59] go from walking to running will be is
[01:03:02] running we'll say is running now we also
[01:03:06] need a condition from running to walking
[01:03:08] and walking back to Idol now the
[01:03:10] condition from running to walking will
[01:03:15] be is not
[01:03:18] running from idle to walking the
[01:03:21] condition will
[01:03:23] be is walking
[01:03:28] now from walking to Idol the condition
[01:03:31] will be is not
[01:03:33] walking is not
[01:03:35] walking now the attack will be a little
[01:03:38] unique so the uh this one from going
[01:03:42] from Attack to idle we're actually going
[01:03:44] to switch it to at end and that's it
[01:03:47] we're not going to have a condition
[01:03:48] we're just going to switch it actually
[01:03:51] sorry I lied we're going to have a
[01:03:52] condition but it's going to be is on
[01:03:54] floor because I should only be able to
[01:03:56] transition if I'm on the floor now from
[01:03:59] idle to attack we're going to actually
[01:04:01] not have a condition for this one and
[01:04:04] we're going to turn off the automatic
[01:04:06] the reason is because we're going to
[01:04:07] transfer or kind of travel from idle to
[01:04:10] attack manually now just make sure that
[01:04:13] in each of these I actually remove um
[01:04:16] some of these and rename it to walk this
[01:04:19] one I'll rename it to run and this one
[01:04:21] I'll rename it to
[01:04:23] death now the condition from all of
[01:04:26] these to death we'll need is going to be
[01:04:29] is dying
[01:04:31] sorry oops need that on auto and then is
[01:04:34] dying like
[01:04:37] this let's say is dying for each of
[01:04:42] these and
[01:04:44] lastly is
[01:04:46] dying all right now that we have our
[01:04:49] animation tree we actually want this to
[01:04:51] work so let's head over to our script
[01:04:53] and pop out the code now do remember
[01:04:55] that here this is where the idle names
[01:04:58] are do make sure that the animations
[01:05:00] that we've added are the same here okay
[01:05:03] so these should look familiar jump
[01:05:05] capital J Attack One death Etc okay so
[01:05:09] do make sure that these are all the
[01:05:11] same otherwise it won't really work
[01:05:14] properly okay so now what we can do is
[01:05:17] in order to make the animation work we
[01:05:20] can actually load our animation Tree on
[01:05:23] the top so what we'll do is at the very
[01:05:25] top I'm going to on ready load that's
[01:05:28] not on ready on ready variable animation
[01:05:32] three I'll say get
[01:05:35] node animation tree we also on ready
[01:05:39] variable playback and this will be equal
[01:05:42] to
[01:05:43] animation uh
[01:05:46] tree do
[01:05:48] get I get
[01:05:52] parameters parameters SL layback
[01:05:56] this is essentially the actual playback
[01:05:59] of the current
[01:06:01] animation so now we just have it as a uh
[01:06:04] variable instead of having to access it
[01:06:06] every time okay so let's take a look on
[01:06:09] the bottom how we would do this at the
[01:06:12] very bottom under the move and slide
[01:06:15] this is actually where I'm going to set
[01:06:17] the conditions whether it's true or not
[01:06:19] to do this all I need to do is access my
[01:06:22] animation tree I'll get the parameters
[01:06:26] the conditions and then the is on floor
[01:06:31] so these are the conditions that I want
[01:06:33] to edit now the variable I'll edit it to
[01:06:36] is going to be this one of course on
[01:06:38] floor now what I can do is I can copy
[01:06:41] paste this a few times and change some
[01:06:43] of these to be what I need the first one
[01:06:46] or the second one will be is in
[01:06:49] air third one will be is
[01:06:53] walking the one after that is is not
[01:06:59] walking this one will be
[01:07:02] is is
[01:07:04] running this one will be is not
[01:07:08] running and lastly is
[01:07:12] dying now for each of these we can kind
[01:07:14] of change them this one will be is not
[01:07:16] on floor this one will be is
[01:07:20] walking this one is is not
[01:07:23] walking this one will be is is running
[01:07:27] you can probably guess this one will be
[01:07:28] is not running uh running running there
[01:07:33] we go and then the last one is dying and
[01:07:36] we don't know need and not is dying
[01:07:38] because well I mean if I'm dying then
[01:07:40] I'm dying right so okay so now let's
[01:07:43] take a look at how I might animate these
[01:07:45] in the actual
[01:07:47] code okay so the first thing I will do
[01:07:50] is I want to uh do the attacking for the
[01:07:53] attacking what I'll do is I'm going to
[01:07:55] scroll up
[01:07:56] right here and I'll do the attacking
[01:07:58] right here now to do this I'll do an
[01:08:02] statement called if attack one uh node
[01:08:06] name is in the
[01:08:08] playback. getet current
[01:08:12] node this will allow me to check to see
[01:08:14] if I'm attacking or not and this is
[01:08:17] where I can just say is attacking is
[01:08:18] equal to True
[01:08:21] otherwise we'll add an else statement
[01:08:23] here otherwise I'll say is attacking is
[01:08:26] equal to false all right now what I can
[01:08:30] do is I can also add a new function at
[01:08:32] the very top right under the is not
[01:08:35] dying called attack one and this will be
[01:08:38] a function I create that will allow me
[01:08:40] to check to see if I'm
[01:08:42] attacking okay so on the bottom we'll
[01:08:45] create a new function by saying Funk one
[01:08:47] back one we'll say inside of here
[01:08:50] if idle node name is in the playback
[01:08:54] node dot get
[01:08:57] current
[01:08:59] node or now this is kind of optional in
[01:09:03] a sense or what I'll do here is I'll
[01:09:07] say we
[01:09:09] go instead of idle I'll also add to see
[01:09:12] if I can walk or if uh if I'm walking or
[01:09:16] if I'm idle now here's another option
[01:09:19] duplicate this and do the running as
[01:09:21] well if you want to be able to attack
[01:09:24] while running or walking this is where
[01:09:26] you would do it but you can check to see
[01:09:29] if you're walking idle or running if
[01:09:32] you're doing any of those things what
[01:09:34] we'll do now is first I need to check to
[01:09:36] see if I'm actually attacking to do that
[01:09:38] I can say is action just
[01:09:40] pressed attack if I attack using my
[01:09:44] mouse I will check to see if I'm not is
[01:09:48] attacking then if I'm not doing any of
[01:09:50] that I will just say playback. travel to
[01:09:56] back one this will allow me to manually
[01:09:59] travel to this node all right so now
[01:10:03] what I can do is hit close on this hit
[01:10:07] play and let's take a look at what we
[01:10:09] have but here you can see when I'm
[01:10:12] walking and running I now play these
[01:10:15] animations there is an issue that it
[01:10:17] doesn't Loop but will change that in
[01:10:19] just a second if I attack and now see
[01:10:22] that I attack and if I jump and now see
[01:10:25] I jump okay now but what about the uh
[01:10:30] looping well that's not too hard in our
[01:10:32] animation here our animation tab let's
[01:10:36] find The Walking a that I'm using and
[01:10:38] make sure it's looped we'll find the
[01:10:40] running make sure it's looped and lastly
[01:10:43] the idle make sure that's looped now
[01:10:47] when I hit
[01:10:49] play you should see my player is playing
[01:10:52] the an idle animation and now I can walk
[01:10:55] with a loop and run infinitely all right
[01:10:59] so here we go here is our player I can
[01:11:01] attack whenever I am running walking or
[01:11:04] whatever and there we go so that is our
[01:11:07] player animation pretty cool I'll see
[01:11:10] you all in the next
[01:11:12] part all right so now that we have our
[01:11:14] player relatively working what we need
[01:11:17] to do next is we need to think about how
[01:11:19] this player is going to interact with
[01:11:21] other things but before we do that need
[01:11:24] those other things right we can't
[01:11:25] interact with a monster we can't kill a
[01:11:27] monster there is no monster so let's
[01:11:30] let's get started with our monster so
[01:11:32] what we'll do here is I'm going to
[01:11:33] create a new folder in our seams
[01:11:37] folder new folder and we'll say
[01:11:41] monsters we're going to create a new
[01:11:43] scene here we're going to create a
[01:11:45] character body 3D as our base this is
[01:11:49] going to be
[01:11:50] our call it our
[01:11:53] skeleton Warrior
[01:11:56] monster we'll add a new node here called
[01:12:00] Collision shape and now we can find
[01:12:03] skeletons we'll find the
[01:12:06] characters we'll use the skeleton
[01:12:09] Warrior drag this out and here we go
[01:12:12] here's our Warrior we can just make this
[01:12:14] local and pop this our actual monster I
[01:12:19] will transform it to
[01:12:21] 0 and here we go here's our monster now
[01:12:25] now the problem is right away we need to
[01:12:27] give it a collision
[01:12:29] shape pop this up a little
[01:12:33] smaller
[01:12:35] go and maybe I'll make it a little
[01:12:37] fatter that's good we'll save this in my
[01:12:40] monster
[01:12:42] scene there we go now I can add this to
[01:12:46] my main scene here I'll find our
[01:12:49] Warrior I'll add this in drag it in like
[01:12:52] so it might take a second like before
[01:12:55] and now we have a monster when I hit
[01:12:58] play I can see that I can kind of
[01:13:00] interact with it in a sense where I can
[01:13:03] kind of run up to it and pack it but
[01:13:06] nothing happens so what we want to do is
[01:13:09] I want to actually add functionality to
[01:13:11] it first what I'll do I'll add a new
[01:13:14] script can use the template it's okay
[01:13:17] I'll make this in my scripts folder make
[01:13:21] a new folder called monsters open and
[01:13:24] create create in here what we'll do is
[01:13:28] we want to now think about our state
[01:13:30] machine and how we're going to actually
[01:13:33] make our monster with its own different
[01:13:36] state
[01:13:37] machine now this guy is going to have uh
[01:13:40] gravity in actual monster so what we can
[01:13:43] do is we can just delete all this input
[01:13:45] the jump input and leave the gravity as
[01:13:48] well we're going to be adding gravity
[01:13:51] now what we can do actually just not
[01:13:54] going to use th we're going to create
[01:13:56] our own uh speed things later we'll
[01:13:59] close this and now when I hit play
[01:14:02] though
[01:14:04] like and when I hit play you'll see that
[01:14:07] my monster does fall to the ground as
[01:14:09] now he has gravity all right that is our
[01:14:12] player setup in the next part we'll take
[01:14:14] a look at how we can start setting up
[01:14:15] our state machines and how State
[01:14:17] machines work uh and you know how we'll
[01:14:20] do this with a
[01:14:21] monster all right so in this we'll be
[01:14:24] taking look at the concept and idea of
[01:14:27] State machines before going into classes
[01:14:29] and custom nodes inside of Gau so the
[01:14:33] general idea of finite State machines
[01:14:36] right so finite State machines now the
[01:14:39] word finite right means the well kind of
[01:14:42] the opposite of infinite right so it's
[01:14:45] something that eventually ends so we
[01:14:47] have a finite State
[01:14:50] machine now let's say for the sake of uh
[01:14:54] a small small example we have the idle
[01:14:57] State this is kind of a circle that
[01:15:00] encompasses things that happen inside of
[01:15:02] the idol state so for example play idle
[01:15:07] right remember that play idle animation
[01:15:09] that would probably go in here right now
[01:15:12] that's one thing now let's say we have
[01:15:14] another state called move right we would
[01:15:18] have well again this the functionality
[01:15:21] of the move state in here right so
[01:15:23] anything that I want to do that should
[01:15:25] involve movement should be inside of
[01:15:28] this so for example well obviously we
[01:15:31] would play the move animation for
[01:15:33] example right now another one that is
[01:15:35] common but we actually won't have is an
[01:15:37] attack State uh this is a very common
[01:15:40] one I'm just going to put it in here
[01:15:41] because uh it's just an
[01:15:43] example now obviously you would play the
[01:15:46] attack animation or do whatever else is
[01:15:48] in there right now the general idea of
[01:15:51] State machines is that we want a kind of
[01:15:54] uh imaginary state right or imaginary
[01:15:58] idea where we hold States so we need
[01:16:01] something to keep track of what state
[01:16:03] we're in and usually that can be used
[01:16:05] using a variable let's say current state
[01:16:08] right so keep some way to keep track of
[01:16:11] what the current state
[01:16:13] is now you can keep track of the current
[01:16:15] state whatever way you want you can use
[01:16:17] a name a string a number it doesn't
[01:16:20] matter it's up to you now what's another
[01:16:23] concept of State machines now this is an
[01:16:25] important one in fact this is probably
[01:16:28] going to take up most of your uh States
[01:16:31] or the most of the code inside of your
[01:16:33] script of your states that is the
[01:16:36] conditions to move from one state to
[01:16:39] another in order to go from idle to move
[01:16:42] I need some sort of condition now
[01:16:44] usually it's an if statement it doesn't
[01:16:46] have to be but usually it is well
[01:16:49] because it's an if statement right now I
[01:16:51] can say if input blah blah blah right
[01:16:55] let's say left right if I move left then
[01:16:59] whoops left like that then I want to
[01:17:01] move to the idle State or the move state
[01:17:03] right well because I'm starting to move
[01:17:06] if I'm moving I should probably go to
[01:17:08] the move state but I need an if
[01:17:10] statement in a condition in the idle
[01:17:13] state that allows me to move to the move
[01:17:17] State now that is important to
[01:17:19] understand you need to understand that
[01:17:21] there is conditions from each state to
[01:17:23] another now from the move State I can go
[01:17:25] to the idle State as well I need
[01:17:27] conditions from the move to the idle I
[01:17:29] also should have some sort of condition
[01:17:31] to go from the idle to the attack now
[01:17:35] ideally you would probably go from
[01:17:37] Attack to idle you would also be able to
[01:17:39] go from move to attack and from Attack
[01:17:41] to move right now the condition from
[01:17:45] Attack to Idol or attack to move is not
[01:17:47] always input right think about it when
[01:17:50] you attack or finish attacking when do
[01:17:51] you go back to Idol well when you finish
[01:17:53] attacking you usually or sometimes I
[01:17:56] would say most of the time it's after
[01:17:58] the attack animation finishes or some
[01:18:01] other condition so those are things to
[01:18:03] think about about when do I want the
[01:18:05] condition to happen when do I want it to
[01:18:07] attack when do I want it to fall stuff
[01:18:09] like that right so these the basic idea
[01:18:12] of finite State machines is essentially
[01:18:15] the idea of having the states themselves
[01:18:18] having the functionality inside of them
[01:18:20] having a way to keep track of what our
[01:18:22] current state is and then we also want a
[01:18:27] condition inside of the states to be
[01:18:29] able to go away from that state to to
[01:18:31] kind of change States right so okay that
[01:18:34] is pretty much it for the finite State
[01:18:36] machine concept video uh I will see you
[01:18:38] all in the next lecture okay so now that
[01:18:41] we understand State machine what I want
[01:18:43] to do is go to my monsters create a new
[01:18:46] folder and call this
[01:18:49] States we'll actually call this one AI
[01:18:53] melee and we'll put our skeleton in here
[01:18:56] as
[01:18:59] well and it might take a second to just
[01:19:02] drag and drop it there we go all right
[01:19:05] now in here we'll create a few new
[01:19:07] scripts the first script we'll have is
[01:19:10] called attack
[01:19:12] State we will duplicate this and call
[01:19:16] this one uh death
[01:19:20] State have one more
[01:19:23] called uh
[01:19:25] ideal
[01:19:26] State quite a few but you know let's do
[01:19:28] these all together so one more time and
[01:19:32] we will create Run
[01:19:35] State duplicate and lastly one more
[01:19:39] called State
[01:19:41] machine uh just State machine actually
[01:19:43] this will be our state machine will kind
[01:19:46] of help us control and hold all these
[01:19:49] states okay so let's take a look at how
[01:19:52] to do this now in each of these states
[01:19:54] what we want to
[01:19:55] do uh we'll open them up first so let's
[01:19:58] open up our Idol let's pop out the
[01:20:00] script uh we'll actually close this for
[01:20:02] now again open them all that way they
[01:20:05] are all open right here and we'll just
[01:20:07] make sure these are all open now in our
[01:20:10] state Machine controller here what I'm
[01:20:12] going to do is I'm going to uh preload
[01:20:14] all our States now to do that what I'll
[01:20:17] do is I'll create a dictionary called
[01:20:19] variable
[01:20:20] States state equal to this curly bracket
[01:20:24] this is
[01:20:25] States we'll have a key called idle here
[01:20:28] will preload our idle script we can do
[01:20:32] that by just typing in Idol State and
[01:20:34] here you can see that I preloaded our
[01:20:37] idle script now alternatively if you
[01:20:40] don't know how to do that you can just
[01:20:42] drag in the idle State path like this
[01:20:44] and it will give you the path another
[01:20:47] way to do this is right click idle a
[01:20:49] script and copy path right here and it
[01:20:52] will copy the path
[01:20:55] all right next what we'll do is we'll
[01:20:57] copy paste this put a comma right here
[01:21:00] copy it
[01:21:02] times uh three times I'll have one
[01:21:04] called
[01:21:07] run one called
[01:21:10] attack and one called Death there we go
[01:21:13] okay and we'll just change all of these
[01:21:15] to the corresponding script so this is
[01:21:17] death this is attack and this is
[01:21:23] run run there we go okay now that we
[01:21:26] have all the scripts we need a helper
[01:21:28] function called change
[01:21:31] State this is a function that will allow
[01:21:34] us to pass through a new state which is
[01:21:37] going to be a
[01:21:39] string make sure that this is spelled
[01:21:41] correctly State and this will allow us
[01:21:44] to change our state now how do we do
[01:21:46] this what we'll do is we're going to say
[01:21:48] get
[01:21:50] child
[01:21:51] count we will see if it's equal to zero
[01:21:54] or not if it's not what we'll do is I
[01:21:57] want to get current child zero and
[01:22:01] Q3 however I don't want to do this if
[01:22:04] I'm in the death state so I'm going to
[01:22:06] see if death not in the get child z.
[01:22:14] name this will essentially check to see
[01:22:17] if the state I'm trying to Q free is
[01:22:20] death I don't want to Q free if I'm
[01:22:22] death I don't want to change States
[01:22:25] now what I'll do I'll say if state has
[01:22:29] uh
[01:22:31] dot has there we go new state then that
[01:22:35] means my dictionary has this state if I
[01:22:38] do I'll say State uh State m is equal to
[01:22:44] State new state. new this will allow me
[01:22:49] to create a new object or a new node
[01:22:52] using this pre-loaded script
[01:22:55] now we'll see why we can do this in just
[01:22:56] a second but for now let's continue we
[01:22:59] can now say State temp is equal do name
[01:23:03] equal to New State we'll set the name of
[01:23:06] that new node equal to the well state
[01:23:08] that we're trying to change into then we
[01:23:11] will just add child State
[01:23:14] M this will allow us to change States so
[01:23:17] this gets rid of our old State and this
[01:23:19] adds our new state okay now in our idle
[01:23:22] State we can get started with our idle
[01:23:23] state that's usually the easiest you can
[01:23:26] see here that we extend node this is a
[01:23:29] script but it extends node now this
[01:23:31] essentially allows us to create a new
[01:23:33] node or a new object using the node as a
[01:23:36] base now what we're going to do here is
[01:23:39] we're going to call or make a new
[01:23:40] variable called AI
[01:23:43] controller and this will essentially
[01:23:46] reference the uh skeleton Warrior script
[01:23:50] so to do this what we'll do is in the
[01:23:52] function uh ready we will say AI
[01:23:56] controller is equal to get parent. get
[01:24:00] parent now the reason we do this twice
[01:24:03] is because here we'll actually add our
[01:24:07] state machine uh we'll actually do that
[01:24:10] by adding a node here we go and we'll
[01:24:12] attach the state machine script and this
[01:24:14] is going to be our state Machine
[01:24:16] controller so let's rename this
[01:24:19] to State machine or state Machine
[01:24:22] controller whatever you'd like now in
[01:24:24] here this will be adding a child in this
[01:24:27] state machine this is where I can now in
[01:24:31] my idle State get parent to get to the
[01:24:33] saate machine and then get parent one
[01:24:35] more time to get to this script this
[01:24:37] will allow me to access the a
[01:24:39] roller okay so now that we have our
[01:24:41] state machine set up we actually need to
[01:24:43] take a step back and set up our
[01:24:45] animation tree so in the next uh video
[01:24:48] FL part we will now set up our animation
[01:24:51] tree okay so to get started with our
[01:24:54] animation we need to add our animation
[01:24:56] tree so let's add an animation tree node
[01:25:00] we'll go to the inspector tab add a DAT
[01:25:03] machine assign the animation player and
[01:25:07] now we head over to the animation tree
[01:25:09] and we will add a few notes and the
[01:25:11] animations will add the first one
[01:25:13] instead of just an idol we're actually
[01:25:15] going to add uh let's just add the death
[01:25:17] FR first so I'll have that kind on the
[01:25:21] top the idol what I'm going to do is I'm
[01:25:23] going to add
[01:25:24] a Sit floor Idol and this will if I play
[01:25:29] it he's just sitting down on the floor
[01:25:33] essentially now the next one I'm going
[01:25:35] to add is a awaken State now this awaken
[01:25:38] state if I search up skeleton or type in
[01:25:41] SSS whatever you'll find the skeleton
[01:25:43] awaken floor long this one will or sorry
[01:25:47] not this
[01:25:49] one we will add the uh awaken
[01:25:56] standing where is that there we go this
[01:25:58] one this one will pop up as if he's
[01:26:01] standing and then we will add a running
[01:26:04] and then an attacking now the attacking
[01:26:06] uh you can kind of pick whichever one
[01:26:07] you'd like I'm going to pick the
[01:26:10] attack
[01:26:12] slice and then I'm going to add one more
[01:26:15] called idle
[01:26:18] combat there we go and now we want to
[01:26:21] add transitions to all of these so from
[01:26:24] awaken back to Idol from standing and
[01:26:27] running back and
[01:26:28] forth Etc and then we also want from
[01:26:32] running to Idol we want from Attack to
[01:26:35] idle then we want from Idol to death and
[01:26:38] from Attack to death we'll also want
[01:26:40] from idle combat to attack and now let's
[01:26:43] rename all these to kind of an easier
[01:26:45] name here this will be idle this will be
[01:26:49] awaken this will be
[01:26:51] run and this will be attack
[01:26:55] this will be we'll leave it as Idle
[01:26:57] combat that makes sense and this one
[01:26:59] we'll just say death now for all of
[01:27:01] these transitions I'm going to take off
[01:27:04] the automatic and just uncheck this for
[01:27:07] each of these transitions because we're
[01:27:09] going to be transitioning from state to
[01:27:12] state through our actual
[01:27:14] code all right so let's make sure that
[01:27:16] we just do this for each of these for
[01:27:19] the Run go to idle combat now from the
[01:27:24] attack right here we'll turn this off
[01:27:27] but from the attack to the idle combat
[01:27:29] we're going to actually leave the
[01:27:30] automatic on and sync it at the end of
[01:27:33] this attack
[01:27:35] animation because I wanted to
[01:27:37] automatically idle combat like this when
[01:27:40] it one every time it finishes attacking
[01:27:42] so that way it's kind of like a cool
[01:27:43] down every time it attacks so it doesn't
[01:27:46] just attack right after attacking right
[01:27:49] so it kind of Waits a little bit and
[01:27:50] then attacks again okay so here we go
[01:27:53] here is our uh animation tree setup and
[01:27:56] now what I need to do is we'll head into
[01:27:59] our scripts and we'll start getting
[01:28:00] things to work all right so next we'll
[01:28:03] go to our actual uh script here for our
[01:28:05] monster and I'm going to start adding
[01:28:08] the variables that we'll need in this
[01:28:09] script to make our cler work so we'll
[01:28:13] add it one by one the first thing we'll
[01:28:15] add is a speed this is going to be a
[01:28:17] float and we'll make it equal speed 1.0
[01:28:20] for now we'll add a on red ready
[01:28:25] variable which will be our state
[01:28:28] controller this will just say get node
[01:28:31] and we'll get access to the uh State
[01:28:34] machine we'll create another variable
[01:28:37] this one will export it and we'll say
[01:28:38] export variable player and this one will
[01:28:41] be a character body 3D this will
[01:28:44] essentially represent a variable as our
[01:28:47] player now to get access to it we'll do
[01:28:49] that in a bit but for now let's just say
[01:28:51] variable Direction and we will set this
[01:28:54] to Vector 3 this is going to be the
[01:28:57] direction from our player or from our s
[01:29:00] the monster to the player so which
[01:29:02] direction is the player we'll create
[01:29:04] another variable called Awakening and
[01:29:08] this is going to be a Boolean we'll set
[01:29:10] it to false by default we create another
[01:29:12] one called attacking a Boolean false
[01:29:17] another one called hell be an INT which
[01:29:19] will make equal to four create a
[01:29:22] variable damage
[01:29:26] intal to two we'll create a variable
[01:29:29] dying will be a Boolean equal to false
[01:29:33] we'll create another variable called
[01:29:35] just
[01:29:36] hit will be a Boolean equal to false all
[01:29:40] right now that we've done all this we're
[01:29:42] going to add a ready function and we're
[01:29:44] going to get access to our state
[01:29:46] controller we're going to change states
[01:29:49] to idle on the ready when our scene
[01:29:52] essentially uh is ready ready and this
[01:29:54] player loads or this monster loads now
[01:29:58] this is all nice and handy and stuff but
[01:30:00] what about our Direction well I want to
[01:30:03] get access to our direction or get the
[01:30:06] direction by saying direction is equal
[01:30:09] to player I'll put it like this player
[01:30:12] do Global
[01:30:15] transform do origin minus self. Global
[01:30:22] transform. origin
[01:30:24] we can also uh
[01:30:27] normalize this
[01:30:29] number now this is cool but this isn't
[01:30:32] something we want to do unless the
[01:30:35] player is valid if the player is not
[01:30:38] valid meaning it doesn't exist then well
[01:30:40] I don't want to do anything right so
[01:30:42] here we'll only get the direction if the
[01:30:44] player is valid all right now let's head
[01:30:47] over to our state machine for sorry idle
[01:30:49] State and we'll take a look at how we
[01:30:51] can get this to work here we can say if
[01:30:54] AI
[01:30:56] controller.
[01:30:58] Awakening then what we'll do is we're
[01:31:00] going to await for that animation to
[01:31:02] finish what I can do is say AI uh
[01:31:06] controller dot get node animation
[01:31:11] three do animation finished so what the
[01:31:15] await function does is it will wait for
[01:31:17] a
[01:31:18] signal a wait essentially stops the code
[01:31:21] and waits for a certain signal to kind
[01:31:24] of happen before
[01:31:26] continuing the signal that we're going
[01:31:27] to wait for is the animation tree
[01:31:30] animation
[01:31:31] finished if I head over to my animation
[01:31:34] tree in the node
[01:31:36] section you will see the animation
[01:31:39] finished signal right
[01:31:40] here okay so that is how that works now
[01:31:44] after this though what I want to now do
[01:31:46] is say AI controller. getet node
[01:31:49] animation 3.get
[01:31:55] parameters SL playback and then I want
[01:31:58] to travel to the idle
[01:32:01] animation now in my physics process
[01:32:04] which I don't have so let me add
[01:32:07] that physics process I will ask if the
[01:32:11] AI controller is valid first then what
[01:32:14] I'll do is if this AI controller is
[01:32:16] valid meaning it exists I have access to
[01:32:18] the monster then I will just AI
[01:32:22] controller veloc
[01:32:24] X is equal to Z similarly I'll just copy
[01:32:28] paste this and change this to Z in the
[01:32:31] idle State all I need to do is just set
[01:32:33] the velocity to zero now what I'm going
[01:32:36] to do is I'm going to copy paste this
[01:32:38] into each of my States so that way I
[01:32:41] have a rough outline to get started with
[01:32:43] in each of these states let's take a
[01:32:45] look at the Run state next as this one
[01:32:47] isn't too complicated and it's not too
[01:32:49] different in our Run state I'm going to
[01:32:51] create a variable though called run and
[01:32:54] this will essentially kind of help me
[01:32:56] run or not in the ready first so I don't
[01:32:59] want to start running until I've
[01:33:01] awakened basically so what I want to do
[01:33:04] first is instead of checking for awaking
[01:33:06] I'm going to check for attacking first
[01:33:09] if I am attacking I will wait for the
[01:33:11] animation finish and what I'll say is AI
[01:33:14] controller. attacking is equal to false
[01:33:18] because after this I've waited for the
[01:33:20] animation to finish and then I stop
[01:33:22] attacking L statement where I'll say run
[01:33:26] is equal to false I'll say AI
[01:33:29] controller. getet node animation tree
[01:33:32] actually I'll just copy paste this right
[01:33:34] here so we'll just copy that and instead
[01:33:37] of traveling to Idol I will travel to
[01:33:40] awaken after that I will say AI
[01:33:43] controller.
[01:33:45] Awakening is equal to
[01:33:48] True after that I can now wait one more
[01:33:51] time but once I start playing the awaken
[01:33:54] I want to wait for this and then uh now
[01:33:57] here I want to once all this is finished
[01:34:00] I want to now say running is equal to uh
[01:34:03] true and then I can set the Awakening to
[01:34:08] false now lastly here I want to travel
[01:34:11] to run because I'm not idle in my run
[01:34:13] animation or my run State I want to you
[01:34:15] know run that would make more sense now
[01:34:17] here I'm going to check for if running
[01:34:20] is also valid because here I'm not only
[01:34:22] just I'm not going to run zero anymore
[01:34:25] I'm going to actually run right so to do
[01:34:27] that I will get my AI controller.
[01:34:29] Direction dox and multiply it by the AI
[01:34:34] controller. speed so this is it this is
[01:34:37] all I need to move my monster towards my
[01:34:40] player now this one I'll copy paste it
[01:34:43] but change it to the Z index and then
[01:34:45] lastly I'm going to get access to my AI
[01:34:47] controller and we're going to use a
[01:34:49] function called look at and this will
[01:34:51] essentially allow me to look at my
[01:34:53] player this is kind of a rotation
[01:34:55] function so I'll pass through the global
[01:35:00] transform. origin then add the AI
[01:35:04] controller.
[01:35:06] Direction all right and then we'll pass
[01:35:08] through the vector 3
[01:35:12] 01 0 like so all right so that's it for
[01:35:17] the Run function hopefully this works
[01:35:19] out
[01:35:22] nicely all right let me just zoom out
[01:35:24] here just a little bit so you can see
[01:35:26] everything and this is the Run State all
[01:35:28] right so now let's take a look at our
[01:35:30] attack State now in the attack State
[01:35:33] this is actually a little easier because
[01:35:35] we don't have to change this because I
[01:35:36] don't want to move when I'm attacking
[01:35:38] now here I can actually keep this
[01:35:40] because if I'm Awakening while I'm
[01:35:42] trying to attack I want to wait now the
[01:35:44] only difference is when I uh after this
[01:35:47] I want to get the a controller and set
[01:35:49] the attacking to true because at this
[01:35:51] point this is probably when I'm going to
[01:35:53] start attacking
[01:35:54] now I want to actually travel to the
[01:35:56] attack node and then I'm actually going
[01:35:58] to go to my run State and copy paste
[01:36:02] this here I want to look at my player
[01:36:06] only in the attack ready obviously this
[01:36:08] is kind of up to you if you want to add
[01:36:10] it in the physics process that's totally
[01:36:12] fine I'm going to add it in the ready
[01:36:14] function so imagine my monster is going
[01:36:16] to only look at me when it's starting to
[01:36:19] attack instead of all the time all right
[01:36:23] now in my death animation this is where
[01:36:25] uh some things are going to get funky so
[01:36:27] here I'm going to say AI controller do
[01:36:30] dying is equal to true and then here all
[01:36:34] I need to do is say death and that's it
[01:36:38] now uh this is pretty much it so now
[01:36:41] what we can do is give this a try we'll
[01:36:44] test this out and see what we
[01:36:46] get okay now if we go to our main scene
[01:36:48] here and we assign the player right here
[01:36:51] on the skeleton sign the player we'll
[01:36:55] actually see if we hit play nothing will
[01:36:57] happen the reason is because we don't
[01:37:01] have a way of changing states but we do
[01:37:03] see that it is working it is playing the
[01:37:05] idle State actually in fact if we go to
[01:37:07] the
[01:37:09] remote we will find under the state
[01:37:11] machine that it is playing
[01:37:13] Idol now in our skeleton we now need
[01:37:17] some sort of condition some automatic
[01:37:19] condition to allow us to detect if I
[01:37:22] want to go into well whichever State I
[01:37:24] need it to be so to do this I'm going to
[01:37:27] add an area 3D I'm going to duplicate it
[01:37:30] and adds a collision shaped 3D both of
[01:37:34] these I'll duplicate this as
[01:37:37] well and put this in here just kind of
[01:37:40] rename it so it's the same now this one
[01:37:42] will be the chase layer
[01:37:46] detection this one will be the attack
[01:37:50] layer
[01:37:51] detection now for both both of these I'm
[01:37:54] going to essentially give an area so
[01:37:56] that it does what I need it to do for
[01:37:59] both of these I'll use a sphere but for
[01:38:01] the chase player I'll make it a little
[01:38:03] bigger here the attack player this needs
[01:38:06] to be a doesn't need to be a cylinder
[01:38:08] but I'll make it a cylinder and this
[01:38:10] essentially will be my attack range this
[01:38:12] will be the range that I want my monster
[01:38:15] to be able to attack in so now what I'm
[01:38:18] going to do is in both of these I'm
[01:38:19] going to go to the chase first and enter
[01:38:22] body entered
[01:38:24] and connect these to my monster I'll do
[01:38:27] this for the body entered and then the
[01:38:29] body exited I will then do this for the
[01:38:32] attack and lastly the
[01:38:35] exited now one more thing that is kind
[01:38:38] of important before we continue here is
[01:38:41] grouping now inside of gdau there is
[01:38:44] something called grouping and this might
[01:38:46] vary depending on your version but uh
[01:38:48] here in good 4.3 all you need to do is
[01:38:51] add a filter here we will add a group
[01:38:54] called Monster and then we'll add one
[01:38:56] more called uh player now we'll uncheck
[01:39:00] the player here in the monster because
[01:39:01] well this isn't a player this is a
[01:39:02] monster in our player though we'll head
[01:39:05] to our our node here and so here we'll
[01:39:09] actually have to add the player here
[01:39:11] again and here we can actually just
[01:39:13] remove the player we don't need
[01:39:17] that and now if we go here we will see
[01:39:20] that these are groups now the cool part
[01:39:23] about this is that inside of these
[01:39:26] signals I can check to see if this body
[01:39:28] is a part of a specific group now I can
[01:39:32] do this essentially let's say the chase
[01:39:34] detection let me zoom in a little
[01:39:36] bit I can say if body is in group Player
[01:39:43] then I can do whatever I want now in all
[01:39:48] of these I don't want to change States
[01:39:50] unless I it's a player and if I'm not
[01:39:53] is dying right if I'm dying then I
[01:39:56] probably shouldn't change States I
[01:39:57] should probably stay in the dying state
[01:40:00] so now what I can do is I can say state
[01:40:02] controller do change
[01:40:05] state to run in this case so if I enter
[01:40:09] the chase state I want to start
[01:40:11] running okay so the is dying is not a
[01:40:14] thing it should be just dying there we
[01:40:15] go all right so now what I can do is
[01:40:18] copy paste this into each of these but
[01:40:21] obviously I'm going to change the state
[01:40:22] to the course responding one now for the
[01:40:25] attack exited or for the chase exited
[01:40:27] this one will go back to idle for the
[01:40:30] attack entered this one will probably go
[01:40:32] to attack and this one is actually
[01:40:34] correct because if I leave the attack
[01:40:37] player detection I want to go back to
[01:40:38] running and Chase the
[01:40:41] player okay now there's one more thing I
[01:40:43] need to do before I kind of test this is
[01:40:46] in our animation tree I'm going to
[01:40:47] actually connect whoops the
[01:40:50] signal signals animation finished
[01:40:53] and I'm going to connect this and in
[01:40:55] here I'm going to check for a few things
[01:40:58] the first thing I'm going to do is I'm
[01:40:59] going to check to see if the
[01:41:02] awaken the word awaken is in the anim
[01:41:05] name if it is what I'll do is I can just
[01:41:08] say Awakening is equal to
[01:41:10] false here I'll add an L if statement
[01:41:13] I'll copy this I'll change this to
[01:41:17] attack and then I'll have an if
[01:41:19] statement saying if the player
[01:41:24] is in the get
[01:41:29] node attack
[01:41:33] detection uh dot get
[01:41:37] overlapping
[01:41:40] bodies
[01:41:42] and not
[01:41:44] dying then this is where I will uh
[01:41:48] change to attack again so if I finished
[01:41:50] one attack so this will kind of allow me
[01:41:52] to so this right here let me kind of
[01:41:55] explain this piece of code will
[01:41:57] essentially allow me to Loop my
[01:41:59] animation for attacking if I finish one
[01:42:02] attack this will check to see if my
[01:42:04] player is still in the current detection
[01:42:07] uh bodies so this will check oh I SP
[01:42:11] wrong if it is in the area attack then I
[01:42:14] will just attack again now I can do that
[01:42:16] by just saying State controller. change
[01:42:20] state to attack
[01:42:23] all right now lastly oops lastly I want
[01:42:26] to say l if uh death so I'll do this
[01:42:29] again but here I'm going to say death
[01:42:32] and if I am playing the death animation
[01:42:34] or I finished playing the death
[01:42:35] animation I'm going to call a function
[01:42:36] Called Death now this function uh
[01:42:40] doesn't exist yet so let's actually
[01:42:41] create it and for now what I'll do is
[01:42:44] I'm actually just going to say self. Q
[01:42:46] free now here is where we'll play
[01:42:49] animations and stuff and blah blah blah
[01:42:51] but uh for now this will just kind of be
[01:42:53] good enough all right now what we'll do
[01:42:55] is close the script and let's hit play
[01:42:57] Let's see what we get let's see if we
[01:42:59] get any crazy bugs that we might have to
[01:43:01] debug
[01:43:02] together okay so here we see that it is
[01:43:05] facing and there's already a few bugs
[01:43:07] and that's okay we can actually fix
[01:43:09] these quite easily but we do see that
[01:43:11] direction is
[01:43:12] working and the attack is working quite
[01:43:15] nicely the only issue is that he's
[01:43:17] facing the wrong way now this is
[01:43:19] actually a very easy fix all I need to
[01:43:22] do is go to my skelet Warrior and I will
[01:43:25] rotate this guy by
[01:43:26] 180 I will also add a weapon because he
[01:43:30] doesn't have a weapon so let's actually
[01:43:32] go to our assets here in our skeletons
[01:43:35] go to fvx and we'll find a skeleton
[01:43:39] blade and in our rig here I might
[01:43:42] actually need to add a new bone because
[01:43:45] here we have a bone helmet but we don't
[01:43:47] have a bone for our hand so what I'm
[01:43:49] going to do is I'm going to search up
[01:43:51] bone attachment which is bone and we
[01:43:54] should find a bone attachment 3D I'll
[01:43:57] add this I'll select the hand slot right
[01:44:01] you can do left if you'd like but now
[01:44:02] you can see that the hand slot is kind
[01:44:04] of on our hand now I can take my bone my
[01:44:08] skeleton blade here and I'll just make
[01:44:10] this local and drag out the dash I
[01:44:14] need and now I can reset its position
[01:44:17] and rotation 3 0 like so and now if I
[01:44:21] hit play on on one of my
[01:44:24] animations I play the attack you'll see
[01:44:29] he kind of plays the attack but it's a
[01:44:30] little funky that might be because I
[01:44:32] need to rotate the blade I do so I need
[01:44:37] to rotate the blade Itself by 180 or
[01:44:41] just
[01:44:41] 180 and now when I hit play one more
[01:44:47] time okay so it kind of still looks a
[01:44:50] little funky let's make sure that this
[01:44:52] is the right hand
[01:44:54] slot B3
[01:44:58] yeah okay so what we'll do is I'm going
[01:45:01] to play the T
[01:45:03] pose find the T pose here oops and this
[01:45:08] guy should be looking this way so we'll
[01:45:10] get this rotate like
[01:45:14] so so this will probably
[01:45:17] be90 and- 180 so whatever your rotation
[01:45:21] is it should be facing this way outside
[01:45:24] of the T pose now let's try one more
[01:45:26] time go to the animation tree and there
[01:45:29] we go now we have a nice smooth attack
[01:45:31] all right let's hit play and see what we
[01:45:36] get okay so here we go he's chasing us
[01:45:39] there's no Loop but we can change that
[01:45:41] in a second but we do see that the
[01:45:43] attack does uh actually Loop which is
[01:45:46] nice now there is few issues right so
[01:45:49] the first one is in the walking or I
[01:45:52] believe in the running
[01:45:54] actually where is the running we go
[01:45:57] running a we'll Loop that now another
[01:46:00] one is the idol which is going to be the
[01:46:02] sit floor idle I think is this one
[01:46:07] right let's take a look so this one
[01:46:11] doesn't need to Loop this one will need
[01:46:13] to Loop so the FL sit four idle and
[01:46:16] running a that's good all right so yeah
[01:46:19] there we go there is our monster so it
[01:46:21] should now Loop if we pick play one one
[01:46:23] more
[01:46:26] time here we go so he's running and he's
[01:46:28] looping if I leave he goes to the idle
[01:46:32] animation now one thing that I like to
[01:46:35] do is inside of our animation tree I'm
[01:46:38] going to actually blend uh some of the
[01:46:42] animations now what does that look like
[01:46:44] well in our run to Idol what I can do
[01:46:48] here is I can change the X fade time I'm
[01:46:52] going to change it to 2 and this will
[01:46:55] allow us to have a smoother animation
[01:46:57] between our transitions now I'll do this
[01:47:00] for all of them
[01:47:03] 0.2 so let me just make sure that all of
[01:47:05] these are
[01:47:06] 0.2 and you can of course do these for
[01:47:09] all of them it's kind of optional but of
[01:47:12] course if you don't it might look a
[01:47:13] little chunky so it is up to you whether
[01:47:16] or not you want to try this or if you
[01:47:18] want to try something else of course you
[01:47:19] can also try the xade perve that is also
[01:47:22] a nice thing but it's more so just kind
[01:47:25] of how how fast it curves into this uh
[01:47:28] time now if we try one more time though
[01:47:31] should see it'll do that and then it'll
[01:47:34] kind of sit back down right
[01:47:36] away yeah so there we go it doesn't kind
[01:47:38] of just chunk back down to the idle it
[01:47:41] kind of Fades back into the idle
[01:47:42] animation all right so there we go
[01:47:44] there's our monster it works pretty
[01:47:46] nicely now in the next part we'll need
[01:47:48] need to now actually add some
[01:47:50] functionality to hit it we need to hit
[01:47:53] the monster and the monster needs to be
[01:47:55] able to hit us we'll do this in the next
[01:47:58] section right so now that we have the
[01:48:00] player and the skeleton working all we
[01:48:02] need to do now is well make them
[01:48:04] interact with each other and this isn't
[01:48:06] actually that hard all we need to do is
[01:48:09] add some things into each scene so the
[01:48:11] things We'll add the general idea of
[01:48:13] this is we're going to add some sort of
[01:48:15] detection area in well specifically The
[01:48:18] Sword and then every time I attack I'll
[01:48:20] be able to detect whether or not I can
[01:48:23] hit the other monster and if I do I'll
[01:48:26] send kind of a signal that will allow me
[01:48:28] to hit the other person so let's start
[01:48:31] with the monster to start what we'll do
[01:48:34] is we need to find the right hand now
[01:48:37] usually you would do this in a sword now
[01:48:40] this could work and you could you're
[01:48:42] more than welcome to add uh the area to
[01:48:45] this sword specifically but a better way
[01:48:47] to do this is if we add a new bone
[01:48:49] attachment just like we did with the
[01:48:51] monster we can attach a right hand slot
[01:48:54] right and we can just add the area to
[01:48:56] this right because this will apply for
[01:48:58] any sword because in the future what if
[01:49:01] you want to hi this and show this
[01:49:03] whatever you may want right it'll be
[01:49:06] kind of more dynamic in this sense so
[01:49:08] what we can do is we can rename this to
[01:49:10] right hand
[01:49:13] slot we will add a new uh node called
[01:49:16] area 3D this is going to be our detector
[01:49:19] we add a collision shape and now we need
[01:49:22] to set the Collision shape I we'll put a
[01:49:25] capsule we need to zoom in here and
[01:49:28] essentially make this the same size as
[01:49:31] the sword so we'll just kind of zoom out
[01:49:34] just a little bit like
[01:49:35] this and there we go now what we can do
[01:49:38] is rename this to damage
[01:49:42] detector and there we go that is our uh
[01:49:45] sword right so now when I attack so if I
[01:49:49] go to my animation tree and throw this I
[01:49:52] mean it's a little fast but you can see
[01:49:54] that the area 2D or 3D sorry follows the
[01:49:57] sword so every time I play well I gu I
[01:49:59] would have to play idol
[01:50:01] first yeah I mean even honestly even in
[01:50:03] the idol you can see that it's following
[01:50:05] the idol right as I walk it's following
[01:50:07] the sword so this is perfect so this is
[01:50:09] exactly what we want now what we can do
[01:50:12] is uh reference or connect the signal
[01:50:16] will connect the body entered signal to
[01:50:18] the player now in here you might recall
[01:50:22] that we cre grouping so this is where we
[01:50:24] can first check to see in fact actually
[01:50:27] this is where I want you to pause the
[01:50:29] video and try seeing if you can detect
[01:50:32] if this body that is entering this area
[01:50:34] is a monster or not see if you can
[01:50:36] figure it out using a similar uh thing
[01:50:39] that we used before so to do this
[01:50:41] hopefully tried it yourself first what
[01:50:43] we need to do is say if body is in group
[01:50:48] monster because if you recall from
[01:50:50] before in our monster here
[01:50:53] we have created a group called Monster
[01:50:56] so here now in our player back in our
[01:50:59] script again we can simply check to see
[01:51:01] if it's in that group and if it is that
[01:51:03] means well I'm hitting a monster and if
[01:51:06] I am what do I want to do well I
[01:51:08] actually want to just call hit on it so
[01:51:11] in order to do this the monster needs a
[01:51:14] function called Hit first otherwise it
[01:51:17] doesn't really make sense like how can I
[01:51:18] hit it without having a function inside
[01:51:21] of it now I could just Q free so for
[01:51:23] example I could just do free like this
[01:51:25] and this could totally work this would
[01:51:26] just destroy the monster however I'm
[01:51:29] going to call a function called Hit and
[01:51:31] the cool part about this is that I can
[01:51:33] now put in a amount of damage in like
[01:51:36] like one or two right so if I want to do
[01:51:38] a certain amount of damage to its Health
[01:51:40] this is where I can do it okay now one
[01:51:43] more thing we'll do though is in the
[01:51:45] body is in group whatever what we want
[01:51:47] to also check for is is attacking I
[01:51:51] don't want to damage the monster if I'm
[01:51:53] not attacking because let's say I'm just
[01:51:56] walking right my player's walking and I
[01:51:59] just walk past a monster and the monster
[01:52:01] enters this area obviously that's not
[01:52:03] very good I don't want that that's a
[01:52:05] pretty terrible interaction right I
[01:52:08] don't want that in my game I only want
[01:52:09] to interact uh when I'm attacking now
[01:52:12] there is actually a better way to do
[01:52:14] this um but I'll show you that in the
[01:52:15] monster so it's going to be kind of two
[01:52:17] different ways to detect whether or not
[01:52:19] I'm attacking or not and this will be a
[01:52:21] nice way to
[01:52:23] for you to kind of learn different ways
[01:52:25] of doing something similar that we need
[01:52:27] to achieve so let's head back to our
[01:52:29] script and what we need to do now is now
[01:52:33] that we've created this hit function or
[01:52:35] called this hit function we need to
[01:52:37] create it we don't have a hit function
[01:52:39] in our monster so in this body right
[01:52:42] this is the body that we would be
[01:52:43] calling but I mean I'm not going to ask
[01:52:45] you do you guys see a h function I don't
[01:52:47] see a h function here so what we need to
[01:52:50] do is create it we'll create a h
[01:52:52] function will pass through an amount of
[01:52:54] damage that will be an integer and then
[01:52:57] all I need to do is say health minus
[01:53:00] equal damage and then we can check to
[01:53:03] see if the health is less than zero if
[01:53:06] it is we'll say self. Q free now here's
[01:53:10] the issue that well the main issue is Q
[01:53:13] free doesn't exactly do what I want
[01:53:16] right I don't want to just Q3 you
[01:53:18] probably guessed it I want to change
[01:53:19] states to death so all I need to do is
[01:53:22] change states to death because we should
[01:53:24] already have this set up okay so now
[01:53:27] that we have our hit
[01:53:28] function um all we another thing I want
[01:53:31] to do is I want to start detecting the
[01:53:33] just hit function what this means is if
[01:53:36] I just got
[01:53:37] hit I actually don't want to do any of
[01:53:40] this so I will only reduce my damage
[01:53:43] I'll only die etc etc if I wasn't just
[01:53:46] hit now this is a variable that we
[01:53:49] created uh kind of a while ago and this
[01:53:51] will essentially allow to detect if I
[01:53:53] was just hit or not now here's the
[01:53:55] kicker is I want to set this to True
[01:53:58] inside of here just hit is equal to true
[01:54:02] but here's another issue is how do I set
[01:54:04] it to false well what we're going to do
[01:54:06] is I'm going to close our script here
[01:54:08] head to our Warrior and I'm going to add
[01:54:10] a new node called the timer this timer
[01:54:14] is going to allow us to essentially
[01:54:16] start when I just get hit and I'll
[01:54:19] connect a signal called Timeout on our
[01:54:22] monster
[01:54:23] here and every time it times out I will
[01:54:26] set the just hit to
[01:54:29] false now the issue is oops false not
[01:54:33] the issue but how do we start this timer
[01:54:35] right because this timer doesn't just
[01:54:36] start like magically we need to start it
[01:54:38] so how do we do that well it's pretty
[01:54:40] easy we just say get node just hit it's
[01:54:43] the timer that we just created and then
[01:54:45] just start it this will automatically
[01:54:48] start our timer well not automatically
[01:54:50] but it'll start our timer and yeah so
[01:54:52] that'll allow us to actually do that
[01:54:55] okay so now what do we need to do well
[01:54:58] uh in our just hit function or sorry our
[01:55:01] hit function we now need to uh not need
[01:55:05] to but one other thing that we can add
[01:55:07] is a knockback this is something that I
[01:55:10] like to do in a lot of my games um it's
[01:55:12] just a very very simple way of adding a
[01:55:14] knockback and that is by something doing
[01:55:16] something called tweening tweening is a
[01:55:19] very simplistic way of animating so
[01:55:22] think of how we might want to animate a
[01:55:24] knockback well one way we could do it is
[01:55:27] doing it through the animation player
[01:55:29] right if we go into our animation player
[01:55:31] if you understand how it works if you
[01:55:33] don't that's okay the basic idea of it
[01:55:35] is that there's something called key
[01:55:37] frames and essentially and we'll
[01:55:39] actually use this for a monster later in
[01:55:40] the next part uh is see let's go to our
[01:55:45] skeleton monster we have keys here and I
[01:55:47] can key one of these and it will kind of
[01:55:50] put that position in this key frame and
[01:55:52] then if I key another one at another
[01:55:54] position it will kind of animate between
[01:55:56] those two frames now I don't want to
[01:55:59] give an example because I'm actually
[01:56:00] going to give an example a little later
[01:56:02] but the basic idea of tweening is that
[01:56:04] it's done in code it's the same thing
[01:56:06] but just done in code so let's take a
[01:56:08] look at how we can do this first I need
[01:56:10] to create a tween you know just a fun
[01:56:13] fact G in G 3 and previous tweening used
[01:56:17] to be an actual node but they removed it
[01:56:19] and now we only can create it through
[01:56:21] code but that's okay okay we can still
[01:56:22] utilize it quite nicely so here we'll
[01:56:25] just say twe property and the property
[01:56:29] that we want to twe first we'll look at
[01:56:31] the object well the object is going to
[01:56:33] be our self okay now what property do we
[01:56:36] want to adjust well I want to adjust the
[01:56:39] uh Global position what I essentially
[01:56:42] want to do is take our Global position
[01:56:44] and then the final value will be its
[01:56:46] Global position
[01:56:49] minus the direction divided by
[01:56:53] 1.5 this essentially will act as a
[01:56:56] knockback now I want to do this over a
[01:56:59] period
[01:57:00] of2 and this is going to basically be
[01:57:02] how long this tween takes so 0 2 seconds
[01:57:05] is very quickly right you'll not really
[01:57:08] not notice it but it's it's just very
[01:57:10] quick okay now that we have our hit
[01:57:13] function Let's test it out let's see if
[01:57:14] this works so let's take a look first at
[01:57:16] our health here we have four health and
[01:57:19] we should be doing in our player script
[01:57:21] two damage it should take two hits to
[01:57:23] kill our monster let's take a
[01:57:27] look play we go and our Monster's
[01:57:31] chasing us and you can even see that
[01:57:33] there's a little knock back and
[01:57:35] eventually it dies and we even saw that
[01:57:38] that second attack didn't go through
[01:57:40] because it just got hit so I couldn't it
[01:57:42] was invulnerable essentially I couldn't
[01:57:44] keep hitting it I wasn't allowed so
[01:57:46] there we go that's our know detection
[01:57:48] that's our monster attacking that's
[01:57:50] pretty neat in the next part we'll take
[01:57:52] a look at how we can now do the opposite
[01:57:54] I would suggest actually with this next
[01:57:56] part you try it on your own first try
[01:57:59] making it doing exactly what we just did
[01:58:01] adding the area 3D to the monster and
[01:58:04] then allowing it to hit the player
[01:58:05] adding a hit function inside the player
[01:58:07] Etc but that's what we'll do in the next
[01:58:09] part so we'll be able to have the
[01:58:11] monster now attack the
[01:58:13] player right so in our next part like I
[01:58:16] said um we now need to make it so our
[01:58:19] monster can hit our player now to do
[01:58:21] this actually a little not easier but
[01:58:24] per say but we already have our bone
[01:58:27] attachment here and I'm going to rename
[01:58:28] this to right and Slot just like I did
[01:58:31] for the player and I'll attach an area
[01:58:34] 3D again and similarly a collision shape
[01:58:38] now I'm going to go to my animation
[01:58:39] player and select the key pose just so
[01:58:42] it's a little easier to add it or you
[01:58:44] know adjust the sword here I'll add a
[01:58:47] cylinder capsule make it much smaller as
[01:58:49] you can tell make it skinnier
[01:58:52] order and there we go here's our sword I
[01:58:55] might actually extend it a little
[01:58:57] outwards just so it can actually hit the
[01:58:59] player okay so now what we can do is you
[01:59:03] need to make sure and me uh we need to
[01:59:06] make sure that we take a look at which
[01:59:08] attack we're using here I'm using the
[01:59:09] two-handed melee attack slice so now
[01:59:12] what we'll do is we'll head into our
[01:59:15] animation player with animation on the
[01:59:17] bottom we will head into the
[01:59:20] two-handed attack slice one that we're
[01:59:22] using now what I want to do is I want to
[01:59:26] turn off the animation tree so that way
[01:59:28] I can look at my animation uh for this
[01:59:31] animation as it actually happens now
[01:59:34] here's the thing I want this area 3D
[01:59:37] only be uh disabled and enabled whenever
[01:59:43] this Frame is kind of like right here
[01:59:46] like in between the attacks so right
[01:59:48] maybe right here and in between here
[01:59:51] after that I want want to disable it so
[01:59:53] what do we do well this is actually
[01:59:55] quite easy this is the key part that I
[01:59:56] was talking about so here what I can do
[01:59:59] is make sure that it's disabled is off
[02:00:02] I'll key here like so and then right
[02:00:05] here I'll check this on and then key it
[02:00:09] again now if we scroll all the way to
[02:00:11] the bottom you will now see this new
[02:00:13] Collision shape 3D with enabled and
[02:00:16] disabled so this will essentially enable
[02:00:19] the Collision shape or yeah Collision
[02:00:21] shape and then disable it after a
[02:00:23] certain frame now here's the kicker is
[02:00:26] we want to find that reset track and
[02:00:28] make sure that this is enabled so by
[02:00:32] default this should be enabled right so
[02:00:34] this will automatically kind of happen
[02:00:37] like this is the reset this is what will
[02:00:39] reset every time I play the game kind of
[02:00:41] it's almost like a ready
[02:00:43] function now let's rename this similarly
[02:00:46] to damage
[02:00:48] detector I will go into this area 3D add
[02:00:52] it into our body entered and connect so
[02:00:55] just kind of uh an ad if you recall from
[02:00:59] our last part uh like just 10 minutes
[02:01:01] ago this is how uh that animation player
[02:01:04] that's another way of detecting if I'm
[02:01:06] currently attacking or not because here
[02:01:08] I I could check for the state so let me
[02:01:11] actually pop this out I could check for
[02:01:13] the state controller I could just check
[02:01:15] for the name or whatever see if I'm in
[02:01:17] the attack State and that could work
[02:01:19] that's totally fine but this is kind of
[02:01:21] a more Accurate Way of detecting for a
[02:01:24] specific frame it's it's just a bit more
[02:01:27] accurate I would say okay now here in
[02:01:30] the damage detector this is from the
[02:01:32] monsters to the player but as a
[02:01:34] reference I can actually just copy paste
[02:01:36] this into here and change this to player
[02:01:40] and then remove this I want I'm not
[02:01:42] going to need that now for the body do
[02:01:44] hit instead of two you recall I already
[02:01:47] have this damage right here so I'll just
[02:01:49] pass that through now I can always
[02:01:51] change the damage that I want uh you
[02:01:53] know to whatever I
[02:01:55] want okay so now on the bottom uh now if
[02:01:59] you recall you know we have this hit
[02:02:00] function we're calling it but again we
[02:02:03] don't have a hit function inside the
[02:02:04] player so let's create it um in fact
[02:02:06] actually as a good reference to create
[02:02:08] it I'll just copy paste this copy this
[02:02:11] here and now we have a good amount of
[02:02:13] stuff now of course we don't have health
[02:02:15] I don't have damage or actually we do
[02:02:17] have damage um and we were going to add
[02:02:20] our I was going to add the health um a
[02:02:22] global variable but for now we can just
[02:02:24] add a health variable here as int equals
[02:02:28] say
[02:02:29] five and then uh instead of State
[02:02:32] Controller here I'll say self. do free
[02:02:36] for
[02:02:37] now okay um actually we could just play
[02:02:41] the death animation so why don't we just
[02:02:42] do that actually so instead of uh self
[02:02:46] talk Q free what we can do is we can
[02:02:48] actually say is
[02:02:49] dying oops is is dying is equal to true
[02:02:54] and then uh here we'll just copy this
[02:02:57] right here and instead of traveling to
[02:02:59] attack node one the attack to the death
[02:03:02] node name here we'll just travel to the
[02:03:04] death now here's the thing is after my
[02:03:07] death animation I want to die I want to
[02:03:10] like end the game and little later we'll
[02:03:12] add a game over overlay but for now what
[02:03:15] we can do is I'll close the script and
[02:03:17] in my animation
[02:03:19] tree here I've already connected uh oops
[02:03:23] in my player here in my animation tree I
[02:03:25] don't have this so I'll connect the
[02:03:26] animation finished connect it pop this
[02:03:30] out and now I can check for the death
[02:03:32] animation see if I just played the death
[02:03:35] animation I'll say if death in random
[02:03:38] name then what I'll do is I'll say self.
[02:03:41] Q free this will allow me to just Q free
[02:03:44] and in the future if we ever want to add
[02:03:46] a game over overlay we'll just add it
[02:03:48] here okay all right so here we have the
[02:03:53] uhing however this might not work
[02:03:56] because we have a
[02:03:59] direction we have a direction this
[02:04:01] direction is facing wherever I am which
[02:04:05] I think will work fine okay so we have
[02:04:08] the just hit being started but I don't
[02:04:10] have that timer so we need to add it but
[02:04:13] let's add our new
[02:04:15] timer our player here and we'll rename
[02:04:18] this to just hit okay so we should be
[02:04:21] able to to give this a
[02:04:26] try Okay so let's see if we can oh okay
[02:04:30] so our monster needs to turn on the
[02:04:32] animation tree
[02:04:33] again go back to the
[02:04:35] inspector it close the
[02:04:39] game okay back to Output here we
[02:04:47] go all right so here's our monster
[02:04:49] should be able to attack us now and even
[02:04:52] knock
[02:04:54] back all right so it seems that I'm
[02:04:58] Invincible now because I never connected
[02:05:01] the just hit uh timeout so that would
[02:05:03] make sense I would probably need to be
[02:05:06] able to turn just hit to false so here I
[02:05:09] turned it to true and then I never
[02:05:10] turned it to false again so that would
[02:05:12] make sense all right so let's H play one
[02:05:15] more time test this
[02:05:19] out so he's waking up going to hit
[02:05:24] all right cool so there we go and then
[02:05:26] eventually I die and then IQ free and
[02:05:29] the reason this is happening is because
[02:05:30] I don't have a camera 3D anymore because
[02:05:32] if you remember camera 3D is in our
[02:05:35] player and we already destroyed our
[02:05:36] player so uh that's probably not the
[02:05:38] best way to do it but it works out quite
[02:05:40] nicely so in the future we'll add a game
[02:05:42] over overlay and it will be able to
[02:05:44] restart the level and stuff this is
[02:05:46] pretty good so far so I'll see you in
[02:05:48] the next part all right now that we've
[02:05:51] pretty much completed the player and
[02:05:53] monster we now want to head into our
[02:05:55] assets and I'm going to now show you how
[02:05:57] to create this custom theme because
[02:06:00] we're going to kind of uh I'm actually
[02:06:01] going to close these guys we're going to
[02:06:03] now head into creating GUI so for
[02:06:07] example um we'll actually create a
[02:06:09] canvas item canvas layer as our base
[02:06:12] here I'll save this as GUI and I'll put
[02:06:15] this in my scenes in my player and save
[02:06:19] and just kind of show you what this
[02:06:20] might look like if I create a
[02:06:23] panel you will see here this is the
[02:06:25] default theme of gdau now this default
[02:06:28] theme if I pop this into the themes
[02:06:31] right
[02:06:32] here you will see it turns into this
[02:06:34] nice pretty thing now in order to create
[02:06:37] this though what we'll do is create a
[02:06:39] new resource search up
[02:06:42] theme save and we can create default
[02:06:47] 2.0 of course if you don't want to do
[02:06:49] this you can of course skip it I've
[02:06:51] already set
[02:06:52] all the default themes you'll need but I
[02:06:54] want to show you how to do this uh you
[02:06:56] know ourselves now okay the font very
[02:06:58] easy just drag and drop the font into
[02:07:00] the default font done super simple now
[02:07:04] what about the rest because here you can
[02:07:06] see in this default theme we have button
[02:07:08] panel progress bar but here I have
[02:07:10] nothing well I go to manage items go to
[02:07:13] import items and we can now import the
[02:07:16] things I want I'm going to import panel
[02:07:18] I'll find the panel
[02:07:21] I'll find
[02:07:23] button I want the button
[02:07:26] here and let's import these first close
[02:07:30] C okay and I forgot the last one
[02:07:33] progress bar right okay we'll go to the
[02:07:35] thing over here manage items and
[02:07:40] progress progress bar there we go import
[02:07:45] selected and now we can see uh in my
[02:07:47] edit items you can even see it here but
[02:07:49] I'll close Okay and now we have our our
[02:07:53] things that I want to give now okay
[02:07:55] we'll start one by one we'll start with
[02:07:57] the panel as this one's probably the
[02:07:58] easiest we'll go to the Styles we're
[02:08:01] going to select this down button and
[02:08:02] select the texture we'll take our UI big
[02:08:06] piece and drop it nowhere because I need
[02:08:08] to click this first then I'll drag it
[02:08:11] into the texture now you can see in the
[02:08:13] background I have this texture now I'm
[02:08:16] going to go to the sub region edit
[02:08:18] region and now I'm going to select this
[02:08:21] guy
[02:08:23] now I could also try pixel
[02:08:26] snap sometimes it's not perfect but it's
[02:08:29] not too bad here we go now I can move
[02:08:32] these dotted lines be kind of below
[02:08:35] where I want it to be and essentially
[02:08:37] what this does is let me actually move
[02:08:39] all these first and it might be easier
[02:08:40] to explain
[02:08:43] it it will use the middle of this as the
[02:08:47] middle of the entire panel so this side
[02:08:51] corner will always be consistent so now
[02:08:54] when I close this and I add a panel here
[02:08:58] more
[02:09:00] time and I set this theme as the theme
[02:09:03] 2.0 you will see if I zoom in here we
[02:09:06] have these dots always no matter how big
[02:09:09] the panel is so essentially everything
[02:09:11] else gets stretched that is kind of the
[02:09:14] advantage you can see that these Corners
[02:09:15] don't get stretched they get uh they
[02:09:18] stay the same size okay so that's the
[02:09:20] panel finished we'll close the panel
[02:09:22] here in our custom theme let's H over to
[02:09:24] the styles of our button the buttons are
[02:09:26] going to be a little more difficult but
[02:09:29] uh just more of a drag I would say let's
[02:09:31] head over to the normal one because that
[02:09:33] one's probably the easiest but we'll
[02:09:35] drag in the UI piece go to sub region
[02:09:38] edit region zoom out and here we can
[02:09:41] find our buttons so this one is going to
[02:09:42] be our normal button this is pressed and
[02:09:44] this is hover for Focus as well so let's
[02:09:48] just do the normal first so we'll drag
[02:09:51] this
[02:09:52] and I can just down just a little bit
[02:09:55] and I can move the dotted line in the
[02:09:58] middle like
[02:09:59] so and just bring this up a tiny
[02:10:06] bit all right we'll close and now if I
[02:10:09] add a button it would should look like
[02:10:11] this but let's finish the rest so what
[02:10:12] I'll do is I'm going to drag this guy
[02:10:15] into the rest of them now here's the
[02:10:17] thing though is that if I edit one of
[02:10:19] these it will edit the rest you're more
[02:10:21] than welcome to give it a try but I'm
[02:10:23] just going to make unique on all of
[02:10:24] these so that way I don't mess anything
[02:10:27] up do make sure that you just make each
[02:10:29] of these unique right now for the
[02:10:32] Pressed we'll go to the sub region and
[02:10:34] select the
[02:10:38] Pressed here we go looks pretty good
[02:10:42] I'll just move
[02:10:43] this I'll just leave it there that's
[02:10:45] fine close and we'll go to the
[02:10:49] hover sub region
[02:10:52] edit
[02:10:53] region and hover we can select this
[02:11:02] one we go and just select the entire
[02:11:06] thing make sure that the inside is kind
[02:11:09] of what you want close and we'll go to
[02:11:12] the focus the focus we can leave as the
[02:11:15] default and then the disabled uh we'll
[02:11:18] select the Pressed one for the disabled
[02:11:21] if we want ever disable the buttons
[02:11:23] which we actually will at for our item
[02:11:27] or our inventory system kind of then
[02:11:29] we'll select this as our disabled okay
[02:11:32] so that's our buttons and lastly the
[02:11:34] progress bar this one's going to be a
[02:11:35] little easier because if you actually
[02:11:37] notice in the default one that I gave
[02:11:39] you in here the background is empty and
[02:11:42] there's a good reason for this but the
[02:11:44] fill is going to be our texture so let's
[02:11:45] do this for our um guy here so
[02:11:48] background I'll set this to empty and
[02:11:50] then the fill I'll set it to texture and
[02:11:53] pop in the texture that I want I'll go
[02:11:56] to sub region edit region and I've
[02:12:00] created this guy so I've edited it I've
[02:12:03] basically just moved these all together
[02:12:04] because that's what we need so here we
[02:12:06] go select the
[02:12:09] red like
[02:12:11] this uh I think it's supposed to be like
[02:12:13] that there we go and I'll just move this
[02:12:15] guy one corner like
[02:12:17] this that's not what I wanted to do I
[02:12:19] want to move this guy up and this guy
[02:12:22] down like so I'll use this as my stretch
[02:12:24] essentially okay so there we go there's
[02:12:26] our theme completed now to actually load
[02:12:29] this into our game I need to go to
[02:12:30] Project
[02:12:31] settings go to General search up
[02:12:35] theme go to theme and add in our custom
[02:12:39] uh theme
[02:12:40] here so here I'll just add in my uh
[02:12:43] default 2.0 or you can add the default
[02:12:46] and I'll save and restart and I'll see
[02:12:48] you in the next
[02:12:50] part right so our next step is to
[02:12:52] actually create a game over overlay this
[02:12:55] will be a little easier so we'll start
[02:12:56] with this as our kind of initial GUI set
[02:12:59] up so to do this we'll create a new
[02:13:01] scene and this new node will be a canvas
[02:13:04] layer base now I know I haven't
[02:13:06] explained what a canvas layer is but
[02:13:07] let's kind of take a look at what it is
[02:13:09] and what it does so to do this we'll add
[02:13:12] a panel and we'll increase this panel
[02:13:15] here and I'm going to actually turn on
[02:13:17] this grid snap and this will just allow
[02:13:20] me to more accur accurately assess how
[02:13:24] big I want this to be so I want it to be
[02:13:25] this big now inside of this inside of my
[02:13:28] panel specifically I'll add a label and
[02:13:31] I'll add a
[02:13:33] button okay so this button let me make
[02:13:36] it a little bigger here me just do it
[02:13:38] like so I'll type in
[02:13:41] retry put this kind of in the middle and
[02:13:44] then the label I'll make it a little
[02:13:46] bigger here and I'll type in game over
[02:13:51] try again now if I want this to be
[02:13:53] bigger that's easy all I need to do is
[02:13:56] go to the theme overrides you could of
[02:13:58] course uh edit the actual theme in here
[02:14:01] right I believe you should be able to
[02:14:03] edit the default size but I'm not going
[02:14:04] to do that I usually like to edit the
[02:14:06] size manually every time I add a label
[02:14:10] um the font size here I can actually
[02:14:12] just overwrite it and make it much
[02:14:13] bigger as I want it to be now what I can
[02:14:15] do is I can just Center it in the
[02:14:17] alignment there we go I can maybe just
[02:14:20] press enter so that way it says game
[02:14:22] over try again on two lines like so and
[02:14:24] even more what's cool about this is I
[02:14:26] can go to the constants and give it line
[02:14:29] spacing outline size uh you know make it
[02:14:31] look pretty whatever you really want
[02:14:33] right so you can kind of start making
[02:14:35] your text a little nicer we'll save this
[02:14:38] as a game game
[02:14:40] over overlay We'll add this to our
[02:14:43] scenes our player I'll make a new folder
[02:14:46] here called
[02:14:48] GUI H save and in our level I'm going to
[02:14:52] now add our game over overlay now when I
[02:14:56] hit
[02:14:57] play the way this works is a canvas
[02:14:59] layer essentially follows the screen no
[02:15:02] matter where it is so here you can see
[02:15:04] the label in on top of our gameplay
[02:15:07] because in our game over overlay here
[02:15:10] the canvas layer is Within These blue
[02:15:13] lines so that is how we canvas layer
[02:15:15] Works anything within these lines will
[02:15:18] show up on our
[02:15:19] screen so you can kind of see or imagine
[02:15:22] why this would be useful specifically
[02:15:24] for uh you know gii and stuff so let's
[02:15:29] rename this to game over overlay we will
[02:15:32] add a script because well I'm going to
[02:15:34] need a script for this guy but I'll put
[02:15:36] it into my scripts folder put into my
[02:15:39] player create a new folder
[02:15:42] UI open create now in here what I'm
[02:15:46] going to do is I'm going to on ready the
[02:15:49] self. hiide I want to hide this game
[02:15:51] over overlay now I want another function
[02:15:55] that we're going to call when the game
[02:15:58] is over meaning like I'm dead this is
[02:16:00] the function I'm going to call one of my
[02:16:01] player dies now in here what I'm going
[02:16:04] to do is I'm going to take my input
[02:16:07] Mouse and make it so that it's captured
[02:16:09] or visible right because before it was
[02:16:11] captured but now I want it to be visible
[02:16:13] so we're going to say mouse mode is
[02:16:15] equal to visible next I'm going to say
[02:16:17] self. show because I want to show this
[02:16:19] overlay that would make sense because
[02:16:21] it's hidden right now right and then
[02:16:23] lastly I want to pause the scene to do
[02:16:26] this all I need to do is say get tree do
[02:16:29] pause is equal to true and then uh
[02:16:33] that's pretty much it now this is it but
[02:16:36] there's kind of an issue um that issue
[02:16:38] is that here let's actually let me
[02:16:41] actually show you so let's go to our
[02:16:43] player and in our player here instead of
[02:16:46] the q3e here what we're going to do is
[02:16:49] we're going to call the game overlay to
[02:16:52] do this I need to get node and get the
[02:16:54] path now to get the path it's actually
[02:16:56] not that hard let's go to our level here
[02:16:58] go to our player script and it might be
[02:17:01] a little
[02:17:02] cramped but all I need to do is now drag
[02:17:05] in uh maybe I'll actually rename this to
[02:17:07] game over overlay and then now I just
[02:17:10] need to drag it in and this will give me
[02:17:12] the path here I can just say get node
[02:17:15] overlay and now I can call that game
[02:17:17] over function that I created so this
[02:17:20] will do that for us now one thing I want
[02:17:22] to do though is before I call this I'm
[02:17:25] actually going to wait one second to
[02:17:26] kind of have that to show the effect
[02:17:28] that oh you're dead and we played the
[02:17:30] death animation but now we're going to
[02:17:32] you know uh wait one second kind of it
[02:17:35] just kind of adds a bit more player to
[02:17:38] our game I'll say so here I'll say get
[02:17:40] tree create
[02:17:43] timer one uh yeah so one second and then
[02:17:46] we'll wait for the timeout uh signal if
[02:17:49] you recall a wait allows us to you know
[02:17:51] wait for a certain signal and this is
[02:17:53] the signal we'll wait for so here I'm
[02:17:55] just going to get tree to create a timer
[02:17:57] once I create the timer I'll wait for
[02:17:59] the timeout signal now the seconds it's
[02:18:01] up to you whether you want one or two
[02:18:02] seconds or whatever I'm going to do one
[02:18:04] second I find that it's not bad so let's
[02:18:07] hit play and you're going to see
[02:18:09] something happen so let's just try to
[02:18:11] die here so get hit
[02:18:13] once twice here we go I died after a
[02:18:16] second this pops up but nothing happens
[02:18:19] now I could kind of click but it doesn't
[02:18:21] actually work the reason why this
[02:18:23] wouldn't work is because in my game
[02:18:25] overlay the process inside the node is
[02:18:29] called or it's on inherit now inherit
[02:18:32] essentially is inheriting the scene or
[02:18:35] the project uh pause scene right so the
[02:18:38] mode and the mode is currently paused
[02:18:41] right we pause the scene so this scene
[02:18:43] is also paused meaning I can't click
[02:18:45] anything so what I need to do is go to
[02:18:47] this mode and turn it on always so that
[02:18:50] way I can always interact with this
[02:18:53] script and these no nodes here no matter
[02:18:56] whether or not the scene is paused so
[02:18:58] okay let's rename this button to retry
[02:19:01] and I'm going to connect this node by
[02:19:03] going to press connect and here now all
[02:19:06] I need to do is a few things first I'm
[02:19:09] going to unpause the scene I'm going to
[02:19:11] say pause uh get Tre is equal to false
[02:19:14] and then I'm going to say get parent dot
[02:19:17] uh
[02:19:19] reload parent
[02:19:21] see oh not get parent what am I doing
[02:19:24] could be get tree that would make much
[02:19:26] more sense that's why we didn't have it
[02:19:28] complete so get current tree there we go
[02:19:30] so now we just we just reload the
[02:19:32] current scene from our get tree so now
[02:19:35] let's hit play and see if this
[02:19:38] works now we should be able to just go
[02:19:40] to our monster here eventually I'll
[02:19:43] die there we go 1 second later I can
[02:19:47] retry and here we go we restart our
[02:19:49] scene there we go that's our game over
[02:19:52] overlay in the next part we'll get
[02:19:54] started with our GUI and you our pause
[02:19:56] menu and stuff like that so see you in
[02:19:58] the next part all right so the next part
[02:20:01] is going to be in our GUI but first we
[02:20:03] need to actually make sure we add our
[02:20:05] GUI into our main scene here let's just
[02:20:07] make sure we add this guy in and I'm
[02:20:09] going to rename it to VII so this is our
[02:20:12] general VII for our inventory our
[02:20:16] profile that kind of thing so let's make
[02:20:18] this panel a little bigger just like I
[02:20:20] did for the game over and I'll rename it
[02:20:24] to
[02:20:25] gy and before I start adding things
[02:20:29] let's add a new script here add a new
[02:20:32] script to our scripts folder player gy
[02:20:35] open create now okay in this script
[02:20:38] there's a few things I'm going to do the
[02:20:40] first thing I'll do is I'm going to go
[02:20:41] into my function physics process I'm
[02:20:44] going to check for the input of my
[02:20:46] paused function or my uh input sorry I'm
[02:20:50] going to check for it just pressed and
[02:20:53] pause here this is where I will start
[02:20:56] pausing things and doing things so the
[02:20:58] first thing I'll do is I'm going to get
[02:20:59] tree. paused and instead of saying true
[02:21:02] or false there's a kind of trick here I
[02:21:05] can do that's just to get it to be the
[02:21:07] opposite of what it currently is and
[02:21:10] then the cool part about this is that
[02:21:12] now I can just say uh get node container
[02:21:17] which we don't have yet uh Dot
[02:21:21] visible is equal to the get tree. pause
[02:21:25] so if this becomes true I will set the
[02:21:28] visible to true it becomes false I'll
[02:21:30] set the visibility to false now okay
[02:21:32] let's add this container because well I
[02:21:34] don't have it so we'll probably want it
[02:21:37] now the reason we're doing this um I'm
[02:21:39] going to add a control node by the way
[02:21:40] so that's our container let's rename
[02:21:42] this to container okay let me explain
[02:21:45] why I'm doing this the reason is because
[02:21:47] I'm G to add a panel into this this is
[02:21:49] where my profile will be this is where
[02:21:52] my inventory will be but the question is
[02:21:54] what about the HP bar the progress bar
[02:21:57] that I add so let's add a progress bar
[02:21:59] for now and here I zoom in I can kind of
[02:22:02] move it to the top left extend it a
[02:22:05] little bit and here I can give it a
[02:22:07] value of let's say 50 I'll turn off the
[02:22:10] show percentage and here I don't want to
[02:22:13] hide or show this guy depending on if I
[02:22:16] pause or not right I always want to have
[02:22:18] the HP bar showing let me just rename it
[02:22:20] to HP bar and now the advantage is I can
[02:22:23] show or hide the container specifically
[02:22:26] this guy depending on if I'm POS or not
[02:22:29] the HP bar I want it to always show now
[02:22:32] before we continue one other thing I
[02:22:33] need to do is make sure the process mode
[02:22:35] is on always for my GUI because
[02:22:38] otherwise I'm not going to be able to
[02:22:40] unpause My Scene if I pause it right
[02:22:43] that would be kind of silly I won't be
[02:22:44] able to do anything if I pause it now
[02:22:47] okay here's the the fun part though or
[02:22:49] the unfun part is we need to match the
[02:22:53] paused uh scene so here I'm going to
[02:22:56] match whether or not I'm paused and if
[02:22:58] it's true what I'm going to do is I'm
[02:23:00] going to say input. mouse mode is equal
[02:23:03] to Mouse
[02:23:06] visible Mouse visible and if it's false
[02:23:09] which is pretty much the only other
[02:23:11] option here I'm going to set it to Mouse
[02:23:14] captured this will allow me to just be
[02:23:17] more dynamic in whether or not I pause
[02:23:19] the scene this kind of comes more into
[02:23:21] play when I add my shop uh well we'll
[02:23:23] add our shop later um because this is
[02:23:26] just kind of it becomes a little buggy
[02:23:29] because our our shop is going to pause
[02:23:31] the scene it's going to show and hide
[02:23:33] some GUI that will'll add later but this
[02:23:36] will just allow us to avoid any weird
[02:23:38] issues where if I go into a shop and
[02:23:40] then try pausing or whatever it just
[02:23:42] avoids all that so let's close the
[02:23:44] script now and let's hit play just to
[02:23:47] test this out here our is paused now you
[02:23:50] can see here that first of all nothing's
[02:23:54] working so let's actually just make sure
[02:23:56] that the pause is right so let's go to
[02:23:57] our project settings input okay so here
[02:24:00] I don't even have anything so let's add
[02:24:02] a
[02:24:03] Escape okay so now uh we have our pause
[02:24:06] but there's an issue is that this is
[02:24:08] still showing on the default now this
[02:24:11] should actually fix itself if I hit play
[02:24:14] and I pause my scene it will show and
[02:24:16] then I unpause it it'll hide but by
[02:24:19] default I should probably show it so
[02:24:21] let's add a ready function and we'll
[02:24:23] just take the visibility here and we can
[02:24:25] just do hide instead so that way we can
[02:24:28] hide it uh by default okay okay so now
[02:24:33] when I hit
[02:24:34] play here we go our container is hidden
[02:24:36] but if I hit Escape we pause the scene
[02:24:39] and uh we have our GUI so this is quite
[02:24:41] nice now from here we can start adding
[02:24:43] our inventory and things and whatever we
[02:24:45] want so let's just set up the general
[02:24:48] things that we need um first I'm going
[02:24:50] to Ren the panel here to BG for
[02:24:52] background I'm going to add two
[02:24:54] containers I'll duplicate it or two
[02:24:57] control nodes I'm going to add a vbox
[02:25:01] container and in this vbox container I'm
[02:25:03] going to add two buttons one will be the
[02:25:06] inventory inventory button I'll
[02:25:10] duplicate this and this will be the
[02:25:12] profile
[02:25:14] button now in my vbox container the cool
[02:25:17] part about this is if I extend it the
[02:25:19] buttons will automatic Al kind of resize
[02:25:21] a little bit here I can just type in
[02:25:23] inventory and then here I can type in
[02:25:26] profile now the spacing is a little
[02:25:29] weird and that is because in my custom
[02:25:31] theme I didn't really space it out too
[02:25:33] well so let me just fix that real quick
[02:25:35] we'll go to our style or normal
[02:25:38] here sub region here you can see that
[02:25:41] this is not spaced out nicely so we need
[02:25:43] to just kind of Center it again we'll
[02:25:46] close that and now we can see it's
[02:25:47] centered a little nicer alternatively
[02:25:49] you can just use this guy I think this
[02:25:51] guy was set up a little better so I
[02:25:53] spent a bit more time setting this up
[02:25:55] properly okay so here we have our
[02:25:56] inventory item and our profile button
[02:25:58] sorry and now what we can do is connect
[02:26:01] a signal for pressed in our GUI for both
[02:26:04] of
[02:26:05] these now what we'll do when we press
[02:26:08] these buttons is I want to show and hide
[02:26:11] these control nodes but these control
[02:26:13] nodes I need to rename them to the
[02:26:15] proper thing so let's rename this to
[02:26:17] inventory and this one to profile
[02:26:20] so what we'll do now is inside of this
[02:26:23] script we're going to show and hide
[02:26:26] depending on what I want so okay what
[02:26:28] we'll do here is for the inventory press
[02:26:30] I'm going to say get node container bbox
[02:26:35] inventory
[02:26:36] button
[02:26:38] disabled is equal to true because now
[02:26:41] I'm kind of showing that I'm in the
[02:26:44] inventory I do that by disabling this
[02:26:46] button now what I can do is duplicate
[02:26:48] this and just change this to
[02:26:52] profile and then enable the uh profile
[02:26:56] button because if I were in here right
[02:26:59] if I were to actually copy paste this I
[02:27:01] would do the opposite so here I would
[02:27:03] set the disabled to
[02:27:05] true and set the in disable to false on
[02:27:08] the but on this one so we're kind of
[02:27:10] just doing the opposite essentially now
[02:27:12] what I want to do is I want to show the
[02:27:15] inventory right so this guy I'm going to
[02:27:17] show
[02:27:18] this but then I'm going to hide the
[02:27:21] profile so here I'll get the profile and
[02:27:23] then hide this now I'll just copy this
[02:27:26] one more time the profile but do the
[02:27:29] opposite so here I'll hide the
[02:27:31] inventory and then show the profile yeah
[02:27:35] that's pretty much it now we won't have
[02:27:37] much of a visual effect um because
[02:27:39] there's nothing in our inventory or
[02:27:41] profile right now um but in the next
[02:27:43] part we'll start filling it in so we'll
[02:27:45] add in our inventory first uh so this
[02:27:48] might actually take a bit of time maybe
[02:27:50] an hour or so the next part um but we'll
[02:27:52] fill in the inventory we'll add a bunch
[02:27:54] of logic to it we'll add some items etc
[02:27:56] etc um and it'll be quite fun we'll
[02:27:59] start using the item pack here that we
[02:28:01] have and yeah so it'll be fun and we'll
[02:28:03] fill it in and yeah so I'll see you all
[02:28:05] in the next part all right so let's get
[02:28:07] started with our inventory first um and
[02:28:10] to do this what we're going to do here
[02:28:11] is we're going to right click our
[02:28:13] inventory and Save branch as scene this
[02:28:16] will allow us to create a new scene
[02:28:18] basically just as an inventory so you'll
[02:28:20] see what I mean in just a second we'll
[02:28:22] save this in rgi I'm going to create a
[02:28:24] new folder here called
[02:28:27] inventory and save and now you can
[02:28:29] should be able to see this kind of
[02:28:31] YouTube looking button here you can
[02:28:33] click into it and it opens a new scene
[02:28:35] let me just close the game overlay we'll
[02:28:37] open this inventory and here we go okay
[02:28:40] so what we need to do first is set up um
[02:28:44] our scripts so let's go to our GUI here
[02:28:46] create a new
[02:28:48] folder inventory
[02:28:51] and in this folder we're going to set up
[02:28:53] a bunch of our scripts now okay this
[02:28:55] next part this these next few parts that
[02:28:58] we're going to be watching and maybe the
[02:28:59] next hour or so will be not hard per se
[02:29:03] but try to keep up as there's quite a
[02:29:05] bit of logic to understand and learn so
[02:29:08] first we're just going to set up these
[02:29:10] scripts that we need so the first one is
[02:29:12] going to be inventory item this will be
[02:29:14] the actual item I'll duplicate this okay
[02:29:19] sometimes uh
[02:29:20] okay here we
[02:29:22] go sometimes it doesn't like when I have
[02:29:24] something else selected to control D
[02:29:26] which will allow me to duplicate it
[02:29:29] we'll say inventory main this will go
[02:29:31] into this
[02:29:33] inventory okay one more time we'll say
[02:29:36] inventory
[02:29:39] slot duplicate one more time and we will
[02:29:42] say um
[02:29:45] item data then we will
[02:29:48] have no that's actually for our for now
[02:29:51] at least we will have one more but that
[02:29:53] will be a little later so the first
[02:29:55] thing we'll start with is the item data
[02:29:57] the reason we're going to start with
[02:29:58] this is because we're going to create
[02:30:00] something called a resource we're also
[02:30:03] going to create something called a class
[02:30:05] now a class resource is something
[02:30:07] slightly specific um but we'll kind of
[02:30:10] go into it one one step at a time so
[02:30:13] let's create a class name here called
[02:30:15] item data this will essentially be our
[02:30:18] item information data right the
[02:30:20] information that will go into it we here
[02:30:23] we're going to extend a
[02:30:25] resource and a resource is something
[02:30:28] inside of gdau it's a built-in feature
[02:30:30] that essentially allows us to add uh GUI
[02:30:33] into a information packet now you'll see
[02:30:36] what I mean in just a second so let's
[02:30:38] close all these scripts and just open
[02:30:40] this up again and for example we can
[02:30:43] export a variable called item name and
[02:30:46] this can be a string now let's take a
[02:30:48] look inside of our 2D here let me just
[02:30:51] make this a little bigger now what I'm
[02:30:54] going to do now is go to my
[02:30:57] scenes that's not my scenes here we go
[02:30:59] inventory scenes I'll create a new
[02:31:01] resource and we'll use the default
[02:31:03] resource at the top I'll create a item
[02:31:07] uh now the item I will create is let's
[02:31:10] say a sword um we'll
[02:31:13] say iron
[02:31:15] sword so now uh what I can do is take
[02:31:18] this iron sword double click it go to
[02:31:21] the inspector Tab and you can see here I
[02:31:23] have the iron resource I have resource
[02:31:26] don't worry about this we have a script
[02:31:29] now the script we want to attach the
[02:31:31] item data and now you can see the item
[02:31:34] data the class name you can see the item
[02:31:36] name with a string now here I can just
[02:31:39] say iron sword so this is where I can
[02:31:42] start filling in information that I want
[02:31:45] inside of my resource so this is the
[02:31:47] kind of the advantage is that there's a
[02:31:48] nice uh property tab or a inspector tab
[02:31:52] for this now think of resources and um
[02:31:55] the script basically as an extension or
[02:31:59] a different way of doing a dictionary so
[02:32:01] a dictionary would look something like
[02:32:03] this so if I created a dictionary say
[02:32:05] item
[02:32:06] data right I can say it's a dictionary
[02:32:09] it would look like this where we have
[02:32:11] curly brackets we can have the item name
[02:32:15] and then this is the key so inside this
[02:32:17] item name we would have another string
[02:32:19] we would say iron sword right and then
[02:32:23] we have to do comma and then we would
[02:32:25] put in item damage Etc right so this is
[02:32:28] kind of how we do this dictionary but
[02:32:30] this is kind of messy right and imagine
[02:32:33] this is just one item so this I wouldn't
[02:32:35] even name item data I would name sword
[02:32:38] iron iron sword right and then I would
[02:32:40] have to create several dictionaries
[02:32:42] inside of another dictionary inside of
[02:32:43] an array inside of different things now
[02:32:45] this is kind of messy and there's just
[02:32:47] no point to that so instead we'll use
[02:32:49] res resources now in our resource we'll
[02:32:52] have a few things here so the first
[02:32:54] thing will be a type this is the type of
[02:32:57] item it is so in our types we will have
[02:33:01] weapon we'll have head body legs
[02:33:07] beat we'll have misk MK is miscellaneous
[02:33:12] so things like um potions and you know
[02:33:16] things you eat or things that aren't
[02:33:17] usable depends on what it is um you can
[02:33:20] kind of make this actually different to
[02:33:22] what you want our miscellaneous that I'm
[02:33:24] going to code in our game is going to be
[02:33:25] a usable item so specifically we're
[02:33:28] going to use a potion the two items that
[02:33:30] we're going to kind of look at in this
[02:33:32] are going to be some sort of equipment
[02:33:34] item so a weapon probably and then a
[02:33:36] miscellaneous item so like a potion that
[02:33:38] way you'll see how we can kind of
[02:33:40] differentiate between the two and then
[02:33:42] lastly we'll have main main is going to
[02:33:44] represent the uh inventory system so the
[02:33:47] actual main
[02:33:48] inventory all right so next we want to
[02:33:51] export the type and we can do this by
[02:33:54] saying lowercase type and then type
[02:33:56] which is the type that we just created
[02:33:58] so this is the enumerator that we just
[02:33:59] created now what I'm going to do is I'm
[02:34:01] going to copy paste this a few
[02:34:04] times and I'm going to change some of
[02:34:06] these do uh we have item name we have
[02:34:08] item damage that we
[02:34:10] want we have item
[02:34:14] Health we have item defense of course
[02:34:17] you can kind of Pi and choose whichever
[02:34:19] ones you want want um I'm going to just
[02:34:21] do the ones that I'm going to need um
[02:34:23] the ones that I'm going to implement
[02:34:26] here we're going to have a stackable
[02:34:27] item whether or it's going to be a
[02:34:29] Boolean I'll change the types in just a
[02:34:31] second um but this is a Boolean that is
[02:34:33] going to tell us whether or not it's
[02:34:34] stackable and if it is we'll have a
[02:34:36] count right next to it and then after
[02:34:38] that we're going to have a ex export
[02:34:43] multi-line and this is going to be our
[02:34:46] description and this is also a string
[02:34:48] but it's just going to be exported as a
[02:34:49] multi-line so you'll see the difference
[02:34:51] in just a second and then lastly we're
[02:34:53] going to need a texture so this is going
[02:34:55] to be a texture
[02:34:58] 2D texture 3 this one will be a
[02:35:03] integer the item defense an integer the
[02:35:07] item Health an integer the item damage
[02:35:10] also an integer so this is a Boolean
[02:35:13] okay actually now that we're done what
[02:35:15] we can do is head over to our item new
[02:35:18] item resource iron uh sword and we can
[02:35:20] start filling things in so we can see
[02:35:22] the type by default is weapon so that's
[02:35:24] cool the item damage we can give it
[02:35:26] damage like five the item health and
[02:35:29] defense I'm not going to fill that in if
[02:35:30] you're wondering what the item health is
[02:35:32] this is kind of the healing that I was
[02:35:33] going to implement so for the potions
[02:35:36] this is where I would do that now the
[02:35:38] description you can see the multi-line
[02:35:39] is more of a multi-line description so
[02:35:42] here what I can do is I can now I can
[02:35:45] kind of just do whatever I want I can
[02:35:46] write in this is a iron sword
[02:35:51] and this is not a stackable item I'm
[02:35:53] going to leave it unchecked I'm going to
[02:35:54] scroll up to my item pack and I can just
[02:35:57] kind of drag in one of these whichever
[02:36:00] one you'd like I don't know I'll just
[02:36:02] drag in maybe this one
[02:36:03] actually iight highlight again we'll use
[02:36:07] the first one um I'm going to use two
[02:36:09] different ones just to represent two
[02:36:11] different items so we'll have a iron
[02:36:12] sword I'll duplicate this and say long
[02:36:16] sword now in my long sword I'll go into
[02:36:19] this and you can see on the top right it
[02:36:22] says long sword so this is not an iron
[02:36:23] sword anymore we'll change this to long
[02:36:25] sword we can change the damage to maybe
[02:36:29] three this is maybe a slightly weaker
[02:36:31] item can say long sword scroll up and
[02:36:35] select a
[02:36:37] different thing maybe this one yeah this
[02:36:39] one kind of looks long I don't know yeah
[02:36:42] so you can kind of Select uh look
[02:36:43] through these and select whichone you'd
[02:36:45] like I'll now make a potion because well
[02:36:49] we'll make a small potion let's say so
[02:36:52] this small potion we rename it to small
[02:36:55] potion this is going to be a
[02:36:57] miscellaneous item the item damage will
[02:36:59] be zero the health we can change it to
[02:37:01] five so it'll heal five you can say this
[02:37:04] is a small ocean that
[02:37:08] heals heals you the count will change to
[02:37:12] one and this is a stackable item so
[02:37:14] we'll check that on so next what we can
[02:37:17] do is find a small potion
[02:37:20] and fill the texture in okay so we have
[02:37:22] a few items which is nice now one more
[02:37:24] thing I'm going to do is I'm going to
[02:37:26] actually create a new folder here called
[02:37:28] default stats this will be for a little
[02:37:31] later and for now what I'll do is I'm
[02:37:33] going to duplicate this and call this
[02:37:36] default
[02:37:38] sword I'll drag this guy into the
[02:37:41] default stats
[02:37:43] folder pop this out duplicate one more
[02:37:46] time and make a
[02:37:50] uh oops default body armor uh body armor
[02:37:56] like this. trust duplicate now these
[02:37:59] guys will be our default stats so for
[02:38:01] the iron sword or for the iron body I'm
[02:38:04] going to actually reset everything and
[02:38:06] here I'll just say default armor the
[02:38:09] default sword I'll say default
[02:38:12] Sword and the Damage I'll say is one by
[02:38:16] default or actually let's say two now
[02:38:19] the rest doesn't really matter we can
[02:38:20] just say the default sword because this
[02:38:23] isn't an actual item we'll have in the
[02:38:25] game it's just to represent our stats
[02:38:27] you'll see why we do this a little
[02:38:29] later okay so now that we have
[02:38:32] everything set up uh we need to actually
[02:38:33] start setting up our scene now the scene
[02:38:36] setup is not going to be actually too
[02:38:37] complicated here all I need to do is set
[02:38:40] or add my inventory main to my inventory
[02:38:44] uh scene here next I'm going to add a
[02:38:48] grid uh scroll scroll up grid container
[02:38:51] this is going to be our grid container
[02:38:53] so I'll rename this to grid this is
[02:38:57] going to be where I put my inventory
[02:38:58] slots now next what we want to do is we
[02:39:01] want to add equipment but our equipment
[02:39:04] is going to be our own node that we
[02:39:06] create now what I mean by this is inside
[02:39:09] of our inventory slot here what we're
[02:39:12] going to start doing in the next part is
[02:39:13] we're going to take a look at how we can
[02:39:15] create our own node from scratch because
[02:39:18] here we extend node but we want to
[02:39:20] create our own node and we'll take a
[02:39:22] look at how that what that looks like in
[02:39:23] just a
[02:39:24] second all right so now that we have our
[02:39:27] inventory slot here to create a new node
[02:39:31] using this script what we can do is
[02:39:34] create something called a class name now
[02:39:37] we already did this but this time we're
[02:39:38] using an extend node so let's take a
[02:39:41] look at how this might work we're going
[02:39:43] to create this class name called
[02:39:45] inventory slot and instead of extending
[02:39:47] node we're going to extend panel
[02:39:49] container so now what we can do is if I
[02:39:52] close the script just as an example well
[02:39:54] it is an example but we're actually
[02:39:56] going to use this if I search up
[02:39:58] inventory or uh slot okay I'm going to
[02:40:02] have to actually save so here I need to
[02:40:04] make sure I contrl S and then try one
[02:40:07] more time here we go we have our
[02:40:09] inventory slot I can create this as its
[02:40:12] own item or is its own node now this
[02:40:15] slot is technically a panel container
[02:40:18] right but here it says inventory slot
[02:40:20] just because it has the script attached
[02:40:22] to it now the coolest part about this is
[02:40:25] in my inventory here what I could do now
[02:40:28] is let's say I create a ready function
[02:40:31] so that's not a ready
[02:40:34] function the cool part is if I say
[02:40:36] create a variable slot is equal to
[02:40:40] inventory slot because now it's a class
[02:40:43] that I can call and then say New I can
[02:40:47] add a child slot
[02:40:49] now the cool part is let me hit play
[02:40:51] Within this
[02:40:53] scene this will add a new slot but if I
[02:40:57] go to the remote section you will see I
[02:40:58] now have two slots whereas here I only
[02:41:01] had one so this is how we will actually
[02:41:03] fill our inventory slot grid through
[02:41:06] this now kind of extend on this example
[02:41:09] you can also do this using any already
[02:41:12] pre-built node inside of gdau so here I
[02:41:14] could create a label right so here let's
[02:41:17] add a label let's go to our REM section
[02:41:20] and here I now have a label additionally
[02:41:23] we can also start editing some things
[02:41:25] and properties from this label obviously
[02:41:27] here it's called slot but I'm going to
[02:41:29] call slot. text equal to I my name is
[02:41:35] coding
[02:41:36] quests and if I hit play you will see a
[02:41:39] label on the top left that has that
[02:41:42] property so this is kind of the
[02:41:44] advantage to what we're going to be
[02:41:45] using we're going to essentially create
[02:41:48] some slots just control Z here and fill
[02:41:51] in our inventory slot now let's complete
[02:41:54] our inventory slot first because we'll
[02:41:57] kind of be confused on what we're doing
[02:41:58] in here and what we're filling in until
[02:42:01] I actually do this so in our inventory
[02:42:03] slot here we're going to start filling
[02:42:05] in some things now the first thing we'll
[02:42:08] need is an on uh sorry export variable
[02:42:12] called variable type and there's a
[02:42:14] reason we're going to export this I'll
[02:42:15] show you in just a second we're going to
[02:42:17] get the item data type so we'll export
[02:42:20] all the types of the uh item data right
[02:42:23] so now if I actually close this you will
[02:42:26] see here I can now pick what sort of
[02:42:29] item this is now the advantage of this
[02:42:31] specifically the reason we're exporting
[02:42:33] it is because now I can create equipment
[02:42:36] system using this same slot and we'll do
[02:42:38] that a little later so let's just go
[02:42:39] back to our script and we'll continue
[02:42:41] this next we need to initialize our um
[02:42:46] slot here to do that we'll say in it P
[02:42:50] item
[02:42:51] data. type we initialize the item data
[02:42:56] CMS and then Vector 2 this is the size
[02:43:00] that will actually have our uh oops this
[02:43:04] is going to return void so here we go we
[02:43:06] say void this is the size of our actual
[02:43:09] inventory panel slot here I can say type
[02:43:12] is equal to T and then I can say CMS or
[02:43:16] sorry custom
[02:43:19] minimum size is equal to DMS the custom
[02:43:22] minimum size right so this custom
[02:43:25] minimum size what this is is if I close
[02:43:27] this real quick is in my layout so if I
[02:43:30] add this to my grid you will see that my
[02:43:32] inventory slot disappeared and that is
[02:43:35] because even though well I guess
[02:43:37] technically now it's just 0 0 this I
[02:43:39] can't actually edit the size of my panel
[02:43:43] or my inventory panel here I can change
[02:43:46] the size of this to 64x 64 or 32 by 32
[02:43:50] whatever I want so here I need to make
[02:43:53] sure I change my minimum size all right
[02:43:56] let's uh make sure that we just have
[02:43:58] that outside for now let's head back to
[02:44:01] our script here all right next we're
[02:44:03] going to add a function called function
[02:44:06] and drop item data this is going to
[02:44:10] allow us to have a true or false it's
[02:44:11] going to return true or false and tell
[02:44:14] us whether or not we can uh drop data or
[02:44:17] not at a certain position now if we can
[02:44:20] right we're going to call another
[02:44:21] function called drop data and this is
[02:44:24] going to return void so here we can
[02:44:26] actually pass here I'll just return
[02:44:28] false for now so that way we get rid of
[02:44:30] that
[02:44:31] error next we're going to have a fun
[02:44:34] physics process function which we'll
[02:44:35] actually return to a little later but
[02:44:37] this is where I'm going to check for
[02:44:42] equipment and adjust stats this is
[02:44:46] something we'll do a little later but
[02:44:48] for now we'll just have it in so that
[02:44:49] way we remember that we're going to need
[02:44:51] it next we're going to add a GUI input
[02:44:55] now a GUI input is a function that
[02:44:57] allows us to detect some sort of input
[02:45:01] only within not only the script but only
[02:45:04] within this actual item so what do I
[02:45:08] mean by this well if here I actually
[02:45:11] print event and I hit
[02:45:13] play let's say if you tried this before
[02:45:17] right event should print like Mouse
[02:45:19] motion and stuff but the cool part about
[02:45:21] this is because this is a control node
[02:45:23] specifically right a panel container is
[02:45:25] part of the control node family here you
[02:45:28] can see it says control this I head back
[02:45:31] to my game
[02:45:32] here let me just play
[02:45:36] again will only print if my mouse is
[02:45:38] within this control so here you can see
[02:45:42] there's motion I can click and you will
[02:45:44] see the mouse button here we go and we
[02:45:46] can detect things only Within the
[02:45:49] specific uh script so this is going to
[02:45:52] allow us to check for a very specific
[02:45:54] thing within this specific slot okay all
[02:45:58] right so and this is where we're going
[02:45:59] to be using a lot of um using buttons
[02:46:03] and uh sorry using like our items and
[02:46:05] stuff like that so this specifically
[02:46:06] will actually be using our items okay
[02:46:10] let's get started with our handrop
[02:46:13] function so here we're returning false
[02:46:15] by default which is actually correct but
[02:46:17] well it's correct and not correct what
[02:46:19] we want to do here is we want to first
[02:46:21] check to see if the data is inventory
[02:46:25] slot uh sorry inventory item now
[02:46:28] inventory item is another class that
[02:46:30] we're going to need to make but let's
[02:46:31] actually make that before we continue so
[02:46:34] I don't eror here here I'm going to
[02:46:36] create a class name inventory item and
[02:46:39] this is going to
[02:46:41] extend let me extend just double check
[02:46:45] the texture rectangle
[02:46:49] texture rect so this is going to
[02:46:51] essentially represent uh our Sprite
[02:46:53] think of it as kind of a Sprite but this
[02:46:55] texture rectangle specifically is a uh
[02:46:58] control node uh sorry so texture wct you
[02:47:02] can see here that it inherits the
[02:47:04] control node properties so it's just to
[02:47:07] display a texture but it's also a
[02:47:09] control node so that's kind of why we're
[02:47:11] using it okay so let's pop this back out
[02:47:14] go back to our inventory slot and now we
[02:47:16] can continue this so here what else I
[02:47:19] need to do or check for is if the type
[02:47:22] is equal to the item data. type. main I
[02:47:27] want to check to see if this is our main
[02:47:29] inventory slot if it is we'll also check
[02:47:32] to see if the child count is zero and
[02:47:35] what this
[02:47:37] is this is to check to see if we have an
[02:47:40] item or not so what we're going to end
[02:47:42] up doing is when we drop the data or
[02:47:45] drop an item in an in a slot we're going
[02:47:48] to actually add a physical item into
[02:47:50] that slot so it's going to be an actual
[02:47:52] node that gets dropped into that filed
[02:47:55] so if I do that the child count will be
[02:47:58] one not zero if it is zero this means
[02:48:01] that I can return this means that there
[02:48:03] is space to return on the inventory slot
[02:48:07] otherwise I will return get child
[02:48:11] z. dat
[02:48:13] type equal to data do dat. type now the
[02:48:19] data is something that we'll have to
[02:48:20] adjust later so don't worry too much
[02:48:23] about understanding this because we
[02:48:24] haven't finished it just yet but next
[02:48:27] we'll create a if statement here or
[02:48:29] check an if statement we'll say if type
[02:48:31] is equal to data.
[02:48:34] getet
[02:48:37] parent do
[02:48:41] type there we go Ty if it is then we'll
[02:48:46] return
[02:48:47] true now lastly we'll say if else here
[02:48:50] and then we'll return false on the
[02:48:52] else okay so here I might have to make
[02:48:55] sure that this gets saved in order for
[02:48:58] this to actually work and I'm going to
[02:49:01] close my game here so I don't get an
[02:49:03] error so
[02:49:05] hopefully okay so we're missing some
[02:49:07] things okay so right here this is
[02:49:09] missing an else statement so over here
[02:49:11] we'll need an else statement here so
[02:49:13] here we'll return the data do dat. type
[02:49:18] equal equal to type so this is going to
[02:49:20] return a true or false depending on if
[02:49:22] this is true or not right okay so this
[02:49:24] is our can drop now if we can drop
[02:49:27] something I want to drop something to do
[02:49:29] that I will first check to see if the
[02:49:31] child count is bigger than
[02:49:33] zero if it is that means there's an item
[02:49:36] that we're currently dropping into this
[02:49:38] item or into this slot so what we'll say
[02:49:40] is variable item is equal to get
[02:49:45] child we'll get the item that is kind of
[02:49:47] in the slot right now now and then we'll
[02:49:50] say if item is equal to data we'll just
[02:49:53] return this basically means item this
[02:49:56] means that I'm trying to replace a slot
[02:49:58] with a with the same item so then I can
[02:50:00] just return I don't have to actually
[02:50:01] change anything next I can just item
[02:50:05] reparent data. get
[02:50:08] parent then outside of this if statement
[02:50:11] I will say data.
[02:50:14] reparent uh
[02:50:16] self here we'll reparent our self the
[02:50:19] item that is kind of currently in our
[02:50:20] hand into the uh inventory slot but if
[02:50:23] there is an inventory or if there's an
[02:50:26] item already in that slot will reparent
[02:50:29] the item there into the previous um slot
[02:50:33] that we were in okay so now this is kind
[02:50:37] of our general Logic for our inventory
[02:50:39] slot let's take a look at our inventory
[02:50:41] item as this is where some of the things
[02:50:44] actually happen for actual
[02:50:46] item all right next up in our inventory
[02:50:49] item we're going to start editing some
[02:50:51] things in here first we will export our
[02:50:55] data now this is the data that we've
[02:50:56] been talking about this entire time
[02:50:58] right this is where the data will be
[02:51:00] stored now the data that's storing or
[02:51:03] that's being stored is an item data
[02:51:05] resource now we can create a ready
[02:51:07] function and say if data we'll start to
[02:51:11] fill in some things that we need first
[02:51:13] we'll say expand mode is equal to
[02:51:16] texture Direct
[02:51:19] rect
[02:51:21] expand mode ignore size here we go we'll
[02:51:26] also say stretch
[02:51:27] mode is equal
[02:51:30] to uh okay there we go error is gone
[02:51:33] texture
[02:51:35] re do stretch
[02:51:38] mode aspect
[02:51:40] centered next we will say texture is
[02:51:42] equal to data. item
[02:51:46] texture next we'll fill in the tool tip
[02:51:49] the tool tip is a very cool thing it
[02:51:52] essentially allows us to cover an item
[02:51:55] and some text will appear so this is
[02:51:57] kind of where the description will
[02:51:58] become so here we can fill in a name
[02:52:01] we'll put in percent s we'll fill in
[02:52:04] that information in just a second we'll
[02:52:07] say new line percent s maybe I'll just
[02:52:12] copy this so it's a little easier to
[02:52:14] put new line and then we'll say stats
[02:52:18] actually no space there stats space new
[02:52:21] line or sorry uh contr s and then damage
[02:52:26] then
[02:52:30] defense and then maybe the health as
[02:52:32] well so now what we can do on this line
[02:52:36] we'll put our
[02:52:38] percent and then an array with the
[02:52:41] information we want to fill that
[02:52:42] information is going to be the item
[02:52:45] name the data Dot
[02:52:48] uh
[02:52:49] description and the data do uh item
[02:52:53] defense or damage and I'll just copy
[02:52:57] this so this one will be item
[02:53:01] defense and then this one is item Health
[02:53:05] hopefully that should be
[02:53:07] right okay so let's go to the new line
[02:53:10] all right so now what we can check for
[02:53:12] is if the item is
[02:53:15] stackable if it is stackable that means
[02:53:17] I want to create a count number right
[02:53:19] below to do this what we can do is
[02:53:22] create a new label to do that we
[02:53:25] actually already kind of went through an
[02:53:26] example I just create a new label like
[02:53:29] so next I can just start adjusting its
[02:53:32] uh properties the text I'll add is a
[02:53:34] string of the data.
[02:53:37] count the position of this I'm going to
[02:53:40] set it to be Vector 2 24 and 16 now this
[02:53:45] you can adjust to whatever you'd like
[02:53:47] later this is kind of something I found
[02:53:49] it works kind of good enough it's in a
[02:53:51] decent position next I'll just add child
[02:53:54] and then add the label okay so this is
[02:53:57] our ready function complete next I'm
[02:53:59] going to initialize our function here
[02:54:01] now make sure that when you initialize
[02:54:04] you do not have the underscore the
[02:54:06] underscore is a very is not very
[02:54:08] different but it is different than
[02:54:10] having this um here I'm going to
[02:54:13] initialize the item data and this is
[02:54:17] going to return void and we'll just say
[02:54:19] data is equal to
[02:54:20] D okay next we'll create a function
[02:54:24] called get uh drag data here we'll just
[02:54:28] pass for now and we'll create one more
[02:54:30] function called make drag review uh
[02:54:35] preview there we go preview um it's
[02:54:37] going to be at position and I'm actually
[02:54:39] just going to copy
[02:54:41] this but here I'm going to return a
[02:54:44] control node next in here uh we'll do
[02:54:47] this part first because this is the
[02:54:49] preview and then this is the get preview
[02:54:51] uh so here in the make preview I'm going
[02:54:52] to create two new nodes the First new
[02:54:55] node is to represent the actual image
[02:54:58] that I have so to do that I'll create a
[02:55:00] texture
[02:55:01] rectangle a
[02:55:04] new oops new like so we'll get the
[02:55:07] texture and we'll say texture is equal
[02:55:09] to self.
[02:55:11] texture we'll get the expand mode and
[02:55:13] I'm actually going to just copy this
[02:55:16] right here
[02:55:19] and then after that I will say t. custom
[02:55:22] minimum size is equal to self. size
[02:55:26] we'll say t. modulate a equal to 0.5 now
[02:55:33] if you're wondering what this is this is
[02:55:34] the modulation a so what that is is
[02:55:38] let's go to our inventory slot go to
[02:55:40] visibility modulate and if we look at
[02:55:43] the a this is kind of the invisibility
[02:55:46] tab the 05 would be in the middle and
[02:55:48] this just makes it slightly transparent
[02:55:50] so this will kind of give it that effect
[02:55:52] that I'm dragging my item okay next I
[02:55:55] want to say p. position is equal to
[02:55:58] Vector 2 minus F
[02:56:02] position next I want to create a control
[02:56:05] node because I'm supposed to return a
[02:56:06] control node here I'll create a
[02:56:10] control do
[02:56:12] new I'll say c.
[02:56:16] addchild I'm going to add that texture
[02:56:18] that I created and then return
[02:56:20] C now for the get preview I'll just say
[02:56:23] get uh set drag preview oops preview do
[02:56:28] the make drag preview which I just
[02:56:31] created and pass through the
[02:56:33] position then I will return
[02:56:36] self all right so this should be it this
[02:56:38] is my entire inventory item script next
[02:56:42] we will head back to our inventory Main
[02:56:45] and start filling in our inventory
[02:56:47] because we don't have any slots right
[02:56:48] now to test anything with and before we
[02:56:51] continue actually we now need to create
[02:56:54] a our Global script This Global script
[02:56:57] will create a new folder for it for
[02:56:59] Global if anything if we ever add
[02:57:02] anything Global it will be in here we'll
[02:57:04] add a new script in
[02:57:06] here new script we'll call this game now
[02:57:10] this the reason we're doing this is
[02:57:11] because we want to essentially globalize
[02:57:14] a lot of our things the one thing we're
[02:57:16] going to globalize first is is um player
[02:57:20] heal we're going to default this as an
[02:57:23] INT to let's say five we'll create a
[02:57:26] player health max this will be well five
[02:57:30] by default as well can't be bigger than
[02:57:32] or smaller than the player Health we'll
[02:57:34] create a right
[02:57:36] hand
[02:57:38] equipped for item data now this is kind
[02:57:42] of where we start to go into uh the
[02:57:44] reason we created the default resource
[02:57:47] so we also create a body
[02:57:52] equipped uh item
[02:57:55] data next we'll create a uh variable
[02:57:58] player damage this will keep track of
[02:58:00] how much damage we
[02:58:03] do to zero variable player
[02:58:07] defense as an in to zero and we'll say
[02:58:11] variable
[02:58:14] uh oh that's it for now uh next we'll
[02:58:17] actually load our items though globally
[02:58:19] so we'll also create an items tab here
[02:58:23] whoops going to be a dictionary not an
[02:58:25] array here I can actually say dictionary
[02:58:29] and then here I will say long sword and
[02:58:32] then I'll load or preload the long sword
[02:58:36] so here I should be able to
[02:58:38] say long sword okay maybe not if it
[02:58:43] doesn't pop up that's okay what we can
[02:58:44] do here is we'll close thisor Scripts
[02:58:49] and we now want to find that long sword
[02:58:52] I've created over here so now I will pop
[02:58:56] this into the new
[02:59:00] row we'll load in all our items that we
[02:59:02] have so we have a long sword we have an
[02:59:05] iron sword we also have a
[02:59:08] small
[02:59:10] potion okay here we'll just load in the
[02:59:14] small
[02:59:16] potion make sure that this is correct we
[02:59:19] go iron
[02:59:21] sword here we go we load in all these
[02:59:24] items okay uh we'll delete that there we
[02:59:28] go so now we have our items globally
[02:59:31] accessible now what we can do is
[02:59:33] actually one more thing we'll create is
[02:59:35] a gold variable here I'll just default
[02:59:37] this to 100 uh this will be for a little
[02:59:40] later but we'll just add it now for why
[02:59:42] not okay so now let's head back to our
[02:59:44] inventory main here and this is where
[02:59:46] I'm going to start adding my inventory
[02:59:48] items first I'm going to export a
[02:59:50] variable called inventory size and equal
[02:59:54] to
[02:59:55] 24 I'm going to on ready variable grid
[02:59:59] and I'm going to get a node grid this
[03:00:02] will just allow me to access the grid
[03:00:04] inventory a little faster now what I'm
[03:00:06] going to do here is I'm going to for I
[03:00:09] in range of our inventory size so I want
[03:00:14] to Loop 24 times every time I do I'm
[03:00:17] going to create a new slot now every
[03:00:19] time I create this new slot though I
[03:00:21] need to initialize it because if you
[03:00:23] remember we created an initialize
[03:00:26] function so in it and then we're going
[03:00:28] to pass through item data. type main
[03:00:32] we're going to initialize every single
[03:00:35] inventory uh to Main and then we're
[03:00:38] going to give it a size of 32x 32 then
[03:00:42] I'm going to get my grid and then add
[03:00:44] the child there now that's it so now if
[03:00:48] I hit play I should be able to just hit
[03:00:52] play and here is my inventory now this
[03:00:55] obviously isn't perfect because I need
[03:00:58] to now head back to my inventory grid
[03:01:00] here and go to columns and search either
[03:01:03] do four or six the four would give you a
[03:01:06] 4X six and six would give you well a 6x4
[03:01:09] right so it's up to you now let's play
[03:01:11] one more
[03:01:12] time and now here we go so I kind of
[03:01:16] think I'll do a 6x4 instead I think that
[03:01:18] might look a little nicer I'll kind of
[03:01:20] move this right
[03:01:21] here and now we can
[03:01:25] start um we can actually delete this guy
[03:01:27] I'll add it a little later but for now
[03:01:30] let's hit play one more
[03:01:32] time and now we have our items now the
[03:01:35] issue is we need to now add items so to
[03:01:37] add an item we'll create a new function
[03:01:40] called add item this will pass through
[03:01:43] the item name as a string and will
[03:01:46] return void
[03:01:48] so what to to do what we need to do
[03:01:51] sorry is create a new inventory item we
[03:01:55] say inventory item. new we initialize
[03:01:58] this item so we'll in it we'll say
[03:02:01] initialize with the game. items items
[03:02:05] that we just globalized we'll call in
[03:02:07] the item
[03:02:09] name okay so the game is not Global
[03:02:12] because I haven't globalized it let's
[03:02:14] head to our project settings go to
[03:02:17] autoload and we need to autoload our
[03:02:20] script so let's add it and this has
[03:02:23] enabled our Global variable you can even
[03:02:25] see global variable and if we close this
[03:02:27] head back to our script this will now be
[03:02:30] globalized all right so sometimes you
[03:02:33] still have an error but that's okay
[03:02:35] it'll go away eventually now what we can
[03:02:37] do there you go see it's gone away
[03:02:39] already so now what we can do is check
[03:02:40] to see if the item is stackable the
[03:02:43] reason is because if this item is
[03:02:45] stackable there's something else we need
[03:02:46] to do now if it's not stackable the
[03:02:49] answer is actually quite easy all we
[03:02:51] need to do is for I in the inventory
[03:02:54] size and you can probably guess why
[03:02:56] we're doing this we need to find an
[03:02:58] empty slot If an item is not stackable
[03:03:01] like a sword and I want to put it in my
[03:03:04] inventory well I need to find an empty
[03:03:06] inventory slot to put it in so this is
[03:03:08] actually quite easy all I'll do is for
[03:03:10] Loop through the inventory and then I'll
[03:03:12] check to see if the grid. getchild child
[03:03:16] I and get child count of that child is
[03:03:20] equal to zero if it is that means the
[03:03:23] inventory uh or that slot specifically
[03:03:25] is empty so what I can do is say grid.
[03:03:28] getchild I do addchild item now if I do
[03:03:34] find it I will just break and no longer
[03:03:36] need to continue looping through my
[03:03:38] inventory now here it's a little more
[03:03:41] complicated because now I need to find
[03:03:43] if the item is stackable I need to First
[03:03:45] find if I have this item or not so
[03:03:48] similarly I will for Loop through the
[03:03:50] inventory first then I will check to see
[03:03:54] I'll just copy this right here I'll
[03:03:56] check to see another way we can do this
[03:03:58] is to see if it's greater than zero that
[03:04:00] means there is an inventory uh in that
[03:04:02] slot so if there is an item right or if
[03:04:05] the child count is greater than zero
[03:04:07] that means there is an item in that said
[03:04:08] slot now if there is an item well you
[03:04:11] can probably guess what I want to do is
[03:04:13] now uh see if that item is equal to the
[03:04:18] item I'm trying to add so here what I
[03:04:20] can do is check to see if the
[03:04:26] grid. get child
[03:04:30] i. getet
[03:04:32] child
[03:04:34] zero this is the uh data and we'll check
[03:04:39] to see if the item. DAT is equal to that
[03:04:42] we'll see if the data is equal to the
[03:04:44] item data meaning it's just the same
[03:04:47] item right
[03:04:48] now if it is then that means we found
[03:04:51] our item in our inventory so what we'll
[03:04:53] do is we'll update the
[03:04:55] counter then we'll
[03:04:57] update oops update the label counter now
[03:05:02] at this point this is where I don't
[03:05:05] actually need to add child this is I
[03:05:06] just need to do this I just need to
[03:05:09] update the counter and update the label
[03:05:11] so to do this I will just get grid here
[03:05:13] I'll just get all this copy this and
[03:05:16] then dot data and then count plus equals
[03:05:20] 1 next I can copy paste it again but
[03:05:23] instead of child I'll get child one more
[03:05:25] time because this is my label so now I
[03:05:28] have access to my label I'll edit the
[03:05:30] text now I can just make it equal to uh
[03:05:34] the item I'll copy this part right
[03:05:36] here I'll get the string of this I'll
[03:05:40] copy the count into the text now once I
[03:05:44] do that what I'll do is I'll go to the
[03:05:46] next line here
[03:05:48] I will just break if I this means I have
[03:05:51] found our item and I've just added it
[03:05:53] now what I can do here is add an lse
[03:05:55] statement and I will add the item if I
[03:05:59] can't find it if I can't find the item I
[03:06:01] will simply add the item right that
[03:06:04] means I don't have it and then here I
[03:06:06] can break
[03:06:07] again okay so now that we've created our
[03:06:11] ad item function we can just add an item
[03:06:15] and then we can say long sword
[03:06:18] we can add an
[03:06:20] item small
[03:06:22] potion now do make sure that the name
[03:06:25] here has to be the same as this so here
[03:06:29] it has to be capital S maybe I'll just
[03:06:32] make sure that these are all the
[03:06:34] same small potion Etc we'll hit close
[03:06:37] we'll hit
[03:06:40] play and now you can see I've added my
[03:06:43] items and I should be able to drag and
[03:06:45] drop them okay cool so this is very neat
[03:06:48] now the question is what if I want to
[03:06:50] use this item specifically the misk item
[03:06:52] what if I want to right click and use
[03:06:54] this and obviously okay you can also see
[03:06:57] here when I hover it you see the
[03:06:58] description which is very cool so okay
[03:07:01] now let's head into
[03:07:03] our um inventory slot I believe yeah so
[03:07:07] this is where we will actually be
[03:07:09] checking for equipment we'll be also be
[03:07:12] able to use the equipment let's take a
[03:07:15] look at how we'll do
[03:07:16] that all right so back in our inventory
[03:07:18] slot here what we're going to do is
[03:07:20] we're going to do our gii input first so
[03:07:22] this is to use a misk item so to do this
[03:07:25] we'll check the event first we want to
[03:07:27] check to see if the event is an input
[03:07:30] event Mouse button if we're clicking and
[03:07:34] I now want to check what sort of
[03:07:36] clicking we're doing well what I can do
[03:07:38] here is I can check to see the button
[03:07:40] Index this is to check if I'm clicking
[03:07:42] left or right clicking or middle click
[03:07:45] technically but here I'm going to check
[03:07:47] for right click specifically now if you
[03:07:49] want left click I believe it's zero if
[03:07:52] you want middle click I think it's one
[03:07:53] but don't putote me on that I might be
[03:07:55] wrong uh here we can say event and event
[03:07:59] button
[03:08:01] mask is equal to zero this button mask
[03:08:05] will check to see if I'm clicking up or
[03:08:06] down this will be like it's kind of like
[03:08:09] a release or press down right so here
[03:08:11] this is uh release so now if I am left
[03:08:14] right clicking and I'm releasing my
[03:08:16] button then I will say get child count
[03:08:21] greater than zero
[03:08:23] oops greater than
[03:08:25] Z then that means there's an item in
[03:08:28] that slot that I'm clicking in if the
[03:08:30] get
[03:08:32] child get filed
[03:08:35] zero is data. type is an item data.
[03:08:44] type. MK that means it's a miscellaneous
[03:08:47] item and I want to use it so to use it
[03:08:49] what I'll do is I'll say game dot
[03:08:53] heal
[03:08:56] player so this is a functional call with
[03:08:59] the uh game dot or sorry not game dot
[03:09:02] we'll get the child hero do
[03:09:07] data. item help here I'm going to use
[03:09:11] the item Health to heal myself now this
[03:09:14] function I need to create otherwise I'll
[03:09:16] airor so let's go to game
[03:09:18] and create this
[03:09:19] function and for now we'll just pass and
[03:09:23] here I need to pass through uh Health
[03:09:25] this will be an INT we'll pass through
[03:09:27] at health and we'll return void I
[03:09:29] believe the
[03:09:31] moment okay so now that we have that
[03:09:32] function hopefully we don't error next
[03:09:35] we will get child zero we want to update
[03:09:38] the count so to do this we say data.
[03:09:40] count minus equals 1 because we're using
[03:09:43] one right next I want to update the
[03:09:45] counter the label to do that we can say
[03:09:48] get child. get child Z again text is
[03:09:52] equal to the new data I'll just copy
[03:09:56] paste this string of that
[03:10:00] data and then after that I want to check
[03:10:03] to see if this data count is less than
[03:10:05] or equal to zero if it is that means I
[03:10:08] mean I'm out of items right so now oop
[03:10:12] now I want to get
[03:10:13] child
[03:10:15] dot do free because this means that the
[03:10:18] item I'm using is all used up right get
[03:10:21] child zero there we go there we go this
[03:10:23] is our usable item so in fact we can
[03:10:26] actually test this out by hitting
[03:10:28] play and here we should be able to right
[03:10:32] click and use our item now of course
[03:10:34] nothing happens because we haven't used
[03:10:36] or implemented our deal functionality
[03:10:39] yet but we'll do that a little later
[03:10:41] okay next for the equipment what we'll
[03:10:44] do is actually not too hard here what
[03:10:46] we'll say is if get child count get
[03:10:51] Childs child count is greater than zero
[03:10:55] that means we have an item in this slot
[03:10:57] if we do we'll get the item we'll just
[03:11:00] assign it a variable by saying get child
[03:11:03] zero we will match the type right so the
[03:11:06] type in this slot itself to the item
[03:11:10] that is equipped we'll match the type
[03:11:12] the item that's equipped so we'll say
[03:11:14] item data. type
[03:11:18] weapon
[03:11:20] weapon here we go if it is a weapon then
[03:11:23] what I want to do is I want to fill in
[03:11:26] the game. right hand equipped with the
[03:11:29] item. DAT this will whoops dat there we
[03:11:33] go so this will fill in my game right
[03:11:35] hand with the item that is equipped so
[03:11:38] essentially if I have this item or if
[03:11:41] this inventory slot is a equipment item
[03:11:44] right or an equipment slot and I have
[03:11:46] this certain type of data inside of it
[03:11:49] then I'm going to fill in my right hand
[03:11:51] equipped with this data now
[03:11:54] alternatively we might have uh now this
[03:11:56] is kind of up to you so you can start
[03:11:58] implementing the body the right hand
[03:12:00] left hand Etc I'm only going to do the
[03:12:02] weapon and the body um so here in the
[03:12:06] body. equipped I will say body equipped
[03:12:09] item data now
[03:12:12] otherwise so this is almost like saying
[03:12:15] else if it's else what I'm going to do
[03:12:17] here is I'm going to load in the AUD
[03:12:20] equipped and the right hand data with
[03:12:24] the default stats so this is going to be
[03:12:26] my default stats here I have default
[03:12:31] SW so this one should actually be on the
[03:12:33] next one s right let's load this for our
[03:12:36] right
[03:12:37] hand and then this one I'm going to load
[03:12:39] in the
[03:12:42] default armor so here we now have our
[03:12:46] default armor and our default sword
[03:12:48] being equipped if I don't have this
[03:12:50] equipped or this equipped and this will
[03:12:52] work for each slot
[03:12:54] independently so now if I close this we
[03:12:57] now need to set up our inventory
[03:12:59] equipment stuff so let's take a look at
[03:13:01] how we can do that it's actually not too
[03:13:02] hard all I need to do is search up
[03:13:04] inventory slot add my inventory slot
[03:13:06] here and now I need to just assign each
[03:13:09] one of these what I can do here is I can
[03:13:13] zoom in here a little bit I can
[03:13:14] duplicate this a few times and now now I
[03:13:17] can rename this to what I need so first
[03:13:19] I'll rename one to right
[03:13:21] hand I'll rename this to body I'll
[03:13:25] rename this to
[03:13:27] head I'll rename this to
[03:13:30] legs and this to feet and this one we
[03:13:34] won't need so I'll delete that now I can
[03:13:36] start moving everything around as I want
[03:13:39] it this is my head this is my right hand
[03:13:42] so I'll put that over here these are my
[03:13:44] legs so I'll put that right there this
[03:13:47] is my body so I'll put that there my
[03:13:50] head and this is my right hand but
[03:13:52] here's my kind of equipment system now
[03:13:55] if I hit
[03:13:57] play uh actually sorry before we do that
[03:14:00] let's just close one more time and now
[03:14:02] we need to make sure that the type is
[03:14:03] all correct so here this is a weapon so
[03:14:05] that's correct the body type I need to
[03:14:07] select body the head I need to select uh
[03:14:11] head here we go the legs I need to
[03:14:14] select legs and feet I need to select
[03:14:16] feet
[03:14:17] all right so now if I hit play I should
[03:14:20] be able to go into my inventory and drag
[03:14:23] this into my weapon system but not my
[03:14:25] body or head now if I drop this in you
[03:14:28] will see in my remote section in my game
[03:14:31] you will now see the right hand is
[03:14:33] equipped with the long sword. tress
[03:14:36] however if I head back to my game and
[03:14:39] unequip this you will see a returns to
[03:14:41] the default sword so that is our
[03:14:43] equipment system our equipment system
[03:14:46] now essentially works
[03:14:47] and inside of this we have all these
[03:14:49] stats that I might need
[03:14:52] okay now in the next part we'll take a
[03:14:54] look at how we can continue our gii
[03:14:57] system because here I don't believe
[03:14:59] we're completely finished so we'll kind
[03:15:00] of continue our whole gii system all
[03:15:03] right next we're going to start filling
[03:15:05] in our profile because right now if I
[03:15:07] hit play and I head into my system here
[03:15:12] go to profile nothing's here and I go
[03:15:14] back to inventory here's my inventory
[03:15:16] equip stuff but I want to be able to see
[03:15:18] my stats now okay what we'll do is we
[03:15:21] will create our profile by right
[03:15:24] clicking our profile Save branch as seen
[03:15:27] and we can save it in our VII group save
[03:15:32] we'll head into our profile here I will
[03:15:34] add a script I'll save the script in my
[03:15:37] scripts folder player GUI open create I
[03:15:43] will uh now we want to add some things
[03:15:46] in this to
[03:15:47] all I'm going to do is add a label now
[03:15:49] this label I'm just going to test some
[03:15:53] things this is a test text yeah and now
[03:15:58] I can just dag this out and I want to
[03:16:02] just put this where it would be in my
[03:16:04] profile here if I actually hit uh
[03:16:07] save I'm going to close my inventory go
[03:16:10] to my gu so this is where the text will
[03:16:12] show here I'm going to Center the text
[03:16:16] and I'll just kind of drag it where I
[03:16:18] would want it to be in my GUI and there
[03:16:21] we go of course alternatively you could
[03:16:23] just use this profile and move this
[03:16:26] around uh but I'm just going to do it in
[03:16:28] my profile it's really up to you now
[03:16:30] here I'm going to rename this to Stats
[03:16:32] label and into my script here and now
[03:16:35] I'm going to pop this out and we're
[03:16:39] going to create a process function now
[03:16:41] I'm just going to say this uh even
[03:16:42] though I probably shouldn't this is not
[03:16:44] good practice to do you don't want to
[03:16:46] just add everything into a process
[03:16:47] function you would ideally want to
[03:16:50] update the text every time you hit
[03:16:52] Escape so ideally you would have a
[03:16:55] function instead that updates the text
[03:16:57] and then you would call it through here
[03:16:59] whenever you hit play so um this is not
[03:17:03] good practice but I'm just going to do
[03:17:04] it anyways because it's quick and easy
[03:17:07] what we'll do is we'll say get node
[03:17:10] stats label we'll edit the text equal
[03:17:15] to a string
[03:17:17] uh not Delta we'll hit uh enter we'll
[03:17:20] say player
[03:17:22] healths player health is space I will
[03:17:26] put in uh percent s and now I'm going to
[03:17:30] hit enter copy this and paste it a few
[03:17:32] times this I'm going to remove or
[03:17:35] replace with attack this is going to be
[03:17:38] defense this is going to be level and
[03:17:41] this is going to be
[03:17:42] XP now these obviously don't exist yet
[03:17:45] or some of these don't so let's head
[03:17:46] back to our game script here and let's
[03:17:49] start adding in some of the things that
[03:17:50] we'll need eventually so here I'm going
[03:17:52] to create a variable called current XP
[03:17:56] this will be an
[03:17:58] integer equal to zero next I'm going to
[03:18:02] have a variable XP to Next Level as an
[03:18:07] INT be equal to 100 by default we'll
[03:18:10] have our player level as an INT equal to
[03:18:14] one by default now lastly we have
[03:18:17] another thing called shopping this will
[03:18:18] be a Boolean that we'll use a little
[03:18:20] later so don't worry too much about this
[03:18:23] when we add our shop we'll you'll see
[03:18:25] why we need this okay let's head back to
[03:18:27] our profile and now I need to fill in
[03:18:29] the information so let's uh hit percent
[03:18:33] array and now we want to fill in the
[03:18:36] game. player
[03:18:40] L we want to add our game uh do
[03:18:45] player damage
[03:18:47] right for the attack we want the game.
[03:18:51] player
[03:18:53] defense and we want the game. player uh
[03:19:00] level then came do
[03:19:03] current
[03:19:06] XP and then game
[03:19:08] dot XP to Next Level now back over here
[03:19:16] we're actually going to have to add a
[03:19:19] flash percent so this will just show us
[03:19:22] how much xp we need to get to the next
[03:19:24] level let's hit close and see if this
[03:19:26] works so let's hit
[03:19:28] play and immediately should air if we
[03:19:31] don't okay so cool it works here we go
[03:19:34] now we can go in and out now if I equip
[03:19:36] something you will not see anything
[03:19:38] happen and the reason is because we
[03:19:40] don't actually update the player damage
[03:19:44] uh depending on where we need it to be
[03:19:46] so the player damage think of the player
[03:19:48] damage and all that stuff as the total
[03:19:52] player damage now we want to have a
[03:19:55] total that we add to it um with our
[03:19:58] stats so let's take a look at how we can
[03:20:00] do
[03:20:01] that right so in our script here we're
[03:20:03] going to head over to our game script
[03:20:05] and pop this out and at the very bottom
[03:20:08] we're going to actually in between this
[03:20:10] we'll create a function process and in
[03:20:13] here what I'm going to do is I'm going
[03:20:15] to say player damage is equal to right
[03:20:18] hand equipped do item damage and this is
[03:20:22] now where you would add other things so
[03:20:25] for example I can add the body equipped
[03:20:30] do item damage obviously my body equi
[03:20:34] doesn't have damage but we'll change it
[03:20:35] in just a second to test this
[03:20:37] out now here I can change the item
[03:20:41] defense similarly but the item defense
[03:20:44] here I'm going to take item defense
[03:20:48] very same thing for the body equipped
[03:20:50] and now this will essentially give me a
[03:20:52] total of well all my player damage and
[03:20:55] all my player defense let's take a look
[03:20:57] at how this might work let's go to my
[03:20:59] iron well I should probably add a body
[03:21:02] so let's say iron
[03:21:05] body let's go into this iron body here
[03:21:08] change this to iron body we will scroll
[03:21:12] up find some
[03:21:15] armor uh we'll go over here here we go
[03:21:18] we'll change the type to body we'll
[03:21:20] change the defense to five as well and
[03:21:24] this is an iron body armor I'm going to
[03:21:28] need to load this in my game script so
[03:21:30] over here I will Control Paste body uh
[03:21:35] iron
[03:21:37] armor and then I need to load the body
[03:21:42] iron body there we go all right so
[03:21:45] that's our added now let's add this in
[03:21:48] my main uh slot here here I'm just going
[03:21:50] to add it so uh I'll
[03:21:55] say iron body we'll add this item we'll
[03:21:59] hit
[03:22:00] play and now when I hit Escape okay so
[03:22:04] here we have an error because iron body
[03:22:06] doesn't exist so here I said iron armor
[03:22:10] so let say iron body play one more
[03:22:14] time here if I uh sorry go to here pop
[03:22:19] this in pop this in and if we can go to
[03:22:21] profile and we can see the t is two
[03:22:26] which is doesn't seem right so let's go
[03:22:28] to over here okay so here we can see
[03:22:31] that the long sword is equipped and the
[03:22:33] iron body is equipped so that's correct
[03:22:35] now here if we go into this it says item
[03:22:37] defense five and here we have zero we
[03:22:40] should have a total of five so this is
[03:22:43] not being updated which is weird now now
[03:22:47] we also have the player Health which is
[03:22:49] correct the attack should
[03:22:53] be okay so the attack should be 3 + 5 so
[03:22:58] it should be eight but it's two let's
[03:23:00] take a look at why this is not
[03:23:03] working here we have player damage is
[03:23:06] equal to right hand equipped do item
[03:23:10] damage this doesn't seem to be working
[03:23:13] so okay I see the problem the problem is
[03:23:17] the this script is not being updated so
[03:23:19] actually if I hit escape and then try it
[03:23:22] again you'll see that it works but what
[03:23:24] was happening is the script the game
[03:23:26] script is being paused because I'm in
[03:23:28] pausing my screen so what I want to do
[03:23:30] is on function ready I'm going to say
[03:23:33] self. process mode is equal to mode
[03:23:37] process always okay this will allow my
[03:23:41] script to always run even when my game
[03:23:43] is paused so now when I hit play now it
[03:23:46] should work properly so hit play pop
[03:23:49] this in and you can see the stats being
[03:23:52] changed okay now um what we want to do
[03:23:55] now is before we kind of head to the
[03:23:57] next part is I want to fix our GUI so
[03:24:00] let's go into our GUI here and in the
[03:24:03] ready function I want to hide a few
[03:24:05] things so first I'm going to get
[03:24:08] node um I'm going to say get node
[03:24:12] profile here we go this guy and I'll
[03:24:15] hide this
[03:24:16] by default so by default I will have the
[03:24:19] Prof uh the inventory selected so to do
[03:24:23] that as well I will also disable
[03:24:26] the uh inventory button by default so
[03:24:29] this kind of gives it that effect that
[03:24:31] I'm by default looking into my uh
[03:24:34] inventory slot okay so now what we can
[03:24:37] do is we'll also get
[03:24:41] node um we will get the HP bar and we'll
[03:24:46] say. max value is equal to game. layer
[03:24:52] Max Health now we'll also start
[03:24:55] implementing the health in just a minute
[03:24:57] but this will just allow us to fill in
[03:24:59] the HP bar okay so let's hit play to
[03:25:02] double check this
[03:25:04] works all right there we go we can see
[03:25:06] our inventory slot is selected I can
[03:25:08] unselect or whatever and there we go now
[03:25:11] everything works pretty nicely all right
[03:25:15] okay next we want want to start doing a
[03:25:17] bit of weird stuff because we want to
[03:25:19] implement the health and stuff but we
[03:25:21] also want to start Implement damage now
[03:25:24] let's close our GUI close our profile
[03:25:27] now we'll head back to our player in our
[03:25:30] script here and if you
[03:25:32] recall in our uh hit thing we here we
[03:25:37] we're doing two but now I want to say
[03:25:39] game do player damage now this will do
[03:25:42] the amount of damage I should be doing
[03:25:45] now at the very top
[03:25:46] we can delete the health at the very
[03:25:49] bottom we can now go over here and
[03:25:51] change this to game. player Health now
[03:25:56] here's the thing though is I want to now
[03:25:58] also apply the defense that I you know
[03:26:01] added right so how do I do that well
[03:26:04] it's kind of up to you in this sense
[03:26:06] that you can kind of create your own
[03:26:09] calculations whether or not you want to
[03:26:11] uh have like some weird calculations I'm
[03:26:13] going to do a very flat damage what I'm
[03:26:16] going to do here is I'm going to say or
[03:26:17] check to see um I'm going to create a
[03:26:21] damage uh done this is going to be equal
[03:26:24] to damage minus the game.
[03:26:29] player defense and then I'm going to
[03:26:32] check to see if Damage Done is greater
[03:26:36] than zero then this is where I will
[03:26:38] actually do damage okay now uh here the
[03:26:44] Damage Done though will be reduced here
[03:26:47] this is the amount of damage I will do
[03:26:48] to my health only if it's greater than
[03:26:51] zero uh now here I want to check to see
[03:26:54] if it's less than or equal to zero if it
[03:26:57] is then we die just the same way we just
[03:27:00] did now I'm only going to get hit though
[03:27:02] if this goes off so here I can say just
[03:27:05] hit is equal to
[03:27:07] True okay now that is pretty much it um
[03:27:11] here is our damage done now what else do
[03:27:13] we want to do we also want to
[03:27:16] uh Implement our health system our
[03:27:19] health system player to do this we're
[03:27:21] going to create a custom signal now
[03:27:24] custom signals are pretty cool let me
[03:27:26] show you an example first before we head
[03:27:27] into this so if I create a new node here
[03:27:30] create a random node it doesn't really
[03:27:32] matter I'll make a buil-in script and
[03:27:35] I'm going to create before I do that
[03:27:37] actually let me show you the signals so
[03:27:40] here on the top right in the node
[03:27:42] section I select the node you will see a
[03:27:45] bunch of signals now the question is
[03:27:47] what if I want my own signal not too
[03:27:50] hard I can create a signal called custom
[03:27:53] signal it's save uh I don't have to save
[03:27:57] the scene because now we see it here
[03:27:59] custom signal and this is how we create
[03:28:01] a custom signal now if I want to pass
[03:28:03] through some sort of
[03:28:05] variable you can now see that it says
[03:28:08] damage variant of course I can uh
[03:28:10] initialize it to an INT and there we go
[03:28:13] now the damage is an INT so this is how
[03:28:15] I create a custom signal let me close
[03:28:17] this going to discard it that was just
[03:28:20] an example now in my game script I'm
[03:28:22] going to create a global variable called
[03:28:25] Health
[03:28:27] changed this is going to pass through a
[03:28:29] damage variable I'm going to have one
[03:28:31] more for later called level up and this
[03:28:35] is going to be a level up signal now in
[03:28:37] order to make these work we're going to
[03:28:39] go to the bottom we're going to in our
[03:28:41] heal player I'm going to say self. emit
[03:28:45] signal
[03:28:47] Health
[03:28:48] changed when I emit the signal I'm going
[03:28:51] to pass through the negative
[03:28:54] amount the reason is because this is to
[03:28:57] heal the player now I'm going to have
[03:28:59] another
[03:29:00] function um let me actually let's finish
[03:29:02] this one first first and then we'll do
[03:29:04] the other one here what I'll say is
[03:29:06] player Health Plus equals okay so here I
[03:29:11] actually need to change this to amount
[03:29:13] there player Health Plus equal amount
[03:29:16] and then I'll check to see if the player
[03:29:18] health is greater than the player max
[03:29:23] Health if it is I want to set the player
[03:29:27] Health to the max the reason we do this
[03:29:30] is well because I don't want to overheal
[03:29:33] right unless that is something you want
[03:29:34] to do but now what I'll do is I'm going
[03:29:36] to copy paste this function and rename
[03:29:38] this one to damage player and this will
[03:29:42] say will emit the signal damage changed
[03:29:44] here we'll do the same thing the amount
[03:29:46] now here I'm going to remove this
[03:29:48] because here I'm going to be subtracting
[03:29:51] damage okay so these are our functions
[03:29:53] that we want to add now the question is
[03:29:56] well what about the Damage Done or
[03:29:59] damage player sorry well uh in our
[03:30:03] player script we can go
[03:30:06] to player
[03:30:09] and we want to uh damage the
[03:30:13] player if uh
[03:30:17] here we go in the hit
[03:30:20] function here we go so instead of Damage
[03:30:24] Done Right here where we subtract the
[03:30:26] Damage Done Now I can just all the
[03:30:29] function that I just created called
[03:30:31] damage ler
[03:30:34] damage layer and pass through damage
[03:30:37] done now the reason we're doing all this
[03:30:39] by the way is specifically for our GUI
[03:30:42] so let's open our GUI one more time
[03:30:44] let's open this guy up and now this is
[03:30:47] where I want to uh create a new function
[03:30:50] on the bottom called on
[03:30:54] node Health
[03:30:57] changed we're going to pass through a
[03:30:59] damage as a
[03:31:02] int pass through an INT and this is
[03:31:05] going to be a function where we tween
[03:31:07] the HP bar so we're going to Tween so TW
[03:31:11] we need to create a tween we will twe
[03:31:14] Dot
[03:31:16] uh between
[03:31:20] property okay so there we go uh the
[03:31:23] thing that we're going to TW is going to
[03:31:24] be the HP bar which we don't have so
[03:31:27] let's actually on ready variable this at
[03:31:29] the top we'll say on ready variable HP
[03:31:35] bar is equal to get node now I can call
[03:31:39] the HP bar here and at the bottom we can
[03:31:43] call the HP bar we can twe the value
[03:31:47] the value I'll set it to HP bar do value
[03:31:52] minus the damage done and we'll do this
[03:31:55] over a period of2
[03:31:57] seconds okay now what we want to do is
[03:32:01] at the very top we want to connect the
[03:32:03] signal to do this we will say variable
[03:32:06] game node is equal to get
[03:32:11] node game. get path this will get us the
[03:32:16] to the game script globally now we have
[03:32:19] access to the game as a variable now
[03:32:22] what we'll do the reason we do this is
[03:32:24] because now I want to say game. node do
[03:32:27] elf
[03:32:28] changed dot
[03:32:32] connect to
[03:32:34] callable and here we'll say
[03:32:38] self then we will copy this new thing
[03:32:41] that we just created and pass it as a
[03:32:44] string and this will pass through the
[03:32:46] signal every time I change my health
[03:32:49] every time this signal is uh shot at
[03:32:53] basically through the game we will
[03:32:54] connect it here and we'll pick it up
[03:32:57] we'll pick up that signal through this
[03:32:58] script and then every time I lose damage
[03:33:01] or gain health or whatever it will
[03:33:03] change my HP bar now here when I hit
[03:33:08] play I should be able to take damage now
[03:33:12] and it doesn't seem to be updated so
[03:33:14] let's take a look at What's happen
[03:33:15] happening let's go to my inspector
[03:33:19] here player health is one so it should
[03:33:22] have changed so something is going
[03:33:25] on something not good is going on so
[03:33:27] let's take a look the damage player is
[03:33:29] not
[03:33:31] working so let's take a look at if I'm
[03:33:35] actually damaging the player here what
[03:33:38] we can do to kind of debug this in a
[03:33:40] sense I
[03:33:42] will well here actually I should be
[03:33:44] adding the amount Maybe that's why so
[03:33:46] here let's try one more
[03:33:49] time okay there we go so now it should
[03:33:52] be working functionally all right there
[03:33:54] we go and we lost all our health game
[03:33:56] over and there we go so now actually
[03:33:59] let's try the health uh potion as well
[03:34:01] so let me just lose
[03:34:03] damage okay so I lost some health let me
[03:34:06] right click and you can see here that I
[03:34:08] added some health now it was pretty
[03:34:10] immediate so let's take a look as to why
[03:34:12] that is here heal player their
[03:34:17] amount amount
[03:34:22] negative okay uh it should be working um
[03:34:25] but one thing we're going to add here is
[03:34:28] a background for our image because this
[03:34:30] looks nice but we want to make it a
[03:34:32] little better now the reason I didn't
[03:34:34] add a image for this before for from our
[03:34:38] texture is let's find our UI big piece
[03:34:41] here drag this in and I'm going to go to
[03:34:43] region enable and edit region and now I
[03:34:47] can select the health bar that I want
[03:34:50] and I will select this
[03:34:52] one this is the health bar I'm going to
[03:34:55] select close and now I can move this in
[03:34:58] put this behind my HP bar and just drag
[03:35:02] it to be a little bigger let me fill
[03:35:05] this in 100 so I know how much it should
[03:35:07] have here I can just start dragging this
[03:35:10] guy to be a little bigger like so and
[03:35:14] then I can turn off the grid snap if I
[03:35:17] need and now here I can just drag this
[03:35:19] in to fit the HP bar like
[03:35:24] so I'll just drag it in like this maybe
[03:35:28] all the way right
[03:35:30] there
[03:35:32] and right there I believe okay so there
[03:35:35] we go there's our HQ bar it's not
[03:35:36] perfect but should now look a little
[03:35:39] nicer visually now if we hit play I lose
[03:35:43] some health now it actually looks like I
[03:35:45] lost some health
[03:35:46] and if I right click okay so it does
[03:35:48] animate it was just really quick there
[03:35:50] we
[03:35:51] go okay so there there's our system
[03:35:54] there's quite a bit and it looks quite
[03:35:56] nice so let's take a look at what we're
[03:35:58] going to do
[03:35:59] next right next now that we have a nice
[03:36:02] system here and everything is working
[03:36:04] relatively well we're now going to
[03:36:06] implement a way to drop items from our
[03:36:09] monster right now I can walk up to him
[03:36:13] kill him uh hopefully without
[03:36:17] dying well I died kind of tried to bug
[03:36:20] out the game there uh let's actually
[03:36:22] equip some stuff see if I can kill
[03:36:25] him okay there we go one shot him but he
[03:36:28] doesn't drop anything so we want to make
[03:36:30] a way so that he drops stuff and I can
[03:36:32] pick it up or whatever now of course you
[03:36:34] could just have the monster die and then
[03:36:37] drop them right away but I want a more
[03:36:40] visual effect so let's create an area 3D
[03:36:43] as our base here now what I'm going to
[03:36:45] do is I'm going to search up some items
[03:36:47] now the first one I'm going to have is a
[03:36:49] sword let's find a sword and here in the
[03:36:52] K kit we can find some swords now it's
[03:36:54] kind of up to you um you can use the
[03:36:56] two-handed you can use this um whatever
[03:36:59] you'd like I'm going to put put this guy
[03:37:01] in then there's also a body armor now to
[03:37:05] get the armor don't think we actually
[03:37:07] have it so we what we'll have to do is
[03:37:10] we're going to cheat a little bit and
[03:37:12] we're going to find the
[03:37:16] Knight drag him in we're going to make
[03:37:18] it local and then we're going to steal
[03:37:20] his
[03:37:22] uht body armor there we go he Knight
[03:37:25] body going to steal this
[03:37:27] guy all right so let's make this local
[03:37:30] as well we'll drag this
[03:37:32] in and we'll rename this to sword rename
[03:37:36] this to body and one more item we'll
[03:37:38] have is a beer we search a beer a beer
[03:37:46] other one was
[03:37:48] called don't remember what was called
[03:37:50] but let's go into the fbx here and we
[03:37:52] can probably just find it oh mug here we
[03:37:54] go so mug full we'll make this
[03:37:58] local and I'll rename this to potion
[03:38:00] I'll use this as the potion obviously I
[03:38:02] don't have a mesh of a a potion but this
[03:38:05] is going to work fine now I'm going to
[03:38:08] reset everything to
[03:38:10] 00 here we go set everything to Z
[03:38:15] now the ocean I'm just going to move it
[03:38:17] up a little bit that way it doesn't go
[03:38:19] into the floor now I'm going to add a
[03:38:22] new uh thing here called Collision shape
[03:38:25] 3D this is going to be the Collision
[03:38:28] that I use to pick up our item I'll make
[03:38:31] this little higher here I'll rename this
[03:38:33] to
[03:38:35] item object I'll save this into my
[03:38:38] scenes I'll save this into
[03:38:41] my maybe I'll make a new object here or
[03:38:44] actually I'll just save it right here
[03:38:45] here as we're going to have this be
[03:38:46] slightly Dynamic now we'll add a new
[03:38:49] script We'll add this as non-b built-in
[03:38:52] script or script folder uh player UI
[03:38:56] inventory We'll add it here create I
[03:38:59] will delete this code and I'm just going
[03:39:01] to connect our body enters uh node here
[03:39:05] I'll pop this out now what I want to do
[03:39:08] is a few things first let's do the
[03:39:11] pickup the pickup is not too hard all I
[03:39:14] need to do is check to see if it's in
[03:39:16] the group Player right because hopefully
[03:39:19] it's oops a player that's picking up
[03:39:21] this item not a monster now what we'll
[03:39:24] do here is I'm going to match RNG now
[03:39:27] the reason we're doing this is because
[03:39:28] I'm going to randomize the item so I'm
[03:39:30] going to create a new variable called
[03:39:32] RNG outside of this if it's zero what
[03:39:35] I'll do I'll get node and I want to add
[03:39:39] the
[03:39:41] item uh long sword
[03:39:43] probably so what we'll do is we need to
[03:39:46] get access to our monster or to our
[03:39:49] inventory now to do this we need to
[03:39:52] First figure out how am I going to do
[03:39:54] this pathing so I'm going to close this
[03:39:56] go to level one and I'm going to create
[03:39:58] a few new nodes here node 3DS I'm going
[03:40:01] to duplicate this a few times I'm going
[03:40:03] to rename this to
[03:40:05] monsters
[03:40:07] monsters going to rename this one to
[03:40:10] code
[03:40:12] projectiles going to rename this one to
[03:40:18] objects and this one to items so the
[03:40:21] objects will be things like torches and
[03:40:24] kind of environmental things now the
[03:40:27] items is where I'm going to add my item
[03:40:29] so what I'll do here I'm going to add my
[03:40:32] item object into my scene make sure it's
[03:40:35] a child of this make sure I save this so
[03:40:37] I can see the script here now I will
[03:40:40] drag in my GUI this will give me the
[03:40:42] path to my GUI I can copy paste is here
[03:40:46] but now we're not done because now what
[03:40:48] we need to do is get the path of the
[03:40:50] inventory right so back to my item
[03:40:52] object I need to say slash container
[03:40:56] slash inventory and now I have access to
[03:40:59] my inventory script which in here I have
[03:41:02] the add item now just remember in order
[03:41:04] to add an item I need to make sure that
[03:41:06] the name is the right name in here I can
[03:41:09] say long sword but it has to be the same
[03:41:12] one okay now we'll head back to the
[03:41:16] script and what we'll do is we'll match
[03:41:19] uh the other numbers so here this
[03:41:21] actually has to be on the next line
[03:41:23] we'll do one uh we'll copy paste
[03:41:26] this one more time two copy paste and
[03:41:31] then outside of this I'm going to say
[03:41:33] self.
[03:41:35] hiide actually sorry I'm going to say
[03:41:38] self. VI three for now there we go so no
[03:41:43] matter what I pick up obviously I should
[03:41:45] self. Q free outside of the match
[03:41:47] function sorry now here I'm going to
[03:41:49] change these so one will be the small
[03:41:55] potion small
[03:41:59] potion the third one we can make it the
[03:42:03] the iron body copy paste that iron body
[03:42:08] and now what I want to do is I want to
[03:42:10] make my RNG work though so to do this I
[03:42:13] will make sure this is an INT I will say
[03:42:15] ready
[03:42:17] function uh what we'll do is we will say
[03:42:19] RNG is equal to Randy range from 0 to2
[03:42:24] we'll get
[03:42:25] node ocean
[03:42:28] oops do
[03:42:30] hiide we get node
[03:42:33] sword do hiide we're just hiding all the
[03:42:37] uh meshes right now the body do hiide
[03:42:42] then what I'm going to do is I'm going
[03:42:43] to uh match
[03:42:45] the
[03:42:46] RNG just like I did before I'll match
[03:42:50] zero so zero should be the sword so I'll
[03:42:52] get the sword and show
[03:42:55] it if it's one that should be the small
[03:42:58] potion so I'll get the small potion I'll
[03:43:00] hide this or sorry I'll show this if
[03:43:03] it's two that means it's the body it is
[03:43:06] the body I'll show the body and that
[03:43:09] should be it now this is pretty much
[03:43:13] General uh our general object now one
[03:43:16] thing I want to do is I want to kind of
[03:43:18] create a floating effect with our object
[03:43:22] so to do this what I'll do is or not a
[03:43:24] floating effect sorry a randomized
[03:43:27] spawning position so to do this I'll
[03:43:29] create a tween that's not a twe create
[03:43:33] TW I'll say variable
[03:43:36] RNG position this is going to be a
[03:43:39] vector 3 we're going to
[03:43:41] randomize the X range from1 to
[03:43:46] one we're going to randomize the Z we're
[03:43:50] going to say Randy range from one to one
[03:43:54] and the Y needs to be one so by default
[03:43:57] the Y needs to be one otherwise if it's
[03:44:00] zero it'll be in the floor if it's two
[03:44:02] it'll be too high Etc right now we can
[03:44:05] tween the property of self we're going
[03:44:09] to twe the
[03:44:11] position to position plus plus the RNG
[03:44:16] position that I just made over a time of
[03:44:20] 0.5 this has to be side of a string like
[03:44:23] so so there we go all right so now I'll
[03:44:27] close this I'll head into my monster so
[03:44:31] let's find our monster here I'll pop
[03:44:33] this into the monsters tab go over here
[03:44:36] and now what I can do is I can load the
[03:44:41] uh item object that I just created so to
[03:44:43] do that what I'll do is at the very top
[03:44:47] I will maybe right here I'll say on
[03:44:49] ready variable item object be is equal
[03:44:54] to
[03:44:56] preload item
[03:44:58] object and now what I want to do is I
[03:45:02] want to find uh where I die so where do
[03:45:04] I die well in my death function so in
[03:45:08] the death function right here this is
[03:45:10] where I'm going to add this so to do
[03:45:12] this I will randomize the object by
[03:45:14] saying
[03:45:15] RNG
[03:45:18] Randy uh Randy range and essentially
[03:45:22] this is going to be a random number
[03:45:23] between two and four is going to be how
[03:45:25] many items I spawn we'll for loop I in
[03:45:29] RNG we'll create the item object M as
[03:45:35] the item object scene do
[03:45:38] instantiated this is going to create a
[03:45:41] new object for us let me actually pop
[03:45:42] this out so it's a bit easier to see we
[03:45:45] get access to this temp you will say.
[03:45:49] global position equal to self. globble
[03:45:55] position and then all we need to do is
[03:45:57] get access to the items tab so this guy
[03:46:00] right here I need to get access to this
[03:46:03] so I I'll remove that and say get
[03:46:06] node items so I'll make sure the path is
[03:46:10] correct and then I will just add the
[03:46:13] child so I'm going to add this guy by
[03:46:15] saying ADD child add item object temp
[03:46:19] and that's pretty much it now one more
[03:46:21] thing since we're here we'll also gain
[03:46:24] XP here so I'm going to add a function
[03:46:26] called gain XP and here I'll just say
[03:46:29] 100 now here I need to create this in my
[03:46:32] game uh script we will create it but for
[03:46:35] now we'll just uh pass we'll say gain XP
[03:46:38] uh amount and we'll pass through an INT
[03:46:42] and we'll return void and pass for now
[03:46:46] now let's close our script here let's
[03:46:48] hit
[03:46:50] play and we should be able to going to
[03:46:53] equip my items here so I can onot him we
[03:46:56] should be able to kill him and he spawns
[03:46:59] some items now we can pick these items
[03:47:01] up and it should add it to my inventory
[03:47:05] all right there we go we even got some
[03:47:06] potions we got some armor should be able
[03:47:08] to switch it out Etc so obviously if you
[03:47:11] have a different item it would visually
[03:47:14] make more sense but since these items
[03:47:15] are the same you don't really notice a
[03:47:17] difference but yeah so that's pretty
[03:47:19] much it for the item object we've now
[03:47:22] also created it so we can spawn some
[03:47:24] items so let's delete this guy we don't
[03:47:26] need it so in the next part we'll take a
[03:47:28] look at how we can create our shop all
[03:47:31] right so let's move into our shop now to
[03:47:33] start our shop we're going to create a
[03:47:35] new scene called canvas item or layer
[03:47:38] we're going to go to level one open up
[03:47:40] our GUI as this is kind of going to be
[03:47:42] where our shop is so let's make sure we
[03:47:45] rename this first to shop I'll save this
[03:47:48] in my
[03:47:50] leri save it in here in here I will just
[03:47:54] drag in the shop that I just created and
[03:47:57] now head back to my shop sure we're in a
[03:47:59] 2d scene of course and now I want to
[03:48:01] start filling in the things I need for
[03:48:03] my shop let's fill in all the nodes that
[03:48:06] we'll need so first I'm going to add a
[03:48:08] panel I'm going to add a Rd
[03:48:13] painter going to add
[03:48:15] a control node and this control node
[03:48:18] will actually contain two labels so
[03:48:20] let's create a label duplicate it and
[03:48:22] then add a
[03:48:24] Sprite uh sorry not Sprite 3D just a
[03:48:26] regular Sprite
[03:48:29] 3D then our shop we will add two buttons
[03:48:33] one is going to be our buy button we
[03:48:36] name this to buy we'll duplicate this we
[03:48:40] name this to
[03:48:41] buy button and this is going to be close
[03:48:45] button so close the
[03:48:47] shop Okay so let's rename this to
[03:48:50] close and let's start organizing things
[03:48:53] let's make our panel a little bigger
[03:48:55] here I'll put it same size as I do for
[03:48:57] everything I'll take our clothes let me
[03:49:00] actually lock in the panel by clicking
[03:49:02] the lock button right there take our
[03:49:04] close button I'll move it to the bottom
[03:49:06] right or bottom right up right whatever
[03:49:09] you want I'll move my buy button kind of
[03:49:11] right there maybe in the middle I'll
[03:49:13] take my control node here here and I'm
[03:49:15] going to uh take my label and I'm just
[03:49:18] going to move everything uh to where I
[03:49:20] want it to be so this is going to be our
[03:49:22] item
[03:49:24] name this is going to
[03:49:27] be the item description and this is
[03:49:31] going to be the item uh
[03:49:34] Sprite this is going to be the
[03:49:38] item info node here I'm going to make
[03:49:41] sure that this is right around here so
[03:49:43] here I can give it a default name by
[03:49:46] like sword I'll Center everything going
[03:49:48] to take the theme override make it a
[03:49:51] little bit
[03:49:52] bigger be 40 41 whatever you'd like and
[03:49:56] I'll just kind of Center it like this
[03:49:58] this is where my item will show the item
[03:50:01] description I'm going to move this down
[03:50:02] here where the description will go say
[03:50:06] this is a item description blah blah
[03:50:09] blah and then I can turn on the auto
[03:50:12] wrap word smart can Center
[03:50:16] everything and I'll leave the text size
[03:50:18] the same the item Sprite what I'm going
[03:50:21] to do here is I'm going to search up for
[03:50:23] a PNG file find my random item and I'm
[03:50:27] going to scale it to be as big as I want
[03:50:30] it to be I'm going to try to keep it
[03:50:31] consistent so here maybe I'll do 13 by3
[03:50:35] and just leave it around there maybe
[03:50:37] I'll move that down move this to the
[03:50:39] right and just readjust things as how
[03:50:41] you want it to be the grid container I'm
[03:50:43] going to rename it to shop
[03:50:45] items I'll move this to the right hand
[03:50:48] side right over here this is where all
[03:50:50] my shop items will
[03:50:52] appear okay now I want to fill this in
[03:50:55] and so to fill this in I need to First
[03:50:57] have a script let's add a shop script we
[03:51:01] put this in our scripts folder player
[03:51:03] GUI and open create now in here we're
[03:51:08] going to have a few things so to get
[03:51:11] started what we're going to do is we're
[03:51:13] going to create a current item
[03:51:16] Cent item like so and this is going to
[03:51:18] be an item data now before we continue
[03:51:21] we need to now create our uh packed
[03:51:24] scene that is going to represent our
[03:51:26] item slot kind of like we did for our
[03:51:28] inventory but this time we're going to
[03:51:30] create it a a bit more manually so to do
[03:51:33] this we'll create a new scene here we
[03:51:35] will create a panel as the
[03:51:38] default zoom in we will add uh we can
[03:51:41] just drag in one of these guys we can
[03:51:45] make the scale three move this here move
[03:51:50] the panel to be a little bigger here
[03:51:52] move this in the middle the panel a
[03:51:55] little bigger once more we can make the
[03:51:57] layout to be 64x
[03:52:01] 64 and we can move this item in the
[03:52:03] middle and then lastly we can add a
[03:52:05] button I'm going to cheat a little bit
[03:52:08] because what I'm going to do I'm going
[03:52:10] to take this button take its theme I'm
[03:52:14] going to take it theme override go to
[03:52:17] style and I'm going to go to press empty
[03:52:22] box I'm going to go to
[03:52:26] visibility self modulate and make it
[03:52:29] invisible and here
[03:52:32] um going actually scale it so going to
[03:52:35] remove the theme I don't really care
[03:52:36] about the theme I'm just going to scale
[03:52:38] it so I'm going to cheat a little bit
[03:52:39] and make this button a bit smaller on
[03:52:41] the x axis I'll make this point
[03:52:45] 75 and there we go there we have our uh
[03:52:49] button so this will act as our shop
[03:52:51] button I'm going to save this as a shop
[03:52:54] item save it in
[03:52:56] here I'm going to rename this to shop
[03:53:00] item I can rename this to image I'll add
[03:53:04] a script this guy add a script to the
[03:53:07] scripts folder player
[03:53:10] DUI uh we'll put in here now in this
[03:53:13] script it's not too difficult what we'll
[03:53:15] do is I'll just create and I'll pop this
[03:53:18] out and I'll just close other tabs for
[03:53:21] now so I have it a bit more organized
[03:53:23] I'm going to create a variable item info
[03:53:26] this is going to be a item data and then
[03:53:29] I'm going to close this one real quick
[03:53:32] and connect the Pressed button if I
[03:53:35] press this all I need to do is fill in
[03:53:38] information in my shop so what I'm going
[03:53:40] to do here is I'm going to click a item
[03:53:42] and then fill in this information
[03:53:45] okay to do that all I'm going to do I'm
[03:53:47] going to say uh go to our item shop here
[03:53:50] to our press button I'll say get
[03:53:55] node get parent get parent and we'll say
[03:53:59] do curent item is equal to item info
[03:54:05] next I will say get node uh well
[03:54:08] actually just copy this right
[03:54:10] here but instead of this I'm going to
[03:54:12] say get the item
[03:54:14] info and I'm going to show this and this
[03:54:18] this thing right here is this guy so
[03:54:21] this is going to let us show or hide
[03:54:23] this so if I do click something
[03:54:24] obviously I want to show it right I want
[03:54:26] to show that item that is being
[03:54:28] presented in my
[03:54:29] shop next I'm just going to copy paste
[03:54:31] this a few times I'll change this or I'm
[03:54:34] going to add to it I'm going to say item
[03:54:36] name is going to be equal
[03:54:38] to the text is going to be equal
[03:54:41] to the item info
[03:54:44] do item
[03:54:46] name the next one is going to be the
[03:54:49] item
[03:54:51] description that one is going to be a
[03:54:53] text as well for this one I can actually
[03:54:56] what we'll do is I'm going to close my
[03:54:57] script I'm going to hit control shift F
[03:55:01] I'm going to find the thing that says
[03:55:03] stats and in here I'm just going to copy
[03:55:07] this so here I'll just copy from
[03:55:10] stats and after that go back to my shop
[03:55:14] item it pop this out and paste this but
[03:55:18] here I need to make sure that there's a
[03:55:21] string here I'm just going to show the
[03:55:23] stats the damage defense and health here
[03:55:26] I don't need the item name I don't need
[03:55:29] the
[03:55:30] description I could add the description
[03:55:32] actually so here why don't I add the
[03:55:34] percent s here for the description and
[03:55:36] then new line with stats we'll have the
[03:55:39] item damage item defense and item
[03:55:42] Health lastly we'll do the uh this is
[03:55:46] actually an invalid path so item info
[03:55:49] item description text is equal to that
[03:55:52] uh here it's saying data is not a thing
[03:55:54] which makes sense because here I have
[03:55:56] item info instead of data make sure to
[03:55:59] replace the data with item
[03:56:01] info and lastly uh the item info here
[03:56:05] this one is going to be the item
[03:56:07] Sprite and hopefully you can guess how
[03:56:09] we do this all we need to do is set the
[03:56:11] texture for this guy equal to the item
[03:56:14] info. item texture there we go now we
[03:56:18] filled in the information with uh the
[03:56:21] sword right so now what we need to do is
[03:56:23] actually create those items though we
[03:56:25] need to create those shop items that I
[03:56:27] just created to do that all we need to
[03:56:30] do is preload at shop item so I'll say
[03:56:34] on ready
[03:56:35] variable shop item scene it's a this is
[03:56:40] a packed
[03:56:41] scene this is going to be equal to a
[03:56:43] preload
[03:56:45] um shop item we'll preload that script
[03:56:48] that I just made going to save we go to
[03:56:52] function ready I'll for loop I in game
[03:56:56] items so I'm going to for Loop through
[03:56:58] all the items I have in my game that
[03:57:01] exist I'll say if I uh don't need
[03:57:06] that we'll say variable
[03:57:09] shop item temp is equal to shop item
[03:57:14] scene. instantiate we want to create
[03:57:17] this scene and then start adding them so
[03:57:19] before we start adding them or we'll
[03:57:22] just add it and then see what we need to
[03:57:23] do before that next we'll get our shop
[03:57:26] items which is going to be our grid and
[03:57:28] we'll just add
[03:57:30] child item Temp and before we add them
[03:57:33] we need to fill in the information which
[03:57:35] is not too hard because we're for
[03:57:37] looping here so we can just say this
[03:57:39] item info is equal to game do
[03:57:45] items at position
[03:57:47] I next we can just get the item temp.
[03:57:52] get node uh image and then fill in the
[03:57:55] texture for that then make it equal to
[03:57:58] game. items at I the item
[03:58:04] texture just double check that's right
[03:58:07] so item texture we're filling in the
[03:58:10] shop item texture so this guy right here
[03:58:13] the image
[03:58:15] let's actually make sure I said that
[03:58:16] right yes
[03:58:18] image okay and lastly what we'll do is
[03:58:22] I'm going to get in the ready function
[03:58:24] I'm going to get this guy not this guy
[03:58:27] actually I'm going to get the item
[03:58:30] info and hide it I don't want to show an
[03:58:33] item in here unless I'm clicking an item
[03:58:36] so let's hit play and see what we
[03:58:38] get all right so we get an error right
[03:58:40] away um it is because
[03:58:44] item
[03:58:48] texture okay so saying the key item
[03:58:50] texture doesn't exist so let's take a
[03:58:52] look in our resource for item
[03:58:57] data let's find
[03:58:59] our
[03:59:04] inventory so the item
[03:59:06] data called item texture so it should be
[03:59:08] working something is going
[03:59:11] on let's just make sure I copy paste it
[03:59:14] right texture is equal to game
[03:59:18] texture okay I see so we can't be
[03:59:21] filling it in with anything empty so let
[03:59:24] me make sure here if I hit
[03:59:28] play
[03:59:31] okay let me figure out what's going on
[03:59:33] and I'll be right back okay so in case
[03:59:35] you were getting that error or not um
[03:59:38] generally those kind of errors are kind
[03:59:39] of annoying uh and what I ended up just
[03:59:41] doing is reloading the project and
[03:59:44] sometimes the resources kind of don't
[03:59:47] load fully unless you restart the
[03:59:48] project so just reload the project and
[03:59:51] make sure that all the textures have a
[03:59:52] texture otherwise you might get some
[03:59:54] weird errors so let's continue um now if
[03:59:57] I hit play you will see that I have my
[04:00:01] shop filled with the items that I have
[04:00:03] now obviously the shop isn't functioning
[04:00:04] fully because I need to actually make
[04:00:07] this work a bit nicer right so let's
[04:00:09] just continue and we'll kind of
[04:00:11] implement this a bit so first let's make
[04:00:14] sure our
[04:00:15] buy is connected and our close so here
[04:00:19] what we're going to do for the close is
[04:00:21] actually quite easy just pop this
[04:00:23] out all I need to do is get
[04:00:26] tree paused is equal to false we'll say
[04:00:31] oops that's not false we'll say game.
[04:00:34] shopping is equal to
[04:00:37] false I'm going to say
[04:00:40] input input Dot Mouse mode is equal to
[04:00:47] input mous mode
[04:00:49] captured self. hiide this will basically
[04:00:53] close my shop now on the buy this is
[04:00:56] actually pretty easy all I need to do is
[04:00:58] say get node go up one I'm going to get
[04:01:02] container inventory and then add child
[04:01:06] now at this point the child that we want
[04:01:08] to add is the string of the current item
[04:01:13] do item name now here's where things
[04:01:16] might get a bit iffy if the item name
[04:01:18] that I'm trying to add is different than
[04:01:20] the like child then this might not
[04:01:25] work okay that doesn't make oh add uh
[04:01:29] item there we go add item and then
[04:01:32] string so what I mean by that is in my
[04:01:36] iron body for example this needs to be
[04:01:39] the same thing as my game here it says
[04:01:43] iron body and it's the same here same
[04:01:45] thing for the iron sword it needs to be
[04:01:47] the exact same long
[04:01:49] sword uh so this one's called iron sword
[04:01:52] so let's change that to long sword and
[04:01:54] small potion small potion needs to be
[04:01:57] capitalized okay everything has to be
[04:02:00] the exact same otherwise it won't work
[04:02:02] with this right okay now to give this uh
[04:02:06] go in our 3D scene here we're going to
[04:02:09] add a AI or a kind of NPC guy this NPC
[04:02:12] is going to allow us to interact with
[04:02:14] our
[04:02:15] shop okay so to do this we'll create a
[04:02:17] new
[04:02:18] scene we'll create an area
[04:02:21] 3D we'll add a adventure just a random
[04:02:24] guy you can go up to the top and find a
[04:02:29] adventure we can find
[04:02:32] a maybe a mage pop this guy in make it
[04:02:36] local and I'll hide the
[04:02:39] Spellbook open one-handed wand agage hat
[04:02:45] I'll show that and I'll show the rest
[04:02:47] now for the animation player I'll just
[04:02:50] play the idle by default I'll play this
[04:02:54] like so and then Loop this okay so I
[04:02:57] can't Loop this so uh what I'll do is
[04:03:00] I'll let's add a collision first add a
[04:03:03] collision
[04:03:04] shape hit play We'll add a c we're not
[04:03:07] going to add a capsule we're going to
[04:03:08] add a circle here or maybe a cylinder
[04:03:11] make this a little higher a little
[04:03:13] bigger
[04:03:14] we'll save this in our scene here we'll
[04:03:16] save it in here why not and we'll save
[04:03:19] this as NPC
[04:03:22] Mage now what we can do is head over to
[04:03:24] level one and find our
[04:03:27] NPC I I called it npv so let's rename it
[04:03:32] new
[04:03:36] npt all right let's pop this guy in put
[04:03:39] him right behind us and I'll just rename
[04:03:41] him to NPC We'll add script to this
[04:03:47] guy go add a script the script I'm going
[04:03:50] to add it into
[04:03:52] the folder we'll just add it right here
[04:03:56] create and what I want to do is connect
[04:03:58] the uh body
[04:04:01] entered and you might imagine we need to
[04:04:04] check to see if this body is in group
[04:04:07] layer if it
[04:04:10] is what we'll do is we will uh do the
[04:04:14] things that we need to do so what do we
[04:04:16] need to do well first I need to say
[04:04:18] game. shopping is equal to True
[04:04:21] next I'm going to pause the scene and
[04:04:24] get paused or get
[04:04:27] free paused is equal to True next I'll
[04:04:32] get node go up one go up one ui/ shop
[04:04:37] and then show the shop next I'm going to
[04:04:40] make sure my input
[04:04:42] Mouse mode
[04:04:44] is equal to um
[04:04:48] visible right so I want to be able to
[04:04:50] show my mouse here now what I'm going to
[04:04:52] do because I couldn't Loop this
[04:04:53] animation all I'm going to do is I'm
[04:04:55] going to go to animation finished
[04:04:57] connect this and every time that
[04:04:59] animation finishes I'll just say get
[04:05:02] this animation player then play the idle
[04:05:06] animation
[04:05:07] again it has to be the same name as this
[04:05:11] right now that's pretty much it this is
[04:05:13] our NPC see let's hit save let's hit
[04:05:16] play now we should be able to test our
[04:05:18] game
[04:05:20] here okay so let's let's just go okay
[04:05:24] let's let's go to our shop we'll go into
[04:05:27] here and we'll say self
[04:05:31] hide hit
[04:05:35] play all right now that our shop is
[04:05:37] hidden we can go into here and see that
[04:05:39] we get an error okay so it's saying that
[04:05:41] this path doesn't exist and that is
[04:05:43] because this guy needs to be in the
[04:05:45] objects tab let's H play one more
[04:05:50] time over here okay here we go here's
[04:05:53] our shop I should be able to now
[04:05:55] interact with it now oddly enough I
[04:05:58] might actually not be able to
[04:06:01] uh seemly enough I can buy stuff but
[04:06:04] just in case I'm going to go over here
[04:06:06] and set the process to all on the shop
[04:06:08] that way I can interact with it hit play
[04:06:11] one more time and just make sure that I
[04:06:12] can actually
[04:06:14] buy something so here I don't have any
[04:06:16] items let's buy this iron
[04:06:19] sword and now you can see I have an iron
[04:06:22] sword and I can even use it and hover it
[04:06:24] and it says iron sword and it has the
[04:06:27] stats that I need here I should be able
[04:06:29] to replace this with the other item and
[04:06:32] it has uh I guess the same stat so let's
[04:06:34] actually change this to
[04:06:37] 10 and the iron sword should be five
[04:06:40] okay let's double test one more time
[04:06:45] here we go okay so here is our iron
[04:06:48] sword this is our long sword it says
[04:06:50] stat 10 damage so that's good let's buy
[04:06:53] it and here we go here's our sword and
[04:06:56] this one should do 10 damage whereas if
[04:06:59] I buy the other
[04:07:01] one so this
[04:07:03] one this one is only five okay cool
[04:07:07] let's just make sure it works in the
[04:07:08] profile
[04:07:10] yep all right there we go so there we go
[04:07:12] we can see it works all right so that's
[04:07:15] our shop that's pretty good all right so
[04:07:17] in the next part we'll Implement our
[04:07:19] level up system all right the last thing
[04:07:22] we need to do before we head into the
[04:07:24] environmental things is the level up
[04:07:26] system this one is not too difficult as
[04:07:28] we already have a lot of things for it
[04:07:30] already set up let's head over to our
[04:07:32] script go to our game and pop this out
[04:07:36] now if you recall we created this level
[04:07:38] up signal but we're not using it so
[04:07:40] let's figure out if we can do something
[04:07:43] with it now to gain XP it's really easy
[04:07:46] right all we need to do is take our
[04:07:48] current XP and add the XP amount uh
[04:07:51] we'll change we'll say XP amount like
[04:07:55] this and we will change the amount to XP
[04:07:58] amount like that now what we need to do
[04:08:00] here is say while press enter a few
[04:08:04] times while the current Uh current XP
[04:08:10] is greater than or equal to X P to the
[04:08:14] next level then we're going to start
[04:08:18] leveling up so the first thing we'll do
[04:08:20] is well we'll level up we'll level up we
[04:08:24] will take our player health max and add
[04:08:29] the player
[04:08:30] level time 10 so that's just like one
[04:08:33] example of a stat adjustment essentially
[04:08:36] we can full heal ourself by saying
[04:08:38] player health is equal to player health
[04:08:41] max we can take now take our current XP
[04:08:45] and subtract the amount of XP I I was
[04:08:48] supposed to add or I can subtract the XP
[04:08:51] to Next Level now the advantage of this
[04:08:54] is if I want to level up more than once
[04:08:57] while I'm kind of doing this and this is
[04:09:00] how we do it inside of a while loop now
[04:09:03] I'm going to take my XP to the next
[04:09:05] level and I'm going to round it to the
[04:09:08] XP to the next level time
[04:09:12] 1.3 and then I'm going to take it again
[04:09:15] and then I'm going to multiply it
[04:09:18] multiply Itself by the power of
[04:09:23] 1.2 with the player
[04:09:26] level minus
[04:09:29] one this is kind of the previous level
[04:09:31] because over here I already added it so
[04:09:33] this is the previous level okay so this
[04:09:35] kind of gives me an exponential growth
[04:09:38] for my XP so now what I can do the last
[04:09:41] thing that we will add but we're not
[04:09:43] going to use just yet is we're going to
[04:09:45] emit the signal level
[04:09:47] up so that signal that we created we're
[04:09:50] going to emit it but we're not going to
[04:09:52] use it just yet because uh this is kind
[04:09:54] of where we'll go into our uh bfx a
[04:09:58] little later so we're going to actually
[04:10:00] Implement um some of the logic for it
[04:10:02] specifically our level up animation so
[04:10:06] um we can connect it right now so let's
[04:10:07] actually do that let's head over to our
[04:10:09] level one go to our
[04:10:12] player we will go to the script open
[04:10:15] this
[04:10:16] up and similarly to before when we
[04:10:19] connected our signal I'm going to just
[04:10:21] uh kind of Pop all these down so that
[04:10:24] way I can see my code a little nicer now
[04:10:27] in my ready
[04:10:28] function if you remember we need to get
[04:10:31] access to the node the game node we can
[04:10:34] do that by saying game node is equal to
[04:10:36] get node
[04:10:39] game G game. get path
[04:10:44] then we can to say game node do level up
[04:10:48] that signal that we created connect
[04:10:52] followable we will connect it to the
[04:10:54] self self and then we'll connect it to a
[04:10:58] signal that we can create we can say on
[04:11:01] level up uh level up like this then of
[04:11:05] course we need to put this in a string
[04:11:07] and that's pretty much it now we need to
[04:11:09] create this function on the
[04:11:11] bottom and here we we go this is our
[04:11:14] function that we've created now this
[04:11:16] function will trigger uh when the signal
[04:11:18] is called right so here I can just
[04:11:20] print uh yeah let's print the game.
[04:11:23] player level just to make sure this
[04:11:26] works let's hit close here and let's hit
[04:11:28] play and now if you remember we should
[04:11:31] be able to gain 100 XP when I kill the
[04:11:33] monster so let me just equip some things
[04:11:35] here and let's kill
[04:11:38] it and now we go to profile we should
[04:11:41] see level two and we see level one the
[04:11:44] reason it's one is because it's emitting
[04:11:46] the uh previous level basically so we'll
[04:11:49] need to it doesn't really matter because
[04:11:51] the signal is more so for an animation
[04:11:54] that will add later anyway so we don't
[04:11:56] really care about the level that's being
[04:11:58] printed we just care that this is being
[04:11:59] updated right here which it is and the
[04:12:01] XP is being updated which is perfect so
[04:12:04] um we're pretty much good to go and even
[04:12:07] see that the health is being increased
[04:12:09] so that is pretty much it for most of
[04:12:12] the logic in our game in next few
[04:12:14] sections we're going to be taking a look
[04:12:15] at our environmental things how we can
[04:12:17] make sure our environment looks good uh
[04:12:20] we're going to start playing around with
[04:12:21] our world environment again as you might
[04:12:23] have noticed we have been getting errors
[04:12:25] depending on whether or not set things
[04:12:28] up similarly to what I did but yeah so
[04:12:30] let's get started into the next part
[04:12:33] which is the Environmental section right
[04:12:35] the first thing we need to do is we need
[04:12:38] to actually fix our engine now what do I
[04:12:40] mean by that well on the top right we
[04:12:42] will see a compatibility now do make
[04:12:45] sure that you have it on forward plus
[04:12:48] I'm going to select forward plus and I'm
[04:12:50] going to save and
[04:12:52] restart right once you've launched the
[04:12:54] game again you might have noticed a few
[04:12:56] errors but don't worry just okay andore
[04:12:59] them and if you hit play you will
[04:13:01] immediately notice a very big difference
[04:13:03] scene you will already notice that the
[04:13:06] scene is very thick kind of just a very
[04:13:08] different environment okay now what we
[04:13:11] can do is head over to our EnV
[04:13:13] environment node we're going to enable
[04:13:15] the glow now as now we have the proper
[04:13:18] things that we'll need in here I'm going
[04:13:21] to turn on the normalized go to blend
[04:13:25] mode and select ad dative ad dative um
[04:13:30] and yeah so that's pretty much it for
[04:13:31] the glow and make sure the settings for
[04:13:33] all these are the same of course at this
[04:13:35] point remember you can always just
[04:13:36] adjust these accordingly to whatever
[04:13:38] you'd like make it thicker thinner
[04:13:40] whatever you'd like right so now
[04:13:43] uh that's pretty much it for the world
[04:13:44] environment now for the grid map I'm
[04:13:47] going to set the cell size over here
[04:13:49] four four and four now we can see here
[04:13:53] though that the air is under the ground
[04:13:56] so what I'll do is I will take my grid
[04:13:58] map and I could either pull this down or
[04:14:02] I can actually just go to level one and
[04:14:05] that is where I'll paint my ground here
[04:14:07] I'm going to go back to level zero and
[04:14:09] remove my ground by pressing delete to
[04:14:13] floor Z or
[04:14:15] sorry1 I will draw my floor here by
[04:14:19] control
[04:14:22] fill uh let's just make sure I'm doing
[04:14:24] it
[04:14:25] right in order to fill we should be
[04:14:28] saying uh well I actually actually
[04:14:30] select a thing so that would make sense
[04:14:33] so let's select a tile and fill in an
[04:14:36] area that I want there we go now I
[04:14:38] should be able to fill it in properly
[04:14:40] and now we have our ground it works the
[04:14:41] exact same but this just allows us to
[04:14:43] properly distance things now here's our
[04:14:46] issue is that when I start adding walls
[04:14:48] it's going to remove the floor I don't
[04:14:51] want that so what I'll do is I'm going
[04:14:52] to rename this grid to
[04:14:55] floor and I'll duplicate this and what
[04:14:58] I'm going to do is in my I'm going to
[04:14:59] make the floor invisible and delete make
[04:15:02] sure floor two is selected and delete
[04:15:04] this floor I'm going to rename this two
[04:15:07] walls and now I'll show the floor and
[04:15:10] now what I can do is start drawing on
[04:15:12] the wall section and of course we can
[04:15:14] make sure we're on1 and at this point we
[04:15:17] can start kind of going wherever I'd
[04:15:19] like so here what I'll do is I'll draw
[04:15:22] right here and I can just whoops select
[04:15:27] like this and contrl F and fill in a
[04:15:31] large wall and at this point I can just
[04:15:34] start be adjusting everything so in
[04:15:37] order to rotate this you just click s to
[04:15:40] rotate it so that way we can have it
[04:15:43] rotated to that way I want to rotate
[04:15:46] this wall this way I'll fill it in like
[04:15:51] this and at this point you can just
[04:15:53] start moving around the scene and just
[04:15:55] fill in uh the walls that you
[04:15:59] want keep those two
[04:16:02] walls and here we go I'll kind of do
[04:16:05] this together with you so at this point
[04:16:07] you can either skip or you know just
[04:16:09] kind of zoom in and do do yourself but
[04:16:12] I'm just going to keep doing this
[04:16:14] together so that way we don't skip any
[04:16:16] big steps here lastly we'll have that
[04:16:18] wall
[04:16:20] there and I'll
[04:16:22] just
[04:16:25] Wall go all the way and we can delete
[04:16:28] this wall and put a corner wall instead
[04:16:31] all right so there we go we have a fully
[04:16:34] encased dungeon here so what I'm going
[04:16:37] to do now is I'm going to put a wall
[04:16:38] right here
[04:16:41] so or I can just put it right
[04:16:44] there and fill in wall section in the
[04:16:48] middle like that I'll put a door kind of
[04:16:52] maybe right there and one right there
[04:16:55] then I can kind of just start doing
[04:16:58] whatever I'd like at this
[04:17:00] point now we do notice that there is
[04:17:02] this Gap so at this point you can either
[04:17:05] duplicate again which is actually what
[04:17:07] I'm going to do because this is a bit
[04:17:09] quicker here I'll just duplicate and
[04:17:11] start filling in the sections that I
[04:17:14] want and here of course it doesn't look
[04:17:17] perfect so this is where you would
[04:17:19] probably need to uh finish the mesh
[04:17:21] library and start adding in the walls
[04:17:23] that you might need if you search up
[04:17:25] wall you might be able to find the wall
[04:17:28] that you'll need um it might
[04:17:31] be it's probably one of these um I know
[04:17:33] it is one of these I have seen it it's
[04:17:35] just uh I don't have it complete so
[04:17:38] we're not going to do that in this
[04:17:39] series that's more of a level design um
[04:17:41] as we're just going to kind of continue
[04:17:43] this level so here we now have our level
[04:17:47] so we can just start drawing make sure
[04:17:49] I'm on the walls wall to I can just keep
[04:17:52] drawing whatever I
[04:17:55] like I'll just kind of draw out a few
[04:17:58] levels here or areas if that makes
[04:18:01] sense and I'll put in this guy maybe
[04:18:05] I'll put that like
[04:18:07] here
[04:18:09] and yeah so you can kind of fill in the
[04:18:11] rest of the level I'm going to now move
[04:18:14] my player over here to the kind of
[04:18:16] corner over here so this is the starting
[04:18:18] area now when I hit
[04:18:20] play we will see my level here is my
[04:18:25] level I can start running around and
[04:18:28] it's my Mage and my monster obviously
[04:18:31] the Mage will have to readjust to make
[04:18:32] sure he's on the floor so let's do
[04:18:35] that let's take our
[04:18:37] NPC uh and we'll drag him to the right
[04:18:40] side and we can just
[04:18:43] B him
[04:18:44] down and we'll maybe rotate him and of
[04:18:47] face the
[04:18:49] corner and we can make sure he's kind of
[04:18:53] looking like he's on the floor put him
[04:18:55] right there maybe floating a tiny bit
[04:18:57] now when I hit play one more
[04:19:01] time we can now walk up to him and he
[04:19:03] looks like he's standing there walk up
[04:19:06] to him interact with the shop close it
[04:19:08] and keep running around okay cool now
[04:19:12] what we'll do is I'm going to now head
[04:19:15] into or we're going to head into the
[04:19:17] torch section so we're going to take a
[04:19:18] look at how we can create a torch and
[04:19:20] add some lighting into our scene let's
[04:19:22] take a look at how we can do that okay
[04:19:25] so to get started with our torch I'm
[04:19:27] just going to close everything from the
[04:19:29] level right click close tabs to right
[04:19:33] make a new scene here and I'll create a
[04:19:36] uh node 3D as the
[04:19:38] base I'm going to search up TCH and find
[04:19:42] the lit torch actually sorry not the lit
[04:19:45] torch just the mounted torch here we go
[04:19:49] I'm going to reset this
[04:19:51] 0 make it local bring in the torch
[04:19:55] delete this guy I'll add two things an
[04:19:59] omn
[04:20:00] light and a GPU particles this is where
[04:20:04] all the magic will happen Okay so in
[04:20:07] this guy this is where we're going to
[04:20:09] actually add and uh start adjusting all
[04:20:11] the particles I'll try to go slow and
[04:20:14] we'll try to do as much as we can
[04:20:16] together to make this as pretty as
[04:20:17] possible so to start what we need to do
[04:20:20] is we need a draw pass and process
[04:20:23] material this is where we will add the
[04:20:27] draw pass so meaning let's actually just
[04:20:29] do this so if I go to path one I will
[04:20:32] add
[04:20:33] a ash plane where is that
[04:20:38] plane and now uh we want to or sorry not
[04:20:41] plane uh quad mesh where is that quad
[04:20:44] mesh there we go now you can see that we
[04:20:46] have this quad mesh here now it's not
[04:20:48] moving because there's no gravity
[04:20:50] there's no things being adjusted to it
[04:20:52] but that's okay first we're just G to
[04:20:54] make sure this guy is pretty and do it
[04:20:57] make it material wise what we want it to
[04:20:59] be so we'll go to the material we're
[04:21:02] going to select new standard material
[04:21:04] we'll go into this and now we can start
[04:21:07] coloring it to be what I want it to be
[04:21:09] we'll go to
[04:21:11] transparency I'm going to uh select the
[04:21:15] alpha make it transparent between uh the
[04:21:19] things just okay on
[04:21:21] that I'm going to go to blend and go to
[04:21:25] add and we'll just C okay uh you might
[04:21:29] have to restart your project if I keep
[04:21:30] getting that we'll do that a little
[04:21:31] later go to shade
[04:21:34] unshaded and then we will
[04:21:36] select the vertex color going to turn on
[04:21:40] the albo
[04:21:43] and we will go to Alo and now we will
[04:21:45] actually select the color we want now at
[04:21:48] this point you can do whatever you'd
[04:21:49] like I'm going to select kind of a dark
[04:21:52] orangish color so maybe kind of right
[04:21:55] around
[04:21:56] here maybe a bright orange kind of like
[04:21:59] this um something like that okay so kind
[04:22:03] of pick whatever you'd like all right so
[04:22:05] now for the billboard on the bottom
[04:22:06] we'll go to mode article
[04:22:11] billboard okay
[04:22:13] and then we're going to turn on the
[04:22:15] scale keep scale
[04:22:17] on okay I'm getting annoyed by this I'm
[04:22:21] just going to restart my project and
[04:22:22] make sure that airor doesn't pop up I'll
[04:22:24] be right
[04:22:25] back all right so I've restarted my
[04:22:27] project and no more errors okay let's
[04:22:29] scroll up a little bit we're going to go
[04:22:31] to the process material now this is
[04:22:33] where the magic will happen this is
[04:22:35] where I'm going to actually essentially
[04:22:38] start of adding the particles well here
[04:22:41] we'll go to new particle material and
[04:22:44] you can see right away when I add this
[04:22:46] it's already doing something now what we
[04:22:48] want to do first is we want to uh adjust
[04:22:52] certain things the first thing we're
[04:22:53] going to do is go into spawn we're going
[04:22:56] to go into the uh angle and we're going
[04:23:00] to change this to 360 for the Max and
[04:23:04] that's it now you can see that it is
[04:23:06] rotating kind of
[04:23:09] randomly next we'll go into the velocity
[04:23:12] right under it we will go into the
[04:23:15] direction we'll set this to zero the Z
[04:23:18] we set it to
[04:23:21] 042 five and then the spread I'm going
[04:23:25] to set it to
[04:23:27] zero type in
[04:23:29] zero and the initial velocity we will
[04:23:32] set the max to three and now we have a
[04:23:36] bit more of a jump for our particles
[04:23:38] here all right so that's our
[04:23:41] velocity next next we want to go to out
[04:23:44] of Spawn into animated velocity we will
[04:23:47] go into the angular velocity and in here
[04:23:50] we're going to set the max to uh 40 or
[04:23:54] 30 we can do 40 though all right so
[04:23:58] that's the angular velocity next we're
[04:24:00] going to go to the acceleration gravity
[04:24:03] and we're going to turn off the gravity
[04:24:04] and put it to zero now at this point you
[04:24:07] can kind of mess around with some of
[04:24:09] these obviously you can see that now
[04:24:11] it's kind of being pushed to the right
[04:24:13] but of course you can push it to
[04:24:14] whatever you'd like all right so now we
[04:24:17] want
[04:24:19] to head over to the linear acceleration
[04:24:22] in the linear acceleration I'll set this
[04:24:24] to one and five it accelerates a bit
[04:24:29] more we'll go to the scale which is
[04:24:32] going to be in the
[04:24:33] display in the display we're going to go
[04:24:35] to scale we're going to go to the scale
[04:24:39] itself and set this to 0.01
[04:24:42] and
[04:24:43] 0.5 this will just make the actual
[04:24:46] particles much
[04:24:47] smaller next we're going to go to the
[04:24:49] color curves and this will allow us to
[04:24:52] kind of curve the initial ramp here
[04:24:54] we'll add a new uh initial ramp
[04:24:58] here go down sorry I guess it went up a
[04:25:00] little bit for no reason we'll go into
[04:25:03] here into the gradient and at this point
[04:25:05] this is where you can kind of start
[04:25:07] picking your colors I'm going to pick
[04:25:09] the left one into making it a red one
[04:25:12] kind of a dark
[04:25:14] redish so and then the middle one I'll
[04:25:17] make it kind of a uh grayish color like
[04:25:21] so and then the very right I'll make
[04:25:23] this a orange
[04:25:25] color something like this and now we
[04:25:28] have just kind of a different uh color
[04:25:31] and radiant now if I click out of it
[04:25:34] you'll see kind of
[04:25:36] that okay so now that's the color curves
[04:25:39] let's undo that or go out of it
[04:25:43] we'll go to the Hue variations and
[04:25:45] inside of this I'm going to set this to
[04:25:48] 0.2 and this to
[04:25:51] positive2 we're going to go to the curve
[04:25:53] texture create a new curve texture go
[04:25:56] into the curve and I'm going to add a
[04:25:58] point right here and drag this down and
[04:26:01] drag this around the middle like so now
[04:26:04] I'll just do that hit save contrl s and
[04:26:09] lastly I'm going to go to turbulence
[04:26:11] turn this on
[04:26:13] and it might lag a tiny bit there we go
[04:26:16] now it's kind of going upwards a tiny
[04:26:18] bit and now I can kind of adjust some of
[04:26:20] these back down to turbulence and I'm
[04:26:23] going to adjust the noise speed to 07
[04:26:27] just a little less than what it
[04:26:28] currently is and now what we want to do
[04:26:31] is go to the very top and turn up the
[04:26:34] amount to
[04:26:35] 500 and now you can see we have fire now
[04:26:40] this isn't perfect but another another
[04:26:42] thing or another issue I'll say is that
[04:26:44] it's upside down so of course we can
[04:26:47] rotate it if we'd like like
[04:26:50] so um or we can actually not can but
[04:26:53] we're going to actually have to do this
[04:26:54] in the direction so let's just reset the
[04:26:56] rotation here and we'll head over
[04:27:00] to so now we see that it's going in the
[04:27:03] right direction for some reason that's
[04:27:05] perfect now we'll move it into the
[04:27:08] mounted area kind of and there we go now
[04:27:12] we'll go into our level one we'll go
[04:27:14] into our objects we'll find our torch
[04:27:18] that we hopefully
[04:27:19] saved and pop this
[04:27:22] in now I'll take my torch here and just
[04:27:26] kind of move it to be on the side of the
[04:27:30] wall here so kind of put it right there
[04:27:34] and if I zoom in a tiny bit you'll see
[04:27:38] that and just move it in ever so
[04:27:41] slightly maybe move it to the side and
[04:27:44] just kind of move it to wherever you'd
[04:27:46] like it to be and now what I could do is
[04:27:48] I can turn on snap and I'll just snap
[04:27:51] this over here I'll duplicate this just
[04:27:54] snap it a few pixels over snap snap and
[04:27:58] just duplicate a few of these now what I
[04:28:00] can do is I can duplicate all of these
[04:28:04] rotate it by about
[04:28:07] 180 and then I can move this guy all the
[04:28:09] way to the other side of the wall now
[04:28:12] obviously this guy right here I don't
[04:28:15] want this so I'll delete this and now
[04:28:17] when I hit
[04:28:18] play we should be able to see the
[04:28:20] Torches in the
[04:28:23] game all right here we go there's our
[04:28:25] torches now I do suggest you play around
[04:28:28] with some of the values in fact I'll
[04:28:30] probably do that as well to make it a
[04:28:32] little less but this is not bad so far
[04:28:35] so yeah it's pretty good maybe we can
[04:28:37] reduce the amount that it's being
[04:28:39] expected um in fact actually this one is
[04:28:42] not on a wall so let's just delete this
[04:28:44] one and another thing that you can take
[04:28:46] a look at is in the world environment in
[04:28:48] the glow you can go to the uh some of
[04:28:51] these settings and increase or decrease
[04:28:54] some of these so if you look at the
[04:28:55] intensity you can decrease the glow of
[04:28:57] the fire if you increase it obviously
[04:29:00] that's probably too much you can look at
[04:29:02] the strength of it and go to the bloom I
[04:29:05] don't really suggest the bloom too much
[04:29:06] Bloom is kind of a weird threshold we
[04:29:09] can look at the HDR threshold and just
[04:29:11] play around with some of these values uh
[04:29:13] they're pretty fun to play around with
[04:29:14] you can also play around with soft light
[04:29:16] maybe some of the other ones um I find
[04:29:19] ad dative to be I wouldn't say the best
[04:29:22] but it's probably the nicest in a sense
[04:29:24] to kind of add to our game so yeah so
[04:29:27] this is pretty nice um if you want to
[04:29:29] get rid of that like random Direction
[04:29:31] you can turn off the turbulence which I
[04:29:34] think I'll actually do here so I'm going
[04:29:35] to turn off the turbulence and here we
[04:29:38] have the direction kind of going in a
[04:29:39] weird angle so let's go to the
[04:29:43] Gravity the directional velocity here
[04:29:47] spawn velocity here we can kind of
[04:29:51] adjust
[04:29:54] the velocity a little bit to whatever
[04:29:57] we'd like or sorry the direction but
[04:29:59] here maybe I can set it to
[04:30:02] 0.2 the random
[04:30:05] Direction
[04:30:08] 01 and this one I'll do yeah that's not
[04:30:12] bad okay and we can kind of adjust some
[04:30:15] of these maybe the initial velocity I
[04:30:16] want it to max out at two and now if we
[04:30:18] hit play we have maybe a more consistent
[04:30:21] fire right so there we go it's pretty
[04:30:24] long but that's okay um I like this it's
[04:30:27] not too bad it looks pretty wonky but
[04:30:30] looks pretty nice okay so there's our
[04:30:32] environmental flame now in our next
[04:30:35] section we'll be introducing a new
[04:30:36] instructor to introduce you to some much
[04:30:39] better GPU particles some better uh
[04:30:42] articles in general and some cool Shader
[04:30:44] stuff so let's take a look at who's
[04:30:47] going to be your instructor for the next
[04:30:50] hour all right so introducing lelu lelu
[04:30:53] will be um your next instructor for the
[04:30:55] next about 45 to 50 minutes um he will
[04:30:58] be showing you some cool effects some
[04:31:00] puff effect a level up effect Etc and a
[04:31:03] hit effect as well so um definitely
[04:31:06] check out his channel as well he makes
[04:31:08] really cool uh just Shader videos in
[04:31:10] general he has some beam effects
[04:31:12] better fire effect than what we made so
[04:31:15] if you want a much better fire effect
[04:31:17] there is one right there for you I'm
[04:31:19] basically just I just introduced you to
[04:31:21] the GPU particles and how and what we
[04:31:24] can do with it but of course you can
[04:31:25] definitely check out his channel he will
[04:31:27] have his uh videos up as there as well
[04:31:30] so the puff effect that we'll be making
[04:31:31] here and the level up effect and once
[04:31:34] he's finished though we will be uh
[04:31:36] implementing them all into our game and
[04:31:39] of course we do already have the project
[04:31:41] files so here at the very top in our
[04:31:45] assets we have the VFX files so if you
[04:31:48] don't want this and you want to do
[04:31:50] everything from scratch you can of
[04:31:51] course just delete this but it is here
[04:31:53] in the starter project so um let's take
[04:31:56] a look at how we can get started so I'll
[04:31:58] see you all in about an
[04:32:00] hour hello guys I am Leu and today we
[04:32:04] are going to see how to create two
[04:32:06] important effects that you can see in
[04:32:09] almost every RPG games
[04:32:12] level of effects and pop effects these
[04:32:16] effects will improve a lot the
[04:32:18] atmosphere in this game and helps the
[04:32:21] player to really feel a progress in the
[04:32:23] game rather by leveling up or the
[04:32:26] killing monsters we will use the Goot
[04:32:29] particle system and some visual shaders
[04:32:32] to create these effects so let's start
[04:32:36] with the level of
[04:32:39] effect this tutorial will be the divided
[04:32:42] into three parts first let's create a
[04:32:46] basic Aura effect using particles and a
[04:32:49] visual Shader then let's improve this
[04:32:53] effect adding an expansive
[04:32:56] wave and finally let's add some extra
[04:33:00] details and coordinate all the
[04:33:03] effects okay let's go ahead and start
[04:33:07] creating the basic Aura effect
[04:33:12] so for the level up effect we first need
[04:33:15] to create a very simple mesh so let's go
[04:33:18] to blender and let's delete this and
[04:33:23] shift a to create a new cylinder mesh I
[04:33:26] want this cylinder to be on field so set
[04:33:29] the this option to
[04:33:32] nothing so let's go to edit mode by
[04:33:35] pressing T move this cylinder
[04:33:39] up and stretch it a little bit
[04:33:47] and finally press W and select shade
[04:33:51] smooth okay so this is the cylinder it's
[04:33:55] a simple long cylinder the only
[04:33:57] difference is that the pivot point is at
[04:34:01] the bottom of the cylinder so let's
[04:34:04] export this file export
[04:34:08] OBG and let's name this cyinder there
[04:34:16] long okay so we are back in Goot let's
[04:34:20] import our cylinder
[04:34:27] mesh and I want to go ahead and create a
[04:34:31] new particle system a GPU particle
[04:34:35] system and in order for these particles
[04:34:38] to work we first need to create a new
[04:34:41] particle process material and also in
[04:34:44] draw passes assigned a mesh to be used
[04:34:47] for the particle system in this case I
[04:34:49] will use the
[04:34:55] cylinder and as you can see we have a
[04:34:57] lot of cylinder meshes falling down this
[04:35:00] is because of the gravity so let's go to
[04:35:02] the particle system into accelerations
[04:35:05] and set the gravity to
[04:35:08] zero also I only need one cylinder so
[04:35:11] set the amount to
[04:35:13] one
[04:35:15] and let's change the size so let's go to
[04:35:18] display scale and set a scale of
[04:35:24] four cool this will be the area effect
[04:35:28] for the level of
[04:35:31] effect oh by the way I don't want this
[04:35:34] cylinder to cast Shadows so let's close
[04:35:38] this and let's go to
[04:35:42] geometry and set cast Shadow to
[04:35:46] off also we need a material for the
[04:35:49] cylinder so let's create a new Shader
[04:35:52] material here in material
[04:35:55] override and let's create a new Shader I
[04:35:58] want this Shader to be a visual
[04:36:00] Shader let's name
[04:36:03] it Shader
[04:36:07] cylinder houra
[04:36:13] so let's open the
[04:36:15] Shader and I want to do some changes for
[04:36:18] example I want this Shader to be the
[04:36:21] cool mode to be disabled so we can see
[04:36:23] both sides of the
[04:36:26] cylinder also I want this material to be
[04:36:30] unshaded and disable
[04:36:33] Shadows cool so let's start creating the
[04:36:39] Shader for this Shader
[04:36:42] first I want to add a gradient so right
[04:36:45] click and create a new texture
[04:36:49] 2D set it to
[04:36:51] color and select gradient texture
[04:36:55] 2D so let's edit this
[04:36:58] gradient I will pick these little points
[04:37:02] because I want this gradient to be
[04:37:07] vertical
[04:37:09] and yeah let's now now connect the
[04:37:13] gradient into the alpha
[04:37:16] Channel and we can see this little line
[04:37:20] up here so in order to fix this let's
[04:37:23] modify the gradient a little
[04:37:26] bit like
[04:37:29] so yeah this is perfect cool so we now
[04:37:33] have this gradient connected to the
[04:37:35] alpha Channel we also need a color so
[04:37:37] right click and create a new color
[04:37:40] fragment
[04:37:42] let's connect the
[04:37:44] color and also let's connect the Alpha
[04:37:48] from the color oh we cannot connect it
[04:37:51] here so let's
[04:37:54] multiply the alpha channel from the
[04:37:56] color with the
[04:38:01] gradient cool so now if we go to the
[04:38:04] particle system we go to display in
[04:38:09] color curves we can pick any color we
[04:38:12] want for the gradient let's pick for
[04:38:14] example a yellow with a row value of 2.5
[04:38:20] 2 and
[04:38:22] 0.5 a very strong yellow also I want
[04:38:26] this cylinder to disappear over the time
[04:38:29] so let's go to Alpha curve let's create
[04:38:32] a new
[04:38:35] curve and I want this cylinder to be
[04:38:38] transparent at the beginning
[04:38:43] and at the end like this or maybe
[04:38:47] something like this it goes from
[04:38:49] transparent to full opaque to
[04:38:52] transparent again at the the end of the
[04:38:54] cylinder cool so we have this
[04:38:57] interesting effect but we can make it
[04:39:00] look even more cool by adding some
[04:39:03] special textures so for example here I
[04:39:06] have a lot of
[04:39:09] textures you can use any texture you
[04:39:12] want the important part is that the
[04:39:15] texture needs to be
[04:39:17] repetitive so let's pick for example
[04:39:21] this this noise
[04:39:25] texture and I want to add this texture
[04:39:28] to the
[04:39:30] gradient so in order to do that
[04:39:35] let's pick the texture this is a black
[04:39:37] and white texture so we don't need to
[04:39:39] pick a full color just one channel and
[04:39:43] multiply this
[04:39:46] texture with the
[04:39:50] gradient like
[04:39:52] this so now we have this special texture
[04:39:55] attached to the gradient we can also
[04:39:58] move this texture over over the time so
[04:40:02] in order to do that we need to create a
[04:40:06] UV panning
[04:40:08] note with this we can move the texture
[04:40:13] and we also need to create a Time
[04:40:18] note and if we connect the time node
[04:40:21] into the
[04:40:23] offset see how the texture is
[04:40:28] moving very simple I also want to
[04:40:32] control the speed of
[04:40:34] this of this texture so let's create a
[04:40:37] new Vector 2 parameter
[04:40:41] let's name it for example
[04:40:46] speed and let's
[04:40:52] multiply the speed parameter with the
[04:40:56] time
[04:41:01] node and nothing changes and this is
[04:41:04] because we created a new parameter so
[04:41:07] let's go to the particle system let's go
[04:41:10] to the material now we have these Shader
[04:41:13] parameters and here we have the speed
[04:41:16] option let's put a speed for example
[04:41:20] of 1.5 into the x axis and three into
[04:41:26] the y axis let's do one more
[04:41:30] change let's say instead of using
[04:41:34] this noise texture we want to use any
[04:41:37] texture we want so let's delete this
[04:41:42] noise texture and instead of that let's
[04:41:44] create a new texture 2D
[04:41:50] parameter let's name it
[04:41:53] our
[04:41:56] texture set it to
[04:41:59] color and in order to use this texture
[04:42:01] we need to sample it so let's sample
[04:42:06] this and
[04:42:08] connect this texture
[04:42:15] so now if we go to the material we have
[04:42:18] the our texture property and here we can
[04:42:21] set any texture we want let's see for
[04:42:24] example this noise
[04:42:27] texture or maybe this
[04:42:31] one so feel free to try using different
[04:42:35] textures any texture you want just make
[04:42:38] sure that the texture is repetitive
[04:42:41] I will also upload these textures here
[04:42:43] in the description in case you want to
[04:42:45] use them but anyways the Shader is
[04:42:53] completed let's go back to the particle
[04:42:56] system and let's do one last change here
[04:43:00] let's go to scale and create a new curve
[04:43:06] XYZ and I want this cylinder to grow
[04:43:11] slowly up so let's go to the curve of
[04:43:14] the y axis of the
[04:43:17] scale and I want this cylinder to slowly
[04:43:21] grow from zero to
[04:43:25] one so we have this interesting
[04:43:30] effect cool the overa effect is
[04:43:33] completed now let's create the expansive
[04:43:39] wave okay so let's name this particle
[04:43:42] system for example Aura cylinder
[04:43:47] one and I want to duplicate this
[04:43:50] cylinder so contrl
[04:43:52] D now we have the ARA cylinder 2 and I
[04:43:56] want to do some changes to this new
[04:43:58] cylinder so let's go to the particle
[04:44:00] process material and because this is a
[04:44:02] new particle system we need to right
[04:44:04] click and make unique and do the same
[04:44:08] for the material right click make unique
[04:44:12] so we can change only this new
[04:44:17] cylinder let's go to display scale and I
[04:44:21] want this in there to be even bigger
[04:44:24] than the last one so let's set a scale
[04:44:26] of
[04:44:28] eight also we can go to the material
[04:44:32] into Shader
[04:44:33] parameters and change the texture for
[04:44:36] this cylinder for example let's
[04:44:38] use maybe this text
[04:44:43] T and set a speed of one and
[04:44:48] three
[04:44:51] Also let's go to scale and I don't want
[04:44:54] this cylinder to grow up instead I want
[04:44:57] it to grow into the from the center and
[04:45:03] go small so let's change the scale and
[04:45:08] because we want to change this new
[04:45:09] cylinder scale we need to right click
[04:45:12] and make unique do the same for all the
[04:45:16] properties of these
[04:45:18] particles make unique make
[04:45:21] unique now we can edit the
[04:45:24] properties so for example I want this
[04:45:27] cylinder to
[04:45:29] grow in all the
[04:45:38] directions but instead of growing up
[04:45:41] in the in the Y AIS I want it to
[04:45:46] go to to shrink down so let's change
[04:45:50] this curve so the cylinder
[04:45:52] goes from Big to small into the y
[04:45:58] axis something like like this I guess
[04:46:02] it's
[04:46:03] okay
[04:46:05] excellent we have done the AA effect
[04:46:09] with a nice expansive wave
[04:46:11] now we only need to add some extra
[04:46:14] details and coordinate everything
[04:46:18] together cool so finally let's go to
[04:46:22] photoshop or any painting program you
[04:46:26] want in this case I will use
[04:46:29] Photoshop and let's create a new
[04:46:32] image and put a text
[04:46:35] here
[04:46:37] level up
[04:46:42] let's move it to the center of the
[04:46:45] image and I want this text to be
[04:46:49] white also maybe we can give it some
[04:46:52] effects so let me see let's go to
[04:46:54] blending
[04:46:55] options maybe we can give it
[04:46:59] a a glow or maybe a contour or something
[04:47:04] like
[04:47:07] that let's try with a bevel
[04:47:13] effect
[04:47:15] okay save
[04:47:17] it as a
[04:47:20] PNG so let's go back to go and I want to
[04:47:24] create a new particle system let's
[04:47:27] create this time a CPU particle
[04:47:31] system and name it for
[04:47:34] example level up
[04:47:38] text so in order for this particles to
[04:47:41] work we need to assign a mesh so let's
[04:47:43] go to drawing and let's select a quad
[04:47:47] mesh so now we have a lot of quad meshes
[04:47:50] falling
[04:47:52] down let's also go to geometry and
[04:47:54] create a new standard
[04:47:59] material let's set the shading to be
[04:48:04] unshaded let's go to alido and here we
[04:48:07] can assign the level of text we just
[04:48:11] created in Photoshop so let's pick the
[04:48:15] text over
[04:48:19] here now we can see oh by the way
[04:48:22] because this is a transparent texture we
[04:48:24] need to go to
[04:48:26] transparency and set the transparency to
[04:48:31] Alpha let's also go to
[04:48:34] billboard and set the billboard to be
[04:48:37] particle billboard
[04:48:41] so now these particles are always facing
[04:48:45] the camera as you can see which is
[04:48:47] really cool finally for the material
[04:48:51] let's go to vertex color and enable
[04:48:53] these options so with this options we
[04:48:56] can now edit the color in the particle
[04:48:59] system cool let's close the material and
[04:49:03] go back to the particle system let's go
[04:49:05] to gravity and set it to
[04:49:07] zero set the amount to one
[04:49:12] also I want this to be this is maybe too
[04:49:16] small so let's go to scale and set a
[04:49:19] scale of
[04:49:22] four and maybe we can make this like go
[04:49:27] from small to big to small again so
[04:49:30] let's go to the scale option and create
[04:49:33] a new scale
[04:49:35] curve I want this particle to be very
[04:49:40] small at the beginning and then grow up
[04:49:46] and then go small
[04:49:50] again
[04:49:53] cool also I want this particle to go up
[04:49:57] so let's go
[04:49:59] to
[04:50:00] Direction and set the direction into the
[04:50:03] y axis 0 1
[04:50:07] 0 and let's go to Velocity and set
[04:50:10] velocity of
[04:50:15] 2.5 set the sprit to zero let's go to
[04:50:21] color
[04:50:23] and we can give it any color we want
[04:50:27] here in my case I want to use a row
[04:50:32] value of
[04:50:33] 2.5 2 and
[04:50:39] 0.5 excellent
[04:50:42] also I want this level up to disappear
[04:50:45] over the time so let's go to color ramp
[04:50:48] create a new
[04:50:50] gradient and delete
[04:50:54] this I want it to be
[04:50:58] transparent at the
[04:51:00] beginning like so and transparent at the
[04:51:07] end finally let's go to dumping
[04:51:11] and let's set a value of 0.8 and
[04:51:17] 1 now in order to keep everything
[04:51:19] organized I will create a new node
[04:51:25] 3D and put everything inside the the
[04:51:28] node
[04:51:30] 3D and we can name it for example
[04:51:35] VFX level
[04:51:38] up and right
[04:51:42] click and create a new Branch
[04:51:51] scene let's open the
[04:51:55] scene and create a
[04:51:58] new animation player so we can
[04:52:02] coordinate all the timing for the
[04:52:04] effects using the animation
[04:52:07] player let's create a new animation
[04:52:10] name it
[04:52:15] default let's put a time of two
[04:52:19] seconds and let's go to the cylinder
[04:52:22] one set it to one
[04:52:25] shot and key the emitting
[04:52:31] option let's do the same for every
[04:52:34] particle let's go to the cylinder
[04:52:36] 2 enable one shot and key
[04:52:45] do the same for this one shot
[04:52:49] key cool so for this effect let's
[04:52:53] say we want to emit all the effects at
[04:52:58] the beginning of the
[04:53:04] animation let's
[04:53:06] play so as you can see now everything is
[04:53:12] coordinated maybe we can put the level
[04:53:15] up effect a little
[04:53:17] bit later like
[04:53:23] this let's see let's play the
[04:53:27] effect okay so let's see how this final
[04:53:30] effect
[04:53:31] looks with the
[04:53:34] character so let's go to the level one
[04:53:37] and let's make this VFX editable
[04:53:41] children so we can play the
[04:53:43] animation and let's
[04:53:46] play excellent as you can see I added
[04:53:49] these little
[04:53:53] particles it's just some quad
[04:53:57] meshes similar to the text OP but yeah
[04:54:02] it it this adds a special touch to the
[04:54:07] effect cool our level up effect is is
[04:54:11] completed remember you can download all
[04:54:14] of these files for free in case you want
[04:54:17] to use them or story up close now let's
[04:54:21] go ahead and let's create the puff
[04:54:25] effects this tutorial is divided into
[04:54:28] three parts let's start creating some
[04:54:31] nice particles using a simple
[04:54:35] sphere then let's convert those spheres
[04:54:39] into some nice animated clouds using a
[04:54:43] visual
[04:54:44] Shader and finally let's customize the
[04:54:47] effect so we can use it in our game so
[04:54:51] let's start with the particle
[04:54:54] system so let's create the puff effect
[04:54:58] for this effect I want to go ahead and
[04:55:00] create a new GPU particle
[04:55:05] system and in order for this particle to
[04:55:07] work we need to create a new particle
[04:55:10] process material and also assign a mesh
[04:55:14] this time I will select the sphere
[04:55:17] mesh and as you can see now we have a
[04:55:19] lot of spheres falling down so let's go
[04:55:23] to accelerations and set the gravity to
[04:55:27] zero instead of using gravity I want to
[04:55:30] use a radial velocity so let's go to
[04:55:33] radial velocity and set a velocity
[04:55:35] between 1 and two
[04:55:41] cool now let's create a material for the
[04:55:46] for the Spheres so let's go to Geometry
[04:55:49] material override let's create a new
[04:55:51] Shader
[04:55:53] material new
[04:55:55] Shader select visual
[04:55:59] Shader maybe we can name it for example
[04:56:03] Shader
[04:56:05] puff now let's open the puff Shader
[04:56:10] and let's create some stuff here first
[04:56:14] we need to add a color so let's right
[04:56:16] click and create a new color
[04:56:20] fragment connect the color and the
[04:56:26] transparency also there's one more
[04:56:30] thing if I move the the Spheres you can
[04:56:34] see how it gets this hard Edge when it
[04:56:39] intercepts with the floor I don't want
[04:56:41] that so in order to fix this we can
[04:56:44] create a proximity fade
[04:56:47] node and let's multiply this node with
[04:56:53] the alpha
[04:56:55] channel so now as you can
[04:56:58] see if we get closer to the floor the
[04:57:01] Spheres disappear it fades we can also
[04:57:05] control the value here maybe we can
[04:57:07] create a float
[04:57:10] parameter let's name it um distance
[04:57:16] faith and give it a default value of
[04:57:23] 0.3
[04:57:26] cool excellent um let's do some changes
[04:57:29] to the particle system for
[04:57:33] example let's go to the particle process
[04:57:35] material and I want these particles to
[04:57:38] scale down so let let's go to scale and
[04:57:42] let's put a random scale between one and
[04:57:46] three and let's create a new
[04:57:52] curve and I want these particles to
[04:57:55] start big and then go
[04:57:58] small like
[04:58:01] this maybe too much maybe something like
[04:58:05] this
[04:58:07] perfect and I also want this particle to
[04:58:10] disappear over the time so let's go to
[04:58:14] color curves and let's create a new
[04:58:17] Alpha
[04:58:22] curve so I want these particles to be
[04:58:26] full opaque at the
[04:58:28] beginning and then I want them to
[04:58:31] disappear
[04:58:36] slowly we can also give it any color
[04:58:39] which want but for now I will leave them
[04:58:45] white okay so the particle system is
[04:58:48] already prepared now let's make these
[04:58:52] spheres look like a clouds using a
[04:58:56] visual
[04:58:58] Shader okay so here's the interesting
[04:59:01] part let's convert this sphere into a
[04:59:06] cloud we can do that using a
[04:59:09] Shader let me show you let's go to the
[04:59:11] Shader and let's go to the vertex option
[04:59:16] here we can control the vertices or the
[04:59:18] vertex of this
[04:59:20] sphere this can be quite confusing so I
[04:59:25] will quickly open my drawing board
[04:59:30] presentation so as we know a 3D sphere
[04:59:34] is composed by many little points or
[04:59:38] vertices
[04:59:41] and let's say all of these points has a
[04:59:45] perpendicular Vector like
[04:59:50] this so the idea is to being able to
[04:59:54] take a black and white
[04:59:57] texture and put that texture into a
[05:00:01] sphere until all these points to move
[05:00:06] depending of if the point is covered by
[05:00:10] white for example if it's white that's
[05:00:13] equal to one if it's black equals to
[05:00:16] zero gray
[05:00:18] 0.5 so we can move the point depending
[05:00:22] on the texture over the
[05:00:28] sphere okay so with that being said
[05:00:30] let's go back to go do let's go back to
[05:00:33] the Shader to the vertex section and
[05:00:36] let's do some stuff first right click
[05:00:39] and create the
[05:00:41] vertex here we have all the vertices of
[05:00:44] the sphere and to this vertices I want
[05:00:47] to
[05:00:51] add a normal
[05:00:53] Vector right click and look for
[05:00:58] normal so look what happen when I
[05:01:02] connect this node
[05:01:05] here now as you can see all the vertices
[05:01:08] or all the points of the
[05:01:10] sphere move in the normal direction of
[05:01:13] the
[05:01:15] vector we can also control
[05:01:18] the like the vector of the normal and
[05:01:21] reduce the size so we can for example
[05:01:24] multiply
[05:01:26] this normal Vector for the value let's
[05:01:30] create a
[05:01:31] float constant for example
[05:01:38] 03 so now we reduce the size of the
[05:01:41] normal Vector 0.3
[05:01:44] units and as you can see we get a small
[05:01:48] a
[05:01:49] sphere
[05:01:52] excellent but now let's do something
[05:01:55] interesting I will take a texture let's
[05:01:58] pick for
[05:02:00] example
[05:02:01] this
[05:02:06] texture set it to
[05:02:08] color and we don't need a full color
[05:02:11] because this is a black and white
[05:02:12] texture we only need to use one channel
[05:02:15] so I will pick this and I want to
[05:02:21] multiply this texture with the normal
[05:02:32] Vector excellent now we get this
[05:02:35] interesting shape and this is the result
[05:02:39] of this text
[05:02:40] controlling the vertices of the of the
[05:02:42] sphere we can also change the intensity
[05:02:45] here using this note let's try with
[05:02:49] one so we get this crazy shape but for
[05:02:54] the clouds let's put a value of minus
[05:03:00] 0.6 so now this looks more like a cloud
[05:03:04] right also I want these clouds to be
[05:03:08] dynamic to move so we need to move the
[05:03:11] texture and for moving the
[05:03:16] texture I will create a
[05:03:20] UV buning
[05:03:24] note Also let's create a Time
[05:03:30] node and multiply the
[05:03:36] time with uh
[05:03:40] Vector
[05:03:42] 2
[05:03:45] constant and let's give it a value for
[05:03:47] example
[05:03:49] of 0.1 and
[05:03:56] 1 now you can see how the texture is
[05:04:00] moving so the vertices of the sphere are
[05:04:03] moving with the texture which is moving
[05:04:06] using these um values
[05:04:13] cool so I think this is cool I think
[05:04:17] this this looks really nice already but
[05:04:20] there's one more thing I want to do I
[05:04:23] would like this clouds to look more
[05:04:27] stylized more tuny so I want to change
[05:04:31] the way the light interacts with the
[05:04:36] clouds and for doing that I want to once
[05:04:39] again
[05:04:40] modify this
[05:04:41] Shader and this time I want to go to the
[05:04:45] light section of the Shader in this
[05:04:48] section we can control like the way this
[05:04:53] sphere interacts with the
[05:04:57] light in this case I want this to look
[05:05:00] more anime style more tuny
[05:05:03] style so I want to make sure that the
[05:05:06] light hits like in the hard way the
[05:05:10] and also I want to give it a nice shadow
[05:05:15] Contour to the to the clouds for doing
[05:05:19] that I am going to create a normal
[05:05:22] vector and I want to dot product this
[05:05:27] multiply this normal Vector with a DOT
[05:05:30] product with the frel
[05:05:35] node let's set this forel to to through
[05:05:39] in inverted and connect to the diffuse
[05:05:42] Channel and I know this is this might
[05:05:46] look a bit confusing I am planning to
[05:05:48] explain this quite better in a in the
[05:05:51] future I want to do a a video about
[05:05:54] anime style in in 3D games but for now
[05:05:57] let's just follow these steps I am doing
[05:06:01] in the video create a smooth step note
[05:06:10] and create a
[05:06:12] float
[05:06:15] constant another float
[05:06:18] constant that goes between 0 and
[05:06:21] 0.1 with this we can control the
[05:06:24] hardness of the
[05:06:30] edges and
[05:06:32] now let's create a clamp note
[05:06:41] and give it a
[05:06:44] value
[05:06:45] between 0.1 and
[05:06:50] one so with this we can control how dark
[05:06:54] are the shadows and how bright are the
[05:06:58] this this
[05:07:04] brightness cool so yeah this
[05:07:08] is this is the the light
[05:07:16] note so yeah that's that was it we have
[05:07:20] the
[05:07:21] Shader with all done already we can
[05:07:24] close the Shader and let's do some final
[05:07:28] adjustments to this puff
[05:07:31] effect set the amount to
[05:07:36] 12 and the explosiveness to
[05:07:43] 0.85 also I want to give it
[05:07:47] a random angle between minus 180 and
[05:07:53] 180 let's go to position I want I want
[05:07:57] this clouds to spawn in a ring
[05:08:04] position with a value of one in the y
[05:08:07] axis
[05:08:09] and a height of zero and a radius of
[05:08:14] one also I want to set a
[05:08:17] velocity in the Y
[05:08:20] AIS between 0.5 and 1 and finally we can
[05:08:26] give it a nice
[05:08:28] color this time I want to use a color
[05:08:31] ramp let's create a new gradient
[05:08:35] texture enable hdri
[05:08:41] and I want to start with a really
[05:08:43] intense strong purple with a row value
[05:08:47] of
[05:08:49] 0.4
[05:08:52] 0.05 and
[05:08:57] 1.2 and I want it to go to a full black
[05:09:01] color at the
[05:09:03] end also we can give it another color
[05:09:06] over here with a row value of
[05:09:11] 0.2
[05:09:14] 0.05 and
[05:09:16] 1 that's it we get this really nice puff
[05:09:21] effect finally if we want we can set it
[05:09:24] to one shot and when we need to use it
[05:09:27] we can just emit the effect one time
[05:09:30] here by clicking
[05:09:36] here I have also added some extra
[05:09:40] details to the puff effect as you can
[05:09:43] see I will not dive too much into
[05:09:46] details about this since I have already
[05:09:49] done this in the past in my heat effect
[05:09:52] tutorial if you haven't seen my tutorial
[05:09:56] please check it out basically here I
[05:09:59] have two particle systems one is a big
[05:10:03] quad mesh with a texture that scales
[05:10:06] down with this curve
[05:10:10] and I did another particle system which
[05:10:14] add a bunch of quad meshes with a simple
[05:10:19] billboard
[05:10:20] texture and this simply helps to add
[05:10:24] some more impact to this puff
[05:10:29] effect as for the step puff effect it's
[05:10:34] almost the same I just Tweed some
[05:10:37] parameters for example I have changed
[05:10:40] the color to a white color and change
[05:10:44] the amount to two
[05:10:47] particles also I have set a simple
[05:10:50] velocity into the x axis
[05:10:54] only the puff effect is completed and
[05:10:58] now we can customize it as we want and
[05:11:02] of course the possibilities are a lot
[05:11:05] but at least you have the basics done
[05:11:08] and you can work from there so that's it
[05:11:12] for this tutorial guys I hope you have
[05:11:14] learned something new today and if you
[05:11:17] want to learn more about visual effects
[05:11:19] in thought please check out my YouTube
[05:11:22] channel thank you for watching
[05:11:28] bye all right so now that we have all
[05:11:30] our FFX or now that you kind of figure
[05:11:33] out how to make them we already have
[05:11:35] them whatever you may have done me
[05:11:38] scratch or you already have them here
[05:11:40] from the started project whatever let's
[05:11:42] take a look at what we have and what
[05:11:44] we'll implement the first thing we're
[05:11:46] going to implement is in our player so
[05:11:47] let's open up our player here and we're
[05:11:50] going to now add the VFX that are in our
[05:11:53] player which
[05:11:55] are the level up scene so this one we
[05:11:59] pop that in we also will need the
[05:12:04] puff puff run the puff run this one we
[05:12:09] that
[05:12:10] in pop it in there we go and we'll just
[05:12:12] make sure that both of these are reset
[05:12:15] to
[05:12:17] 0
[05:12:19] go okay so for the level up I'm going to
[05:12:22] have to make this local and now I have
[05:12:24] access to the animation player so here I
[05:12:27] don't want this to play by default I'm
[05:12:28] going to uncheck
[05:12:30] that no and now I'll actually rename
[05:12:34] this
[05:12:35] to I'm not going to rename it I'm just
[05:12:37] going to go into my script and remember
[05:12:39] this level up function that we created
[05:12:41] well this is where I will get node get
[05:12:45] this animation player
[05:12:47] here and we will
[05:12:51] play the initialize function so uh in it
[05:12:56] this is my level up and we can test this
[05:13:00] out play and if we go find a monster to
[05:13:04] kill which we'll have to spawn them in
[05:13:07] in just a minute here we
[05:13:11] go okay maybe I'll uh oh he died okay
[05:13:14] there we go there's our level up there
[05:13:16] we go we saw that we leveled up and we
[05:13:18] even got the signal and we played the
[05:13:20] animation there we go now what about the
[05:13:23] puff well this is not too hard because
[05:13:25] all we need to do is emit this every
[05:13:28] time I run now of course there's a few
[05:13:30] options either I can emit this while I'm
[05:13:32] running in my code or whatever I'm going
[05:13:35] to do this through the animation Tree in
[05:13:38] my animation tree in my night here pop
[05:13:41] my animation fee up I will find the
[05:13:44] running a which is the one I'm using and
[05:13:47] every time I I run so maybe like kind of
[05:13:51] one
[05:13:53] step maybe one right there I can go to
[05:13:56] my puff here and turn this on or I'll
[05:14:00] just kind of re track that and here I'll
[05:14:03] have to click into this and turn this on
[05:14:05] so now when I play this you'll see the
[05:14:08] puff
[05:14:10] so there we
[05:14:11] go now when I hit
[05:14:15] play you will see that when I
[05:14:18] run I have that puff
[05:14:25] effect there we go so it's at The First
[05:14:28] beginning of that animation track right
[05:14:31] okay so that's our puff run now we need
[05:14:33] to implement our puff monster death
[05:14:37] effect so here we will add add our big
[05:14:41] puff we'll pop this in our scene here
[05:14:44] we'll make sure that this is at position
[05:14:48] Z and now uh we want
[05:14:54] to out we want to make local and here we
[05:14:59] have the hit effect so this is cool but
[05:15:02] this is the entire puff effect so here
[05:15:04] we want this entire puff effect to hit
[05:15:06] play but I'll uncheck this oops so I
[05:15:09] want this entire animation to play right
[05:15:11] here when I die so here in my uh script
[05:15:15] here when I die my death function all I
[05:15:18] need to do is play
[05:15:24] this
[05:15:25] play uh hit there we go that's pretty
[05:15:29] much it here I'll just say get node
[05:15:31] instead because I like to use a
[05:15:34] consistent way of getting nodes all
[05:15:36] right there we go we played this
[05:15:38] animation
[05:15:39] now instead of queing free I'm going to
[05:15:41] hide ourself or I'm actually going to
[05:15:44] hide the skeleton Warrior okay and then
[05:15:49] I'm going to wait for this to finish
[05:15:51] connect the animation finished once it's
[05:15:54] finished then I will self duct Q free
[05:15:57] but now what I can do here is let's head
[05:15:59] back to level one and I'm actually going
[05:16:01] to move my monster here to be right in
[05:16:03] front of my player that way I don't have
[05:16:05] to uh wait for him to run all the way
[05:16:08] there
[05:16:09] let me just equip some weapons stuff
[05:16:12] here kill this guy he dies pu effect
[05:16:15] shows up and eventually he'll you free
[05:16:20] there we go that is a cool way that we
[05:16:22] can do that now of course you can also
[05:16:25] um here in the death of course hide so
[05:16:29] here this is when the death happens so
[05:16:32] here we'll hide the Sprite and here I'll
[05:16:34] just say get node instead
[05:16:39] skon Warrior there we go all right so
[05:16:42] that is pretty much it for our effects
[05:16:44] um we do have the hit effect left so
[05:16:46] let's take a look at our hit
[05:16:48] effect here we go the VFX hit we can pop
[05:16:52] this in uh we can pop this in
[05:16:54] realistically anywhere we want I'll pop
[05:16:56] this into my uh player here and if I
[05:17:00] make this local we'll find the spark
[05:17:02] effect and this I wanted to happen on my
[05:17:05] sword so what I can do is I can find my
[05:17:08] sword here in my right hand slot pop
[05:17:12] this in my hand slot I will take the
[05:17:15] position and reset
[05:17:18] it and I'm going to take my animation
[05:17:20] player here uh
[05:17:23] for the Knight play the T pose real
[05:17:26] quick this
[05:17:28] guy let's play the T pose that way I can
[05:17:31] move the spark effect I want to move it
[05:17:34] kind of right around there that's
[05:17:36] probably where I will hit something
[05:17:38] that's where I'll actually um you know
[05:17:40] hit something so here I'm going to turn
[05:17:42] off the hit by default in my functions
[05:17:45] here when something enters this area so
[05:17:48] I can actually just go over here go to
[05:17:50] node double click this and this will
[05:17:53] take me to where it needs to be I can
[05:17:55] take this this is my path for my hit
[05:17:59] animation I will say get
[05:18:03] node animation player and then
[05:18:06] play hit so here we go go we now have
[05:18:09] that hit effect being played every time
[05:18:11] I hit something so let's take a look if
[05:18:14] this
[05:18:15] works now if I play we now see that full
[05:18:21] hit effect every time I hit something
[05:18:24] more specifically a Monster yeah there
[05:18:26] we go there's our game with some sound
[05:18:29] effects or some effects now next we'll
[05:18:31] add some sound effects let's take a look
[05:18:33] at how we can do that all right so we're
[05:18:36] going to add three different sound
[05:18:37] effects which doesn't sound like much
[05:18:39] but that's okay here in our player we're
[05:18:41] going to add a audio stream player 3D we
[05:18:47] create we'll rename this to damage we'll
[05:18:51] duplicate
[05:18:53] it D we rename this one to hit and these
[05:18:58] two effects are pretty easy we just need
[05:19:00] to find the hit effect so can find
[05:19:04] either sword attack human maybe we can
[05:19:07] put this one for our damage and then for
[05:19:09] the hit we can
[05:19:11] find one that gets hit maybe the sword
[05:19:15] hit and we can play this by going to
[05:19:18] playing you should be able to hear it
[05:19:21] it's pretty
[05:19:22] cool now what we can do is head over to
[05:19:25] our script this is actually not too hard
[05:19:27] because all we need to do is in our hit
[05:19:29] function I just need to get
[05:19:31] node hit and then dot play so it's that
[05:19:35] easy I'll just copy this and then every
[05:19:38] time I get hit or I hit something this
[05:19:41] is where I'll damage it so I'll say
[05:19:44] damage stop play all right so that's our
[05:19:47] sound effects for a player one more
[05:19:49] thing we'll add is our item
[05:19:51] object over here we'll add a audio
[05:19:54] stream
[05:19:56] player we'll rename this to
[05:19:59] pickup we're going to connect the
[05:20:01] finished to this uh the signal to the
[05:20:04] node or to the script uh let's actually
[05:20:07] fill this in with a thing first so let's
[05:20:10] find whichever one we want we can maybe
[05:20:12] do crate
[05:20:13] open realistically it doesn't actually
[05:20:15] matter maybe stack open that might sound
[05:20:18] decent so let's say that is our pickup
[05:20:20] sound effect and the reason I'm doing
[05:20:22] this is because here we're queuing free
[05:20:25] now this is kind of a different way of
[05:20:26] doing this is here I'm going to ceue
[05:20:29] free once the sound is finished but
[05:20:31] until then I'm just going to hide self
[05:20:34] it's going to look as if I destroyed it
[05:20:36] but really it's just hiding so now now
[05:20:38] when I hit
[05:20:40] play I create my game
[05:20:43] here I can po this
[05:20:47] in there we go and go and kill it you
[05:20:52] can see we have some sound effects which
[05:20:53] was nice and then when I pick these up
[05:20:56] nothing happens uh probably because I'm
[05:20:58] never playing it so that makes sense so
[05:21:00] when I enter this I need to play it so
[05:21:02] let's get node pick up
[05:21:07] play and let's hit play one more time
[05:21:10] hopefully you caught on to that what I
[05:21:12] just did there I made a small mistake
[05:21:14] it's okay
[05:21:17] though all right so there we go there's
[05:21:19] our sound effect you should be able to
[05:21:21] hear it being picked up all right so
[05:21:23] there we go that is how we create um
[05:21:26] some sound effects and that's pretty
[05:21:28] much it so in the next part I think all
[05:21:31] we have left is to um have our monster
[05:21:35] spawn in our world so here I want to
[05:21:36] spawn our monster but I don't want to
[05:21:38] spawn it in a wall right so we're going
[05:21:41] to have to figure out how we can do
[05:21:44] that all right so now what we're going
[05:21:46] to do is in our level one we're going to
[05:21:48] create a new script attach this to our
[05:21:51] script level one we'll put this in our
[05:21:53] level or script system here hit create
[05:21:56] and pop this out now I'm going to on
[05:21:59] ready variable our Warrior scene we're
[05:22:04] going to pack this
[05:22:07] scene and I'm going to reload it here a
[05:22:12] skeleton Warrior we go and now I'm also
[05:22:15] going to load the grid map grid map to
[05:22:20] get node grid map now this isn't going
[05:22:24] to 100% work uh sorry floor because
[05:22:26] renamed it uh and I'll kind of show you
[05:22:29] why in a
[05:22:30] second we'll kind of look through this
[05:22:33] together so first let's create a
[05:22:35] function a ready function and we're
[05:22:39] going to say while the get node
[05:22:42] monsters. getchild
[05:22:47] count count is less than 10 I'm going to
[05:22:50] start adding monsters until I get 10
[05:22:52] monsters now what we can do is I'm going
[05:22:55] to get a x position and randomize it by
[05:22:58] saying Randy range from -40 uh
[05:23:03] 240 I'll do the same thing for the
[05:23:07] Zed and then I'm going to create a
[05:23:09] monster temp
[05:23:11] variable now monster temp now here's the
[05:23:16] thing is this monster temp we need to
[05:23:18] instantiate it so here we'll just say
[05:23:20] warrior scene do instantiate done now we
[05:23:24] need to check to see if the grid map.
[05:23:27] get
[05:23:28] cell cell item at Vector 3 I at The X 3
[05:23:38] I at The X position that I'm trying to
[05:23:40] add at -1 at The Zed position that I'm
[05:23:45] trying to add as well is equal to Z Now
[05:23:49] is it zero let's find out let's close
[05:23:52] this and head over to our walls and
[05:23:54] floor now if we go to the library the
[05:23:57] item and zero this is the one we're
[05:24:00] looking for here I need to make sure I'm
[05:24:03] adding my monster on a floor cell and
[05:24:06] not a uh all wall arched right so what I
[05:24:11] can do here is I can do two things first
[05:24:14] I can check to see if I'm on a floor and
[05:24:17] then I can also check to see if I'm not
[05:24:20] in a wall and I can do that by saying
[05:24:23] grid map walls here I can maybe rename
[05:24:26] this one to
[05:24:28] flor of course here I'll have to this to
[05:24:31] grid map floor now here I'm checking to
[05:24:34] see if I'm on a floor if I am on a floor
[05:24:37] I now want to check to see if I'm on a
[05:24:39] wall so I can do that by also checking
[05:24:43] for the same thing I'll just say copy
[05:24:46] this except this one I don't want it to
[05:24:48] be zero I want it to be the this one
[05:24:51] wall arched so I have to find which
[05:24:53] position that it is in here it is going
[05:24:56] to be two now you might have a different
[05:24:58] one maybe you have yeah maybe you have
[05:25:01] something else I don't know you'll have
[05:25:02] to check them and the number here is
[05:25:04] corresponding to the number we need so
[05:25:06] here I'm going to make sure it's not not
[05:25:09] equal to two then if it is or if it's
[05:25:12] not equal to two meaning I'm on a floor
[05:25:15] and I'm not on a wall then I will add
[05:25:17] the monster to do that I'll say monster
[05:25:20] temp
[05:25:21] position is equal to Vector
[05:25:25] 3 at X
[05:25:29] position at position let's say three
[05:25:32] just so it kind of starts in the air and
[05:25:34] then Z
[05:25:36] position then we'll say monster 10
[05:25:39] player is equal to get node player
[05:25:42] because we need to assign the player uh
[05:25:45] to our monster right because before we
[05:25:47] have exported it close this remember
[05:25:50] here we had it exported but now we need
[05:25:52] to assign it manually the code okay so
[05:25:55] now we need to actually add the monst to
[05:25:57] our scene so that's not too hard we can
[05:25:59] over here we can say get
[05:26:02] node
[05:26:04] monsters monsters go do add child
[05:26:09] monster ATT all right so there we go now
[05:26:13] now we will pray that this does not
[05:26:15] crash because we added a while loop so
[05:26:17] hopefully this works out nicely all
[05:26:20] right here we go we have not crashed and
[05:26:24] we have some monsters that have been
[05:26:26] added to our game and none of them are
[05:26:27] in the wall so obviously all of them
[05:26:29] were added to this side um that might be
[05:26:32] because the positioning was over here um
[05:26:36] you can change the range that they get
[05:26:38] uh spawn in right here right depending
[05:26:40] on what you want for the X and Y
[05:26:42] position it really is up to you I just
[05:26:44] did 40 to 40 I think that will cover a
[05:26:46] wide range um it might be more it might
[05:26:49] be less not 100% sure actually no that
[05:26:53] should cover most of it so here you can
[05:26:54] see that this is 30 and this is around
[05:26:58] -30 probably on the other side Etc so
[05:27:00] this should cover the entire map that we
[05:27:02] have and it will only spawn 10 monsters
[05:27:05] in our map okay so that is how we make
[05:27:09] sure that things don't spawn in our
[05:27:10] walls we make sure that they spawn in
[05:27:12] our map Etc so and it's a relatively
[05:27:15] randomized position so pretty neat all
[05:27:18] right so that is it for this section
[05:27:20] believe we're done but we'll find
[05:27:23] out congratulations on completing this
[05:27:25] course course was not very easy pretty
[05:27:28] long but got through it and good job so
[05:27:32] we actually created a pretty neat game
[05:27:34] in the end we have a relatively good
[05:27:36] working player with a monster and an
[05:27:39] inventory system that's pretty neat and
[05:27:42] all that good stuff so congratulations
[05:27:44] completed this course and H yourself on
[05:27:47] the back all right so now what do we do
[05:27:50] next what is the next step well first of
[05:27:52] all I'll just kind of encourage you to
[05:27:53] check out my channel of course and hit
[05:27:55] that sub button there um but what about
[05:27:58] what else what else can I offer you to
[05:28:00] help you along well I have weekly
[05:28:02] challenges and the point of the weekly
[05:28:04] challenges is terms of practice so this
[05:28:07] is kind of you going forward you need to
[05:28:10] probably practice if you want to learn
[05:28:11] gdau or game development you will
[05:28:14] probably need to practice now I offer
[05:28:16] free weekly challenges every Sunday I'll
[05:28:18] be offering uh and sending out a weekly
[05:28:21] challenge and the next week I'll be
[05:28:23] sending out the solution to that
[05:28:24] challenge every week I'll essentially
[05:28:26] send out the challenge and the solution
[05:28:28] to the previous week right so I've been
[05:28:30] doing this for about three months now
[05:28:31] and uh everybody has been enjoying it on
[05:28:34] my channel so far so I'm going to keep
[05:28:36] doing it for a while to access it all
[05:28:38] you need to do is join my email list for
[05:28:42] my patreon as well email list is
[05:28:44] completely free so all you need to do is
[05:28:46] just hit subscribe and you will be added
[05:28:48] to the email list for that and yeah
[05:28:50] that's it so what else can you do well
[05:28:53] of course there are courses as well I
[05:28:55] have several other courses on my website
[05:28:57] that you can check out um some are free
[05:28:59] some are paid but of course you can also
[05:29:02] access all of it um if you're a
[05:29:04] membership or if you buy a membership
[05:29:05] sorry um so definitely check that out as
[05:29:08] well now the advantages of my courses
[05:29:11] specifically is that I try to structure
[05:29:13] my courses slightly differently than
[05:29:15] many other people might and it's more
[05:29:18] specific in the sense that I split it up
[05:29:20] into kind of two or three different
[05:29:21] sections the first section is
[05:29:24] essentially teaching you the concept and
[05:29:26] idea of what we're going to do and what
[05:29:28] we're going to learn to apply then in
[05:29:30] the middle I give you an assignment and
[05:29:33] That assignment will hopefully help you
[05:29:35] guide uh guide you into creating the
[05:29:37] game that we need to make and then the
[05:29:39] third section or the second part of that
[05:29:41] course will be kind of like what we just
[05:29:43] did in this course where I kind of just
[05:29:45] do a follow along a code along tutorial
[05:29:47] where you follow me and we kind of look
[05:29:49] through the solution of doing the
[05:29:51] assignment and the project together so
[05:29:54] if you if you're interested in that sort
[05:29:57] of format definitely check it out on my
[05:29:58] channel I have a few courses up for free
[05:30:00] and I have a few courses up that are
[05:30:02] paid definitely check it out and
[05:30:04] hopefully I'll see you guys around

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
