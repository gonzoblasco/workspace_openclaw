# Transcripción: Codex & AI Coding Agents — Learn Agentic Coding

- Fuente: https://www.youtube.com/watch?v=ajfQWhGQGLE
- Canal: Scrimba
- Expositor: Tom Chant (Head of Education, Scrimba)
- Duración: 1:50:43 (6643 s, medida en el reproductor)
- Idioma original: inglés · Transcripción: ASR en inglés, 2.968 cues, ~23.900 palabras
- Descargada: 2026-11-10 con `youtube-transcript-api` (el endpoint `timedtext` del HTML devolvió 0 bytes sin `pot`)
- Curso interactivo oficial: https://scrimba.com/learn-agentic-coding-c0g68l84pg (el código de cada lección vive ahí, no en el video)

## Glosario de errores del ASR

| ASR dice | Real |
|---|---|
| Scribbis / Scriber / Scriber's | Scrimba |
| Tomch Chant | Tom Chant |
| Codeex / codecs | Codex |
| agents.mmd / agents.m | AGENTS.md |
| config.l / Config.l / config.comtoml | config.toml |
| Shad CN / Shadcn | shadcn (shadcn/ui) |
| mpm / nmp | npm |
| process.mm | process.env |
| M / M.local | .env / .env.local |
| characterization / characterisation | characterization test (test de caracterización) |
| low risk / on request / full access | approval policy: untrusted / on-request / never |
| danger full | `danger-full-access` (sandbox_mode) |
| Stylist | app del curso (e-commerce demo, "Stylist") |

_Los cues no se editan: los errores del ASR se resuelven con este glosario._

---

## Transcript

**[00:00]** Agentic Coding uses AI agents to read your codebase, edit multiple files, and run tests alongside you. In this hands-on course, Scribbis Tomch Chant shows you how to get reliable results from tools like Codeex by managing context, planning tasks, and verifying every change. You will practice prompting, setting up agents.mmd, testdriven development, git safety,

**[00:26]** secret management, and connecting tools via MCP. It's built for both experienced developers adding AI to their workflow and non-coders building software from scratch. Back in the early days, developers actually had to write their own code. And if they needed help or advice, they had to ask a colleague or go somewhere like Stack Overflow, where you could

**[00:53]** normally get help pretty quickly. Although the experience left something to be desired. But then in late 2022, AI went mainstream and developers could get bespoke code snippets written for them by chat GPT, which they could then paste into editors. Agentic coding is the next paradigm shift. It's a software development approach in which the AI system is right there in the editor and

**[01:18]** that AI has got a degree of autonomy to carry out all sorts of programming tasks such as reading and editing files, writing code, running commands, running tests, iterating, so going over the same task multiple times until it's completed satisfactorily, and using tools. All of which we're going to see examples of in this course. Now, the word agentic refers to the capacity to make decisions

**[01:45]** and adapt based on feedback from the results of its own actions. So, it's basically closing the loop between writing code and verifying that it works. If it's broken, the agent iterates over it again, but if it works, then all's good. The task is complete. So, is the human developer redundant? Heck no. Firstly, because AI can make mistakes, but more importantly, because

**[02:10]** agents are complex tools which depending on how they're used can produce results which are actually dangerous. So, they expose secrets, they expose client data, and they create malfunctioning apps. They can create code which is mediocre. So, the code is messy, it's hard to maintain, it's poorly documented, it's hard to extend. or they can create code which is excellent. It's clean, well

**[02:33]** doumented, easy to maintain, and easy to extend. And so that's really what this course is about. How to get the most from agents regardless of your coding level. And also how to do it safely and efficiently. And as we go, you're going to see that the human developer is still the key cog in the machine because from ideation through development to deployment, human input is not just

**[02:55]** desirable, it's a necessity. Now let's talk quickly about the agent options which are out there at the moment. The two biggest names in coding agents are OpenAI's Codeex and Anthropics Claude Code. But they're far from the only options. There are also tools like GitHub Copilot, Devin, Windsurf, and Cursor. And of course, there are more besides. The important thing to

**[03:17]** understand is that coding agents are becoming a category of tool rather than something tied to one company or model. Different coding agents do have their own conventions and their own configuration files, but there's a growing push towards shared standards and we will see that in this course and that means that although this course is codeex focused, what you learn in this

**[03:36]** course is useful right across the industry. Now we should also talk at this point about the different ways you can use coding agents and these basically fall into three categories. We have got the CLI or command line interface-based agents. These run from the command line and are especially popular with developers who are comfortable working in the terminal.

**[03:56]** Next up, we've got IDE based agents. These live inside your code editor like VS Code, giving you a more visual interface and controls that you can use without needing to know terminal commands. And on top of that, we've got desk or web-based agents. These put a graphical interface around the agent and can hide more of the underlying development workflow, making them more

**[04:17]** approachable for people who aren't used to working directly with code. And then on top of that, we've also got mobile and cloud possibilities as well. Now, there's plenty of overlap between these categories. And the same agent is often available in several forms. In fact, for both cloud code and codeex, we have got the desktop tool, the IDE extension, and the CLI tool as well. Now, in this

**[04:39]** course, we're going for the IDE based agent because it gives us the user friendliness of a graphical user interface while keeping us close to the code, which is ideal for web development. Okay, it's time to start learning how to use agents. The Scriber agent is open for business right here. So, in the next scrim, let's get hands-on with it.

**[05:03]** Let's get stuck into aic coding. This is Scribba's very own coding agent and it works a lot like Codeex. So everything you learn in this course is relevant to working with Codeex and other agentic [clears throat] platforms like Claude Code as well. We built this agent into Scriber so you could get hands-on practice right here in the lessons. And in fact that is

**[05:23]** going to start right now. I just built this landing page for a flavored mineral water company. or should I say the agent did it for me because all I needed to do was write this one short prompt. And I think you'll agree the results are pretty decent. But now we are going to make an addition underneath this hero section. So just about right here, let's add a sales section where we offer five

**[05:49]** bottles of mineral water for $10. So that is going to be your first challenge. In a moment, this scrim will automatically pause, and it's going to happen right when you reach that little Pac-Man style ghost on the timeline. When that happens, you can get to work on the challenge by typing your prompt in right here and sending it off with this button or just hitting enter. Now,

**[06:09]** we'll look at the art of prompting in more detail later in the course, but for now, just ask for what you want. Now, I should warn you, agents can take a bit of time, so don't be concerned if the agent is thinking for 20 or 30 seconds. It will get to work when it's ready. And when you're happy with what it's given you, click the green submit solution button, which you'll see at the top. And

**[06:29]** if you've successfully completed the challenge, you'll get confetti. Else, you'll get a hint to point you in the right direction, and you can try again and resubmit. Okay, so to recap, your challenge is to add a sales section offering five bottles for $10. Here comes the ghost. Go ahead and try that now. Okay, I really hope your first prompt

**[06:50]** was successful and you've now got a sales section offering five bottles for $10. I'm just going to type my prompt right here. I'll say add a sales section under the hero section. Offer five bottles for $10. Let's send that off and see the agent get to work. And it's already got to work. We can see in the background if I just close down the mini browser, it's working away on the HTML.

**[07:14]** And now it's adding some styles in styles.cs. CSS. Let's just see what's happening in the mini browser. If I scroll down, there we are. It's just appeared. Five bottles for $10. Special offer. And the agent is done. So, actually, that was really quick. Just 26 seconds. And it's nicely styled and exactly what we asked for. Now, while we're having our first play with the

**[07:35]** agent, I want to introduce you to what's really quite an important feature, and it's called diffs. And diffs is short for differences, i.e. what has changed. And you can see the diffs by clicking on these colorful numbers which you'll see alongside the files that have been changed. So if we click here on index.html, we can see red lines which is code which

**[07:55]** has been deleted and green lines which is the new code which was added. Now if you're a non-coder that doesn't mean too much to you right now and you don't need to worry about it. But for coders that can be really useful because you've got to remember that the human is still vital in agentic coding in lots of ways. And this is one place where you can catch problems and just keep an eye on

**[08:15]** what the agent is up to. Okay, that was a really easy first glimpse of the agent and a really basic prompt. But throughout this course, we are going to study a whole lot more. We're going to look at the art of prompting in more detail. We'll talk about giving the agent memory. We'll look at permissions so you can keep in control and we'll look at custom skills. Also, there's the

**[08:34]** context window to discuss testing, git and version control and MCP. Now, if you don't know what some of those things are, or indeed what any of them are, don't worry at all. Everything will be explained and we'll be taking it step by step. And along the way, you're going to have plenty of challenges so you can get hands-on and get some experience working with agents. Now, that does bring us to

**[08:55]** the question of who this course is for. Well, firstly, it's for devs who want to learn about agentic coding and specifically codecs. But it's also for people who don't professionally code but work in adjacent spaces. So designers and product managers for example. And on top of that, it's for anybody else who's interested in building apps with agents. And that's true regardless of coding

**[09:17]** level. [clears throat] Everyone will gain something from this course. And you don't need to understand the code we will be working with. I'll always give you a highle overview of what's going on. Okay, that's enough chatter. If you're ready to explore how agents like Codeex are supercharging the development process, let's go. When you talk about good prompting,

**[09:41]** you'll often hear people say, "Prompting is just asking for what you want, isn't it?" And that's kind of true. In fact, just asking for what you want will take you a long way. But it's not the whole picture. And if it's all you do, your results will plateau. Let's put it to the test. Here's an app I mocked up. It's really basic, but it's going to help demonstrate something. The app is

**[10:02]** used by delivery drivers. When they make a delivery, they hit log package and it just renders package number one delivered. They make a second drop off. They hit log package again. Package number two delivered. So, it is a really simple app and it's got really simple code. We've just got this HTML and a tiny bit of JavaScript in script.js. Okay, so it's time for a challenge.

**[10:24]** Sometimes packages get lost. So, your task is to add a second button. The second button is going to log lost packages and it should render for example package number four lost. Should be pretty simple, right? So the agent is open. Go ahead and get to work. Okay, so the easiest way for you to solve this challenge was probably just to copy and paste. Let's send that off.

**[10:48]** And I'm just going to open up index.html because I expect this is where we're going to see. Yep, absolutely. We've got a second button. And in script.js, js. We've got some updated JavaScript. Let's check it's working. So, we've got log package and log lost package. Okay, so that is pretty cool. But look at this code. Even if you really don't know much about code, you can probably see that

**[11:12]** the logic we've got here is basically the same as the logic we've got here. In fact, the only real difference between them is that we've got the word delivered here and the word lost here. The rest is the same. So this code is unnecessarily repetitive. You've probably heard the acronym dry, do not repeat yourself. Well, this code is not dry and that is a common problem with

**[11:36]** agent created code. The agent would rather add more code than refactor existing code and that can lead to bloated inelegant code which is ultimately harder to maintain. So how do we prompt better? Well, the core idea is this. Bad outcomes come from ambiguity. And so your job is to reduce ambiguity across three areas. What the agent's task is, what context the agent is to

**[12:03]** use, and what the output should look like. So when in doubt, you can structure your prompts like this. Task context output. In a moment, you're going to have a go at this yourself. But before you do that, I'm just going to put the code back to its original state. So we'll delete the extra button. And then in script.js, js. Let's just paste back in the original JavaScript. Okay,

