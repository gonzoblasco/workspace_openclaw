# Transcripción — I Built This Interactive 3D Website With AI (Gemini 3.8 Flash)

- Fuente: https://www.youtube.com/watch?v=y1pM7bS6IY8
- Canal: MiladiCode
- Publicado: 2026-09-06
- Duración: 13:01 (781 s, `video-meta.json`)
- Idioma: inglés
- Captions: automáticos de YouTube (`en-orig`, pista `variant=gemini`), 758 eventos crudos → 379 cues deduplicados, 2.596 palabras
- Último cue: 0:12:59 (cierra a 2 s del final)
- Sin capítulos oficiales en la descripción: el mapa temporal del outline se derivó del transcript y del índice que el propio video recorre en orden.

## Glosario de errores del ASR

| ASR | Real |
|---|---|
| Runnable / Runable | **Runable** (`runable.com`) — el patrocinador; el ASR alterna las dos formas |
| RunDiffusion (02:20) | El ponente lo dice así, pero el flujo de imágenes/video/frames que describe es el de Runable; probable desliz del propio hablante o del reconocimiento. No se corrige el cue |
| Trepo / Tripo (09:45) | **Tripo** (`studio.tripo3d.ai`) |
| Gemini 3.6 Flash (05:29) | El título y la descripción dicen **Gemini 3.8 Flash**; en el cue de 05:29 el hablante dice «3.6». Discrepancia de fuente, no de ASR |
| Bento / Bentō | **bento grid** (layout tipo caja de bento) |
| Seedance 2.5 | Correcto: modelo de video del patrocinador |
| Antigravity / Anti-Gravity | **Google Antigravity** (IDE agéntico) |
| EasyGIF | `ezgif.com`, que el ASR deforma |

Los cues no se editan; los errores se resuelven en este glosario y en el outline.

## Transcript

