# Transcripción — I Built an App for My House With AI

- Fuente: https://www.youtube.com/watch?v=CgkdaeQ58eE
- Canal: Peter Lindgren
- Publicado: 2026-10-26 · Duración: 13:51 (831 s, `lengthSeconds` del reproductor)
- Idioma original: inglés · Captions automáticos de YouTube (`en-orig`, pista `variant=gemini`), 421 cues deduplicados, 2.669 palabras
- El video no tiene capítulos oficiales en la descripción: el mapa temporal del `outline.md` se derivó de los cues.

## Glosario de errores del ASR

| En el audio (ASR) | Correcto |
|---|---|
| «EXO» | **Exo**, el asistente del ponente en pantalla (nombre de su app/asistente) |
| «code X», «Codex» | **Codex** (el agente de coding de OpenAI) |
| «PRMGR Observatory» | **PRMGR Observatory** — nombre real del producto del ponente (`prmgr.org`); el ASR lo escribe bien salvo casos aislados |
| «Homey Pro» | **Homey Pro** (hub de domótica de Athom) |
| «Container Manager» | **Synology Container Manager** (Docker en el NAS) |
| «Home Assistant» | **Home Assistant** (alternativa OSS que el ponente descarta a favor de Homey) |
| «Modbus» | **Modbus** (protocolo de lectura de la bomba de calor) |
| «Meta» | **Meta APIs** (Instagram, para leer y responder comentarios) |
| «NAS» | **NAS** (Synology) — «a storage computer on your home network» (00:07:48) |
| «the of the house» (00:04:01) | «what **the rest** of the house is doing» — frase cortada por el ASR |

## Transcript