**[12:26]** now we're back to where we were. Okay, let's head back to challenge.md and we're going to think task context output. And what we've got so far is basically part one of that. That is the task. Underneath I'm going to create headers for context and output. And then it's over to you. I want you to create a better prompt using this structure. I'm not going to say too much more other

**[12:52]** than that the context should be what parts of the codebase you want the agent to look at and the output doesn't need to be super technical. You don't need to know a lot of coding language to prompt this. Well, you just need to describe what output you're expecting based on what I've just said about the repetition that we saw in the code it created before. I'm going to leave you to puzzle

**[13:14]** that one out. Go ahead and get to work. Okay, hopefully you created a really good prompt and the agent gave you more elegant code. Let's just create a bit of space here. So, I'm going to paste in the context that I'm going to use. I'm saying inspect the existing code and use shared logic where possible. I've put avoid duplicating event handlers. This is not strictly speaking necessary. I

**[13:40]** did say you could do this without any technical language, but if we just go back to script.js, JS, we've got an event listener and then we've got a function here which fires when the event listener is triggered. That's called an event handler. And I'm just being really specific by saying avoid duplicating event handlers. Now for my output, again, no need to be super technical.

**[14:00]** I'm just going to say keep the code dry and easy to extend if we add more buttons later. Okay, I don't actually need to give the agent these headers. So I'm just going to copy and paste these individually. Okay, let's send that off and see what happens. And again, we'll open up index.js. I expect we're going to see another button that can't be avoided.

**[14:20]** Yep, there we've got the second button. Let's open up the mini browser and head to script.js. Okay, and now it's writing the logic quite differently. And it says it's done. Let's give it a test. So, we've got log package and log lost package and is working. And what we can see here is we've got much more elegant code. And now we've only got one event listener

**[14:42]** and one function to handle the event. So now our code is dry. And the major take-home here is that you should prompt for good code, not just UI outcome. That was our mistake first time round. We just thought about the outcome and the usability of the app. We did not think about code quality. So if you think about code quality and structure your prompts well, the overall performance of

**[15:05]** the agent and the code you get out of it is going to be much better. Codeex is actually better at imitation than interpretation. So if you care about the style, structure or patterns of your code, it might be a good idea to show rather than tell. So instead of describing how you want a function written, just show one or two model functions and then tell the agent to

**[15:32]** follow this style. Now I want to give you a big caveat here. AI can intuitit a lot as we've already seen. So, it's definitely not always necessary to model. Quite the opposite in fact. But modeling can be really useful. It's a really good tool to have in your kit and it can actually be a timesaver. And we're going to see an example of that right now. Here in API.js, I've got a

**[15:55]** script which is bringing in some JSON from the JSON placeholder API. At the moment, I've got these two functions, get post by ID and get user by ID. Get post by ID is using the async await syntax, the more modern syntax and get user by ID is using these chained then statements. Now, it's not at all important for you to understand the code. All you need to understand is that

**[16:20]** these functions are doing two very similar things, but they're doing them in a different way. The more modern syntax here, the older traditional syntax here. Now I want this second function refactored to use the async await syntax. I could just come to the agent and ask for it. But it might actually be quicker to do this as a comment prompt. Let me tell you what I

**[16:43]** mean. Codeex pays a lot of attention to local context. That means things like comments which are adjacent to a piece of code. So this is the function that I actually like the style of. So I'm going to put one comment above this and it's just going to say model function. Now your challenge is to write a comment prompt and I want you as concisely as possible to prompt the agent to refactor

**[17:08]** this function to use the modern async syntax just like we have in this first function. In this challenge MD file, I've given you some reminders because this is about showing not telling. You don't need to specify anything. Write your prompt as a comment above the function. That's the function you want to change. And then just tell the agent to read your comment. That is all you

**[17:31]** need to do. Now, I'm going to start you off with a reference point you can refer to when you brief the agent. I'm going to say to-do and in brackets I'll put AI. Now, over to you. You can write your comment prompt right here. You have got the reminders in challenge.md if you need them. Okay. Hopefully, you managed to do that without too many problems. All I'm going

**[17:53]** to say here is refactor this function to follow the same style as the model function. Let's save that. Now, that was probably quicker than going into an explanation about async await versus chaining with the agent. We've just said, "Here's a model. Now, go ahead and use it." So, let's prompt the agent. I'm just going to say, "Complete the to-do in API.js. JS and it's done in 20

**[18:22]** seconds. And what we can see is it's made a really close copy. So it's not just using the async await syntax, it's using the same error response handling as well. So now we've got this model function. We can actually scale and replicate this pattern massively across a codebase. So that is really really useful. Now I do just want to say a quick word about the comment I used

**[18:45]** which was to do and then in brackets AI. This is by no means a codeex feature or a feature of any other coding agent or any hard or fast coding rule. This has just become a bit of a convention. So you mark a comment with to-do in brackets AI and that just signals to any human reading your code that this is a task for AI. And it also makes it easier for AI agents to identify areas of code

**[19:10]** you want them to work on. So for example, you can prompt do all of the to-dos in index.js js and it will just go ahead and find them based on these comments. Now, this style that I've used here to-do in brackets AI is common, but you will also see other styles of comments used. That's just one example. Okay, that was a quick dive into prompting. Let's look at a few

**[19:31]** takehomes. Firstly, you want to reduce the ambiguity. Secondly, reduce the overbuild. And thirdly, give examples where appropriate. Okay, let's move on. I've got an expense tracker app which I just built with the agent and I'm going to use it to illustrate two problems particular to agentic coding. The first problem is more of a problem for dev teams and the second problem is an issue

**[20:00]** for solo coders as well. Now this app works really well. I've already added a couple of expenses. Let's add another. I'm going to say I bought some painkillers. Let's say they cost $10 and the category will be health. Click add and it gets added to the list of expenses. And we can choose an emoji here to see expenses by category. There's the food, the travel, and the

**[20:23]** health. Okay, this app at the moment is front end only. And what I want to do now is share it with a colleague who's going to add a database, some data visualization, and probably a ton of other features as well. And this presents us with problem number one. my colleague when they get this codebase will not have access to my conversation history and that's less than ideal

**[20:46]** because now anything which I've specified in this conversation history is going to be lost. For example, right here I've said for color palette use subtle shades of green. Now that's hardly Van Go levels when it comes to styling, but it is what I specified. And then down here I've said refactor the HTML and CSS to use BM naming conventions. And if you haven't come

**[21:07]** across Ben before, it's a naming convention for HTML that makes the CSS much easier to read. So there we've got two things which I've specified that when I share this codebase with my colleague, they are not going to know about. Now my colleagueu's agent will of course be able to review all of the code, but it's not going to know which aspects of that code were conscious

**[21:28]** developer decisions that I made and what was just whatever the agent decided to do. And that makes this code harder to maintain for a team of developers because individually they will not know what the other developers were thinking. And I did say there's a second problem. And this is a problem that you face even when you're working alone. Because every time we write to the agent, we send off

**[21:50]** a whole ton of data. And I've abbreviated this to two key points. We send off the prior conversation. That's what you can see right here. And we also send off relevant parts of the codebase. And there's a whole ton of stuff beyond that, but these are the two important ones for the moment. Because, as you can imagine, as you keep developing the app and the conversation with the agent

**[22:10]** grows and grows, eventually we will send so much information off to the agent that the model will get overwhelmed. We're actually going to send more information than the model can ingest. Now, later in the course, we're going to talk more about the problem of larger conversations and how you deal with them. But for now, I just want you to understand that if this conversation

**[22:29]** here gets too big, the information in it gets truncated and some of it will get lost and that can cause confusion down the line. So what we need is a way to specify the fundamentals of this app, the basic specifications. So we might want to list how the app should be built. So which text stack to use, which libraries, which coding patterns like BM. We might want to specify particular

**[22:54]** aspects of style. So the layout, the fonts, the color palette and also as things get more complex, how the app should be structured, how the code is organized and what the overall architecture of the app should be. And what we need to do is specify that to an agent away from these regular prompts because we know that these prompts here in this conversation do not get shared

**[23:15]** with colleagues and they do not necessarily stay intact if this conversation gets too big. So ideally what we need is a way to provide all of this information to the agent in a specific format that the agent knows how to use. And thankfully most agents like codeex give us a way of doing exactly that. So in the next grim we are going to talk about a special file called

**[23:37]** agents.md. Sash commands are a thing on most agentic coding platforms. If we bring the agent into focus and we hit slash, it brings up a list of commands which are available to us. For your challenge in this scrim, you are going to use this in it command. And it says here, generate or improve agents.mmd. That sounds like what we want. All you need

**[24:03]** to do is hit slash to bring up the menu. I'm going to close that down for now. Select that init command and send it off to the agent. And then keep your eyes over here on the file tree and see what happens. Then we'll talk about it. Okay, go ahead and get to work. Okay, let's give that a try. I'll hit slash, select init, and send it off to the agent. And it is writing us an

**[24:27]** agent.mmd file, which has appeared in our route right here. And let's just check out what we've got here. We've got the name of the app, which is just expense tracker. It tells us that it's a vanilla JavaScript project. It's got the commands to start the project. It's got the text stack, the project structure, which is really basic, and then some key coding patterns right here. So,

**[24:50]** basically a ton of goodness on how this app works. But what does this file actually do? Well, we saw this diagram before. We know we send off the prior conversation and relevant parts of the codebase with every prompt that we send to the agent. And we're going to add to that list agents.md. So now this file gets sent off with every prompt and it's given special

**[25:12]** priority. So whatever the agent does, it's going to have all of these specs in mind when it does it. And what's really good about this is that when we share this codebase with any colleague or collaborator who wants to work on the project, this agents.mmd file will be right there for them and their own agent to read. And whenever they prompt the agent, the info here will be given

**[25:33]** priority. So there will be continuity between the developers. And again, if this conversation ever gets truncated, any information gets lost. All of the information in here will persist. It will stay unchanged. So, it's really important that you keep agents.md file up to date at all times. That means if you make any big changes to the app, those changes should be reflected in

**[25:55]** here. And when we went for that init command, it did actually say generate or improve. So, you can use that command again to update this agents.md file. And that is something you should do periodically. Just before we wrap up this scrim, I want to say a quick word about crossplatform compatibility. Although agents.md is heavily associated with codeex, the concept actually

**[26:18]** emerged as a cross tool convention with codeex among the early tools that helped establish it. So you will find that an agents.md file is read and respected by a whole range of agents including devin, cursor, windsurf and many others. So whichever agent you go on to work with, knowing about agents.mmd is going to be highly relevant. Okay, there's just a little bit more to say about agents.mmd

**[26:42]** files. So in the next grim, let's look at how you can have multiple agents.md and why you might want to. In both scribbers agent and codeex, you can have more than one agents.mmd file. At the moment, we've got our agents.mmd file in the root of our project and influences decisions taken by the agent for all of the files and folders in this project. Now, we could also have one in

**[27:09]** a lower level folder which has specific guidance for all files under it. So, if I create a backend folder, I could also have an agents.md file right here and that would be for specs relevant to the backend files only. Now in codeex there's another potential use of agents.mmd and that is in the global scope. That means that it influences every codeex project you work on. So one