[0:00:00] What if you could build a website like
[0:00:01] this with AI? Complete with cinematic
[0:00:04] animations, interactive sections, and
[0:00:06] even your own custom 3D model. Well, in
[0:00:09] this video, we're going to build exactly
[0:00:11] that using Antigravity. And we're not
[0:00:13] just going to generate another basic AI
[0:00:15] landing page. We're going to create a
[0:00:17] fully interactive AI-powered image and
[0:00:20] video generation platform with a
[0:00:22] cinematic hero section, smooth
[0:00:24] scroll-driven animations, an infinite
[0:00:26] logo carousel, modern Bento sections,
[0:00:29] and a fully interactive 3D model. I'll
[0:00:31] even show you how we can take a simple
[0:00:33] image, turn it into a 3D model, and then
[0:00:36] integrate that model directly into our
[0:00:37] website. The interesting part is that
[0:00:40] we'll be using AI throughout the entire
[0:00:42] process, from creating our visual assets
[0:00:44] and animations to designing the sections
[0:00:46] and writing the code. I'll also share
[0:00:48] all the prompts I use throughout the
[0:00:49] video, so you can follow along and
[0:00:51] recreate the same workflow. So, let's
[0:00:53] jump into Antigravity and start building
[0:00:55] this website from scratch.
[0:01:04] >> [bell]
[0:01:06] >> So, guys, for this tutorial, I'm going
[0:01:08] to be using Antigravity, but you can
[0:01:10] absolutely follow along using any other
[0:01:12] AI tool or IDE you prefer. The overall
[0:01:14] workflow is going to be pretty much the
[0:01:16] same. So, let's start by creating a new
[0:01:18] folder for our project. Now, in this
[0:01:20] video, we're going to take things a step
[0:01:22] further and build an advanced
[0:01:24] interactive website with smooth
[0:01:26] animations, engaging interactions, and
[0:01:29] even custom 3D models that we can
[0:01:31] integrate directly into the website.
[0:01:33] When you're building a website for a
[0:01:34] product, startup, or personal project,
[0:01:36] the design and overall visual direction
[0:01:38] can make a huge difference. One of the
[0:01:40] easiest ways to find inspiration is by
[0:01:42] exploring platforms like Dribbble or
[0:01:44] Pinterest. For example, I found this
[0:01:47] image that I really like, and I want to
[0:01:48] use it as the first frame of an
[0:01:50] animation. Then, for the final frame,
[0:01:52] I'm going to use this second image. The
[0:01:54] idea here is to create a smooth
[0:01:56] cinematic transition between these two
[0:01:58] visuals and then use that animation to
[0:02:00] build the scroll-based experience for
[0:02:02] our hero section. So, I'm going to walk
[0:02:04] you through the entire process from
[0:02:05] preparing and refining these image
[0:02:07] assets to generating the video and
[0:02:09] finally converting that video into
[0:02:11] individual frames that we can use to
[0:02:13] create the scroll animation on our
[0:02:15] website. All right, now that we have our
[0:02:16] initial image assets, the first thing we
[0:02:18] need to do is prepare them properly. For
[0:02:20] this, I'm going to use RunDiffusion,
[0:02:21] which is an all-in-one AI platform that
[0:02:24] allows us to work with images, generate
[0:02:26] videos, and even extract video frames
[0:02:28] within the same workflow. So, I'll start
[0:02:31] by uploading the first image and ask the
[0:02:32] agent to enhance the image quality and
[0:02:35] convert it to a 16:9 aspect ratio. I'll
[0:02:38] send that request and as you can see, it
[0:02:40] only takes a few seconds. And perfect.
[0:02:42] For the second image, I want to make a
[0:02:44] few more changes. I'm going to ask the
[0:02:46] agent to modify the overall visual style
[0:02:49] and adjust the colors so that it matches
[0:02:51] the first frame more closely. And of
[0:02:53] course, I'll also ask it to convert the
[0:02:55] image to 16:9 so both images have
[0:02:57] exactly the same dimensions. So, let's
[0:03:00] send that request.
[0:03:01] And there we go. Now we have our two
[0:03:03] finalized images, which we can use as
[0:03:05] the starting frame and ending frame for
[0:03:07] our video. Let's move on to creating the
[0:03:10] actual video. I'll open a new task and
[0:03:13] switch the tool from image generation to
[0:03:15] image to video. But before uploading the
[0:03:17] images, there's one small thing we need
[0:03:19] to take care of. I'm going to rename the
[0:03:21] files so it's immediately clear which
[0:03:23] image is the first frame and which one
[0:03:26] is the last frame. Now, I'll upload both
[0:03:29] images and give the agent a detailed
[0:03:31] prompt describing the animation I want.
[0:03:34] The important part here is that we want
[0:03:36] a continuous cinematic shot that
[0:03:38] naturally transitions from the first
[0:03:40] reference frame into the second one. So,
[0:03:42] in the prompt, I'll describe the
[0:03:44] movement, camera motion, transitions,
[0:03:47] lighting, atmosphere, and other visual
[0:03:49] details I want the AI to preserve
[0:03:51] throughout the animation. Also, I've
[0:03:53] shared all of the prompts I'm using in
[0:03:55] this video, so you can find them through
[0:03:57] the link down below in the description
[0:03:59] box. With Runnable, you have different
[0:04:01] AI models available for image and video
[0:04:04] generation. So, if you're not satisfied
[0:04:06] with the results of your video, you can
[0:04:08] simply change the model and try again.
[0:04:10] Seedance 2.5 worked perfectly for me,
[0:04:12] and the results are exactly what I
[0:04:14] wanted. Now, if you're using Runnable to
[0:04:16] extract the frames from this video, all
[0:04:18] you need to do is ask your agent to
[0:04:19] extract the frames once the video is
[0:04:21] complete. You can also use websites like
[0:04:23] EasyGIF, where you can upload the video
[0:04:25] and extract the individual frames. Okay,
[0:04:28] Runnable has completed the task here, uh
[0:04:30] and now I can download a zip file
[0:04:32] containing all of the video frames.
[0:04:34] Next, let's start creating our website.
[0:04:36] First, we're going to install a plain
[0:04:38] empty Next.js project. For that, just
[0:04:40] head over to nextjs.org. Right in the
[0:04:42] center of the page, you can copy the
[0:04:44] installation command. Now, I'll navigate
[0:04:46] back to Antigravity, open the terminal,
[0:04:49] and paste the command right here. Also,
[0:04:51] don't forget to add the slash to the end
[0:04:53] of the command, so it installs the
[0:04:55] Next.js project in the current
[0:04:56] directory. I'll hit enter, and it will
[0:04:58] start installing all the required
[0:05:00] packages for us. All right, now it's
[0:05:01] time to create our hero section design.
[0:05:03] For that, once again, I'm going to head
[0:05:05] over to Pinterest to find a hero design
[0:05:07] that I can use as a reference. I really
[0:05:09] like this structure, so I'll go ahead
[0:05:11] and download this image, and then head
[0:05:13] back to Antigravity. I'll upload the
[0:05:14] image right here. Now, we want to
[0:05:16] recreate this exact design, but optimize
[0:05:19] it so it matches our own brand and
[0:05:21] project details. For that, I've provided
[0:05:23] a complete prompt that you can use as a
[0:05:24] reference. I'll copy this prompt, paste
[0:05:27] it into my agent, set the AI model to
[0:05:29] Gemini 3.6 Flash, and hit send. After a
[0:05:31] few minutes, our hero section design is
[0:05:34] complete. Okay, the overall design and
[0:05:36] look of the hero section looks really
[0:05:37] nice, but I want to make a couple of
[0:05:39] changes. First, I want to remove this
[0:05:41] image from the center, and I also want
[0:05:43] to remove any background effects so we
[0:05:45] can apply the scroll animation in the
[0:05:48] next step. So, I'll paste the prompt
[0:05:49] explaining the changes I want and
[0:05:51] Antigravity will update the project. And
[0:05:53] there we go. It's exactly what I wanted.
[0:05:55] Now, it's time to apply the scroll
[0:05:57] animation. For that, I've also provided
[0:05:59] a complete prompt that you can use to
[0:06:01] apply the animation in one go. But
[0:06:03] before running the prompt, you need to
[0:06:04] make a few changes. Here, for the last
[0:06:07] frame number, you need to make sure that
[0:06:08] it matches the exact same number in your
[0:06:10] zip file. So, open your zip file, check
[0:06:13] the last frame number, and then replace
[0:06:15] that number here. Also, make sure that
[0:06:17] the frame image name matches the actual
[0:06:19] image names inside your zip file. And
[0:06:22] make sure to update that in the scroll
[0:06:23] logic section as well.
[0:06:25] Finally, you need to mention the
[0:06:26] location of the zip file here. In my
[0:06:28] case, the zip file is inside the public
[0:06:32] folder of my project. So, I'll
[0:06:35] right-click on this file and copy its
[0:06:36] relative path.
[0:06:38] Then I'll paste it right here in the
[0:06:40] prompt. And that's it. Our prompt is
[0:06:42] ready.
[0:06:43] I'll go ahead and copy the entire
[0:06:44] prompt, paste it into Antigravity, and
[0:06:46] hit send. That's it. After a few
[0:06:48] minutes, our project is updated. And
[0:06:51] there we go. And if I scroll down, we
[0:06:53] can see this really smooth animation.
[0:06:55] The effect looks perfect. But as you can
[0:06:57] see here, because of the color of the
[0:06:59] background, our text is not fully
[0:07:01] visible. So, I'm going to ask my AI
[0:07:03] agent to refine the design, make the
[0:07:05] headline text bolder, and change some of
[0:07:07] the visuals. I'll also ask the agent to
[0:07:10] add a shadow effect so our text is fully
[0:07:12] visible on top of the animation. I also
[0:07:14] asked ChatGPT to refine this hero
[0:07:16] section for me, and the results were
[0:07:18] great. So, I'm going to attach this
[0:07:19] image to the prompt as a reference as
[0:07:21] well. Now, I'll copy this prompt,
[0:07:23] navigate back to Antigravity, upload the
[0:07:25] reference image to the chat, and then
[0:07:27] paste the prompt right here. I'll hit
[0:07:29] send, and within a few seconds, it will
[0:07:31] update the design with a much better
[0:07:33] look. And there we go. Our hero section
[0:07:35] is now complete, and we're ready to move
[0:07:37] on to the next step. For the next step,
[0:07:38] we're going to add two more sections to
[0:07:40] our project. I've prepared the prompt
[0:07:42] for this as well. First, I want to
[0:07:43] create an infinite logo carousel section
[0:07:46] with two rows. The first row will
[0:07:48] continuously move from right to left,
[0:07:51] while the second row will move in the
[0:07:52] opposite direction. And below this
[0:07:54] section, I want to create a bento grid
[0:07:57] section. For the bento grid section, I'm
[0:07:59] going to explore Pinterest once again
[0:08:01] and find a reference design that I like.
[0:08:03] So, I really like this bento grid
[0:08:05] design. I'll go ahead and download it,
[0:08:07] just like that. Now, I'll copy my
[0:08:08] prompt, navigate back to Antigravity,
[0:08:10] paste the prompt right here, and also
[0:08:12] upload the reference image. That's it.
[0:08:14] I'll hit send and wait for the results.
[0:08:16] Finally, it's done generating, and now
[0:08:17] if I scroll down, we have our infinite
[0:08:19] logo carousel with two rows moving in
[0:08:22] opposite directions. And just below
[0:08:24] that, we have our bento grid section
[0:08:27] with different cards and visuals
[0:08:28] arranged in a clean, modern layout. But
[0:08:30] as you can see, we have some design
[0:08:32] problems with these three cards that
[0:08:34] need to be fixed. So, I'll go ahead and
[0:08:36] take a screenshot of them. I also want
[0:08:38] to remove the container box around each
[0:08:41] logo in the logo carousel, and I want to
[0:08:43] set the logo colors to black and white.
[0:08:45] So, I'll navigate back to Antigravity
[0:08:48] and paste a prompt explaining all the
[0:08:50] changes I want to make, and then I'll
[0:08:51] upload the screenshot to the chat as a
[0:08:53] reference. That's it. Now, I'll hit send
[0:08:55] and Antigravity will fix everything for
[0:08:57] us in about a minute. And there we go.
[0:09:01] It looks awesome now. Okay, now it's
[0:09:04] time for the interesting part of this
[0:09:05] video, which is creating and integrating
[0:09:08] a 3D model into our project. For this,
[0:09:10] all you need is an image of your product
[0:09:13] or any model that you want to turn into
[0:09:15] a 3D model. For example, I really like
[0:09:17] this astronaut sitting on the orange
[0:09:19] bus, but before we can use this model, I
[0:09:22] need to prepare the image by removing
[0:09:23] the background, the land, and the text
[0:09:26] from it. So, I'm going to use ChatGPT to
[0:09:28] make these changes. I also want to
[0:09:30] remove the ladder, so I'll mention that
[0:09:31] as well send. And there we go. The model
[0:09:34] looks nice, but let's actually add the
[0:09:36] ladder back and see how that looks.
[0:09:38] Okay, I think this version is better, so
[0:09:41] I'll I'll download this image. For the
[0:09:43] 3D model generation, I'm going to use a
[0:09:45] tool called Trepo, which is a really
[0:09:47] powerful AI 3D model builder. So, just
[0:09:50] create your account here and then upload
[0:09:51] your image. Here, we have two options,
[0:09:54] best quality and clean topology. I'm
[0:09:57] going to go with best quality and hit
[0:09:58] send. And after about a minute, it
[0:10:00] generates a clean and professional 3D
[0:10:02] model that you can customize, export,
[0:10:05] and use in your own projects.
[0:10:06] Okay, now let's also test the smart mesh
[0:10:09] option. I'll go ahead and upload my
[0:10:10] image here once again, and once it's
[0:10:12] uploaded, we can also see a generate
[0:10:14] multi-views feature here. So, I'm going
[0:10:16] to use this option as well.
[0:10:18] Perfect. Now, let's hit generate. And
[0:10:21] just like that, it starts generating the
[0:10:22] mesh from our image. Once you're happy
[0:10:25] with the result, simply hit the texture
[0:10:26] button, and just like that, it starts
[0:10:28] creating our textured 3D model. And
[0:10:31] there we go. This actually looks better
[0:10:32] than the previous result. So, let's
[0:10:34] export this one.
[0:10:36] I'll hit the export button, and make
[0:10:38] sure to export it in GLB format, since
[0:10:41] that's the format we're going to use
[0:10:42] later to integrate our 3D model into the
[0:10:44] website. Okay, now that we have our 3D
[0:10:47] model, it's time to find a design
[0:10:48] reference. I'm going to create another
[0:10:50] section for our website, a 3D creator
[0:10:52] tool section. And I found this design
[0:10:55] that I really like. So, I'll go ahead
[0:10:56] and download it, then navigate back to
[0:10:58] Antigravity. I'll upload the reference
[0:11:00] image and paste a prompt asking the
[0:11:01] agent to create our new section based on
[0:11:04] this reference image. Now, while it's
[0:11:06] updating our app, let's move the 3D GLB
[0:11:08] file into our project folder. For that,
[0:11:11] I'll create a new folder inside the
[0:11:12] public folder and name it 3D model, and
[0:11:15] then I'll drag and drop the 3D model
[0:11:17] right inside this folder.
[0:11:19] That's it. Now, let's take a look at the
[0:11:21] task results.
[0:11:22] Okay, it's done generating, and now we
[0:11:24] have a new section here with interactive
[0:11:26] elements and a really nice layout. But,
[0:11:28] I want to add my own 3D model right here
[0:11:30] in the center. So, I'll go ahead and
[0:11:32] take a screenshot of this large
[0:11:34] container, navigate back to
[0:11:35] Anti-Gravity, and here I'll ask the
[0:11:37] agent to remove this section and replace
[0:11:39] it with my 3D model. And at the end of
[0:11:41] the prompt, I also need to provide the
[0:11:43] path to my 3D model GLB file, just like
[0:11:46] that. Now, I'll upload my screenshot
[0:11:48] here and hit send.
[0:11:50] After about a minute, our project will
[0:11:52] be updated. And as you can see, it
[0:11:54] applied all of the changes we asked for,
[0:11:56] and this looks perfect. Actually, all
[0:11:58] the elements here are not just simple
[0:12:00] mock-up designs. Everything is working
[0:12:02] just like a real 3D platform, which is
[0:12:04] quite impressive. As the final step, I
[0:12:06] just want to ask my agent to change the
[0:12:08] overall design and colors of this
[0:12:10] section, and also add a background image
[0:12:12] here.
[0:12:13] I'll also replace the images inside the
[0:12:15] Bento cards with some better visuals.
[0:12:18] And finally, I'll ask it to add a footer
[0:12:20] to our project as well. And just like
[0:12:22] that, you can add, remove, edit, and
[0:12:24] customize almost anything in your
[0:12:26] project simply by giving your AI agent
[0:12:29] the right instructions. And the best
[0:12:31] part is that we were able to build this
[0:12:32] entire experience step-by-step, from
[0:12:35] creating the initial image assets,
[0:12:37] generating the cinematic animation, and
[0:12:38] turning it into a scroll-driven hero
[0:12:40] section, all the way to creating
[0:12:42] interactive sections, and integrating
[0:12:44] our own custom 3D model. I've included
[0:12:46] all of the prompts and resources I used
[0:12:48] throughout this tutorial in the
[0:12:49] description below. And if you enjoyed
[0:12:51] this tutorial, make sure to like the
[0:12:53] video, subscribe to the channel, and let
[0:12:55] me know in the comments what you want me
[0:12:57] to build next. Thanks for watching, and
[0:12:59] I'll see you in the next one.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