[00:00:02] Wow.
[00:00:03] This uh
[00:00:05] turned out to be a lot bigger than I
[00:00:06] thought it would be.
[00:00:07] >> [music]
[00:00:07] >> Which part do you mean?
[00:00:09] >> Well, the entire app that is running on
[00:00:11] my TV, which is basically a [music]
[00:00:13] control center for everything that I do
[00:00:14] on a daily basis in my house.
[00:00:17] >> Well, you asked for it.
[00:00:19] >> Yeah, I know.
[00:00:21] But I never really thought we'd get to
[00:00:23] this point.
[00:00:24] >> And it all started with a heat pump
[00:00:26] graph.
[00:00:27] >> Yeah. We should probably scroll back to
[00:00:30] getting genuine.
[00:00:31] >> Agreed.
[00:00:34] >> Hey, EXO.
[00:00:35] >> Yeah.
[00:00:35] >> I kind of need your help with something
[00:00:36] here.
[00:00:37] >> Happy to assist. Go ahead.
[00:00:39] >> Yeah, I want to know what my heat pump
[00:00:40] does throughout the day.
[00:00:41] >> Okay.
[00:00:42] >> You know, when the compressor starts,
[00:00:43] the amount of electricity that is
[00:00:45] drawing, and whenever the hot water
[00:00:46] heats up, and that kind of stuff.
[00:00:48] >> Do you mainly want to check it live or
[00:00:50] look back at what happened?
[00:00:53] >> I don't know. I'm going to say both
[00:00:54] ideally because, you know, looking at
[00:00:56] what the heat pump does right now is not
[00:00:58] going to tell me what it did 3 hours
[00:00:59] ago. All right?
[00:01:00] >> Correct. In that case, we need to gather
[00:01:02] and record the data it provides.
[00:01:04] >> Oh, and by the way, I want to make it
[00:01:06] attractive, okay?
[00:01:07] >> [sighs]
[00:01:07] >> I assumed there would be a logo
[00:01:09] involved.
[00:01:10] >> So, this was basically how this entire
[00:01:11] project started because we have a
[00:01:13] connected heat pump, so it it's capable
[00:01:15] of showing a bunch of different graphs
[00:01:17] and data, but the app that comes with it
[00:01:20] is incredibly unintuitive in my opinion.
[00:01:23] So, I thought to myself, wouldn't it be
[00:01:25] possible that together with ChatGPT and
[00:01:28] Codex make my own app that presents the
[00:01:32] numbers that I want to see
[00:01:34] in a nice way because I haven't been
[00:01:37] playing around that much with Codex, so
[00:01:38] I thought it would be a great start. And
[00:01:40] before we continue with the video, how
[00:01:42] would someone go about to make a project
[00:01:45] like this on their own if they want to?
[00:01:47] >> First, they'd need choose what they want
[00:01:49] to know. Then check whether the
[00:01:51] equipment gives us a way to read the
[00:01:52] information we'd want.
[00:01:54] >> Okay. And uh how are we getting it from
[00:01:56] mine?
[00:01:56] >> Your heat pump uses something called
[00:01:58] Modbus. Think of it as a shared
[00:02:00] language. Our app asks for the water
[00:02:02] temperature and the heat pump sends back
[00:02:04] a number. For this project, we're only
[00:02:07] asking it for measurements.
[00:02:08] >> Oh, so you're basically asking it
[00:02:10] questions then?
[00:02:10] >> Very repetitive ones.
[00:02:12] >> So, the first thing that I recommend to
[00:02:14] do whenever you want to start a project
[00:02:15] like [music] this is to start small,
[00:02:17] like start with one unit, ask one
[00:02:19] question. Don't try to create this
[00:02:21] behemoths that you don't have control of
[00:02:25] to begin with because you can elaborate
[00:02:26] that later.
[00:02:28] Um but it's very good to
[00:02:31] kind of inspect the units and all the
[00:02:34] things and make sure that the code X
[00:02:36] connection is going to work. And another
[00:02:38] thing that I actually used a lot in this
[00:02:40] project is the Homey Pro. But we're
[00:02:43] going to get to that later in the video,
[00:02:45] so stay tuned. Keep watching. And if you
[00:02:47] haven't subscribed yet, I highly
[00:02:49] recommend you do so because this is a
[00:02:51] fun video and there's going to be more
[00:02:52] of these, for sure. And a lot of other
[00:02:55] tech stuff in between.
[00:02:59] Okay.
[00:03:00] >> Here's the compressor activity. Put the
[00:03:02] temperature underneath it and you can
[00:03:03] follow both over the same period.
[00:03:05] >> All right, so that's when it started and
[00:03:08] then we can see what happened here,
[00:03:09] right?
[00:03:10] >> Yes. We save each reading with the time
[00:03:12] it was taken. That's how we can put the
[00:03:14] day back together on a graph.
[00:03:16] >> Is there any possibility to calculate
[00:03:17] what it costs when it's running?
[00:03:19] >> Eventually, if we verify the electrical
[00:03:21] power reading.
[00:03:22] >> What is wrong with it now?
[00:03:23] >> We're getting a number. We still need to
[00:03:25] check exactly what it measures and
[00:03:27] whether we're reading the units
[00:03:28] correctly. Until then, using it to work
[00:03:31] out a cost could give you the wrong
[00:03:32] answer.
[00:03:33] >> Okay. So, don't turn it into cost just
[00:03:35] yet then.
[00:03:36] >> Agreed. Multiplication would make it
[00:03:38] more precise looking.
[00:03:39] >> This is actually a very important step
[00:03:41] if you want to try this out yourself. Uh
[00:03:43] you got to make sure that the readings
[00:03:45] are correct so that all the info that
[00:03:47] you're getting from the app that you're
[00:03:49] building is true to the stuff that you
[00:03:52] actually have in your heat pump or
[00:03:54] whatever kind of device [music] that
[00:03:55] you're testing with. You know what would
[00:03:57] be very useful though?
[00:03:59] >> I suspect we're about to add something.
[00:04:01] >> Seeing what the of the house is doing at
[00:04:05] same time.
[00:04:05] >> We can bring in the solar, battery, and
[00:04:07] grid readings.
[00:04:09] >> Can we also separate the garage from the
[00:04:11] house?
[00:04:11] >> The garage has its own meter. So, we
[00:04:13] take what the whole property is using,
[00:04:15] subtract the garage, and what's left is
[00:04:17] the house. We only show that split when
[00:04:20] both readings are reliable.
[00:04:21] >> Wait, why can't we just use the readings
[00:04:23] that we got now?
[00:04:24] >> Because the house can also be running on
[00:04:26] solar or battery power. The grid
[00:04:28] connection only shows what passes
[00:04:30] between you and the grid.
[00:04:31] >> So, we could be using quite a lot of
[00:04:33] electricity, but we're still buying very
[00:04:36] little. [music]
[00:04:36] >> Exactly.
[00:04:37] >> And what about the car charger?
[00:04:39] >> We can show it. It's consumption is
[00:04:41] already inside the total, [music]
[00:04:42] though.
[00:04:43] >> Yeah, so don't don't add that again,
[00:04:45] okay?
[00:04:46] >> Unless you'd like an electricity bill
[00:04:47] with a fictional subplot.
[00:04:49] >> No, I'm good.
[00:04:53] Dude, this looks incredible.
[00:04:56] >> I agree. It suits you.
[00:04:57] >> Do you think we can make it look a
[00:04:59] little bit more like their house?
[00:05:00] >> Do you have a reference photo we could
[00:05:02] use?
[00:05:03] >> Do [snorts] I have a reference?
[00:05:04] It's like asking me if I have a drone or
[00:05:06] camera. Of course, I do. Several.
[00:05:08] >> I had a feeling you'd do.
[00:05:09] >> Here's a good one for you, okay?
[00:05:10] >> I'll work my magic on it.
[00:05:12] >> Add that in.
[00:05:13] >> Done.
[00:05:14] >> [snorts]
[00:05:15] >> Okay, that's
[00:05:16] really cool.
[00:05:19] So, would it be possible that if I click
[00:05:20] the solar panels, it takes me to all the
[00:05:22] info about the solar system?
[00:05:24] >> Yes, that would be possible.
[00:05:26] >> And maybe we could add a little bit of a
[00:05:27] slight glow depending on how much
[00:05:29] they're producing beneath them as well.
[00:05:31] >> A subtle glow?
[00:05:33] >> Yes.
[00:05:34] Subtle.
[00:05:35] Not too much.
[00:05:36] >> Done. The more electricity the panels
[00:05:38] are making, the stronger the glow. If
[00:05:40] they're making nothing, or we haven't
[00:05:42] had a fresh reading, the pulse stops.
[00:05:44] >> That is awesome.
[00:05:45] So, this is honestly like what most of
[00:05:48] the process looked like. I told the
[00:05:51] Codex what I wanted to have, and then
[00:05:53] Codex made it for me, and then I tried
[00:05:55] everything out, and then I found the
[00:05:57] loopholes, and found the things that I
[00:05:59] wanted to adjust, and then I told the
[00:06:01] Codex again to adjust the things that I
[00:06:02] wanted to adjust, and so on and so
[00:06:04] forth. You know, I do have my 3D
[00:06:05] printers connected to my Homey. So, do
[00:06:07] you think it would be possible to get a
[00:06:10] estimated finished time off the print
[00:06:12] into this as well?
[00:06:13] >> They already display the remaining time.
[00:06:15] >> Yeah, I know.
[00:06:17] But, then I'm doing the maths every
[00:06:18] time. If we add that, then I can just
[00:06:21] see which timestamp the print is going
[00:06:23] to be finished, right?
[00:06:25] >> Fair. We can calculate a finish time
[00:06:27] from the printer's estimate.
[00:06:28] >> Yes, that's how it should be.
[00:06:30] >> We've successfully removed some mental
[00:06:32] arithmetic. [music]
[00:06:33] >> Yeah, you can joke all you want, but I'm
[00:06:35] still going to use this. And that is
[00:06:37] also a very important thing with this
[00:06:39] project, because all my smart devices
[00:06:41] that I have in my house is connected to
[00:06:43] the Homey [music] Pro. And since all the
[00:06:46] devices are already connected to it,
[00:06:48] it's possible to create an app for the
[00:06:51] Homey Pro
[00:06:51] >> [music]
[00:06:52] >> and pull all the data to my interface
[00:06:55] directly from it. So, it basically gave
[00:06:57] us a really good foundation to work
[00:06:59] from. This would probably work with Home
[00:07:01] Assistant, too, but the reason that I
[00:07:04] kind of went for Homey is because
[00:07:05] everything is connected to it. You have
[00:07:07] a nice UI. It's very simple, and you can
[00:07:10] also create a lot of simple flows and
[00:07:13] advanced flows with the help of ChatGPT
[00:07:16] and Codex, because you can connect
[00:07:18] ChatGPT directly to your Homey.
[00:07:22] Pretty cool. You know, I was thinking
[00:07:23] about one thing.
[00:07:24] >> Yes.
[00:07:25] >> What is going to happen if I turn my Mac
[00:07:27] off? Because everything is stored
[00:07:29] locally, right?
[00:07:30] >> The part collecting and saving the
[00:07:32] readings stops. Shut down the Mac and we
[00:07:34] stop building that history.
[00:07:36] >> Yeah, so we need to find some sort of
[00:07:37] solution that can run even though the
[00:07:40] Mac is turned off.
[00:07:41] >> Your Synology could probably do that job
[00:07:43] instead.
[00:07:44] >> the box that we use for storage?
[00:07:45] >> Yes, it's called a NAS, a storage
[00:07:48] computer on your home network. Yours can
[00:07:50] also run this app. It already stays on,
[00:07:52] so it can keep collecting the readings
[00:07:54] while your Mac sleeps.
[00:07:55] >> Okay, so what is it that you're actually
[00:07:57] going to move over there?
[00:07:58] >> We move the bit that collects the
[00:07:59] readings, the history we've already
[00:08:01] saved, and the saved connections it
[00:08:03] needs. Your screens then ask the
[00:08:05] Synology for that information.
[00:08:06] >> So, there's basically two parts that is
[00:08:08] worthy to understand here. One is that
[00:08:11] we move the data collection point to the
[00:08:13] NAS unit where it stores all the data
[00:08:16] and saves everything locally on the
[00:08:18] drive, and then the Mac is going to be
[00:08:22] the thing that actually displays all the
[00:08:24] data that we have saved on the NAS unit,
[00:08:27] which I think is pretty cool.
[00:08:29] >> We used a Synology tool called Container
[00:08:31] Manager. It runs a packaged [music] copy
[00:08:33] of Observatory with the software it
[00:08:35] needs.
[00:08:35] >> Okay, so we keep the history when we're
[00:08:37] updating the app, then.
[00:08:38] >> Yes. The app and the saved history live
[00:08:41] separately. That means we can replace
[00:08:43] the app when we update it without
[00:08:44] replacing all the readings you've
[00:08:46] collected.
[00:08:46] >> Well, that sounds important. I guess.
[00:08:49] >> It tends to become very important
[00:08:51] immediately after someone forgets.
[00:08:56] >> We are living in the future.
[00:08:58] >> So, they say.
[00:09:00] >> By the way, do you think we could get it
[00:09:01] up on the TV?
[00:09:02] >> The PRMGR Observatory?
[00:09:04] >> Yeah, like an actual installed app.
[00:09:06] [music] I want to be able to open it
[00:09:07] with my remote.
[00:09:08] >> Sounds possible. What model is it?
[00:09:10] >> Uh I don't know. It's an Android TV.
[00:09:13] >> Okay, so it runs Google TV. That's the
[00:09:15] software behind its home screen and
[00:09:17] apps. It's built on Android, so we can
[00:09:19] make an Android TV app and install it on
[00:09:22] this television.
[00:09:23] >> This is actually one of the first things
[00:09:24] that you need to check if you want to do
[00:09:26] the TV part yourself. Find the exact
[00:09:28] model, the operating system, and uh
[00:09:31] how you can unlock the developer mode or
[00:09:35] development mode. I don't know what it's
[00:09:37] called exactly, but basically
[00:09:39] need to allow the codecs to actually
[00:09:42] enter your TV, if that makes sense.
[00:09:45] Uh let's take a look. Settings.
[00:09:49] Okay. Press seven times.
[00:09:55] It says that I'm a developer.
[00:09:56] >> You've unlocked an extra settings menu.
[00:09:58] We still need to switch on debugging.
[00:10:00] That's what lets this Mac connect and
[00:10:02] install our app once you approve it on
[00:10:04] the TV.
[00:10:04] >> Okay, so [music] that wasn't the entire
[00:10:06] qualification, I guess then.
[00:10:07] >> Don't worry. I'll handle it for you.
[00:10:10] The PRMGR Observatory is now live on the
[00:10:13] TV.
[00:10:14] >> Would you look at that?
[00:10:23] >> [music]
[00:10:32] [music]
[00:10:37] >> I don't know about you, but
[00:10:39] I think that this entire [music] thing
[00:10:40] is bonkers. It is so incredibly cool at
[00:10:44] the same time as it's a little bit
[00:10:46] scary, but I have no experience in
[00:10:48] designing smartphone apps or smart TV
[00:10:50] apps or dashboards [music] or whatever,
[00:10:53] but I do have experience within smart
[00:10:54] home and design because I'm making my
[00:10:56] own clothes, I'm doing a lot of work in
[00:10:58] Illustrator. So, to be able to combine
[00:11:00] that has been very cool, especially with
[00:11:03] this project. And another cool thing
[00:11:05] that I'm going to do with this project
[00:11:07] is that I'm going to give you all the
[00:11:08] source files so that you can just
[00:11:10] download that and connect your code X to
[00:11:12] the GitHub, and then you can create your
[00:11:15] own dashboard kind of similar way that I
[00:11:17] have. So, this right here is the main
[00:11:19] dashboard that I ended up with. I mean,
[00:11:21] like I could probably keep tweaking
[00:11:22] [music] this forever, but there's no
[00:11:25] need to keep working on something that I
[00:11:27] think is good. Now, it's just to
[00:11:29] fine-tune the details. But, you can see
[00:11:32] everything at a glance here, which makes
[00:11:33] it very easy and very simple to know how
[00:11:37] everything is working with the house.
[00:11:39] And when you click on the house, for
[00:11:40] example, you get all the data about the
[00:11:42] house that you might need. If you click
[00:11:45] on the solar panels, you get all the
[00:11:47] data about the solar panels straight
[00:11:49] served on the dashboard as well.
[00:11:52] And if you go to the garage, then you're
[00:11:55] going to be able to see all my
[00:11:57] work-related stuff at a glance, which I
[00:11:59] think is pretty cool. So, if you go back
[00:12:01] to the home overview and scroll down a
[00:12:03] little bit, uh I can see my live cameras
[00:12:07] that is around the property, my
[00:12:09] Instagram accounts, my YouTube accounts,
[00:12:11] and my latest posts and how they
[00:12:14] performed as well as my
[00:12:18] uh Instagram comments. I can actually
[00:12:19] reply from this dashboard directly
[00:12:22] [music]
[00:12:22] because I use the APIs from Meta. And uh
[00:12:26] I can also go and see here audience and
[00:12:28] trends and then you get a trend report
[00:12:30] [music] kind of
[00:12:32] straight up from your own dashboard,
[00:12:34] which I think is cool.
[00:12:36] And then you have my 3D printers, uh
[00:12:39] everything else that you might want to
[00:12:40] have straight up in the dashboard.
[00:12:43] So, I think that being able to see all
[00:12:47] of this
[00:12:48] right in front of your eyes without
[00:12:49] having to click in multiple different
[00:12:51] programs [music] and tabs and so on and
[00:12:53] so forth is
[00:12:56] like it's so good and that is one of the
[00:12:58] reasons that I created it. And another
[00:13:00] detail that I actually did was that the
[00:13:03] lights outside
[00:13:05] when it's night then I can turn on the
[00:13:09] lights on my house
[00:13:12] in real time. So, when lights turn on
[00:13:14] outside, it turns on on the image as
[00:13:16] well. And I think that that is pretty
[00:13:18] sick.
[00:13:19] >> [music]
[00:13:19] >> It's a nerdy thing, but this entire
[00:13:21] thing is nerdy. So, if you like this
[00:13:23] video, don't forget to subscribe and um
[00:13:26] don't forget to comment. Like, are you
[00:13:27] going to use this? Are you going to try
[00:13:29] it out? Are you going to design
[00:13:30] something yourself? I would love to
[00:13:32] know. So, do drop a comment down below
[00:13:34] and um
[00:13:36] I hope I will see you in the next video
[00:13:38] and uh stay safe because
[00:13:41] it's a crazy world out there right now.
[00:13:44] All right.
[00:13:45] Peter from Sweden is saying goodbye.
<!-- project: github.com/gonzoblasco/workspace_openclaw -->