**[27:33]** agents.md file multiple projects. This globally scoped agents.mmd file lives in a special codeex folder which you'll find in the home directory of your PC. And that precise location will of course differ depending on whether you're using Windows, Mac or Linux. Now, when you've located thecodeex folder, you can create an agents.md file inside it or indeed have the agent do it for you. And a

**[27:57]** global agents.mmd file might seem like a strange idea. Why are you applying the same specs to multiple projects? Well, it can be really useful if you want to enforce, for example, certain coding or styling conventions across every project you work on. Now, if we're going to have multiple agents.md files, we need to talk about hierarchy because there could be clashes. agents.mmd files will be

**[28:19]** read by the agent in this order. It's going to read the global scope first, then the project scope, and then the folder scope. And it's going to give priority to the closest agents.mmd file to the code in question. So if there's a clash between the global agents.md and the folder scope like this one we've got in the back end, the backend one will win through for any code in this folder.

**[28:42]** Okay, that's it for agents.md. Let's move on. If any given task is complex, ambiguous, or hard to describe to the agent, well, we have the option of using plan mode, which tells the agent to do some thinking and potentially ask clarifying questions before providing a plan. Now, in plan mode, the agent will not change or add to the code. It means you can

**[29:09]** throw around ideas without breaking anything. Now, I want to give you an important caveat straight up. Most people don't need plan mode very often. When a task is easy to describe and precisely scoped, plan mode is just not necessary and it will needlessly cost you time and money. But you will come across situations where things are more ambiguous than that and that's where

**[29:29]** plan mode comes into its own. So let's take a look at how it works. I've got a blog here and it's got about 20 science-based articles in it. The implementation is pretty straightforward. Each article is on a card and you click read article to read the entire article. And because this is just a test site, the articles are pretty small. The app is built using

**[29:49]** TypeScript and React. And the data for the articles is just stored inside this data folder in this articles.ts file. This is the array which has actually got all of the articles that we're displaying on the blog. All right, I'm pretty happy with how this app is working. I want to add a recently viewed articles feature. so that when a user clicks on an article and reads it, when

**[30:12]** they come back to the homepage, they can quickly see the articles that they read most recently. Now, this is a good use case for plan mode because it is a big change. There are plenty of moving parts and there are multiple ways you could implement it. I actually don't specifically know how I would tackle this if I were developing alone. So, if I were to just go ahead, open up the

**[30:31]** agent and ask it to implement that feature, it might actually take me down the wrong road and before I know it, I'm building my app on shaky foundations. And in the future, I'll need to make huge changes right across the codebase before I get back on track. So, instead of doing that, let's enter plan mode. And we can do that in one of two ways. We can use a slash command, plan, and

**[30:52]** select it. That will do the trick. Or we've got a UI option. If we click this plus sign, we can just toggle plan mode on and we can see that reflected down here. Okay, let's go ahead and prompt the agent. I'm just saying add a recently viewed articles section. We'll send that off and let's keep an eye on the file system over here. In fact, I might just close down the mini browser

**[31:16]** quickly. Right, did you notice that this agent folder just appeared? And inside here, we've got plans and current plan MD. Over in the agent, we've got the plan as well. It's just a little bit easier to read in this file. And then down here, it says ready to implement the plan. Yes or no keep planning. Well, let's check out what we've got. Firstly, it's recapping what it's going to do.

**[31:37]** And this is where it gets interesting. It says persisted in local storage. And that is actually really useful. So, the agent is telling us a decision it's going to take for us. We want these recently viewed articles to persist beyond refreshes of the browser. So, we need somewhere to store data. We don't want to set up a whole database for this local storage. So just a tiny bit of

**[31:58]** data stored on the user's PC is going to be perfect for this task. If we move on down, we can see more decisions that it's taken for us. It says showing the last five viewed articles. We didn't specify five. We might be happy with five or we might want a different number. But again, that's a question that we didn't think about at the outset. So it's good that all of this

**[32:19]** stuff is coming out now before we actually write any code. Moving on down, it's telling us the files that it needs to create or change. So, we've got some new files and then three edits to existing files. This information is more useful the more you understand about code and the more you understand about how apps are structured. Overall, we do want to keep changes as lightweight as

**[32:40]** possible. It's always best not to overengineer and make things unnecessarily complicated. Okay, so that all looks pretty useful, but is there anything that we've missed? Any edge cases? Let's just scroll up to the top. It says this is going on the homepage, but it hasn't specified where on the homepage. Is it going right at the top? Is it going between the articles and the

**[33:01]** header? Is it going right at the bottom of the page? That's something we might want it to include in its plan. But likewise, we might just be happy for the agent to take that decision for us. It is just a style decision at the end of the day and will be easy to change later. Perhaps a more interesting question is what would happen if a user reads an article and that article is

**[33:22]** then deleted? Will the deleted article still appear in the recently viewed articles section? Edge cases like that are not getting covered. And that brings us to a challenge. I want you to select no. Keep planning. And then I want you to ask the agent to deal with that situation where an article is deleted. It's going to add to its plan. Check what it's done. If you're happy, you can

**[33:43]** tell it to implement the plan and then give it a test. And in order to test that edge case, all you need to do is come to this file and you can just delete one of the articles that you've already looked at which is appearing in your recently viewed articles section. Then refresh the mini browser and see if that has been handled. Okay, over to you. Go ahead, click no, keep planning,

**[34:04]** and get the agent to deal with that edge case. Okay, hopefully you got that working and you covered that edge case. Let's have a go. So, I'm going to say no, keep planning, and I'll say deal with the edge case where an article is deleted after it has been viewed. Let's send that off. And if we go back to the current plan, and it's now rewriting the plan. A lot of this is likely to be very

**[34:29]** similar to what we had before. Again, we've got the last five articles, and we've got the files that are going to be changed and edited. And then up here it has actually dealt specifically with the edge case. And this is the key sentence right here that this is going to be handled gracefully. It's going to silently skip ids that don't match any article in the current articles array.

**[34:51]** I.e. if there's an article listed in local storage which doesn't exist in the array, then that article will be ignored. Okay. So now this plan is looking pretty good. Let's just click yes, implement it, and we'll let the agent get to work. And it is going to work now pretty quickly because it's already done. And it is now going to work pretty quickly because it's already

**[35:11]** done a lot of the planning. Okay, it says it's done. Let's open up the mini browser. And I'm going to click on this environment article. Let's head back to the homepage. And I've got a recently viewed section. And there's the article I just clicked on. Let's take one more. We'll take this space one. Back to homepage. And now recently viewed, I have got those two articles.

**[35:32]** Now, of course, there's plenty we might want to do here. We might want to restyle this so it takes up much less space. I think that would be a good thing to do. But the priority right now is just to check the edge case. So, let's remember this article, bringing Mars back to Earth. If we close down the mini browser and go to the articles, here we are. We've got bringing Mars

**[35:51]** back to Earth. Let's delete it. We'll save, open up the mini browser, and it's disappeared from the recently viewed articles. So, that edge case is working. And it might just be interesting to see what would happen if we now put that back again. Let's save. Open up the mini browser. And there we are. It's added it back in for us. Okay, so that was plan mode, which is useful for when you have

**[36:14]** an idea of what you want but don't know how it should be implemented. You're struggling to describe what you want clearly. There are multiple ways of implementing an idea, and there are lots of questions to ask, decisions to make, and things you haven't considered. So really, plan mode helps you clear up ambiguity and it provides a space for both you and the agent to think before

**[36:34]** acting. Check out this e-commerce site which the agent just built me. It's called Stylist and it's got a range of practical products for everyday life. Things like bags, drink wear, light bulbs. Doesn't get much more practical than that. Let's just check out some of the features. So, I can log in and then I can add some products to my basket. I think three

**[37:00]** will do. Let's go to the basket. And if I scroll down, I can check out via a mock payment gateway and get to this order history page. Okay, so this app is the real deal. It's database driven. It's got a pretty complex codebase over here with a separate front end and back end. The front end is running on port 3000, the back end on port 4,000. So overall there's a lot going on and we

**[37:23]** are going to use this app to explore a core agentic coding feature skills. What is a skill? Well fundamentally a skill is a reusable wrapper around a prompt and it gives us a consistent and reproducible workflow. Now to show you what I mean I've got a really basic skill already set up. If we check out this agent folder inside that we've got a folder called skills and inside that

**[37:46]** we've got a folder called file tree. And what this skill does is it creates a file tree of the codebase. Let's just quickly check out the files that we've got in it. So we've got generate tree.js. That's just the script that the skill runs to create the file tree when it's invoked. And skill.md has got the overall instructions for the skill. This is essentially the prompt. And this is a

**[38:09]** description of what the skill does. Generate a file tree of the codebase and save it to tree.md. So when we invoke this skill, we are going to get a new file called tree.md with our file tree. Now invoking a skill is pretty easy. Let's just open up the agent. And if I hit slash, that brings up a list of commands. And down at the bottom, I've got skills. And we can see the file tree

**[38:30]** skill right here. There's another way of accessing it. You can also use the dollar sign that brings up just the skills and not the rest of the slash commands. Okay, let's just select file tree and hit send. So, it wants our permission to run the JavaScript from the skill. Let's click yes. And we see tree.md has appeared. Let's open it. And already we can see the tree being

**[38:53]** generated. And it looks like it's done. It says the project contains 29 directories and 66 files. And here's a tree of all of them. So, that could actually be pretty useful if you needed to quickly understand the layout of your app. But to be honest, this skill is pretty basic. It's nothing more than a mini timesaver so I don't have to write the same prompt every time I want the

**[39:16]** agent to create me a file tree. Basically all this skill is is an instruction. And instructions are an important part of skills. Every skill needs one. But the real power of skills come when you give the skill not just instructions but also knowledge and opinion. Because what [clears throat] you're doing then is giving the skill something that an AI model cannot know.

**[39:37]** An agent is great at general tasks, but the agent is completely clueless about the specific decisions your team has taken. There are lots of things it can't intuitit. It doesn't know your team's idea of best practice. It doesn't know your house coding and commenting style. It doesn't know the guard rails you work within. It doesn't know your policy on legacy code and when to update it. And

**[39:59]** there are many more things besides. Now, [snorts] you could chuck all of that information in a prompt, but as we've discussed before, we can't assume that information given to the agent in a prompt will always be available to it. And that's why skills are so useful. They live in the file system. They can be passed around between projects, shared online, given to colleagues.

**[40:18]** They're completely portable, and they give you a solid, reproducible workflow. So, now we've got the basics of what skills are and how they're invoked. In the next scrim, let's go through the process of creating a really useful opinionated skill and then after that I'll be setting you a challenge to create your own. Here's a problem. The code in this

**[40:43]** codebase is of a pretty high quality and it's been written to house style. Now, there's one exception and that is this file right here, service.ts in the payments fake folder. This file is purely weird. We've got all sorts going on with for loops. We've got while loops. And honestly, I have absolutely no idea what this is at all. In fact, almost all of the code in this file is

**[41:08]** completely impossible to understand. Code like this is a nightmare to maintain and a nightmare to extend. So, what we're going to do in this scrim is get it into house style and we're going to create a skill to do that for us. We can create a skill in the agent using the built-in skills creator. And if we hit slash, we bring up the list of slash commands. And then at the bottom, we've

**[41:30]** got skills creator. We need to pass in an instruction setting out what we want the skill to do. Now, each skill is different. So, I can't give you one template to prompt for good skills, but as a rule of thumb, we need to cover four points. And if I open up prompt.md, I've got those four points already set out. Let's start with task and purpose. I'm going to say create a skill which

**[41:54]** refactors code in a given file to use house style. Now this second category which I've called inspect or capture is really important. This is where we're going to give it something which it can't possibly know. And I've said to learnhouse style look at admin orth basket catalog orders in server/src/ modules. So if we just have a quick look at the file tree right here, we've got

**[42:17]** server src and then we've got all of these modules apart from payments fake and I'm saying look at those. That is what we consider to be good code. That is our house style. Now for constraints, I'm just going to say do not change code in any other file other than the one specified. And in fact, I'm just going to change that to a plural because for how to invoke, I've said the skill is

**[42:41]** invoked with /house style and a path to one or more files. Okay, that is the prompt. Let's just copy all of that. And to be honest, we don't really need these headings, but they're not going to do any harm. So, I'm just going to invoke skills creator and pass in that prompt. Let's send that off. And we're going to open up this agent file. And this is where we should see our new skill being

**[43:03]** created. And we can see that the agent is going to inspect the module files to capture the house style patterns. That's what we've asked it to do. That's really good. And here comes the skill. And we can see that it's analyzed all five modules. So all of that knowledge is now being encoded into the skill. Okay, it looks like it's done. We have got just the one file in the house style skill.

**[43:24]** It's skill.md. It's the instruction. It's got a whole ton of information in it. We just want to put it to the test. And remember, we do that by invoking the skill and passing it a file path. And a quick tip to get a file path really quickly, you can just rightclick on one of these tabs and from the drop-own menu, select path to file. Go ahead and get this service.ts file refactored into

**[43:48]** house style. Okay, hopefully you saw that skill in action. Let's give it a go. So, I'm going to rightclick here and I'm going to copy the path to the file. And then I'll use slash. Scroll right to the bottom. We've got the house style skill. Let's select that. Paste in the path to the file and send it off. Okay, the agent is getting to work and there is a

**[44:09]** lot of activity in this file. And it looks like it's done and it's given a whole load of detail about what it's done here. And you are welcome to open up these other files and do a comparison if you want to. I already know that code and I'm happy that this code is written in the same style. Now, to be sure, we should give the app a quick test. And of course, if this were real world, we'd

**[44:30]** give it a very thorough test indeed. But we can see here that it is looking good. We can log in. Everything is working just fine. So what we've done here is we've created actually a really useful skill. And by giving it the knowledge of our house style and telling it what we consider to be good code, we've made a skill that can really efficiently refactor old, strange, and convoluted

**[44:54]** code. Okay, good job. In the next scrim, you're going to build your very own skill. I've run into a problem. I was doing some general maintenance on the site and I've broken it. Nothing is displaying in the mini browser. And if we look in the runner, we can see we've got some errors going on, but nothing which gives me an instant clue as to how to fix it. Now,

**[45:18]** I've got a feeling that somewhere in this codebase, there are docs with specs and constraints and useful project information that could help the agent find the problem and also help the agent avoid bad fixes in the future. So, I want you to use that information as the knowledge in a bespoke dev skill for our codebase. And that is a skill that you are going to create. Now, the aim of

**[45:40]** this skill is to guide the agent on what to inspect whenever it's debugging the app or making complex changes. This will help the agent work safely on the codebase. Now, I've made a short list of the kinds of things the skill should know. It should know about project specific guard rails, known platform constraints, pin dependency versions, debugging strategies, and anything the

**[46:00]** agent should avoid changing. Now, I also want to be clear on what this skill is not because this skill is definitely not a generic debugging checklist. The agent can do generic debugging just fine already. We don't need a special skill for that. Remember, a good skill has got knowledge and opinion that the model cannot know. And in this case, that is the specific rules, constraints, and

**[46:23]** quirks of this repo. And the skills creator can find that in the various comments and readme files that we've already got in the codebase. Secondly, this skill is not specific to the current problem we're facing. It should be a versatile skill which can be called upon anytime work is being done on the app. Okay. In prompt.md, I have left you with the same template we used before.

**[46:45]** You definitely do not have to stick to it rigidly. Feel free to go your own way. Use skills creator to create the skill. Remember, when you hit slash, it will be right down there at the bottom. And when you've created the skill, you should see it on this list. Once you get to that point, go ahead and see if you can fix this site and get the app working again. Okay, I'm going to leave

**[47:05]** you with this slide. Go ahead and get to work. Okay. Hopefully you got a really useful skill which fixed the site and a big pat on the back if you did because there was quite a lot of work to do there. I am going to show you my approach in the next scrim. Okay, let me show you how I created this dev skill. So coming to the prompt,

**[47:29]** we've got the task and purpose. I've said create a repos specific dev skill for this project. Its purpose is to help the agent work safely in this codebase when fixing bugs, reviewing changes or doing maintenance. Now for inspect and capture, this is the important part. I have said as you create it, inspect the repo for project specific guardrails, known platform constraints, pin

**[47:50]** dependencies, and anything the agent should avoid changing. So the skills creator is going to have a look through everything in the codebase and find that information that will give the skill its knowledge. I've also added some constraints. This should not be a generic debugging checklist. It should capture the specific rules and quirks of this repo so a dev can invoke it later

**[48:10]** when something breaks. So that's just really clarifying what this skill is for. And then finally to invoke it. This skill should be invoked with /stylist-dev and an explanation of a bug or problem. Okay, let's save that. I'm going to copy it. Open up the agent. We'll bring up the skills creator and I'm just going to paste this in and send it off. And let's

**[48:33]** just open up the agent folder and the skills folder and we should see it created right here. Okay, here comes the skill. And it looks like it's done. So let's see what we've got here. It's telling us it's captured a bunch of repo specific rules and quirks. And then in the skill itself, if we just check that out, we've got the instructions here. We've got a section on platform

**[48:54]** dependencies, architecture, legacy code, and things not to touch. and then a big list of known quirks, a warning about changing specific areas, and a section on debugging for quick reference. So, that all seems pretty comprehensive. I think we should put it to the test. So, let's go ahead and invoke the skill. So, if we do the dollar sign in this case, let's go for stylus dev. And we need to

**[49:20]** give it an explanation of a problem. We could paste in for example error messages but I think in this case I'm just going to say the browser is not displaying anything. Let's send it off. And it says that this SQLite 3 package which is a package we're using for the database is failing. And it's giving us a reason for that. The version at the moment is 6.0.1

**[49:42]** but the project requires exactly 5.1.7. So, it looks like that package has been upgraded and it's now not compatible with the rest of the codebase. So, it's suggesting we install the package at the correct version. Let's say yes. And it says it's fixed it. So, let's open up the mini browser. And we might just click run to restart it. And there we are. We have got the site back up and

**[50:05]** running. So, this is a super useful skill. It knows the specifics of this repo and how to run the app on this platform with all of the quirks and oddities. So that makes it a super efficient tool when debugging. And if this were a live codebase, we would be using this skill again and again. And look, it fixed that problem in 1 minute and 4 seconds. So that is really super

**[50:26]** fast. Okay, that's it for skills. Now is a really good time to take a break and then move on when you're feeling fresh. Testing is a huge part of development and that doesn't change with agentic coding. In fact, agents allow us to write and run tests faster than ever before. That brings plenty of potential benefits, but also some pitfalls. In the next few scrims, we are going to get

**[50:53]** hands-on with some testing. The testing framework which we're going to use is Vest, and that works really well with our JavaScript setup. And if you're new to testing, don't worry. You don't need to understand the test syntax. All you really need to know is that a test runs a piece of code with known inputs and checks that what comes back matches what you expected. The test will either pass

**[51:15]** or fail. Okay. So, what problem are we going to solve with testing? Well, what I've got here is a widget from Mr. Smiles Dentist which allows people to book available appointments. They can select a day, choose their service, such as a 15-minute quick checkup, and then click show available dates, and see the available appointments for that day. Now, this widget looks simple enough,

**[51:37]** but actually it has loads of behavioral quirks. The dentist is closed on Sunday. Standard weekday hours are Monday to Thursday, 9 to 5. There's an early finish on Friday. Saturday is morning only. Lunch break is not applied on Saturday. Slots are generated at 15-minute intervals from business open. Slots whose start time is before current time are excluded. And any slot that

**[52:00]** overlaps lunch, not just fully inside, is also excluded. Now, you're welcome to go ahead and play about with this widget and see all of that in action. But honestly, I expect what you're thinking right now is, Tom, why? Why all of this? Why not just show me something simple? And that is a very good question, but I have a very good answer. This is mimicking the real world. Over time,

**[52:23]** staff at this dental practice have gone to the developer and said, "Please add Saturday morning opening. Please add Friday early closing, etc., etc." And if we just open up this file we've got right here, scheduleuler.js. We can see that there is a lot going on. And in fact, most of the business logic here is happening inside this function, get available slots, which has a lot of

**[52:46]** data coming into it. So what's happened is that over time this code has got kind of messy and hard to read and that makes it awkward to extend or refactor. So the problem in a nutshell is this. We have got an app with behavior which we want to keep but tangled code which makes it easy to break something. Now when we combine agentic coding with testing, we actually get a really neat solution to

**[53:10]** this and it's called a characterization test. At a high level, what you need to understand about a characterization test is that we use it to protect the character or behavior of a feature so that that behavior doesn't get changed during refactor or when adding new features. And these are all of the characteristics that we want to protect. Now, this would be a nightmare to do

**[53:31]** manually, but Agentic coding actually makes it really easy. And the workflow for a characterization test is like this. First, you select a working feature that you want to protect. and working is underlined here because we do not want to protect this feature unless we're absolutely sure it works as we want it to. If it's buggy, then we definitely do not want to protect the

**[53:51]** bugs. Now, I've checked this feature. I know it works. Secondly, we have the agent create a passing test which captures the features current behavior. And I say passing test because this feature already works. So, the tests the agent creates will pass. What we're doing here is locking in the features behavior because when the test enshrines how a given input leads to a predictable

**[54:14]** output, we can run that test and we can see if we've accidentally changed anything that we didn't want to. Now, in order for this to be effective, we need to ensure the agent runs the test after every task which affects that code. And that's important because from now on, whenever we go anywhere near the code that we've got in this scheduleuler.js js file. Once we're done, we want to

**[54:35]** check the protected features are still intact. So once we've got that test automatically set up to run after every time that code has been affected, we can go ahead and develop a new feature as part of the same widget or refactor the code. And then the characterization test will run and that's going to have one of two results. Either the tests will pass in which case the refactor or addition

**[54:57]** hasn't changed the character we wanted to protect and we are done. We have been successful. The test may of course fail and that means we've changed the character we wanted to protect and the agent must iterate until the task is completed successfully with the characterization test passing or revert to the old code. Okay, that's the theory. Let's put it into practice in

**[55:17]** the next scrim. Okay, we have this widget from Mr. Smiles with all of its various behaviors. What we're going to do now is protect these behaviors with a characterization test. I've got my prompt ready right here in prompt.md. Let's take a look at it. So, I've put write a characterization test for get available slots in scheduleuler.js using

**[55:42]** vest. Now, get available slots. If we come down to scheduleuler.js and have a look on line 16, we will see we've got that function right here. And it's in this big function that the business logic for this widget really comes together. Next, I've got this strange line which I want to explain to you. I've said used a fixed future week for all test dates so

**[56:05]** that time already passed today logic never fires. Now, I did this because when I was trying this out, the agent would normally use today's date and then find a bunch of times didn't work because they were already in the past. So what I've done is told it to use a future week. And I've given an example of a week which is 2 years from today as it happens. And that will allow the

**[56:25]** agent to write the tests more smoothly. And then underneath that I've got what the code actually does. And again when creating a characterization test it's a really good idea to spell that out. Okay. Let's take all of this and send it off to the agent. And by the way we're asking the agent to do something fairly complicated here. So it is likely to ask us for permissions which it's doing

**[56:46]** right now. It wants to install the vest testing package which is of course fine. Also, it may make mistakes or have a few problems. So, let's see what happens. Okay, now we can see that the test writing is in progress. And now it wants to run the tests. So, we'll say yes to that. And as predicted, the tests have failed. So, it has run into a couple of problems. Let's see if it can sort those

**[57:09]** problems out itself. Okay. And it's telling us that it found six failures, all due to incorrect assumptions in the test expectations, plus a time zone bug. And what it's going to do now then is rewrite those test expectations. It's definitely not going to change our code because we have specifically told it that that's behavior we want to protect. Let's run

**[57:31]** those tests again. And all of the tests now pass. Now, we could actually go through these tests and analyze exactly what they're testing for. But because they simply capture what the code already does, we don't actually need to scrutinize each expected value. So, the use of this test comes in later when it's going to flag if anything has changed. Okay, let's

**[57:52]** just go back to this flowchart that we looked at in the previous scrim. So, we've selected a feature that we want to protect and now we've created these passing tests which capture the features current behavior. What's up next? We need to ensure the agent runs the test after every task which affects the code. And that brings me to a challenge for you. And I've got it in a file right

**[58:13]** here. I want you to make sure this test is run anytime scheduleuler.js is changed. This is really important. Remember, the whole point of this exercise is to protect a feature we know works from accidental change down the line. So think about how best to do this. And I've given you a hint in hint.md. You can check that out if you need to. Okay, go ahead. put your

**[58:34]** thinking cap on and get to work. Okay, hopefully you realized that the answer lies in an agent.mmd file. We don't have one yet. So, let's use the slash command in it to generate one. Now, in my hint, I did say you can edit this file manually if necessary. Well, that might be necessary. Let's check out what we get. Here's the agent MD file. We've got the testing convention down

**[58:59]** here and it does say run npm test after any change to scheduleuler.js. It's got that right there. So, we don't need to make any manual edits ourselves. Okay. Second challenge for you. I want you to ask the agent to refactor the code we've got in scheduleuler.js for better readability. What it should do is refactor the code and then run the tests to make sure that the existing

**[59:21]** characteristics, the existing behaviors have been protected. So go ahead and ask it to refactor this code. Okay, hopefully you saw a characterization test in action. Let's see what happens. I've just said refactor the code in scheduleul.js for better readability. We shouldn't need to say more. Let's send it off. And after thinking about it, it said it's going to

**[59:44]** refactor that code all while preserving exact behavior. And now it's saying it wants to run the tests. So of course, we're going to say yes to that. And it says all 35 tests have passed. So that has worked. We've refactored that code in scheduleuler.js, but we've protected all of the existing behaviors and the test has automatically run to make sure that that has happened. Now, I just want

**[1:00:09]** to be clear about testing workflows because we've set this up so the agent runs the characterization tests specifically when code in this scheduleuler.js file is changed. We didn't ask the agent to run the test after every task it carries out because that would just add unnecessary time and costs to the process at this development stage. After all, a small style change

**[1:00:30]** in the footer is not going to affect the behavior of this code. So, it would be wasteful to run the characterization test. But later, before you merge this code into your live app and deploy it, at that point you should run a broad range of tests as a final check that everything is in order. So the workflow is like this. Narrow and specific tests while developing whenever you do

**[1:00:52]** anything that could affect the protected behavior and then run broad tests before merging the code or deploying. We're not done with testing. We've got another technique to look at. Let's pick that up in the next scrim. In this scrim, we're going to talk about adding new features and tests for those new features. But first, let me draw your attention to a few changes I had

**[1:01:16]** the agent make to the code we were working on in the previous scrim. Firstly, to keep things tidy, I moved the tests into this tests folder. And in agents.md, I added this line right here. I just wanted to make the instruction to run tests after making any changes to scheduleuler.js more prominent. And in the file itself, I also added a comment right here to the

**[1:01:39]** same ends. And I did this because in testing I didn't find the agent that reliable in always running the test. Now this is probably a quirk of the model we're using here in the scriber agent. It probably wouldn't happen with claude code or codeex. Now the big change I made though was this. I have added an extra feature. Now when you select an appointment and you click book now

**[1:02:02]** you're taken to this checkout page because Mr. Smiles is not done making money from clients. So, when you book your appointment, you're offered some extras that you can add on. So, we've got a total down here. So, we've got a running total here. Let's add all of the options, the total updates. When I click confirm and pay, we just get confirmation of our booked appointment

**[1:02:24]** with the date, time, and final price. So, that feature works, but to boost sales, I want to add a discount box. You know the kind of thing. You enter a code, in this case, smile 15. You click apply discount and you get a 15% discount off your total. And of course, while adding that feature, I want to add a test to make sure that feature is working. So let's prompt for that. And I

**[1:02:47]** have got a prompt right here. Add a discount code option. When the user inputs smile 15, apply a 15% discount. And then create tests using V test to verify that it works. Looks good enough. Let's open up the agent. Paste that in and send it off. Okay, it looks like it's finished. Let's just check that it's run all of the tests.

**[1:03:10]** Let's go ahead and run the test command. So, it's telling us that all 43 tests passed, including eight new calculate discount tests. So, that means the feature should work. Let's open up the mini browser and give it a go. I'll select my appointment. And we've got a discount code box. Let's select all of the options. I'm going to type in smile 15. Click apply. And we have got the

**[1:03:33]** discount applied. And that brings the total down to 23542. So everything's fine, isn't it? Well, not exactly. I've got a bit of a problem. Our pre-iscount total was 276.97. With the discount applied, that is 235.4245. Now, obviously, we don't charge to four decimal places. So, what does the

**[1:03:55]** customer actually pay? Do they pay 23543 or 23542? Well, according to the app, they pay 23542. Now, the question is, should the discounts be applied per line item? So, the discounts are counted individually, tallied up at the end, and then rounded, or is the discount applied to the basket total with just one rounding at the end.

**[1:04:17]** These choices can produce different final prices, sometimes off by a penny. And a penny that doesn't reconcile is a real bug in a real store. If Mr. Smiles was scaled to Amazon proportions, we would be juggling with millions of dollars. and we've given that decision over to an agent. And what's more, the agent has enshrined that decision in a test. So, this figure looks plausible

**[1:04:38]** and the tests add respectability. But actually, this is an agent looking in the mirror. It didn't encode a wrong answer. It encoded an answer to a question that we never asked. You might think that I'm splitting hairs over single pennies here, but these are decisions that we, the human, should be taking. We do not want to hand this over to the agent and let it dictate policy.

**[1:04:59]** So the take-home here is don't ask the agent to write code and create tests for it in the same pass. In the worst case scenarios, the agent will be marking its own homework just writing tests which pass the code it's just created. And in the best case scenarios, you still run the risk of having the agent make policy decisions for you as we've just seen. So this is a real problem. And in the next

**[1:05:20]** grim, let's look at a more sensible way to do this. I've reverted the code that we added in the last scrim, which gave us the discount box. So now we're back to exactly where we were. When I click on book now, I can see the extras to add and the total, but no discount box. And what you're going to do in this scrim as a challenge is add that feature back in,

**[1:05:46]** but we're going to do it in a much more sensible, logical, and safe way. And we're going to do it using something called a spec test. And with a spec test, we decide on a feature we want to add. So in this case, a discount box where the code smile 15 gets you a 15% discount. We then create a spec test which describes the behavior that we want to see. And in this case, I want

**[1:06:09]** you to have the agent calculate the discount based on the total. So not adding discounts line by line, but taking the total and applying the 15% discount. On top of that, I want the discount to be rounded up to two decimal places. Okay, so those are the behaviors we want to see. We then check the test to make sure it's testing what we want to do. Now, you can do that by looking

**[1:06:32]** at the test file or you can just interrogate the agent, which is a bit easier. Just ask the agent to explain exactly what the test is testing for. Once we're happy with the test, we can tell the agent to write the code to add the feature and then run the test to check it's working. If all of the tests pass, then we're done. We've added the feature. And because the tests pass, we

**[1:06:54]** know that it meets the criteria that we set out right here in the specifications. Now, if the test fails, the agent can iterate until they pass. So, the basic idea here is that we create a failing test. That test fails because we haven't got the code yet for that feature. And then passing that test becomes an aim for the agent. So when the agent writes the code that makes

**[1:07:17]** that test pass, we can be confident that that feature is complete and will work in the way we intended. And being able to view the test before letting the agent develop the feature means that we can get a grip on any decisions being taken and make sure they are our decisions. Remember, the agent thrives on ambiguity. If you leave ambiguity, the agent will fill the space and take

**[1:07:40]** decisions for you. That is what we're trying to stop here. So, just a reminder, a 15% discount applied to the total rounded up to two decimal places. The agent is open. You've got quite a lot to do. Go ahead and get to work. Okay, I really hope you got that working and you saw how powerful this kind of test can be. Let me just paste my prompt in right here. I've said create a

**[1:08:04]** failing test for a feature which doesn't exist yet. A discount code option. When the user inputs smile 15, apply a 15% discount. The discount should be applied to the final total and round it up to two decimal places. Let's take that pass it to the agent. Now already if we open up the test folder, we can see a new file has been created and it's asking us if we want to run the test command.

**[1:08:28]** Let's say yes. And it's saying here that the test is failing as expected. And basically the code doesn't exist yet. And this is what it's calling the classic TDD red phase. Now TDD stands for testdriven development. And that is exactly what we're doing now. We're creating a test and we're developing towards making that test pass. Now, at this point, we could take a deep dive in

**[1:08:50]** here, understand the test syntax, and see exactly what's going on. But it's actually given us a summary right here. Smile 15 applies a 15% discount to various amounts. Rounding up to two decimal places, eg 87.125 would become 87.13. That looks good. Unknown invalid code returns the original total unchanged. Case sensitivity smell 15 lowerase does

**[1:09:15]** not match. That's absolutely fine. Edge cases zero, negative, and fractional scent inputs. That's a good thing to look out for. And some of these things obviously we didn't think of in advance. The agents done it for us. That's absolutely healthy and fine. So that looks like a really valid test. Let's go ahead and add the new feature. I'll just say write code to make the tests pass.

**[1:09:36]** and we'll let it run the tests. Of course, if we just scroll up, we can see that all 51 tests pass. That is good news. Let's open up the mini browser and put it to the test. So, I'll select my appointment slot. I'll click book now. And if we just apply everything, we get the 276.97. Let's add smile 15. Apply it. And we get the discount this time. The penny is

**[1:10:00]** rounded up. Okay. So that was a much better process specifically because we wrote a test which described exactly what we wanted the code to do and then had the agent develop to that goal. Now, at the outset of this course, I acknowledge that when it comes to prompting, just asking for what you want gets you a long way. And it's true, sloppy, quick, lazy prompts do get you a

**[1:10:23]** long way. But when it comes to testing, more than ever, it's only really careful prompting as part of a diligent, wellthoughtout workflow that will get you quality tests you can rely on. And there needs to be some independence between writing the test and writing the code that's going to be tested. If not, in good faith, the agent will simply write a test to pass the code that is

**[1:10:45]** written. And this is a known issue. Agents will turn out a ton of junk tests which don't hold any water at all. And running those tests is largely a waste of time. But as long as you're aware of that problem and you know a bit about testdriven development, where you create a specification and have the agent write code towards that goal, testing can take you a very long way and make your code

**[1:11:08]** much more reliable. As an agentic coder, you should be using version control. Version control allows you to make changes and experiment without losing a working state of your app. As you refactor code and add features to your app, sooner or later, you will get some weird behavior or something will break and you will wish you were able to revert to a previous

**[1:11:33]** good version. We are not going to take a deep dive into version control in this course, but I am going to give you some pointers on how best to use it when agentic coding. Now, Git is the most widely used version control system and GitHub is the most popular platform for hosting Git repositories. If you're new to them, I recommend you take this Scrimber course, which will get you up

**[1:11:53]** and running. And if you're not comfortable working in the terminal, the course includes a section on the GitHub desktop client, which is a smoother entry into the world of version control. Okay, let's start by talking about git hygiene. As we've seen in this course, agents love to write code. You can give them very wide open-ended tasks with few guardrails, and they will happily churn

**[1:12:14]** out 500 or a thousand lines of code. Now, before that code goes live in a real world app, somebody needs to review it. And that someone should be a human who understands it. It might be you or a colleague or a collaborator. Now in git each change which you store in your code repository is called a commit and each commit comes with a commit message. So the commit is the change to the

**[1:12:37]** codebase. The message describes the changes. Now put yourself in the shoes of a code reviewer. You might get a commit which is 800 lines of code. And the commit message might be all sorts of things. Update the hover state on the navbar. Align the footer center. Resize the hero image on mobile layouts. Implement a same day delivery option. The list could go on and on all in one

**[1:12:58]** commit. This is a real no no because trying to wrap your head around tons of new code is extremely difficult and extremely timeconuming. So the key rule is this. Keep your commits small and well described. So how about you commit four lines of code to update the hover state on the navbar. Maybe one line of code is enough to align the footer center and then six lines of code to

**[1:13:21]** resize the hero image on mobile layouts. Now, commits of course can't always be that small. They are going to be bigger. But the take-home is rein in the agent and give it small, precise, coherent tasks and treat each task as a commit. The reviewer would much rather review a bunch of focused small commits than one tangled web of code. Okay, we've got a couple more things to talk about in

**[1:13:44]** terms of version control. So, in the next scrimm, let's talk about config files. Let's talk about version control and config files. In this codebase, we have got an agents.mmd file and there might well be other config files like readmes etc. in the codebase as well. Now this information belongs to the codebase and not to you. If you've specified specific

**[1:14:11]** package versions or policy on handling legacy code, your colleagues and indeed you in the future need to know about it. So we must always make sure to push the config files to the repository whenever they are updated. Now there might be complexities in doing this. If different people involved in the project are using different agents, you might end up with for example a claw.md file as well. So

**[1:14:34]** if a colleague is using claude code, they might push their claw.md file to the repo and then the next time you work on the project, you've potentially got two competing files. So a claude.mmd file is actually very similar to an agents.mmd file but it's specific to the claude code ecosystem. So that's the claude code tool, the IDE extensions and the desktop app. Now if that happens you

**[1:14:57]** do end up in a bit of a tangle because the agents.mmd file is a recognized standard across multiple platforms whereas the claude.md file is specific only to claude. Now in a team situation, this conflict will need to be handled by whoever owns the codebase as obviously there will be differences across those competing config files as the project evolves. Now just because codeex does

**[1:15:19]** not respect a claw.md file by default. There's nothing wrong with asking codeex or indeed any other agent you're working with to manually compare multiple config files and check for clashes. If there are any, at least you know and then you can get clarity from your team. So for the sake of continuity, make sure conflicts are handled by whoever owns the codebase. Now the real takehome from

**[1:15:40]** this is just to make sure that the config files do get pushed to your repo and that you only exclude files which are personal to you, contain your personal opinions and are of no value to your colleagues. Now there are of course other things which should be excluded from your repo and in the next scrim we're going to talk about secrets. Apps often have secrets and we need to

**[1:16:05]** protect them. Secrets can include things like API keys, passwords, database URLs, and any other security critical credentials that you need to keep well secret. A common way of storing the secrets our app needs when we're developing is to use the M system. With M, you keep the secrets and other environment specific configuration data in a special M file just like this one

**[1:16:31]** and refer to them in the code where needed. So if we have a quick look in server.js, I'm getting the port right here from the M file. So it says port all in uppercase. It's set to 8,000. And in server.js, we're accessing that with process.m.port. So it's process.mm which gets us access to the data from the m file. And I should just quickly point out that we

**[1:16:55]** don't normally use the m system in scribble because we actually have our own system. But this is a working m file and you're welcome to check out this codebase by the way which is one we haven't looked at before. You don't need to know anything about it at all. We're barely looking at the code. I just wanted to use it to give you some real world examples of how we can protect

**[1:17:12]** secrets. Okay, let's go back to this M file. And what this does is it allows us to keep secrets all in one place. And this is useful because one of the most popular way to expose secrets is to push them to a GitHub repo. And because even private GitHub repos cannot be considered secure, any secret exposed like this is compromised and must be binned. So to avoid pushing this file

**[1:17:37]** with all of our secrets to GitHub, we have a git ignore file. And this lists all of the files and folders that we wouldn't want in our GitHub repo, perhaps because they contain secrets or just to avoid unnecessary bloat. So any file or folder listed here will be ignored from commits and won't be pushed to GitHub. Now this system serves us well in regular development, but when

**[1:17:59]** you code using an agent, keeping those secrets secret becomes a little bit harder. And here's the problem. This M file is in our codebase. So by default agents like codeex and claude code have access to it. That means the agent can read your secrets and use them elsewhere in your codebase. In a classic example, the agent reads the M file. The agent hardcodes a secret in a file. And

**[1:18:24]** remember, the agent is concerned with making the app work. And so agents do sometimes cut corners and take risks. Now, if we don't pick up on this, we merily push our code up to GitHub, not realizing we have an API key in one of our non-ignored files. Someone then steals that API key, says, "Thank you very much," and then destroys our site or uses up our AI credit. Now, there's

**[1:18:46]** another risk I want to show you. If we just go back to the code in server.js, right here on line 12, we've got something very common, a consult.log. Now, in this case, all we're logging is the port. That's pretty harmless information. But we should also be aware that depending on how your app is set up, log files can be saved and might end up getting pushed accidentally to GitHub

**[1:19:07]** or shared carelessly and be compromised. If I just check out this log file we've got right here, we can see that we've got port 8000 added to it along with a bunch of errors, warnings, and info. Pretty harmless stuff, but we definitely would not want to add an API key to that list. So, let's take a quick look at a list of dos and don'ts when agentic coding. And the first one is pretty

**[1:19:29]** obvious. Never type secrets into the chat. You never know where they might end up. So, rule number one, just don't deliberately share a secret with the agent. Number two, keep secrets out of logs. We've just talked about that. Number three, what I mean by that is where you have something like an API key which gets you access to a service, for example, the OpenAI API and you have got

**[1:19:51]** some AI credit which you've paid for, you will want to keep that token on a short expiry. Also, you want to keep it with a tight spending limit. So, basically all of the time you're trying to think about damage limitation. So, if your API key does get compromised and you don't notice it, at least it will expire relatively soon. and if somebody is using it, they will hit a spending

**[1:20:13]** limit relatively soon as well, so you won't lose too much money. Last, but most definitely not least, inspect the diffs yourself. Remember, every time the agent edits a file, it tells you what it's deleted and what it's added. Now, you can also have the agent commit and push code to GitHub for you, and that is beyond the scope of this course. But whatever happens, you should always

**[1:20:35]** inspect those diffs and make sure only files that you've checked are going to be pushed to GitHub. That's the best way to ensure that no keys are getting compromised. Okay, just before we finish, let's have a quick investigative challenge. I want you to look at the four files which are open here and I want you to see if you can identify a total of three potential security

**[1:20:56]** problems and I want you to eliminate them. Now, you could ask the agent to help you, but really this is designed for you to do manually. These are all things that we've discussed in this scrim. You do not need to understand the codebase at all, and you don't need to have a deep knowledge of coding in general. All you need to do is have a quick look through these four files,

**[1:21:16]** find three security problems, and eliminate them. Okay, go ahead and do that. Okay, so hopefully you eliminated these security flaws. Let's have a quick look. So, in this file, products controllers, we've got a few problems here. Let's start off down on line 33 here. We've got a console.log. And look what we're logging. We're logging a secret from the

**[1:21:39]** M file. We definitely don't want to be doing that. So, let's delete it. And if we scroll up near the top, we've got some commented code here, but commented code still counts. The agent can still read it. What are we doing here? Well, we are hard coding a secret. Perhaps the agent did that for us. Perhaps we did it ourselves. These things happen. The best solution here is not to have loads of

**[1:22:00]** commented code. Just get rid of it. So that is two security problems fixed. Let's find one more. If we go to get ignore right here, we are ignoring the M file. And we've got M right here. We're ignoring it. So all of these secrets are safe. But what have we got here? We have got M.local. It's another environment file. And if we look, it's a carbon copy pretty much of the M file. So all of

**[1:22:25]** these secrets could get pushed to GitHub. What we want to do here is add it to the ignore list. So we can just say M. Okay, that is all of these security problems. So congratulations if you found them all. And hopefully this scrim will teach you to keep an eye on what you're doing and just be vigilant about your secrets and make sure the agent can't compromise them for you.

**[1:22:46]** Okay, if you've been at this for a while, now would be a good time to take a break. When you come back, we're going to take a look at setting up the VS Code Codeex extension. At this point, we are going to use the codeex extension in VS Code to explore a few concepts we can't look at so easily in the Scriber environment. Firstly, let's get set up. You can click on this

**[1:23:10]** screenshot to go to the chat GPT signup page if you haven't already got an account. There's a range of prices, but you can actually make limited use of codecs on the free plan. And if you're just playing around, why not go with free and see what you get? And if you hit limits, you can always upgrade later. The limitation of the free plan is basically the amount of credits you

**[1:23:29]** get. So, you might end up at a point where you've used your credits and you have to wait for your allowance to reset, but also the newest features and best models might not be available to you on that free tier. So, see how you go and you've always got more options and you can upgrade at any time. Okay, once you've got your account, open up VS Code. And if you don't have VS Code, you

**[1:23:49]** can download it for free. Just search online for the correct version for your operating system. When you've got it open, click on this icon right here, and that opens the extensions. Search in here for codeex and make sure you select the official extension. Click on it and click install. Once it's done, open up a folder that you want to work on. And you can click the codeex icon that you'll

**[1:24:12]** see right here. That will open up the codeex window. And at this point, you'll go through a login process to attach the codeex instance to your OpenAI account. And then you're all set up and you can start aentic coding with Codeex. Codeex works against the folder or workspace currently open in VS Code. So whatever you see here, that is what Codeex will be working with. Let's just have a quick

**[1:24:34]** explore and orientate ourselves with some of the features of Codeex. Plenty of which we're already familiar with. Remember the Scriber agent is similar but not exactly the same as Codeex. Now, if I click right here, that brings up a couple of things. Firstly, reasoning. We've got light down to ultra. Now, you can adjust it depending on the complexity of the task. For a lot of

**[1:24:54]** tasks, light or medium is fine. And then you can always ratchet it up for the more complex problems or if you find results are disappointing. Just remember that higher effort levels take more tokens and are therefore more expensive. And we'll have a choice of models and they basically go in descending order of capability. So selecting something a bit lower down the list is good to save

**[1:25:15]** money and you'll likely find you don't see much performance degradation unless you're working on very complex tasks. So that can be a good way of saving a bit of money. But again, it's a bit of trial and error and finding what models work for the kinds of tasks you're asking the agent to complete. Now, lastly, we've got a speed option here. I don't touch that much. You can turn up the speed,

**[1:25:36]** but greater speed equals higher cost. And you probably don't need to bother changing this unless you're super impatient. Clicking here gives you permissions. And permissions is something that we're going to talk about shortly. And then if I type in the slash, we get the familiar slash menu and the skills. And there are things here we've already talked about. We've

**[1:25:54]** got in it. We've got plan mode. And if I were to scroll down, I would see skills creator as well. And there are some other things here which we'll be talking about in the coming scrims. Oh, there's one thing I should show you which is a bit different to Scribbers's agent. And that is the context window icon which is now a bit hidden away in codeex. They've actually chopped and changed on how to

**[1:26:14]** do this in codeex. So it might have changed again by the time you watch it. But at the moment, if we just focus in on the agent and I type in /compact, that actually brings up the context window icon and it tells you the percentage that you've used so far. So that's useful to know about. It's now just a little bit hidden away in codeex. Okay, that's it for this quick tour of

**[1:26:35]** the Codeex VS Code extension. You should go ahead and get to this point, get Codeex set up in VS Code, and then you'll be able to better understand what we talk about next, which will be permissions and then MCP. I've already mentioned a couple of times that letting this conversation that we have with the agent get too long can cause us problems. And in this grim,

**[1:26:59]** we're going to go a bit deeper into this problem and look at some solutions. Firstly, let's talk about context. You've seen versions of this diagram before. Every time we prompt the agent, we send off all sorts of information including the prior conversation, the current prompt, system instructions, relevant parts of the codebase, agents.md,

**[1:27:21]** and more. And this is context. So context is all of the information the agent has available to it when it formulates its response. And this prior conversation is a large part of that context. Now there's a limit on the size of context and this is often called the context window and the size of that window depends on the model being used. Now at the time of recording decent

**[1:27:43]** models can handle a context of 1 million tokens or more and a token as a very rough rule of thumb is about four characters. So a million tokens is a lot of text or code. Okay. So what happens when your context becomes too big for the context window? Well, in theory, the model would return an error, but agents won't let it get to that point. Let's say you've been working on some tasks

**[1:28:06]** with your agent. You started off by building a landing page. You added a database and or then you made some style tweaks and now you're nearing the end of your context window and sometime before the context window is full, the agent will have its own limit, which is what we can see right here. So, you are now in the danger area. Now, when you reach this point, the agent will get to work

**[1:28:30]** cutting your context down to size. And it will do this in one of two ways. Either by compacting the context, so everything you talked about gets reduced to a much smaller summary. We've got all the same topics there, but now plenty of space left in the context window. The other common method of reducing context size is truncation. And in this example, the agent has removed the early part of

**[1:28:53]** the conversation, the landing page, and has left the other two completely intact. Now, I just want to be clear here. This is an illustration. It wouldn't be as neat as chopping off a whole topic, but truncating context does mean losing earlier parts of the conversation. Now, all of this happens under the hood, and there's nothing you need to do to make it happen. And also,

**[1:29:14]** different agents will handle it in different ways. But what you do need to know is that this process is lossy and that means some information or nuance is being lost from the conversation and that can lead to erratic behavior from the agent. So in the next script let's look at how we can manage context and why we might need to. Let's look at context management. How do

**[1:29:40]** you know how much context you've used? Well, I've got the same codebase here that we were working on when we were creating skills. And in the scriber agent, you can see a circular icon right here. This is actually a meter and it's got a small chunk eaten out of it. And this is actually showing you how much context has been used. But don't worry, for a more accurate picture, you can

**[1:30:01]** click on the icon and we get this panel which shows us that the context window is 4% full and we've used 38,000 of a million tokens. It also reminds us that the agent automatically compacts its context, and we'll talk more about that in just a moment. Now, in the VS Code Codeex extension, things are a little bit more complicated. They used to show exactly the same icon right here, but in

**[1:30:24]** an update, they hid it by default, but you can view it by going to this settings icon right here, clicking codec settings, and here under composer, we've got show context window usage. toggle that to on and then you can close the settings and you still won't actually see the icon there until you start prompting. So let's type something in and we can see that that icon has

**[1:30:46]** appeared and it's actually the reverse now of the scribba icon. So it starts off as an almost invisible circle and the circle outline grows as context is used and again you can click on it and it will give you the stats on context used. So what are the rules of managing context? Well firstly don't panic. The agent is designed to deal with this so you can mostly just let it do its job

**[1:31:08]** and only act when it's becoming an issue. It actually doesn't cause too many problems. And the fact that Codeex now hides that context window meter icon from you shows that they think most users can just leave this well alone. And as we can see in Scriber, we've actually built a load of skills with this codebase and all we've used is 4% of the context window. So that gives you

**[1:31:29]** an idea of actually how little you need to worry about this problem. Now, it's good practice to use one session per task. And I'm talking here about codeex sessions. So, if you're adding a new nav element, for example, when it's done, you can close the session and start a fresh one for the next task. In Scriber, we have a slash command to do that. It is clear. So, you just type /clear and

**[1:31:51]** send it off. That will completely clear the context and you can start again with a fresh context window. Now, I'm not going to execute that command right now because in a moment I will show you a compact command. But in VS Code, you can close the session and start a new one with command or control depending on whether you're Mac or Windows plus shift and P. And you're going for the

**[1:32:09]** developer reload window option. You'll see something like that. It will appear in the command pallet at the top. When you click that, you actually get a fresh codeex session. And when you prompt, you'll see the meter icon doing its thing. And if you click on it, you'll see that you've actually started with a fresh context window. Now, if the task is too big for a session, so you're in

**[1:32:28]** the middle of a task, but the context window is nearly full, and prompt the agent with something like this. And this isn't a one-sizefits-all prompt, but that said, asking the agent to summarize these things should give the next codec session all of the information it needs to continue with the task with a clear context window. So, literally put that into the agent. It's going to give you

**[1:32:49]** back a bunch of text. You can then paste that text into a fresh codec session and keep developing. Now, I did say that Scriber has its own compact command that will do this for you. VS Code's codeex extension used to do exactly the same thing. I'm just going to show you it quickly because to be honest, codeex is changing things constantly at the moment. So, I wouldn't be at all

**[1:33:08]** surprised if this feature or something similar came back. So, in the scriber agent, it's just/compact. You select it and it will say it's compacting the context. And if you'll remember, the context is 4% full at the moment on 38K. In a moment, we will check it out when this changes to compacted context. There we are. The context has been compacted. We won't see a change reflected

**[1:33:29]** immediately. We'll need to prompt the agents. And we can just say anything we want. I might just update the agents.m MD file, for example. Okay, so the agent's done some work. Let's click on this icon. And now we've gone to 3% full and we're down to 34,000 tokens used. So you can see that our context window was really pretty empty already. So compacting it has not achieved a lot,

**[1:33:53]** but that's just a feature that we've got in the scriber agent and which you may well see in the future in other agents you use. Okay, so that is it for context. The major takehome is you probably don't need to worry about it too much. Oh, the agents just rewritten agents.mmd. That's fine. So you probably don't need to worry about it too much, but you should start a new session for

**[1:34:13]** each task. And if things get more complex than that, now at least you know what's going on under the hood and you've got some options. Whichever agent you use, permissions will be a thing and you need to be on top of it. In Scribbers's agent, we have got these three permissions settings. Ask for approval, approve for me, and full access. And if we just open up VS

**[1:34:39]** Code, we can click on this icon right here to bring up the permission settings. And in fact, I'm just going to zoom in on this panel. Okay. So, we can see that the Scriber agent is mirroring the VS Code setup. We've got ask for approval, approve for me, and full access. And these go in order of the leeway that you give the agent. The first setting, ask for approval, will

**[1:35:00]** allow the agent to read and create files, but it will ask for permission before deleting files, installing packages, or running terminal commands. The middle option gives you a smoother experience. the agent will think more about what really needs your permission and so there will be fewer interruptions. And this is probably the go-to setting for most developers. The

**[1:35:20]** agent will only disturb you if it needs to make changes outside of your workspace or do something potentially destructive like deleting large amounts of data or carrying out some Git operations that it deems risky. This one here, full access, this is not encouraged. You should not surrender all of your control to the agent unless you really know what you're doing. Now in

**[1:35:40]** the Scriber agent, we've actually fixed permissions at ask for approval. We don't allow users to use these other two possibilities. But in VS Code, you do have that freedom. So just be a little bit careful. Now down here we can see we also have a custom option and it says in brackets config.toml. When you select this option, you can exert more granular control over permissions by editing this

**[1:36:03]** config.toml file. And config.toml is something you should know about. So let's have a look at it in the next scrim. Config.l is a humanreadable config file for custom settings for permissions and other aspects of codeex behavior. And just like with the agents.mmd file, this file can live in your project and be project specific in which case it will

**[1:36:28]** live in its owncodeex folder. And I've got one mocked up right here. But codeex defaults to creating and reading a global scope config.toml toml which means it lives in a familiar place the do.codex codeex folder on your local machine's home directory where you might also have your global agents.mmd file. And just to be clear, you don't have to have custom settings. So if you look in

**[1:36:48]** thiscodeex folder and find there's no config.l, that is fine. You can manually create one. Okay, let's look at the example that I've got right here in Scriber. But just to be clear, it won't work in Scriber without agent. You need to take this over to VS Code and use it with VS Code. I'm just using it here for easy live editing. Let's go through it. So firstly, we've got some permission

**[1:37:10]** settings. And these lines with the hashtags at the start are just comments. [clears throat] They tell us what each setting does. So starting off, we've got approval policy on request. And this is controlling when Codeex is going to ask you for permission before doing something. So on request means ask before higher risk actions while allowing normal agentic work. So mostly

**[1:37:31]** codeex will do its thing without asking for permissions. But some higher risk actions will require your permission. Another option for the approval policy is untrusted which is ask before commands that are not considered very low risk. So codeex will still do some trivial tasks without bothering you for permission but will ask for permission much much more. And the other option

**[1:37:51]** we've got here is approval policy never and that means never ask for approval. So, the agent will do whatever it thinks it needs to do, but of course, it will stay inside other permissions settings. Okay, I'm going to put this one back to its default, which is on request. Okay, this second setting right here is the sandbox mode, and that controls what access codeex has to files and folders

**[1:38:13]** on your PC. The default is workspace, write, and that means Codex can edit files in the current workspace, but not elsewhere on your machine. Now, regardless of whether your config.toml toml is in your project route or in the global.codex file in the home directory of your PC. The current workspace here refers to the project folder of the project that you're currently working

**[1:38:34]** on. Now, we have other options here. Setting sandbox mode to read only does exactly what you would expect. Codeex can inspect files, but it cannot edit them. So, that's along the lines of plan mode. And at the other end of the scale, we have got sandbox mode, danger full access. Codeex can access and modify files outside the current workspace. That potentially gives the agent access

**[1:38:58]** to your entire PC. And this of course is not recommended. That is why they've used the word danger. But you do have that option available to you if you want it. Now moving on down, we move away from permissions and we've got the default model. That's fairly self-explanatory, but we will talk about it more in the next scrim. And then finally, we have got some reasoning and

**[1:39:17]** response style settings. So the effort is set to medium, veosity medium and personality pragmatic. If you want to play around with these and find out what other settings are available, I have given you a link right here with this screenshot. Just click on it. It will take you straight through to the config page in the docs. Now it's important to know about config.toml. But a lot of the

**[1:39:38]** time you are going to find the UI settings are sufficient for your needs. Okay. In the next scrim, let's have a challenge with this and troubleshoot some common problems. Let's see custom settings in action with a challenge for you to do in VS Code. At the moment, every time you open a codec session, it will default to a model. Let's zoom in on this part of the codeex

**[1:40:02]** panel. And we can see at the time of recording, it's defaulting to 5.6 soul. Now, [snorts] unless you're doing something very taxing, you can save money by downgrading that model. But it's annoying to have to remember to do it every session because every time you open up a new codec session, it's going to go back to its default. So your challenge is actually very easy. I want

**[1:40:23]** you to edit the global config.tl to change the default model to a cheaper one. Now when I do this, I'm going to downgrade from 5.6 to 5.4. But you can choose any model which is available to you in codeex and those will change over time. If you click on the model, the other options will appear and these are the ones which are available to me at time of recording. Once you have edited

**[1:40:44]** the globalconfig.comtoml and you can do that right here in Scriber and copy it over or edit it right there in VS Code, it doesn't matter. Once you've done that, open up a project in VS Code and your new default model should be displayed in the UI. Now, I've put here restart the codec session if necessary and I've said that because changes to config.toml will not take effect until a

**[1:41:04]** codec session is restarted. Now, if you didn't have codeex open when you edited the globalconfig.toml, that's absolutely fine. But if you already had codeex open, you will have to restart it. And there is a bit of a procedure to do that. You need to hit command or control depending on whether you're Mac or Windows plus shift and P. That will bring up the command pallet

**[1:41:24]** and the option developer reload window. It's going to look something like that. When you select that, codeex will reload and you'll see the new model reflected in your UI. Okay, go ahead and get to work on this challenge. Okay, hopefully you defaulted to a cheaper model. So, I did this. I went to my globalconfig.toml, this one in the home directory of my PC

**[1:41:47]** and I made the change right here, downgrade to 5.4. I saved that and then I went through this restart procedure and when it restarted, the default 5.6 had changed to 5.4. And that's just a bit of a timesaver, but don't forget you've done that because if in the future you do want to use the more powerful model, you will need to undo that config.l setting. Okay, let's have

**[1:42:10]** a quick word about troubleshooting. If you find that changes you've made to your config.l is not having an effect, there are a couple of things to check. Firstly, you cannot override your organization. So if your codeex openai account is part of an organization that is to say you've got a work account for example that organization can set management policy which you cannot

**[1:42:32]** override. If you want to change something you will need to speak to whoever owns or administrates that organization. The second common problem comes down to whether your repo is trusted. And this is something which normally arises because you've made a change to a project scope config.toml and you're not seeing any effect. Now, when you open up a new codebase in VS

**[1:42:53]** Code, you'll likely be met with something like this. It's basically asking you if you trust the code and if you trust where it comes from. If you do, then your project level config.l file should be respected. But if for any reason that doesn't happen, so VS Code thinks that your codebase is not trusted, you can actually force it to be trusted by going to your global scope

**[1:43:12]** config.toml and adding this at the top. And it should be at the top. It should be the first thing that's read in the config.toml. So all you need is inside these square brackets we've got projects dot and then we've got the path to your project. So it's important obviously to get that right and then set the trust level to trusted and that should make your project scope config.toml. So the

**[1:43:33]** one actually in your project directory visible to codeex. So when you restart the codec session that project scopeconfig.toml should take effect. Okay that's an overview of permissions and custom settings. I'll leave you with a link to the docs if you want to do a bit more research. Agents have the ability to use external tools to complete certain tasks and

**[1:44:00]** that's really useful because reasoning alone is not enough because the agent cannot inspect the outside world. tools enable agents to retrieve current information, query databases, use external services, send emails, and much [clears throat] more. Besides, now having an AI assistant user tool is made so much easier by MCP. MCP stands for model context protocol, and it's

**[1:44:25]** designed to be the USBC for AI, allowing AI assistants to securely connect to external tools and data sources. So the overall idea of MCP is that you've got a standardized protocol which makes it easy for agents and AI assistants to interface with external tools. Let's see how we can use MCP in agentic coding and that means understanding the MCP loop. So the MCP loop starts with the user

**[1:44:50]** giving a task for example fix the broken UI. The agent reasons about what it needs and decides to call a tool. The tool call goes out via MCP to the relevant server which executes the actual action. The results are returned to the agent and added to the context and the agent evaluates the result and either calls another tool or produces the final answer. And this is where the

**[1:45:13]** loop comes in because these steps can repeat until the agent decides the task is complete or it hits some kind of limit. Eventually, assuming it's been successful, the outcome is delivered back to the user. In the next scrim, we're going to see MCP in action as we work on this app which I've built. It's a camb board for a product launch. And at first glance, it looks okay. But if

**[1:45:35]** we dig deeper, we can see that there are some pretty big UI issues. A lot of these cards have got border inconsistencies. Look, there's all sorts of things going on here. Different border radiuses. Some borders are dotted, others are full lines. Right here, we've got buttons of completely different sizes. And there's also something strange going on with the

**[1:45:54]** shadow effect, which is applied somewhat randomly. In fact, when you look closely, this whole thing is a mess, and you can tell that it's been bolted together piece by piece without a coherent strategy. But luckily, Shadcen is coming to the rescue. Shad CN is a collection of ready-made customizable UI components for React apps. And as this canban board is built in React, it's

**[1:46:16]** going to be perfect. But what's even better is that Shad CN has an MCP server. So Codeex will be able to access its UI components and use them to refactor our app. And this is a great use case for MCP because having the agent use the Shad CN tool set is going to be much better than the agent coming up with its own UI ideas. And it's also going to be a lot quicker and the

**[1:46:38]** results will be more uniform. Okay, let's head on to the next Grim and see it in action. Okay, let's use the Shad CN MCP to tidy up the UI of this app. There's some setup involved, but Codeex is going to do all of the hard work for us. Firstly, go to the cog icon bottom right, click download as zip, and then bring the code into VS Code. And to check it's working,

**[1:47:07]** open up a terminal and do mpm install and mpm rundev. Then you should be able to see the app hosted locally. Now I'm simply going to prompt Codeex to set up the Shad CN MCP server. And now Codeex is going to have to do quite a lot of work. But the main thing it's going to do is download and run the Shad CN package. And that is going to be available to it whenever Codeex starts

**[1:47:29]** using the MCP server. When it's done, if you look in your config.toml file, you should see this. You don't need to understand what this block of code is doing. You just need to understand that config.toml toml needs to register any MCP servers that the agent wants to use. And by the way, I'm looking here at the globalconfig.toml. So this is in thecodeex folder in my

**[1:47:51]** home directory. It is possible that this will appear in the config.toml in the project scope, but in my experience, codeex is defaulting to registering MCP servers in the global config.l. Now the now the change you will notice in the project codebase is that you've got this components.json JSON file. Again, we don't need to understand everything that's going on in here. You just need

**[1:48:14]** to know it's an essential part of the setup. Okay. So, how will Codeex use Shad CN? Well, via the MCP server, it's going to get access to Shad Cen's component library, and then it can choose which ones to use on our app. So, as a sanity check and to make sure SADC MCP is set up properly, let's prompt show me all available components in the SHAD CN registry. When I put that in, I

**[1:48:37]** got back this a long list of 61 UI components. And it did that in just 26 seconds. And that's telling us that this is not something that the agent has just gone away and researched. It's actually taking this straight from Shad CN via the MCP server. Okay, it's time to prompt Codeex to refactor the UI of our app. And the prompt that I eventually came up with is pretty long. And I did

**[1:49:00]** chat a little bit with the agent to figure out how best to phrase this. So that's the prompt I used. I'm not going to expect you to copy that out. I have given you a copy right here in prompt.md. So you're welcome to just copy and paste that. And when I took that, pasted it into Codeex and sent it off. It did take quite some time. It took about 6 minutes, but it was a

**[1:49:21]** success. And Codeex gave a rundown of all of the files it's updated. And of course, the proof of the pudding is in the eating. So when I open up the app, it now looks like that, which is so much better. And just as a reminder, let's flick between the old UI with all of its weird border radius problems, shadow problems, and these strange dotted lines everywhere to this much cleaner, much

**[1:49:45]** more uniform layout. Now, remember, if you look carefully at the prompt, we did specifically tell it to look at the UI components. We didn't say anything about color, and that is why that rather funky color scheme has been preserved. Now, in doing this, we have given the agent quite a lot of freedom. We've told it which tool to use, but it's then decided how to use that tool. So, you don't have

**[1:50:06]** to consider this a oneshot thing. You're welcome to keep going, keep prompting the agent, asking for changes, and persevering until you get the product you want. Okay, so that is MCP. It's a whole world of tool calling for agents. I recommend you go and check out a few more MCP servers and see what you can do with them. Ones I'd recommend include GitHub, Playright, which lets an agent

**[1:50:29]** open a site, interact with the UI, and verify that a feature works in the browser, and file system, which gives controlled access to selected folders and files. And there are thousands more out there on the internet. Just go ahead and see what tools you can use and see what you can

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
