# Transcript — LangGraph Complete Course for Beginners

- **Video:** https://www.youtube.com/watch?v=jGg_1h0qzaM
- **Canal:** freeCodeCamp.org
- **Expositor:** Vaibhav Mehra (robotics & AI student)
- **Duración del reproductor:** 11.391 s (3:09:51)
- **Código:** https://github.com/iamvaibhavmehra/LangGraph-Course-freeCodeCamp
- **Fuente del transcript:** subtítulos automáticos de YouTube (`en-orig`, `fmt=json3`), bajados con `curl` desde `automatic_captions` de yt-dlp. 4.509 cues deduplicados, ~31.500 palabras. Último cue en 11.387 s contra 11.391 s del reproductor: el audio está cubierto hasta el final.
- **Formato:** `[h:mm:ss]` al inicio de cada bloque de cues. Los cues no se editan.

## Glosario de errores del ASR

| En el ASR | Es |
|---|---|
| Langraph / Lang graph / Langro / Lagraph / Langra | LangGraph |
| Vbeca / Vava / V | Vaibhav (el propio expositor) |
| GPD40 / GBD40 / GPD4er / GPD 40 | GPT-4o |
| chat open AAI / chat openai / open AAI | `ChatOpenAI` (langchain) |
| Olama / OAMA / chat oama | Ollama |
| dock string / doc string / docstrings / dock strings | docstring |
| dossage / dosage | `message` (módulo `langgraph.graph.message`) |
| add messages / add message | `add_messages` (reducer) |
| annotated / sequence | `Annotated`, `Sequence` (typing) |
| type dictionary / typed dictionary | `TypedDict` |
| bind tools | `bind_tools` |
| react agent / react graph / R agent | ReAct agent (reasoning + acting) |
| chromo / chroma vector data | Chroma (base vectorial) |
| pi PDF loader | `PyPDFLoader` |
| recursive character text splitter | `RecursiveCharacterTextSplitter` |
| ragation / rag agent | `rag_agent` |
| Javis / JavaS / mini Javas | Jarvis |
| tree / path | (en el `add_conditional_edges`: `path` y `path_map`) |
| canary wolf (lugar inventado en la demo) | *sin valor factual* |

## Capítulos oficiales (descripción del video)

| Tiempo | Capítulo |
|---|---|
| 0:00:00 | Introduction |
| 0:01:24 | Type Annotations |
| 0:08:35 | Elements |
| 0:18:39 | Agent 1 Intro |
| 0:21:08 | Agent 1 Code |
| 0:32:22 | Agent 1 Exercise |
| 0:33:07 | Agent 2 Intro |
| 0:34:02 | Agent 2 Code |
| 0:43:27 | Agent 2 Exercise |
| 0:44:29 | Agent 3 Intro |
| 0:45:18 | Agent 3 Code |
| 0:54:04 | Agent 3 Exercise |
| 0:55:36 | Agent 4 Intro |
| 0:56:37 | Agent 4 Code |
| 1:13:09 | Agent 4 Exercise |
| 1:14:14 | Agent 5 Intro |
| 1:15:45 | Agent 5 Code |
| 1:29:19 | Agent 5 Exercise |
| 1:31:01 | AI Agent 1 Intro |
| 1:32:49 | AI Agent 1 Code |
| 1:42:54 | AI Agent 2 Intro |
| 1:43:58 | AI Agent 2 Code |
| 2:03:20 | AI Agent 3 Intro |
| 2:05:00 | AI Agent 3 Prerequisite |
| 2:12:28 | AI Agent 3 Code |
| 2:28:46 | AI Agent 4 Intro |
| 2:30:59 | AI Agent 4 Code |
| 2:52:09 | RAG Agent Intro |
| 2:53:01 | RAG Agent Code |
| 3:06:15 | RAG Agent Testing |
| 3:09:04 | Course Outro |

## Transcript

[00:00:00] Welcome to this video course on
[00:00:02] Langraph, the powerful Python library
[00:00:04] for building advanced conversational AI
[00:00:07] workflows. In this course, Vbeca will
[00:00:10] teach you how to design, implement, and
[00:00:12] manage complex dialogue systems using a
[00:00:15] graph-based approach. By the end, you'll
[00:00:18] be equipped to build robust, scalable,
[00:00:20] conversational applications that
[00:00:22] leverage the full potential of large
[00:00:25] language models. Hey guys, my name is
[00:00:27] Vava and I'm a robotics and AI student.
[00:00:30] In this course, we're going to be
[00:00:32] learning all about the fundamentals of
[00:00:34] Langraph. Now, I assume you've heard of
[00:00:36] Langraph before, hence why you clicked
[00:00:39] on this course. But I'm also going to
[00:00:41] assume you have never coded in Langraph
[00:00:43] before. Now, because of this assumption,
[00:00:46] I have explained every single thing in
[00:00:48] as much detail as I possibly can. Now,
[00:00:51] also this might mean that I might be
[00:00:53] going slow at times. So if you want you
[00:00:55] can always speed me up. Now what are we
[00:00:58] going to be learning in this course?
[00:01:00] Well to start we're going to be building
[00:01:02] a lot of graphs, a lot of AI agents.
[00:01:05] We're going to be learning a lot about
[00:01:06] the theory and I've also provided
[00:01:09] exercises throughout the course in which
[00:01:11] all of the answers will be provided on
[00:01:13] the
[00:01:13] GitHub. With that being said, if you're
[00:01:16] ready to start on this journey with me,
[00:01:18] let's go to our first section
[00:01:21] then. All right people. So welcome to
[00:01:24] the first section of this course. Now in
[00:01:26] this section we'll be covering something
[00:01:28] called as type annotations. Now
[00:01:31] admittedly this is going to be a
[00:01:32] completely theoretical section but it
[00:01:34] will be short and brief. I promise. The
[00:01:36] reason I've kept this specific section
[00:01:38] in the course is because when we do
[00:01:40] eventually go on to code uh our AI
[00:01:42] agents, our graphs and langraph, these
[00:01:45] will start popping up everywhere. And I
[00:01:47] don't really want you to look start
[00:01:49] coding without ever having seen these
[00:01:51] before or really not knowing what these
[00:01:53] actually are. So that's why I've kept it
[00:01:55] here. But I promise this will be short
[00:01:57] and brief. Cool. Okay. Let's begin with
[00:02:00] dictionaries. Now dictionaries are a
[00:02:02] data structure. Yes, but there's a
[00:02:05] reason I've kept it here. So let's see
[00:02:07] how a dictionary is described in Python.
[00:02:09] You should already know this. So in this
[00:02:11] case, I've described a very simple
[00:02:13] dictionary called uh movie. and it has
[00:02:16] two keys, the name and the year. And it
[00:02:18] has two values, Avengers Endgame and
[00:02:21] 2019. Now, dictionaries are awesome,
[00:02:23] don't get me wrong. They're they allow
[00:02:25] for efficient data retrieval based on
[00:02:27] their unique keys. They're flexible and
[00:02:29] easy to implement, but there's a
[00:02:30] potential problem with them. See, it's a
[00:02:34] challenge to ensure that the data is a
[00:02:35] particular structure. And this could be
[00:02:38] a huge problem in larger projects. So to
[00:02:41] put things in simple words, it doesn't
[00:02:43] really check if the data is the correct
[00:02:44] type data type or structure and that
[00:02:47] could be the source of a lot of logical
[00:02:50] errors in your project. And if your
[00:02:52] project is really really large, then
[00:02:54] this could be quite a headache to
[00:02:56] identify, right? Cuz it's quite a small
[00:02:58] detail. So what is the solution for
[00:03:00] this? Well, it's something called a type
[00:03:03] dictionary. Now, here is an example on
[00:03:06] how you create a type dictionary in
[00:03:07] Python. And I just want to uh emphasize
[00:03:10] that this type annotation is used
[00:03:13] extensively in langraph. This will be
[00:03:15] used to define states. Now don't worry
[00:03:18] you we haven't covered states yet. We
[00:03:19] will cover that in the next section. But
[00:03:21] just be mindful that this is quite
[00:03:23] important. So a type dictionary is quite
[00:03:26] easy to implement. You implement it as a
[00:03:28] class. In this case, I've implemented
[00:03:30] the same um example I uh uh showed you
[00:03:34] in the previous section where I
[00:03:36] described the movie is the same exact
[00:03:38] keys and values. So, it still has the
[00:03:40] name and the year. But notice in this
[00:03:42] class, I have defined the actual uh data
[00:03:46] type of what that key should be. So, for
[00:03:48] example, the name is a string and the
[00:03:50] year is an integer, right? And to
[00:03:53] initialize a dictionary uh I have done
[00:03:56] the exact same thing. to have engineet
[00:03:57] game in 2019. So now there are two main
[00:04:01] uh benefits of using a type dictionary
[00:04:03] it's type safety because we've
[00:04:06] explicitly defined what should be in
[00:04:08] this data structure and so this will
[00:04:10] really reduce the runtime errors and
[00:04:12] obviously the readability is enhanced as
[00:04:14] well and this will make debugging easier
[00:04:16] if something goes wrong within this type
[00:04:19] dictionary. Cool. So we've covered type
[00:04:22] dictionary now. Now we move on to
[00:04:24] another type of annotation which is
[00:04:26] union. Now you might have seen these
[00:04:29] future these later uh types annotations
[00:04:31] before if you coded in Python but again
[00:04:33] I'm just giving you a highle overview
[00:04:35] what these are. So union take a look at
[00:04:38] this example. So I've created a very
[00:04:40] simple function which takes in a value
[00:04:42] and it squares it. Now in this case the
[00:04:46] uh input x could be either an integer or
[00:04:48] float and union basically says that
[00:04:52] whatever value you have can be these
[00:04:54] data types only. So in this case x can
[00:04:57] only be integer or float. So if I pass
[00:04:59] in five or 1.23 4 this would be
[00:05:01] completely fine. It would square the
[00:05:02] number and everything. But if I passed
[00:05:04] in a string like I am a string it would
[00:05:06] completely fail. Now admittedly yes this
[00:05:10] function is quite easy. If I passed in
[00:05:12] I'm a string, it would have failed
[00:05:13] anyway. But in more complicated
[00:05:15] applications, hopefully you can see how
[00:05:17] this actually is useful. In fact, the
[00:05:19] makers of Lang Chain and Langraph used
[00:05:22] Union quite extensively throughout u
[00:05:24] making the actual library. So again,
[00:05:27] it's flexible and it's easy to code and
[00:05:30] it allows for type safety. So because it
[00:05:32] can provide hints to uh help catch
[00:05:35] incorrect usage. Now something similar
[00:05:37] to union is another type annotation
[00:05:40] which is optional. Now optional is quite
[00:05:42] similar and in this case I've described
[00:05:45] another function nice message. So you
[00:05:48] pass in a name. If you pass in a name it
[00:05:51] will say hi there name. So for example
[00:05:53] let the name be Bob. If I pass in Bob to
[00:05:56] this uh function it would say hi there
[00:05:58] Bob. But what if I don't pass in
[00:06:01] anything? Now if I don't pass anything
[00:06:03] optional because I've used optional says
[00:06:06] that the name parameter could either be
[00:06:08] a string or a none value. Now if I pass
[00:06:12] in nothing it will go in this if
[00:06:13] statement and say hey random person. But
[00:06:16] this is also important to emphasize that
[00:06:18] it cannot be anything else. It can't be
[00:06:20] an integer or or a boolean or a float or
[00:06:23] anything like that. It has to be either
[00:06:25] a string or a none value because that's
[00:06:27] what I've defined here. Cool. Now comes
[00:06:30] another type annotation called any. And
[00:06:33] any is really the easiest one to
[00:06:36] understand. It literally means this
[00:06:38] value could be anything. It could be any
[00:06:40] data structure. So in this case I've
[00:06:42] created a simple um function called
[00:06:45] print value where it takes in something
[00:06:47] and it prints that. And for example I
[00:06:51] passed in this string and it prints it
[00:06:54] and anything and everything is allowed.
[00:06:56] Cool. one last type annotation I promise
[00:07:00] and it's the lambda function. So lambda
[00:07:02] functions are quite useful. For example,
[00:07:05] in this I'll give you two examples now.
[00:07:07] So the first example is this really
[00:07:10] simple uh example. Now we've already I
[00:07:13] already created a square function
[00:07:14] before, right? Where it takes in a
[00:07:16] value, it takes in a number and it
[00:07:18] squares it. So for example, if I passed
[00:07:20] in square 10, it would give me 100.
[00:07:23] Quite an easy example. Now let me give
[00:07:25] you a second
[00:07:26] example. this. So if you've come from a
[00:07:29] leaf code background, then you've
[00:07:31] probably seen you've either used lambda
[00:07:34] before and you've definitely used math
[00:07:35] before cuz it's quite efficient. So for
[00:07:37] example, if I pass in 1 2 3 4, what this
[00:07:40] piece of code is saying is that it
[00:07:42] squares each number in nums. So this map
[00:07:46] function maps each value uh and performs
[00:07:49] this function to it. So x * x. So 1 4 9
[00:07:54] 16 and then converts that back into a
[00:07:55] list. Now lambda functions really are
[00:07:58] just a shortcut to writing small
[00:08:00] functions and they make everything quite
[00:08:02] efficient. Now obviously this could have
[00:08:05] been done in one line as well but for
[00:08:06] example this a beginner programmer could
[00:08:09] have might have used a for loop but a
[00:08:12] more advanced programmer could have used
[00:08:14] this and this is obviously much more
[00:08:16] efficient. Right? So hopefully you can
[00:08:18] start to see what how powerful these
[00:08:21] type annotations are and these will be
[00:08:23] coming up. So again, no need to memorize
[00:08:25] this. Just need to have a highle
[00:08:27] overview what they are. Okay, cool. So
[00:08:29] now I'll see you in the next section.
[00:08:31] See you
[00:08:33] there. All right, perfect. So let's
[00:08:36] continue on. In this section, we will
[00:08:39] look at the different elements in
[00:08:41] Langraph. So let's begin with our first
[00:08:44] element, one of the most fundamental
[00:08:46] elements in all of Langraph, the state.
[00:08:49] So what is a state? Well, it's a shared
[00:08:52] data structure that holds the current
[00:08:54] information or context of the entire
[00:08:57] application. In simpler terms, it is
[00:08:59] like the application's memory where it
[00:09:01] keeps track of the variables, the data
[00:09:04] that nodes can access and modify as they
[00:09:06] execute. Now, don't worry if you don't
[00:09:08] understand what a node is yet. That is
[00:09:10] what we will be talking in the next
[00:09:12] slide about. But as a good analogy,
[00:09:15] think of the whiteboard in a meeting
[00:09:16] room analogy.
[00:09:18] Now imagine you're in a meeting room and
[00:09:20] there are different participants as well
[00:09:22] and every time you come up with
[00:09:23] something new or you want to record some
[00:09:25] new uh information or update some
[00:09:27] information you write it on the
[00:09:29] whiteboard. In this case the whiteboard
[00:09:32] acts as your state and the participants
[00:09:34] act as a
[00:09:35] node. So the state shows us the updated
[00:09:40] content/in information of your entire
[00:09:43] application. Hopefully that made a bit
[00:09:45] of sense.
[00:09:47] So let's move on to the node another
[00:09:49] fundamental element in lang graph. So
[00:09:52] these are just individual functions or
[00:09:54] operations that perform specific tasks
[00:09:56] within the graph. So each of these node
[00:09:59] receives an input which is often just
[00:10:01] the current state of your application.
[00:10:03] It processes it and then produces an
[00:10:05] output or an updated
[00:10:08] state. So here's a good analogy of this.
[00:10:12] The assembly line station analogy. Now
[00:10:15] look at this image. Each of these
[00:10:17] station does one specific job. It could
[00:10:20] be attaching a part. It could be
[00:10:22] painting it. It could be inspecting the
[00:10:24] quality and so on and so on. The point
[00:10:27] is each of these stations represent a
[00:10:30] node because they do one specific
[00:10:33] task. So how do you actually connect
[00:10:36] these different nodes together? Well,
[00:10:38] before we go into that, I think it's
[00:10:40] important we understand the most
[00:10:42] important element of them all, the
[00:10:46] graph. It is so important that it's even
[00:10:48] in the name Langraph. So, the graph is
[00:10:52] just the overarching structure and it
[00:10:54] maps out how different tasks aka nodes
[00:10:57] are connected and executed. So it
[00:11:01] visually represents the workflow showing
[00:11:03] the sequence and the conditional parts
[00:11:06] between various
[00:11:07] operations. Now a graph is quite
[00:11:09] self-explanatory but you can think of it
[00:11:11] as a road map. On a road map you can see
[00:11:15] it display the different routes
[00:11:16] connecting cities with the different
[00:11:18] intersections offering choices on which
[00:11:20] path to take next.
[00:11:22] Now, here's a great image of what a
[00:11:24] graph is, and these are the individual
[00:11:26] nodes, but you'll see they're connected
[00:11:28] somehow. So, how are these connected?
[00:11:32] That brings us to the next element,
[00:11:35] edges. So, edges are just the connection
[00:11:37] between nodes and these determine the
[00:11:40] flow of
[00:11:41] execution. So, they tell us or tell the
[00:11:44] application which node should be
[00:11:45] executed next after the current one
[00:11:47] completes its task. A really good
[00:11:50] analogy of this is imagining a train
[00:11:52] track. So this is the train track and
[00:11:55] think of it as an edge and think of it
[00:11:57] as connecting two stations one here and
[00:12:00] one here which represent nodes together
[00:12:03] in a specific
[00:12:05] direction. Now the train which will go
[00:12:07] on the train track that acts as your
[00:12:10] state. So the state gets updated from
[00:12:13] one station to another.
[00:12:16] But there is another type of an edge and
[00:12:19] it's called a conditional
[00:12:21] edge. So this is still not very
[00:12:24] complicated. It's quite simple to
[00:12:25] understand. These are just specialized
[00:12:28] connections that decide the next node to
[00:12:30] be executed based on the specific
[00:12:32] condition or logic applied to the
[00:12:34] current state. Now a really good analogy
[00:12:37] for this is the traffic light analogy.
[00:12:40] So green could mean to go one way, red
[00:12:42] could mean to stop. yellow could mean to
[00:12:44] slow down. The point I'm trying to make
[00:12:47] here is that the condition, in this case
[00:12:49] the light color, it decides the next
[00:12:52] step. If you want to think even more
[00:12:54] simply, you could think about an if else
[00:12:58] statement. So that being said, we move
[00:13:01] on to the next element, the start point.
[00:13:04] So the start point or the node, the
[00:13:06] start node is a virtual entry point in
[00:13:08] langraph and this marks where the
[00:13:10] workflow begins. Now it's important to
[00:13:12] note that it doesn't perform any
[00:13:14] operations itself but it serves as the
[00:13:17] designated starting position for the
[00:13:18] graph's
[00:13:19] execution. Now in terms of analogy it is
[00:13:22] quite simple to understand but if you
[00:13:25] really want think of it as the starting
[00:13:27] line of
[00:13:29] race. Now if you have a start point well
[00:13:32] you need an end point as well and that's
[00:13:34] where the end element comes in. So the
[00:13:37] end nodes just signifies the conclusion
[00:13:39] of the workflow in Langraph. So when the
[00:13:42] application reaches this node, the
[00:13:44] graph's execution completely stops and
[00:13:46] it indicates that all intended processes
[00:13:49] have been
[00:13:50] completed. And again, a good analogy for
[00:13:52] this is just the finish line in a
[00:13:55] race. So nothing too hard yet. But now
[00:13:59] let's look at
[00:14:01] tools. So tools are specialized
[00:14:04] functions or utilities that nodes can
[00:14:06] utilize to perform specific tasks. For
[00:14:09] example, it could be fetching data from
[00:14:11] an
[00:14:11] API. They basically enhance the
[00:14:14] capabilities of these nodes by providing
[00:14:16] additional
[00:14:17] functionalities. Now, one common
[00:14:19] question could be, well, what's the
[00:14:20] difference between a tool and a node?
[00:14:23] The node is just the part of the graph
[00:14:25] structure. Whereas the tools, these guys
[00:14:28] are functionalities used within the
[00:14:31] nodes. Now, a really good analogy for
[00:14:33] this is just tools in a toolbox. So
[00:14:36] imagine a hammer for the nails, a
[00:14:38] screwdriver for the screws, etc. The
[00:14:41] point is each tool has a distinct
[00:14:43] purpose. Again, don't worry. You will
[00:14:46] understand the differentiation between
[00:14:48] tools and nodes in a lot more detail
[00:14:50] later when we code this, but this is
[00:14:52] just for a general
[00:14:53] overview. Now, another question you
[00:14:56] could be asking is, is there a middleman
[00:14:58] between a tool and a node? Short answer
[00:15:01] is yes. That's where tool node comes in.
[00:15:05] So a tool node is just a special kind of
[00:15:07] a node whose main job is to run a
[00:15:11] tool. So for example, a tool node could
[00:15:14] be a node where its only job is to use a
[00:15:18] tool and that tool's job is to fetch
[00:15:21] some data from an
[00:15:22] API. So it connects the tools output
[00:15:25] back into the state so other nodes can
[00:15:28] use that information.
[00:15:30] So think about this analogy going back
[00:15:33] to the assembly line. In this case,
[00:15:36] imagine the operator as the tool node
[00:15:39] and it controls the machine which is the
[00:15:40] tool and then sends all of these results
[00:15:43] back into this assembly
[00:15:46] line. Now if we progress further, let's
[00:15:50] look at the state graph. So this is
[00:15:53] quite an important element as well. This
[00:15:55] will be one of the first elements you
[00:15:56] actually interact with and its main
[00:15:58] purpose is to build and compile the
[00:16:00] graph structure. So it's quite
[00:16:02] important. It manages the nodes, the
[00:16:05] edges, the overall state and it makes
[00:16:08] sure that the workflow operates in a
[00:16:10] unified way and all of the data flows
[00:16:12] correctly between components. So again
[00:16:15] it's quite an important element. You can
[00:16:18] think about it as a blueprint of a
[00:16:20] building. So just as a blueprint
[00:16:22] outlines the design and the connections
[00:16:25] within a building, the state graph does
[00:16:28] exactly that, but it just defines the
[00:16:30] structure and the flow of your workflow
[00:16:32] or
[00:16:35] application. Now here's where the
[00:16:37] runnable comes in. Now some of you will
[00:16:39] be coming from a lang chain background
[00:16:41] and runnable is quite common there and
[00:16:43] it's quite similar in langraph as well.
[00:16:46] A runnable in langraph is just the
[00:16:48] standardized executable component that
[00:16:51] performs a specific task within an AI
[00:16:53] workflow. It basically acts as a
[00:16:56] fundamental building block allowing for
[00:16:58] us to create these modular
[00:17:00] systems. Now a question you could have
[00:17:02] right now is well what's the difference
[00:17:04] between a runnable and a node?
[00:17:07] Short answer is a runnable can represent
[00:17:10] various operations whereas a node in
[00:17:13] lang lang graph typically receives a
[00:17:16] state performs an action on them and
[00:17:18] then updates the state. Now don't worry
[00:17:22] if you didn't 100% get that when we go
[00:17:24] into the coding section you will get it
[00:17:26] a lot better. But a good analogy is a
[00:17:29] Lego brick. So just as how Lego bricks
[00:17:32] can be snapped together to build these
[00:17:34] complicated structures, runnables can be
[00:17:37] combined to create sophisticated AI
[00:17:39] workflows. So now let's move on to the
[00:17:42] different types of
[00:17:45] messages. Now again, if you come from a
[00:17:47] lang chain background, you'll be quite
[00:17:48] familiar with these. If you haven't,
[00:17:51] don't worry. We will look at the five
[00:17:53] most common message types in Langraph.
[00:17:57] So to start off, there's the human
[00:17:58] message which represents the input from
[00:18:00] a user. The AI message which represents
[00:18:03] responses generated by AI models. The
[00:18:06] system message which is used to provide
[00:18:08] instructions or context to the
[00:18:10] model. Tool message which is similar to
[00:18:13] the function message but specific to
[00:18:14] tool usage. And the function message
[00:18:17] represents the tool of a function call.
[00:18:20] If you've used an API like a large
[00:18:22] language model API before, such as
[00:18:24] OpenAI's API, a lot of these will be
[00:18:26] quite familiar, especially the system
[00:18:28] message, the AI message, and the human
[00:18:31] message. And that concludes this
[00:18:33] section. So, I will see you in the next
[00:18:38] section. Awesome. So, now this is quite
[00:18:41] exciting. We're actually about to start
[00:18:42] coding in Langra for the very first
[00:18:44] time. Now that we've covered all the
[00:18:46] theory, admittedly the boring section,
[00:18:49] we're now actually going to code up some
[00:18:51] graphs. And we're about to code up our
[00:18:54] very first graph in this sub section.
[00:18:55] But um for this overall section, I have
[00:18:58] a slight confession to make, which is
[00:19:01] we're not going to be building any AI
[00:19:02] agents in this
[00:19:04] section. Why? because I thought that one
[00:19:08] we haven't really even seen uh how to
[00:19:10] actually code in Langraph and combining
[00:19:12] all of these LLMs APIs and tools and all
[00:19:15] of that stuff which comes with it
[00:19:17] combining them together would be quite
[00:19:19] messy and it could be quite confusing at
[00:19:21] times especially the fact that we have
[00:19:23] never coded in Langraph before again
[00:19:25] like I said at the beginning of the
[00:19:27] course this course is supposed to be
[00:19:29] beginner friendly detailed and
[00:19:30] comprehensive and we're going to go in
[00:19:33] steps like little by little so hopefully
[00:19:36] understand but don't worry we will be
[00:19:37] coding AI agents soon we're just going
[00:19:39] to be building a couple of graphs right
[00:19:40] now uh understand lang graph better the
[00:19:44] syntax better and how to actually code
[00:19:46] up graphs and get confident with it and
[00:19:48] then we will actually build AI agents
[00:19:50] okay cool so what is the graph which
[00:19:53] we're going to be building together in
[00:19:54] this section I call it the uh hello
[00:19:57] world graph mainly because it's the most
[00:19:59] basic form of graph we can actually code
[00:20:01] in lang graph so the objectives are
[00:20:04] these
[00:20:05] So we're going to be understanding and
[00:20:07] defining the agent state structure and
[00:20:11] don't worry you'll understand what that
[00:20:12] is in a few minutes and we're going to
[00:20:15] be creating simple node functions nodes
[00:20:17] like we discussed in the previous
[00:20:18] section uh and we're going to be
[00:20:21] processing them and updating the state.
[00:20:23] We're going to be building the first
[00:20:25] ever basic langraph structure and we
[00:20:28] will understand how to compile it,
[00:20:29] invoke it, process it, everything. And
[00:20:32] really the main goal of this section is
[00:20:35] to really understand how data flows
[00:20:37] through a single node in langraph. Now
[00:20:40] just to give you a bit of a heads up as
[00:20:42] to what we'll actually be covering uh
[00:20:44] what we're going to be building I should
[00:20:46] say is this graph. Again like I said
[00:20:49] this is the most basic form of graph you
[00:20:52] can build in langraph. It has a start
[00:20:54] point and an end point and this node
[00:20:56] sandwiched in between them. All right
[00:20:59] cool. So hopefully you've understood
[00:21:01] what the objectives are. It's quite
[00:21:02] basic and yeah, I'll see you at the
[00:21:08] code. Okay, cool. Now let's actually
[00:21:11] code this very first graph. So I've
[00:21:13] imported three main things here. The
[00:21:16] dict, the type dict and the state graph.
[00:21:18] The dict and type dict is obviously
[00:21:20] dictionary and type dictionary but um
[00:21:23] and state graph. These three are
[00:21:25] elements which we covered in the
[00:21:26] previous section. So I would highly
[00:21:28] recommend you going back there if these
[00:21:30] are completely unfamiliar. But again you
[00:21:33] don't need to memorize what these are.
[00:21:34] Okay. But just to refresh your memory
[00:21:36] I've written in the comment here what
[00:21:38] the state graph is. So think of the
[00:21:41] state graph as a framework that helps
[00:21:43] you design and manage the flow of the
[00:21:45] tasks in your application. Um again that
[00:21:48] might sound a bit complicated but it's
[00:21:51] not. Once we actually start coding you
[00:21:53] will it'll make more sense. So now the
[00:21:56] first thing we're going to do after
[00:21:57] importing everything is create the state
[00:22:00] of our agent and let's call it agent
[00:22:04] state. And just to refresh your memory
[00:22:06] again what the state is. Think of the
[00:22:09] state as a shared data structure. And
[00:22:11] this keeps track of the your all of the
[00:22:13] information as the application runs. All
[00:22:15] right cool. So now let's build the agent
[00:22:18] state. And the way we do this in
[00:22:20] Langraph is through a class. So let's
[00:22:22] build class agent state and in this in
[00:22:26] these parenthesis we will try to the the
[00:22:30] state needs to be in the form of a typed
[00:22:32] dictionary. So that's why we specify
[00:22:35] type dictionary here. Now let's keep
[00:22:38] this very very fundamental and basic.
[00:22:40] Let's just pass in one input. Let's call
[00:22:44] it something like
[00:22:46] message and obviously we put colon and
[00:22:51] the we specify the data type of that uh
[00:22:54] attribute. Now obviously the data type
[00:22:57] of message will be string right so
[00:23:00] that's why we specify strl again this is
[00:23:02] just normal python so once we've done
[00:23:05] that we are now going to be coding our
[00:23:08] very first node again another very
[00:23:10] fundamental element in langraph so how
[00:23:14] do we actually define a node it's quite
[00:23:17] simple it's just a normal standard
[00:23:19] python function and this is how you do
[00:23:21] it so let's say let's first try to find
[00:23:24] The objective um let's say we are trying
[00:23:28] to let's a greeting message a simple
[00:23:31] greeting message. So we'll write def
[00:23:34] greeting node and we need to pass in an
[00:23:38] input and pass what the output type
[00:23:40] should be. Now the input type of a node
[00:23:44] needs to be the state and the output
[00:23:46] type also has to be the state because
[00:23:49] remember the state keeps track of all of
[00:23:52] the information in your application
[00:23:54] right so obviously you need to pass that
[00:23:56] as an input and you need to pass out the
[00:23:58] or return the updated state. So here's
[00:24:01] how you do it. You pass in state and
[00:24:04] what is the state of our application?
[00:24:06] Well, it's the agent state which we
[00:24:08] defined earlier, right? And the output
[00:24:11] is going to be agent state cuz we need
[00:24:14] to output the updated state. And our
[00:24:16] updated state will again just be the
[00:24:18] agent state once we've done all of the
[00:24:21] um all of the mechanics we do in this
[00:24:23] function, the actions we perform in this
[00:24:25] function. All right. Okay. So now we
[00:24:28] need to do something very very important
[00:24:31] and it gets annoying sometimes but um
[00:24:34] it's really a key habit which I want you
[00:24:36] to form and it is dog strings. Now dock
[00:24:39] strings and lang graph is quite
[00:24:41] important. Why? Because dock strings is
[00:24:44] what will tell your AI agents when we
[00:24:46] actually build the AI agents your LLMs
[00:24:48] what that function actually does what
[00:24:50] that function's actions are what it
[00:24:52] performs. So in this case uh by the way
[00:24:55] to create a dock string is just three
[00:24:57] quotation marks three pairs of quotation
[00:24:59] marks. Uh let's call the dock string in
[00:25:03] this case let's just write simple node
[00:25:05] that adds a greeting message
[00:25:09] to the state. Perfect. So now how do we
[00:25:14] actually refer to this message? Well
[00:25:16] again this is just normal Python code.
[00:25:19] So we will pass in state and we will
[00:25:22] type in message.
[00:25:25] Now this specific part allows us to
[00:25:28] actually update the state or the message
[00:25:31] part of the state. And let's say let's
[00:25:34] come up with something like hey
[00:25:37] plus state
[00:25:40] message. Um we can also add something
[00:25:42] like how is your day going something
[00:25:46] basic. Now what's the last thing which I
[00:25:48] need to do in this function? Think about
[00:25:53] it. Okay. So now remember in uh a few
[00:25:56] moments ago I said we have to return the
[00:25:58] state or the updated state. Well the
[00:26:00] updated state we've already done we've
[00:26:02] just manipulated the state here. So all
[00:26:04] we have to do is just simply return the
[00:26:06] state. Cool. And yeah that runs without
[00:26:10] any errors. Okay. Now let's actually
[00:26:13] build the graph uh which is again
[00:26:16] obviously very important. So how do we
[00:26:18] build the graph? Remember here I said
[00:26:21] state graph is a framework that helps us
[00:26:23] design and manage the flow of tasks as a
[00:26:25] graph. Well that's exactly what we're
[00:26:27] about to do now. So hopefully it clicks
[00:26:29] now. So to create a graph in lang graph
[00:26:32] you use the state graph attribute and
[00:26:35] you pass in your state. You can see the
[00:26:38] state schema which VS code has uh asked
[00:26:40] for what uh the description of what the
[00:26:42] parameters are. So our state schema in
[00:26:45] this case is just the agent state which
[00:26:47] we define right. So we pass an agent
[00:26:49] state. I will actually also write here
[00:26:52] our state
[00:26:54] schema. So
[00:26:57] uh you can physically see what it is.
[00:26:59] Okay. And let's store this in a variable
[00:27:01] called graph or something. Okay. Now now
[00:27:07] here comes a very important method. How
[00:27:09] do we actually add a node to this graph?
[00:27:11] Cuz this graph is completely like
[00:27:13] nothing right now. So to add a node we
[00:27:16] use the inbuilt function graph add node
[00:27:18] and it requires two main parameters. Now
[00:27:22] what VS code is suggesting is a god I
[00:27:25] don't even know what that all of all of
[00:27:27] that is right it's very confusing. So to
[00:27:30] put things simply you require really two
[00:27:33] uh parameters the name of your node and
[00:27:36] what action it will perform. So let's go
[00:27:39] with the name. The name could be
[00:27:40] absolutely anything sensible of course.
[00:27:43] Um let's call something like
[00:27:45] greeter. Cool. And you can see VS Code
[00:27:49] has also asked us to um input an action.
[00:27:53] Now what's the action going to be? Well,
[00:27:55] the action will just be whatever your
[00:27:57] node will actually perform. And what
[00:28:00] action or mechanics will this node
[00:28:03] actually perform? Well, all of that is
[00:28:05] defined by this function, right? The
[00:28:07] greeting node function. So we simply
[00:28:09] just put that the name of the greeting
[00:28:12] node function here and that's it. We've
[00:28:14] successfully added the greeting node to
[00:28:18] our function to our graph and it will be
[00:28:21] named as
[00:28:22] greater. So remember this
[00:28:27] diagram in this diagram there is
[00:28:29] supposed to be a start and an end point.
[00:28:31] We've done the node which is sandwiched
[00:28:33] in between these but we haven't really
[00:28:35] added the start and the end point yet.
[00:28:37] So, how do we do that? Well, there's
[00:28:39] actually multiple ways to do that. In
[00:28:41] this subsection, in this graph, I'm
[00:28:43] going to teach you one way. Further down
[00:28:45] the line, I'll teach you another way.
[00:28:46] So, but they're both they're quite easy.
[00:28:49] So, you simply just call the inbuilt
[00:28:51] function set entry
[00:28:53] point and as the parameter is just one
[00:28:56] parameter which is the key. Now, the key
[00:28:59] is the name of your node which you want
[00:29:01] the start node to connect to. Again,
[00:29:04] visualize it. The start the start point
[00:29:06] is here and the node is here. Obviously
[00:29:09] you need to reference a node for it to
[00:29:11] create like an edge right. So we simply
[00:29:14] pass greater and similarly graph dot set
[00:29:17] finish point. We will again pass greater
[00:29:20] here as well. Why? Because imagine again
[00:29:24] the node is here and your finish point
[00:29:25] is here and you need to connect some
[00:29:27] sort of connection between these two
[00:29:28] right and that's why we use uh greater
[00:29:30] in this case. Don't worry, you will
[00:29:32] solidify this once you complete the
[00:29:34] exercises and as we go down building
[00:29:36] more graphs. All right. And one last
[00:29:39] thing which we need to do is actually
[00:29:40] compile this graph. So graph compile
[00:29:43] using the inbuilt uh graph using the
[00:29:45] inbuilt compile function. And let's just
[00:29:47] store this in a
[00:29:48] variable. Cool. So that run without any
[00:29:51] errors. But just a word of caution here.
[00:29:54] Just because the graph compiles without
[00:29:56] any error doesn't mean it will
[00:29:58] successfully run. I mean, God knows once
[00:30:00] we build like more complicated graphs,
[00:30:02] there could be so many logical errors.
[00:30:04] So, that's just an important thing to
[00:30:06] know. So, don't get too happy once it
[00:30:08] compiles cuz there might be logical
[00:30:11] errors. Trust me, I know. Okay.
[00:30:15] So, I want to write some code which will
[00:30:18] actually help you visualize this. And
[00:30:20] you can use the IPython library. So, you
[00:30:22] can use this uh this um piece of code
[00:30:26] here.
[00:30:27] This code is awfully familiar with the
[00:30:30] first ever graph I showed you, right? I
[00:30:33] I'll put a picture somewhere here for
[00:30:35] you to compare. The only difference is
[00:30:38] really the name of the node which we've
[00:30:39] set. In this case, it's greater. Why is
[00:30:41] it greater? Because that's the name we
[00:30:42] gave to this node, right? Cool. So
[00:30:47] that's looks pretty good. Let's actually
[00:30:50] run this. So to run you use the inbuilt
[00:30:54] method
[00:30:55] invoke. Um so let's pass in the message
[00:31:00] as something like Bob or something and
[00:31:04] let's actually store this result in a
[00:31:09] variable. Okay. Now how can we actually
[00:31:12] specify uh how can we actually get the
[00:31:15] value of result?
[00:31:19] So result we need to actually reference
[00:31:22] a certain attribute. Now the only
[00:31:24] attribute we have in uh the entire graph
[00:31:27] is message right. So we simply just put
[00:31:29] message and perfect you we get the final
[00:31:32] answer which is hey Bob how's your day
[00:31:34] going now why is it like this because
[00:31:36] this is exactly how we set our act how
[00:31:39] we set our function to be what action it
[00:31:41] performs it says hey then concatenates
[00:31:44] the uh input message in this case it's
[00:31:46] just the name and it says how's your day
[00:31:49] going now I could have changed this to
[00:31:51] absolutely anything else right uh what
[00:31:54] goes here like these functions are
[00:31:56] almost endless but That's the whole flow
[00:31:59] of how everything works. So hopefully
[00:32:03] you understood how to build this very
[00:32:06] first hello world graph. It's quite
[00:32:08] simple. But um don't worry if you didn't
[00:32:11] fully 100% understand this. I'm now
[00:32:14] going to show you what exercise you need
[00:32:15] to complete uh to be able to solidify
[00:32:18] this. All right. All right. I'll see you
[00:32:20] at the
[00:32:21] exercise. Okay. So time for your very
[00:32:24] first exercise. So the exercise for this
[00:32:27] graph is quite similar to what we just
[00:32:30] did, but I want you to create a
[00:32:32] personalized compliment agent. So you
[00:32:35] should pass in your name as like
[00:32:38] something like Bob or something and then
[00:32:40] output something like Bob, you're doing
[00:32:42] an amazing job learning langraph. And to
[00:32:44] give you a hint as to what you need to
[00:32:46] do again, you again have to concatenate
[00:32:48] the state, not replace it. All right,
[00:32:51] it's very similar to what we just did
[00:32:53] and it's quite basic. You should be able
[00:32:55] to do this, but um this is really just
[00:32:57] to get your hands dirty. All right.
[00:33:00] Okay. Once you've completed this
[00:33:01] exercise, join me when we build the
[00:33:03] second graph. I'll see you
[00:33:06] there. Okay. So now we're about to build
[00:33:09] our second graph as you can see here.
[00:33:12] And it's again quite similar to the
[00:33:15] first graph we built except now we're
[00:33:17] going to be able to pass multiple inputs
[00:33:19] as you can see here. So again, what are
[00:33:22] the objectives which you will be
[00:33:23] learning in this? Well, we're going to
[00:33:25] build a more complicated agent state.
[00:33:28] Uh, and we're going to be creating a
[00:33:30] processing node that performs operations
[00:33:32] on list data. So now we're about to see
[00:33:34] how we can really work with different
[00:33:36] data types apart from just string. And
[00:33:39] we're going to set up the entire graph
[00:33:41] that processes and outputs these and
[00:33:43] computes these results. And we're going
[00:33:45] to be able to invoke the graph with the
[00:33:47] structured inputs and retrieve the
[00:33:49] outputs. But the main goal which uh I
[00:33:53] want you to be able to learn in this
[00:33:54] specific subsection is really how to
[00:33:57] handle multiple inputs. All right. Okay.
[00:34:00] Let's code
[00:34:02] this. Okay. So now let's actually code
[00:34:05] the second graph up the second
[00:34:07] application up. So again I've just
[00:34:09] imported the same things again the type
[00:34:11] dictionary and the state graph. And I've
[00:34:13] also imported the list this time. But
[00:34:15] list is just a simple data structure
[00:34:16] which you should know already. So if you
[00:34:19] remember from the previous graph we made
[00:34:21] we are supposed to uh implement the
[00:34:24] state schema first right. So how do we
[00:34:26] do that? Again we use the class agent
[00:34:29] state uh type
[00:34:32] dictionary. Okay before I continue just
[00:34:35] a heads up I could have named the state
[00:34:37] schema anything I want. I could have
[00:34:39] named it uh something arbitrary
[00:34:41] completely like a bottle for example. In
[00:34:43] this case I've just said agent state
[00:34:45] because one that's how I learned it.
[00:34:47] It's like a habit for me now. But it
[00:34:49] also really tells you what it actually
[00:34:52] is. It's the state of your agent, right?
[00:34:54] So that's why I've just kept it like
[00:34:55] that. But again, just a heads up, you
[00:34:57] could have named this whatever you want.
[00:34:59] Cool. Okay. So now let's the if you
[00:35:02] remember the main goal for this graph
[00:35:04] for this uh building this graph was to
[00:35:07] be able to handle and process multiple
[00:35:09] different inputs, right? So how do we
[00:35:13] actually assign and I really do that?
[00:35:17] Well, the answer is in the state which
[00:35:19] is here's what uh which is what we're
[00:35:21] about to do now. So you really cuz
[00:35:24] remember this is just a type dictionary.
[00:35:26] So you basically have multiple keys now
[00:35:30] you uh create that. So let's say
[00:35:33] something like
[00:35:34] values list integers.
[00:35:37] So let's say one of our input is a list
[00:35:40] of integers and let's also pass in a
[00:35:43] name which will obviously be in a string
[00:35:46] and let's have the result in a string
[00:35:50] something completely random. But now you
[00:35:52] can see we're now operating on two
[00:35:54] different types of data structures uh a
[00:35:56] a list of integers and a string. And
[00:35:58] we're handling three different uh
[00:36:01] different uh uh inputs values name
[00:36:04] result. Okay cool. So let's run this.
[00:36:08] Perfect. So now let's actually build our
[00:36:10] node because in again in this uh graph
[00:36:14] we're just going to have a single node
[00:36:15] to keep things easy. Remember step by
[00:36:17] step. So let's call let's write dev
[00:36:20] process values and again what was what
[00:36:24] needs to be
[00:36:26] here? Yeah. So we need to pass in the
[00:36:29] state and we need to return the updated
[00:36:31] state. So how do we do that? Well, we
[00:36:33] write state agent state and we pass out
[00:36:37] the agent state. Cool. Now, again,
[00:36:41] building healthy habits. I know it's
[00:36:43] annoying. We have to write the dog
[00:36:46] string. So, let's just write something
[00:36:48] like this
[00:36:50] function process
[00:36:52] handles multiple
[00:36:55] different value in multiple different
[00:36:57] inputs. Cool. Again, I'm not being super
[00:37:00] specific here because one, uh, I don't
[00:37:03] want to spend too long on writing
[00:37:04] doctrines and everything, and two,
[00:37:06] there's no AI or LLM here, right? So
[00:37:08] that's why it doesn't really matter. I'm
[00:37:09] just doing this to build healthy habits.
[00:37:11] Okay, so now let's do something like
[00:37:14] whatever values we pass the list of
[00:37:16] integers. Let's sum them up. And let's
[00:37:19] also concatenate the name as well and
[00:37:21] store it in the result. Sound cool?
[00:37:24] Okay, so how do we do that? We pass in
[00:37:27] state result cuz that's what we are uh
[00:37:29] the action we're performing is on result
[00:37:32] uh the attribute result and let's say
[00:37:34] something like hi
[00:37:36] there and then we refer to the name
[00:37:41] um cool and your sum is equal to and
[00:37:45] let's just use the inbuilt Python
[00:37:46] function sum and we pass state
[00:37:51] values cool and lastly we obviously
[00:37:54] return the
[00:37:56] Okay, perfect. And that's that done.
[00:38:00] Okay, so now we actually create the
[00:38:03] graph. Again, this is going to be very
[00:38:05] very similar to what we did in the
[00:38:07] previous section because again there's
[00:38:10] just a node, there's a start point and
[00:38:11] an endpoint. So like last time, we use
[00:38:14] the state graph to initialize a graph
[00:38:16] and we pass in our state schema. So
[00:38:18] agent state and let's store this in the
[00:38:21] variable graph. Okay. Uh let's add our
[00:38:24] node. So graph add
[00:38:27] node and again remember it requires two
[00:38:30] parameters. It requires the name and the
[00:38:32] action. So in this case the name will be
[00:38:35] let's call it processor for example.
[00:38:37] Again this could be anything you want
[00:38:40] and your action will be performed by
[00:38:42] this function right process values. So
[00:38:44] we can just add that. Okay. Now I've
[00:38:48] already told you how to uh how to
[00:38:50] initialize a start point and an end
[00:38:52] point and this is just given by that
[00:38:54] code. So you attach your entry point to
[00:38:56] your node. In this case it's just one
[00:38:58] node which is the processor node and
[00:39:00] again same goes with finish and you
[00:39:02] compile it using
[00:39:05] graph.compile. Perfect. So take a moment
[00:39:08] now. How do you think this graph will
[00:39:10] look
[00:39:15] like? That again like I said very very
[00:39:18] similar on how the graph actually looks
[00:39:21] like but the only difference now is the
[00:39:24] name of the uh node which we've kept
[00:39:26] this as processor. Okay. So now let's
[00:39:30] actually test this. Let's actually
[00:39:31] invoke this graph. So how do we do that?
[00:39:34] Well, we use the invoke function. Now
[00:39:37] here's another important part which is
[00:39:39] quite a common mistake especially like I
[00:39:41] have done this many times. Make sure to
[00:39:44] store your compiled graph in a variable
[00:39:47] cuz if you invoke the graph i.e. if you
[00:39:50] write something like graph.invoke that
[00:39:52] won't make sense cuz you haven't
[00:39:54] compiled the graph. That's why you need
[00:39:56] to uh invoke using app. That's why I've
[00:40:00] also done app here. If I did graph get
[00:40:03] graph. Oh, it's completely messed up.
[00:40:05] Right? It says state graph object has no
[00:40:07] attribute because your graph hasn't been
[00:40:09] compiled yet. That's why when I do
[00:40:11] appget graph the uh process works. Cool.
[00:40:16] So now let's again store this in uh
[00:40:20] let's store something like answers is
[00:40:21] equal to app.invoke. Cool. Let's pass in
[00:40:25] some values. Let's say something like
[00:40:29] values and let's have a list of
[00:40:32] integers. 1 2 3 4. Again, I'm just
[00:40:35] trying to prove a point. I'm not trying
[00:40:36] to make a very complicated um graph yet.
[00:40:40] And let's pass the name as something
[00:40:42] like
[00:40:43] Steve something. Okay. Uh cool. And
[00:40:48] let's print let's print answers. Let's
[00:40:50] see what
[00:40:52] happens. Perfect. So now you can see
[00:40:55] your values is 1 2 3 4. Your name is
[00:40:58] Steve. And your result is Hi there
[00:41:00] Steve. Your sum is equal to 10. Again,
[00:41:03] why? because that's exactly what we uh
[00:41:05] asked the node the action to perform. Hi
[00:41:09] there, your name which in this case is
[00:41:10] Steve. Your sum is equal to the sum of
[00:41:12] the values and 1 + 2 + 3 + 4 is 10.
[00:41:16] Right? And that's how you get this
[00:41:18] answer. Now what if I wanted to just
[00:41:21] access result? I didn't want any of this
[00:41:24] other uh
[00:41:26] nonsense. Well to do that you can again
[00:41:29] just specify result and you will get it
[00:41:31] in a more clean manner.
[00:41:33] Cool. Okay. Now I want to try one more
[00:41:38] thing just to build your understanding a
[00:41:40] bit more. Uh let's put some print
[00:41:43] statements here. So let's have a print
[00:41:47] state
[00:41:49] here. Then we perform the action and
[00:41:51] then we print the state here. This is
[00:41:55] really just to show you how the state
[00:41:57] gets updated and it should be easy like
[00:42:00] interpretable cuz this is quite a basic
[00:42:02] piece of code. Again, print stated
[00:42:04] before the action and print state after.
[00:42:06] So there
[00:42:09] cool and here you go. So value is equal
[00:42:12] to 1 2 3 4 name is equal to Steve and
[00:42:15] these are the inputs we passed. Now
[00:42:17] notice I didn't pass results as an input
[00:42:19] as well. I could have uh done that but
[00:42:23] Langraph automatically sets that as like
[00:42:25] a a none value in this case if you don't
[00:42:27] pass an
[00:42:29] input. Now here's where you need to be
[00:42:33] cautious. If I had actually used state
[00:42:36] result here as well to uh update state
[00:42:39] result like I used state result to
[00:42:41] update either itself or something else
[00:42:44] then you would run into a problem
[00:42:46] because your state result has been
[00:42:47] initialized as none because you didn't
[00:42:49] pass it as an input. So be mindful of
[00:42:52] that. But in this case it worked because
[00:42:54] we're only assigning state result. We're
[00:42:56] not using it to assign something. It's
[00:42:59] getting assigned. Cool. And you can see
[00:43:03] after the action has been performed uh
[00:43:05] your operation has been performed and
[00:43:07] the thing has been concatenated. You can
[00:43:10] see result is here and that was exactly
[00:43:12] what we were getting before we cleaned
[00:43:14] this up. Cool. So hopefully you
[00:43:16] understood that. Again it should have
[00:43:18] been quite intuitive and interpretable
[00:43:20] but um to solidify your understanding
[00:43:22] even more complete the exercise. So I'll
[00:43:25] see you at the exercise
[00:43:27] then. Okay. Welcome to the exercise,
[00:43:30] your second ever exercise. And for this
[00:43:34] exercise, I want you to create a graph
[00:43:37] which passes in a single list of
[00:43:38] integers along with a name and uh an
[00:43:42] operation this time. And if the
[00:43:44] operation is a plus, you add the
[00:43:47] elements. And if a well times, you
[00:43:51] multiply all the elements all within the
[00:43:54] same node. So don't create an extra node
[00:43:56] yet. So for example your input should
[00:43:59] could be jack sparrow your values 1 2 3
[00:44:01] 4 again and then your operation uh uh
[00:44:04] multiplication and your output should be
[00:44:06] in the format of hi jack sparrow your
[00:44:08] answer is 24 so just to give you a hint
[00:44:11] as to how you would perform something
[00:44:13] like this uh you would need an if
[00:44:15] statement in your node so slightly more
[00:44:17] complicated but the whole concept is the
[00:44:19] same so once you've completed this
[00:44:22] exercise I will see you in when where we
[00:44:25] build this third graph All right, see
[00:44:27] you
[00:44:30] there. Okay, welcome to your third
[00:44:33] graph. So, what are we going to do this
[00:44:35] time? Well, enough processing multiple
[00:44:39] values and everything. Let's actually
[00:44:40] get the graph more complicated. So,
[00:44:42] that's why we're going to be building a
[00:44:44] sequential graph. So, all it all that
[00:44:48] basically means is we're going to be
[00:44:49] creating and handling multiple nodes
[00:44:51] that can sequentially process and update
[00:44:53] different parts of the state. So we will
[00:44:56] learn how to connect nodes together in a
[00:44:58] graph through edges of course and we're
[00:45:00] going to invoke the graph and really see
[00:45:02] how the state gets transformed as we uh
[00:45:05] progress through our graphs step by
[00:45:06] step. So again your main goal is should
[00:45:10] be to understand how to create and
[00:45:12] handle multiple nodes in langraph.
[00:45:15] Sounds cool. Okay I'll see you at the
[00:45:18] code. Cool. So now we're about to code
[00:45:22] up the third graph. Uh, and we're making
[00:45:25] quite fast progress. So well done on
[00:45:26] that. So again, the imports are the
[00:45:30] same. State graph and type
[00:45:32] dictionary. Perfect.
[00:45:35] And like we've done in the previous two
[00:45:37] graphs, we're going to be coding the uh
[00:45:40] the state schema or the agent state
[00:45:42] first. So let's have class agent state.
[00:45:46] And again, it needs to be in the form of
[00:45:48] a typed dictionary, right? And in this
[00:45:51] case, let's have the three attributes as
[00:45:53] all strings because we've already we
[00:45:55] already know how to handle multiple data
[00:45:56] types, right? So, let's keep it simple.
[00:45:59] Name string, age string, and final
[00:46:04] string.
[00:46:06] Okay. Now, here's what we're going to
[00:46:08] build. Now, we're about to build our two
[00:46:11] node functions,
[00:46:14] uh, which are again the actions. Okay.
[00:46:16] So again you simply write first well
[00:46:19] I'll name it first node in this case and
[00:46:22] like I mentioned before we pass in the
[00:46:26] state and we return the updated state.
[00:46:29] Okay. So again healthy habits doc string
[00:46:34] again. So this is the first node of our
[00:46:39] sequence. Okay. And what do we want to
[00:46:42] do in this specific node? Well, I really
[00:46:44] just want to manipulate uh the final
[00:46:48] part. So, let's say something like
[00:46:51] state final is equal to state or let's
[00:46:56] have an f string
[00:47:02] f state name.
[00:47:05] Let's say something like
[00:47:08] hi
[00:47:10] that. Cool. And we'll just return the
[00:47:13] state. Perfect. And now again we create
[00:47:16] a new node. So state agent state. Return
[00:47:21] that. Perfect.
[00:47:23] And I'm just going to copy this dock
[00:47:26] string and just change it. This is the
[00:47:27] second nerf. Perfect. Okay. To speed
[00:47:30] things up. And in this case I also want
[00:47:34] to have state final is equal
[00:47:39] to you are
[00:47:43] state
[00:47:46] age years old. Again quite a simple
[00:47:50] example easy to follow. That's why I've
[00:47:52] kept it as quite a basic graph. I mean
[00:47:55] it's not going to solve the world's
[00:47:56] problems or anything but it will help
[00:47:58] you understand.
[00:48:00] There is one logical error which I've
[00:48:04] put deliberately here. I want you to try
[00:48:07] to identify
[00:48:11] it. Okay. So the logical error in this
[00:48:15] case is the that once we've built our
[00:48:18] graph and everything what would have
[00:48:20] happened is we would have said hi to
[00:48:24] whoever uh we pass in let's say Charlie
[00:48:26] or something. So, hi Charlie. And we
[00:48:28] store that in the final uh attribute in
[00:48:31] the state, which is what we want. But
[00:48:33] here's where things get like start to be
[00:48:36] well logically incorrect. Once we
[00:48:39] finally get to our second node, again,
[00:48:40] we're updating state final, which you
[00:48:42] can do. You can repeat, you can um
[00:48:46] interact with these attributes at in in
[00:48:49] any node possible in all of the nodes.
[00:48:52] And you can do it as many times as you
[00:48:54] want. But notice this part. What's
[00:48:58] happening here is we've completely
[00:49:00] replaced all of the content we had
[00:49:01] before. So remember how we had hi
[00:49:03] Charlie? We've just completely replaced
[00:49:06] it with you are age years old. But we
[00:49:10] want both of them both of those stuff,
[00:49:12] right? So how do we get both of them?
[00:49:15] Well, again we just concatenate them. So
[00:49:17] we can have something like
[00:49:19] state
[00:49:21] plus state file. And there we go.
[00:49:25] Logical error should be now solved,
[00:49:27] right? Cuz now we have concatenated
[00:49:29] state final. Uh we're essentially just
[00:49:32] like adding on to uh we're preserving
[00:49:35] what we had before, right? Okay. Now
[00:49:38] let's get to the fun part. How do we
[00:49:41] actually build this graph? And really
[00:49:44] it's quite similar to the previous two
[00:49:46] graphs except there is one new thing
[00:49:48] which you're about to learn. So like
[00:49:51] always we use state graph to start the
[00:49:53] framework. So agent state and let's
[00:49:56] store it in
[00:49:57] graph. Again I could have had this name
[00:50:00] the width variable into anything. I've
[00:50:02] just kept it graph cuz it makes
[00:50:04] intuitive sense. Okay. Now we add our
[00:50:07] nodes. So we do graph add node. And for
[00:50:11] simplicity sake I'm just going to have
[00:50:13] the name as the same name as the uh
[00:50:16] function. Okay. So that way it'll just
[00:50:19] be easy to follow. So graph add
[00:50:24] node and second
[00:50:27] node. Second node. Cool. Okay. Now that
[00:50:32] we've added both nodes, we need to
[00:50:34] obviously s uh add the entry point and
[00:50:37] the end point, right? So we set the
[00:50:40] entry point like this. Again, quite
[00:50:42] self-explanatory because we wanted to
[00:50:43] connect to the first node, not the
[00:50:45] second node, right? So it should be
[00:50:47] start uh first node, second node, end
[00:50:51] point. How do we connect the first node
[00:50:54] and the second node together
[00:50:59] though? Hopefully you had an answer for
[00:51:01] that. Uh if you remember or recall from
[00:51:04] the previous section, theory section,
[00:51:06] there was an element in Langro called
[00:51:08] the edge. That's exactly what we're
[00:51:10] about to do right now. We're about to
[00:51:12] use edge and that was the new thing
[00:51:14] which I was talking about a few moments
[00:51:15] ago which you're about to learn. So how
[00:51:17] do we use it? Well you use graph edge
[00:51:20] add edge and if we can hi perfect. So
[00:51:25] again it's quite simple you use a start
[00:51:27] key and end key. So sim similar to entry
[00:51:30] point where but your in this case you
[00:51:33] need to pass two parameters. So the edge
[00:51:35] we want is between the first node and
[00:51:38] the second node right? Well that's
[00:51:40] exactly what we pass here. So first node
[00:51:42] and second node and like before we will
[00:51:48] just set the finish point at second node
[00:51:50] and we will compile this. Now how will
[00:51:53] this graph look like? Take a moment to
[00:51:56] try to think of how it will look
[00:52:02] like like that. Start point end point
[00:52:06] and these two notes are sandwiched in
[00:52:07] between. But now there is a
[00:52:10] edge. It should be called a directed
[00:52:12] edge if I'm being like quite picky. But
[00:52:15] yes, a directed edge cuz the flow of
[00:52:18] data or your flow of your state updates
[00:52:20] is from the first node to your second
[00:52:22] node. Right? Cool. So now that we've
[00:52:24] built that, let's again invoke this. So
[00:52:27] I've got this code ready here. Uh let's
[00:52:30] invoke it. Let's pass the parameter as
[00:52:33] Charlie and let's pass the age as 20.
[00:52:37] Cool. Print
[00:52:39] result. Perfect. Apart from the uh
[00:52:43] misalignment here which I can just
[00:52:44] change right
[00:52:47] now. Perfect. Okay. So now you can see
[00:52:49] it says hi Charlie you are 20 years old.
[00:52:52] Now obviously we could have performed
[00:52:54] all of this in one single node which we
[00:52:56] have been doing in the previous
[00:52:58] subsection but the obviously the aim was
[00:53:00] to be able to create multiple nodes
[00:53:03] right and handle um the state how the
[00:53:05] state progresses. So yes you one
[00:53:08] important thing which you've learned is
[00:53:09] obviously how to use the add edge method
[00:53:13] but another concept which you have
[00:53:15] solidified here is you can uh change
[00:53:18] these at these keys of your state at in
[00:53:22] at any point in time like as long as as
[00:53:27] however many times you want cuz remember
[00:53:29] here we've passed in state final um we
[00:53:32] implemented state final here we
[00:53:34] implemented state final in the second
[00:53:35] node if we had more nodes in the
[00:53:37] sequence. We could have done that again
[00:53:38] and again and again. And we also learned
[00:53:41] how to like one key logical error is
[00:53:43] sometimes a lot of people just
[00:53:45] accidentally replace uh their content in
[00:53:48] one of the attributes and that leads to
[00:53:50] a lot of logical errors. So always be
[00:53:52] mindful of that. And yeah, that again
[00:53:55] was quite simple, not too hard and
[00:53:58] hopefully the exercise which I'm about
[00:54:00] to give you solidifies this. Cool. So I
[00:54:03] will see you at the exercise then.
[00:54:06] Awesome. So now we will move on to the
[00:54:09] exercise for this third graph. And what
[00:54:12] I want you to do is really build on top
[00:54:15] of what we just covered. Instead of two
[00:54:18] nodes, I want you to build three nodes.
[00:54:20] Again, in a sequence, don't need to go
[00:54:22] too fancy yet. We will again three nodes
[00:54:25] in a sequence. And we will have you will
[00:54:29] need to accept the user's name, their
[00:54:30] age, and a list of their skills. So the
[00:54:33] first node will be specifically for
[00:54:35] personalizing the name field with a
[00:54:37] greeting. The second node will be
[00:54:39] describing the user's age. The third
[00:54:42] node will be listing all of the user
[00:54:44] skill in a formatted string. And then
[00:54:46] you'll need to combine this and uh store
[00:54:49] it in a result field and output that.
[00:54:51] And this should be a combined message.
[00:54:53] And the format I would like you to
[00:54:55] output is something like this. So let's
[00:54:57] say the name was Linda. And let's say
[00:54:59] Linda welcome to the system. You are 31
[00:55:03] years old and you have skills in Python,
[00:55:06] machine learning and langraph. Okay. And
[00:55:09] just as a hint for this exercise, I
[00:55:12] would you'll need to use the add edge
[00:55:14] method twice. So this will really
[00:55:16] solidify your understanding on how to
[00:55:19] build graphs in general. All right,
[00:55:22] cool. So once you've done that, again,
[00:55:24] answers will be on GitHub for all of the
[00:55:26] exercises. Once you have uh cross
[00:55:28] referenced and checked that you've done
[00:55:30] it right, I will see you in the next
[00:55:32] section where we build our fourth graph.
[00:55:34] All right, see you
[00:55:36] there. Welcome, welcome, welcome. Okay,
[00:55:39] I'm particularly excited for uh teaching
[00:55:41] you this graph, graph 4. Why? Because
[00:55:44] we're about to learn how to build a
[00:55:46] conditional graph. So for the very first
[00:55:49] time, we're about to implement
[00:55:51] conditional logic. And obviously we've
[00:55:54] done it in a previous exercise before
[00:55:56] but that was within a single node. This
[00:55:58] is how to implement conditional logic in
[00:56:00] the overall graph structure. And so we
[00:56:03] will be implementing conditional logic
[00:56:04] to route the uh flow of data to
[00:56:07] different nodes. We will be using the
[00:56:09] start and the end nodes to manage entry
[00:56:11] and exit points. We will be designing
[00:56:14] again using multiple nodes to perform
[00:56:16] different operations such as addition
[00:56:18] and subtraction. And we will be able to
[00:56:20] create a router node to handle
[00:56:22] decision-m and control the graph flow.
[00:56:25] So the main goal is really to you how we
[00:56:28] can use this inbuilt function which uh
[00:56:30] allows you to create conditional edges
[00:56:32] in langraph. All right, exciting stuff.
[00:56:35] I'll see you at the
[00:56:38] code. Okay, so let's actually code this
[00:56:41] up now and you'll see the imports are
[00:56:44] slightly modified this time. Again, type
[00:56:47] dictionary and state graph is there. But
[00:56:49] now I've also imported start and end
[00:56:51] point. Again, if you remember a few
[00:56:54] subsections ago, I told you there are
[00:56:56] multiple ways to be able to initialize
[00:56:58] the start and the end point. And this is
[00:56:59] another way you could. Arguably, this is
[00:57:02] the easier way, but um whatever. I don't
[00:57:06] really have a preference, but I'll teach
[00:57:07] you both ways regardless. Okay, let's
[00:57:10] import these. Successful. Okay. like
[00:57:13] standard procedure we will design we
[00:57:15] will um code up the uh the schema the
[00:57:19] state schema so class agent state and
[00:57:22] let's again type dictionary in this case
[00:57:27] uh uh I want to be able to pass in two
[00:57:30] numbers and pass in an operation so a
[00:57:33] plus operation and a minus operation one
[00:57:35] of those two operations now obviously I
[00:57:38] could have handled uh all of this within
[00:57:40] one single node But that's not the point
[00:57:43] here. I've kept it deliberately very
[00:57:45] very simple. So the main concept which
[00:57:48] you learn is how to uh implement
[00:57:50] conditional logic. Okay.
[00:57:53] So let's code the different uh keys
[00:57:56] which we require. So number one will be
[00:57:58] an integer. Operation will be in the
[00:58:01] string a plus or a minus. Uh number two
[00:58:05] will be an integer and final number will
[00:58:08] be an integer. the final number will be
[00:58:09] the result of either adding or
[00:58:11] subtracting the two
[00:58:13] numbers. Easy enough. We've done this
[00:58:15] multiple times now. Okay. Now, here's
[00:58:18] where things get interesting. Now, just
[00:58:21] a heads up. Initially, this won't make
[00:58:24] sense. But when we look at it from a
[00:58:27] bird's eye view and we look back at all
[00:58:29] the code in this subsection again, uh
[00:58:32] everything will start to click. So
[00:58:34] again, it won't make sense initially,
[00:58:36] but it will once we look at it. Uh
[00:58:38] again, don't worry. All right. So let's
[00:58:40] create our first node function. Let's
[00:58:42] call it adder. And it's again still a
[00:58:46] node. And we input the state schema. And
[00:58:49] we return the updated state schema and
[00:58:53] dock string again. But uh this time I'm
[00:58:55] just going to copy it from here. Uh it's
[00:58:59] tells exactly what it does. This node
[00:59:01] adds the two numbers. Uh and easy
[00:59:04] enough, we just do state final number is
[00:59:06] equal to state uh number one plus
[00:59:11] state number two. Okay. And we just
[00:59:14] return the
[00:59:16] state. Quite simple, right? And just
[00:59:20] like what we did with the addition, we
[00:59:22] need a node for subtraction as well. So
[00:59:25] def subtractor. Now uh I already
[00:59:29] implemented it to uh don't to not waste
[00:59:31] time but this node subtracts the two
[00:59:34] numbers. It's very similar to the
[00:59:36] previous uh node function. Uh it just
[00:59:39] subtracts these two numbers. Again yes
[00:59:42] you could be saying what if number one
[00:59:44] is uh smaller than number two it'll give
[00:59:46] you a negative result. It that doesn't
[00:59:48] matter. The main aim again was to
[00:59:51] implement the conditional logic not the
[00:59:53] um inner workings of each node. Okay.
[00:59:57] Okay. Now we built another type of node.
[01:00:00] Uh and we initialize it the same way but
[01:00:02] this time let's call this node decide
[01:00:06] next node. Let's actually give it a name
[01:00:08] which actually says what it does. Right.
[01:00:11] So again we use state agent state and we
[01:00:15] pass like this. Perfect. Okay. Now the
[01:00:19] dock string will be something like so.
[01:00:23] So this node will select the next phase
[01:00:25] of the graph or well next node of the
[01:00:27] graph I should say.
[01:00:30] Okay. Now we use an if statement and
[01:00:33] before I code something let's just try
[01:00:36] to map how this will work. This specific
[01:00:39] node will be at the start of our uh
[01:00:41] graph. So we will have the start node.
[01:00:43] We will have this uh this specific node
[01:00:46] we'll call it the router. and this
[01:00:48] router because it routes uh the next uh
[01:00:52] to the next node depending on what the
[01:00:54] state schema is at that point. So we
[01:00:56] will have the uh I will put an image up
[01:01:00] right now so you kind of get what I'm
[01:01:01] trying to say but we essentially will
[01:01:05] have the router decide whether we uh add
[01:01:08] the two numbers and subtract the two
[01:01:09] numbers and obviously this will be
[01:01:11] decided with the operation uh attribute
[01:01:14] right which you should see from here.
[01:01:16] Okay, let's code this up now. So this is
[01:01:20] not the hard part. If state operation,
[01:01:24] if I can spell if state operation is
[01:01:28] equal to equal to
[01:01:31] plus. Okay, if state operation is equal
[01:01:34] to equal to
[01:01:35] plus, we need to do a certain thing to
[01:01:38] pass it to the next node. Okay, now
[01:01:42] here's well your first guess could be
[01:01:45] okay. Well, we guess I guess just call
[01:01:47] this function, right? Not exactly. Not
[01:01:50] in langraph. You actually return
[01:01:54] uh return the edge. Now, we haven't
[01:01:57] described the edge yet, right? But for
[01:02:00] now, I will just say the edg's name is
[01:02:02] addition operation. So, addition
[01:02:05] operation. Similarly, if it's
[01:02:07] subtraction, we will do this like so. So
[01:02:11] just to reiterate we will uh you we will
[01:02:15] see what the um value is at the
[01:02:18] operation in the state schema. If it's a
[01:02:20] plus we call we will return the edge
[01:02:23] addition operation and if it's a
[01:02:25] subtraction we will use the subtraction
[01:02:28] operation edge. Again we haven't
[01:02:30] described or defined these two edges
[01:02:32] yet. That's what I was saying earlier.
[01:02:34] When we look at it from the bird's eye
[01:02:36] view later on in a few moments once
[01:02:37] we've built everything it will make much
[01:02:40] more sense. So stick with me for now.
[01:02:42] Okay. And runs perfect. Now we build the
[01:02:47] graph. And now here's the exciting part.
[01:02:50] So we again like normal standard
[01:02:53] procedure we use state graph to create
[01:02:56] the graph framework. So graph is equal
[01:02:58] to
[01:02:59] that. And let's add these nodes uh to
[01:03:02] the
[01:03:05] uh to our graph. So graph add
[01:03:08] node and let's say
[01:03:11] router. Okay. And again we will pass
[01:03:15] this decide next node. Perfect.
[01:03:21] Okay. Now I have another confession to
[01:03:23] make. Lots of conventions. I know this
[01:03:26] won't work. I know I haven't built the
[01:03:29] rest of the graph yet but this
[01:03:30] eventually will not work. And there is a
[01:03:34] subtle reason why this won't work. You
[01:03:37] know, it's mainly in this line. Add node
[01:03:40] router decide next node. The problem is
[01:03:44] with decide next node cuz oh, you can
[01:03:47] see that the dock string appears once we
[01:03:50] press uh the decide next node. But the
[01:03:52] reason this won't work is look closely
[01:03:54] at these three functions. What are we
[01:03:57] doing in these two functions that we're
[01:03:59] not doing in this?
[01:04:01] I'll give you a moment to try to analyze
[01:04:10] this. Okay. So, doesn't matter if don't
[01:04:14] worry if you didn't get that. The
[01:04:16] correct answer is we are returning this
[01:04:19] updated state in this one and this one.
[01:04:21] But in this node, we're not. We're just
[01:04:25] returning the edge. Subtle difference I
[01:04:28] know but that's how Lang graph works and
[01:04:31] you will see why they do it like that
[01:04:35] uh right now. So how do we deal with
[01:04:37] this? Now I obviously could have built
[01:04:39] this graph and then I would have shown
[01:04:41] you the error but then things would have
[01:04:43] just gotten messy. That's why from the
[01:04:44] get- go I have told you why this
[01:04:45] wouldn't work. So now that you know why
[01:04:48] this won't work, how do you fix this?
[01:04:51] Simple. You use this code lambda
[01:04:54] state. Now, if you have used lambda
[01:04:57] functions before, this is quite easy to
[01:04:58] understand. If you haven't, don't worry.
[01:05:00] All this is saying is your input state
[01:05:03] will be your output state. That's it. In
[01:05:07] even more simpler words, think of this
[01:05:09] as a pass through
[01:05:11] function. So, what it's saying is your
[01:05:14] input state will be passed, your state
[01:05:17] will be inputed and your output will be
[01:05:21] the exact same state. Now, why is it the
[01:05:23] exact same state? because you're not
[01:05:25] changing the state at all. You're
[01:05:28] comparing stuff here, but you're not
[01:05:30] assigning anything. There's a difference
[01:05:32] between comparison and um and
[01:05:34] assignment. Right? Again, even in this
[01:05:37] one, you're just comparing to see
[01:05:39] whether the operation is a minus, but no
[01:05:41] assignments been made at all. In fact,
[01:05:44] there's been no changes to this state
[01:05:47] whatsoever. That's why we can use this
[01:05:49] as a pass through
[01:05:51] function. Now, hopefully that made
[01:05:53] sense.
[01:05:54] Okay, let's continue. Again, we will get
[01:05:58] a lot more practice. Don't worry, this
[01:05:59] is the first time you're seeing this.
[01:06:02] Okay, so now we will add the edge. And
[01:06:05] this is just the normal edge we did last
[01:06:06] time. So, we will need the start key.
[01:06:09] And now here's how you initialize
[01:06:11] differently. Remember how we used to do
[01:06:13] set entry point and set finish point? We
[01:06:16] don't do that anymore. Uh we use start
[01:06:19] the keyword cuz that's what we imported.
[01:06:21] Make sure to import it if you do it this
[01:06:23] way. uh you use start and end. So your
[01:06:26] start will be a start point and your
[01:06:29] what do you want the start to be
[01:06:30] connected to? Well, we want it to be
[01:06:32] connected to the
[01:06:33] router. If I put this in quotation
[01:06:36] marks, perfect. Now, why not add node or
[01:06:38] subtract node? Well, think again. Refer
[01:06:41] back to that diagram which I'll show in
[01:06:43] right here.
[01:06:46] We if we connected the start point to
[01:06:48] the the add node or the subtract node,
[01:06:50] well then what's the point of the router
[01:06:52] in the first place, right? The whole
[01:06:54] point was the router decides what the
[01:06:56] inputs are and then from there it
[01:06:59] branches off to the correct node. So
[01:07:01] that's why the router needs to be the
[01:07:02] first node we uh connect our start point
[01:07:04] to. Cool.
[01:07:07] Okay. Perfect. Now we add the we now
[01:07:12] implement the main the new thing which
[01:07:14] we are going to learn in this section is
[01:07:17] graph dot add conditional edge. So graph
[01:07:21] dot add conditional
[01:07:22] edges. Now again wow looks really
[01:07:26] confusing but it's actually much more
[01:07:28] simpler than it looks
[01:07:30] like. So the first uh part is your
[01:07:33] source which you can see here as well.
[01:07:36] So the source will just simply be the
[01:07:38] name of the node. And what's the name of
[01:07:40] the node which we want the conditional
[01:07:42] edge to be? It's the router node, right?
[01:07:44] So that's going to be the source part.
[01:07:47] Perfect. Now if you look here, it's
[01:07:49] asking for a path. What's the path you
[01:07:51] would like it to do? Now before we
[01:07:54] implement the path, we obviously need to
[01:07:56] per uh imple uh tell it what action what
[01:07:59] what action it needs to do. And that's
[01:08:01] where this node will come in the decide
[01:08:02] next node part. So we pass that as the
[01:08:04] second parameter. So that's the
[01:08:07] path. And now we implement something
[01:08:10] called the path map which you should
[01:08:12] have briefly saw
[01:08:15] here. Uh there path map. So we've
[01:08:20] implemented the source which is the
[01:08:21] router. We've implemented the path which
[01:08:24] is your uh decide next node function. Uh
[01:08:27] again don't need to worry about hashable
[01:08:29] runnable any and all of this stuff.
[01:08:31] Okay, it's you don't need to over
[01:08:33] complicate it. Now it's time for the
[01:08:35] path map. Okay, so now your path map
[01:08:37] will be in a form of a dictionary. And
[01:08:40] remember how I said earlier that we had
[01:08:42] implemented addition operation and
[01:08:44] subtraction operation. These were edges.
[01:08:46] So now we're about to implement those
[01:08:48] only. So we're about to create two new
[01:08:52] edges here. Let me just write this code
[01:08:55] up for you and then it will make sense.
[01:08:57] Give me one second.
[01:09:01] Okay, so there we go. Now what is this
[01:09:05] code actually saying? Well, this is in a
[01:09:07] format of
[01:09:10] edge and
[01:09:12] node. Now the starting point of this
[01:09:14] edge will obviously be this router node
[01:09:17] and it's telling us where it will
[01:09:18] connect to. This uh visualization will
[01:09:22] be it will be it'll be much easier to
[01:09:24] visualize when I actually show you the
[01:09:25] graph. Don't worry. But for now,
[01:09:27] addition operation and subtraction
[01:09:28] operation is the edge. And the two nodes
[01:09:31] are add node and subtract node. Right?
[01:09:34] Okay. Uh lastly, we now we're now at the
[01:09:38] point where we need to create the end
[01:09:40] point. But obviously, we if you look
[01:09:43] back at this diagram which I've shown on
[01:09:44] the screen right now, you can see that
[01:09:48] the we need two edges to connect to the
[01:09:51] end point, right? We need to we need an
[01:09:53] edge from the and node and we need an
[01:09:55] edge from the subtract node. So we can
[01:09:58] add two edges like this. graph
[01:10:02] edge. Uh we uh start at the add node and
[01:10:05] then we end at the endpoint. Again
[01:10:07] similar subtract node and endpoint. And
[01:10:10] then we just compile this. So app is
[01:10:11] equal to
[01:10:15] graph.compile. Cool. No errors. Okay.
[01:10:18] Now here comes the most exciting part.
[01:10:21] Again try to visualize what this graph
[01:10:23] will actually look
[01:10:26] like. Okay. So it should look something
[01:10:29] like
[01:10:31] that. Probably slightly different to
[01:10:34] what you initially anticipated but
[01:10:36] that's okay. We again have a start
[01:10:37] point. We have the router and we have
[01:10:40] the our two nodes add node subtract
[01:10:42] node. And notice remember when I said
[01:10:45] addition operation and subtraction
[01:10:46] operation are the edges names. Well,
[01:10:48] here it is. Addition operation and
[01:10:50] subtraction operation. It's telling us
[01:10:53] uh what the which direction to go into.
[01:10:55] Do we go how do we go to add node? Well,
[01:10:58] we use the addition operation. How do we
[01:11:00] go to subtract node? Well, we go to the
[01:11:01] subtract operation. And then obviously
[01:11:04] we create these two
[01:11:06] edges, these two to connect to the
[01:11:10] endpoint. Awesome. So, we will once
[01:11:12] again look at it from a bird's eye view.
[01:11:14] But let's actually invoke this graph to
[01:11:16] see what happens.
[01:11:19] So let's use this piece of code. So what
[01:11:23] it's saying is it's defining number one
[01:11:25] as 10, operation as minus and number two
[01:11:27] as five. So because we've used
[01:11:30] subtraction, the final number should be
[01:11:32] 10 - 5 which is five. And we've printed
[01:11:36] the results and the answer is like such.
[01:11:39] Uh number one is equal to 10, operation
[01:11:41] is equal to minus, number two is equal
[01:11:43] to 5 and final number is uh five.
[01:11:45] Obviously the way I've invoked it is
[01:11:47] slightly different to what I have done
[01:11:49] before. Again, this is another way you
[01:11:51] can
[01:11:51] invoke. Okay, so not too hard. But let's
[01:11:56] just go through everything one more time
[01:11:58] to solidify everything. Okay, so we
[01:12:02] imported everything. We created the
[01:12:03] state schema using agent state and a
[01:12:05] type dictionary. Then we created our
[01:12:07] three different nodes which is the add
[01:12:09] node, subtract node and the decide next
[01:12:11] node. And this is in within the decide
[01:12:15] next node. You can see that if the
[01:12:17] operation is a plus, it goes to the
[01:12:19] addition operation edge which is this
[01:12:22] edge. And if it's subtraction operation,
[01:12:24] it goes to this side. And this is how we
[01:12:28] built the graph. We added the nodes. We
[01:12:30] added the edge from the start point uh
[01:12:32] to the router. And then we added the
[01:12:34] conditional edge. the new thing which
[01:12:35] we've learned in this section uh which
[01:12:37] is we uh reference router and we use the
[01:12:40] edge node format. So the edge will be
[01:12:43] addition operation uh to add node then
[01:12:47] it will be subtraction operation to
[01:12:49] subtract node. Visually speaking it will
[01:12:51] be addition operation to add node
[01:12:53] subtraction operation to subtract node.
[01:12:55] Now, I know this will be quite confusing
[01:12:57] at first and don't worry, it took me
[01:12:59] quite a while to understand this myself
[01:13:01] as well, but hopefully the exercise I've
[01:13:03] given you will really be able to help
[01:13:05] you understand this much better. Okay,
[01:13:08] so I will see you at the exercise
[01:13:11] then. Awesome. So, let's actually find
[01:13:13] out what the exercise is for this graph.
[01:13:16] So, you need to make this monstrosity.
[01:13:20] Now at first glance it looks terrifying
[01:13:22] but if you analyze it a little bit
[01:13:24] closer all it is is what we just coded
[01:13:27] twice. So we coded this and we need to
[01:13:30] replicate it once more. So in essence
[01:13:33] you need to actually input four numbers
[01:13:34] and two operations and you need to
[01:13:36] output their final results. For example
[01:13:39] number one, number two, number three,
[01:13:40] number four and the respective operation
[01:13:42] and the respective results. Right? So in
[01:13:44] this case we would have to do 10 - 5
[01:13:47] which is 5 and 7 + 7 + 2 aka 9 and those
[01:13:51] two numbers should be outputed. Now the
[01:13:53] reason I gave you this exercise to do is
[01:13:56] because this will really solidify your
[01:13:57] understanding about conditional edges
[01:14:00] which will really be important for the
[01:14:02] next few next graph and the next AI
[01:14:04] agents we make. Okay. So once you have
[01:14:07] uh completed it by looking and cross
[01:14:09] referencing the answer on GitHub, I will
[01:14:12] see you in the next graph.
[01:14:15] Okay. All right. Well done. We're almost
[01:14:18] at the end of this section and we're
[01:14:20] about to build our final graph aka graph
[01:14:22] 5. Now we've learned quite a lot about
[01:14:25] Langraph and its internal mechanisms.
[01:14:27] And this will really help us in the next
[01:14:29] section where we finally build the AI
[01:14:31] agents you were looking for. Now in this
[01:14:34] section in this subsection sorry we're
[01:14:36] going to be learning an important
[01:14:37] concept. There's still one more concept
[01:14:39] we haven't learned and that's about
[01:14:40] looping. So we're going to be creating
[01:14:42] well a simple looping graph. Now I kept
[01:14:45] the objectives to be quite small here.
[01:14:48] There aren't that many objectives. It's
[01:14:50] essentially implementing logic uh which
[01:14:52] involves looping uh to route the flow of
[01:14:54] data back to the nodes. And we're going
[01:14:56] to be creating a single conditional edge
[01:14:58] which you know how to do in the previous
[01:15:00] section. Regarding the previous section,
[01:15:02] however, I know the exercise. Please do
[01:15:05] complete that exercise. That exercise
[01:15:07] will be probably the hardest exercise
[01:15:10] you would have done until this point.
[01:15:12] So, don't worry if you didn't get it. If
[01:15:14] you did, great job. You're doing really,
[01:15:16] really well. But if you didn't get it,
[01:15:18] look at the GitHub. Try to compare where
[01:15:20] you went wrong. Remember, in Langraph,
[01:15:23] there's more than one way of building
[01:15:24] the graphs. Make sure the graphs are
[01:15:27] well built and it actually functions.
[01:15:29] And if you want an extension, try to
[01:15:31] make it even more robust than it is. All
[01:15:33] right, but back to this now. Final
[01:15:35] graph, I promise. The main goal really
[01:15:38] is to code up the looping logic. So,
[01:15:40] with that out of the way, let's build a
[01:15:42] final code for this section. See you
[01:15:46] there. Awesome. So, final code we have
[01:15:49] to build for this section. And here we
[01:15:52] go. So, graph 5 squ. Now, I'm going to
[01:15:55] take a slightly different approach this
[01:15:56] time. And I'm actually going to show you
[01:15:58] the graph we want to end up building
[01:16:00] from the get- go. And there's a reason
[01:16:02] I'm going to start that from now so we
[01:16:04] get in good practice. The reason is once
[01:16:07] you finish this course and actually
[01:16:09] start either making your own AI agentic
[01:16:12] systems for someone else, for your
[01:16:13] clients or for yourself like make your
[01:16:15] own JavaS system or whatever. You
[01:16:18] obviously need to plan how it works,
[01:16:20] right? You need to see okay, what nodes
[01:16:22] do I need? What edges do I need? Does is
[01:16:24] this does this need to be a conditional
[01:16:25] edge? where's the start point going to
[01:16:26] go, end point going to go etc etc and
[01:16:29] you can either do that via pen and paper
[01:16:31] or software like I've used but point is
[01:16:34] you need some sort of blueprint and
[01:16:38] that's how really it works in the
[01:16:39] industry as well um you can you will
[01:16:42] obviously have a blueprint and then from
[01:16:44] there you will code up the graph similar
[01:16:46] to how a UI designer for example uh
[01:16:49] renders um their UI designs and then
[01:16:52] sends that off to a software developer
[01:16:55] who uh well develops the application
[01:16:57] forwards. Right? So that's the habit I
[01:17:00] want to start uh creating with you. All
[01:17:03] right. So this is the graph I want to
[01:17:07] build in this section. So there's
[01:17:09] obviously going to be a start and end
[01:17:10] point. And this really should be mostly
[01:17:13] familiar except for this loop. So there
[01:17:15] we're going to create a simple greeting
[01:17:16] node and another node which is called
[01:17:18] the random node. So in the greeting note
[01:17:21] I essentially want the user to have uh
[01:17:24] stated their name and it should output a
[01:17:27] simple hi there your name and then the
[01:17:31] graph progresses to the random node and
[01:17:33] in the random node I essentially want to
[01:17:36] generate five random numbers. Okay, now
[01:17:40] just as a heads up, yes, this graph in
[01:17:44] industry would be completely useless. I
[01:17:46] know, but I've deliberately kept it
[01:17:48] simple again so you know the
[01:17:49] fundamentals. Like this loop is could
[01:17:53] have easily been avoided and transferred
[01:17:55] into a for loop for example, right? Like
[01:17:57] I could have had a for loop within this
[01:17:59] node and ran it five times to generate
[01:18:02] the numbers. I get it. But this is again
[01:18:04] kept deliberately simple so you actually
[01:18:06] understand the concept. Okay, cool. So
[01:18:09] let's the usual inputs and the only
[01:18:11] difference is this time I've also
[01:18:13] imported random but if you have used
[01:18:15] Python before quite a lot you would have
[01:18:17] come across this library right okay so
[01:18:20] let's start with our agent state so
[01:18:23] class agent state type
[01:18:26] dictionary and what's the first thing
[01:18:29] we're going to need well let's see we
[01:18:31] have the start point do we need anything
[01:18:33] any keys that no for greeting note what
[01:18:36] did I say I want uh I wanted the user to
[01:18:38] be able to input their name. So, we need
[01:18:41] a name attribute or a key. And then for
[01:18:43] the random number, a random node, we
[01:18:47] need some form of um a list to like
[01:18:51] actually store the numbers. So, we have
[01:18:53] number and list
[01:18:56] int. Okay, cool. And one more thing,
[01:19:00] look at this loop. How will we actually
[01:19:02] know when to stop? We need some form of
[01:19:04] counter, right? So, counter int.
[01:19:08] Perfect. Now, obviously, just as a heads
[01:19:11] up, when you do go on to make your AI
[01:19:13] agents and everything, you're not going
[01:19:15] to know what attributes you need right
[01:19:17] from the get- go, unless if you planned
[01:19:19] it like extremely extremely well. But
[01:19:22] chances are you won't get it. But don't
[01:19:25] worry, iteratively well, you'll
[01:19:27] obviously be better at speculating what
[01:19:29] attributes you need through practice.
[01:19:31] But you can obviously do iterative
[01:19:32] development as well, right? Okay, cool.
[01:19:35] So now let's actually build these
[01:19:37] nodes. Okay. So let's start off with the
[01:19:40] uh greeting node. So how we normally
[01:19:43] define uh a function. So def greeting
[01:19:46] node, we obviously need the agent
[01:19:49] states like such. Perfect. And the dock
[01:19:55] string. But uh luckily for me, I've
[01:19:57] already got that here. So I don't need
[01:19:58] to do it again. I know it's boring, but
[01:20:01] habits. Now let's update update the uh
[01:20:06] name uh key. So how do we do that? Well,
[01:20:10] you should know by now state name is
[01:20:12] equal
[01:20:13] to let's say something like hi
[01:20:16] there. State name.
[01:20:19] Perfect. So what will this do? I input a
[01:20:22] name and it'll replace that name with a
[01:20:23] string of hi there this person. Now
[01:20:27] let's also initialize the counter
[01:20:29] variable here. Now why am I doing that?
[01:20:32] Let me just first write it and think
[01:20:34] about this.
[01:20:36] Okay. Now, obviously I'm changing I'm
[01:20:40] setting like the value. So, I will need
[01:20:41] to have passed in like an valid integer
[01:20:45] when I am passing the uh value when I'm
[01:20:49] invoking the graph, right? But here's
[01:20:52] the thing. What if I pass in minus2 for
[01:20:54] example?
[01:20:56] Well, as the counter value, as the
[01:20:58] initial counter value, if this line
[01:21:00] wasn't there, well, it would have just
[01:21:02] kept on incrementing until it got got to
[01:21:05] five cuz I want to have five numbers.
[01:21:07] But if it starts at minus2, well, it
[01:21:09] would end up giving me seven numbers.
[01:21:12] Now, that's not robust, right? So, this
[01:21:15] basically wipes out whatever rubbish
[01:21:18] integer the user even inputs. If they
[01:21:20] had put zero, well, okay, we replaced it
[01:21:22] to zero. If they put like minus 20
[01:21:25] because they're greedy or something,
[01:21:27] then we have made sure to like set that
[01:21:29] back to zero. So, so just a way to make
[01:21:31] it robust. That's all. Uh, return state.
[01:21:36] Okay, cool. So, now let's create our
[01:21:38] second node which is a random node. So,
[01:21:41] we can say random node state agent state
[01:21:46] agent state. Perfect. Dog string.
[01:21:49] Again the dog strings will be useful. I
[01:21:52] promise in the next section they will.
[01:21:55] So this generates a number random number
[01:21:57] from 0 to 10. Now this piece of code
[01:22:01] here
[01:22:03] essentially appends the appends the
[01:22:06] randomly generated number to the number
[01:22:09] list. Okay, that's all it does. And what
[01:22:11] else do we need to do in this node?
[01:22:13] Well, we need to increment the counter
[01:22:15] value, right?
[01:22:18] So C uh plus equals to one. So this will
[01:22:22] increment uh the value by one and then
[01:22:24] we just return the
[01:22:25] state. Okay, cool. Now here's where
[01:22:31] we're how we're going to implement the
[01:22:32] looping logic. Now just a warning here
[01:22:34] and please listen to this. Like in any
[01:22:37] software development uh program or
[01:22:40] programming language G2, there's more
[01:22:42] than one way of coding up an
[01:22:44] application, right? Same goes with
[01:22:46] Langraph as well. There is multiple
[01:22:47] multiple different ways of coding like a
[01:22:50] looping code like this graph. I'm going
[01:22:52] to be showing you one of them. I
[01:22:54] obviously can't show you all of them cuz
[01:22:56] there it's just time constraint, right?
[01:22:58] But obviously the more you practice the
[01:23:01] uh uh better ways you'll more efficient
[01:23:03] ways you'll find, right? But the way I'm
[01:23:05] going to show you is pretty efficient as
[01:23:07] well. Don't worry. Okay. Now, you might
[01:23:10] have speculated that I'm going to create
[01:23:12] like a router node. It's close. I'm not
[01:23:16] going to create another router node. You
[01:23:18] can see in the graph the uh the client
[01:23:21] let's say the client wants this graph.
[01:23:22] The client doesn't want another router
[01:23:24] node here. So how do we go about that?
[01:23:27] Well, we could create a conditional
[01:23:29] edge. How do we do that? Okay, let's
[01:23:31] begin that. So let's write a new
[01:23:33] function say defaf should continue
[01:23:36] uh state agent
[01:23:38] state agent
[01:23:41] state and um let's create this block
[01:23:44] string um function to decide what to do
[01:23:49] next something like that. Okay cool now
[01:23:53] here's where we set our looping logic
[01:23:55] and this should look quite familiar to
[01:23:57] you
[01:24:00] now. Perfect. So let's run that. Okay.
[01:24:03] So what have I written here? Well, if
[01:24:05] the counter value is less than five
[01:24:07] because we're starting with zero, right?
[01:24:08] So 0 1 2 3 4. That'll be five values. Um
[01:24:12] I've also written a print statement so
[01:24:14] like we can keep track of um um the
[01:24:18] progress. Also whenever I'm writing the
[01:24:20] code as well when you're uh coding with
[01:24:22] me or doing the exercise, it's really
[01:24:24] helpful to print uh statements uh like
[01:24:27] put in print statements everywhere. Or
[01:24:29] you could also use break points as well.
[01:24:31] So you know uh where to where the code
[01:24:34] failed if it
[01:24:36] fails. Okay. So here we return the loop
[01:24:41] a loop edge and the exit edge. So
[01:24:44] obviously we have the loop edge and this
[01:24:45] will be the exit edge. So everything is
[01:24:47] going to plan so far but um so far is
[01:24:50] the key. You never know, right? Okay. Uh
[01:24:53] just as a heads up though, I want to
[01:24:55] show you this. So this is how the
[01:24:58] trajectory should follow. We start at
[01:25:00] the greeting node. Why? Cuz we obviously
[01:25:02] go from the start to the greeting node.
[01:25:04] And then we enter the random node. And
[01:25:06] we enter the random node and exit it
[01:25:08] five times. So 1 2 3 4 5. Why five
[01:25:13] times? Because we want five random
[01:25:14] numbers, right? By then this if
[01:25:16] statement will uh well it won't work. It
[01:25:19] will fail. So we will go to the else
[01:25:20] statement and return exit. And if we
[01:25:22] return to exit, we'll go to the end
[01:25:25] node. Uh okay. endpoint. Okay, so that's
[01:25:28] how the general gist is. Okay, let's
[01:25:29] quickly make this graph. So you should
[01:25:32] know how to initialize a graph agent
[01:25:35] graph and let's just add these nodes. So
[01:25:39] we have our two nodes which are
[01:25:43] here greeting and random which is
[01:25:46] exactly what we wanted, right? Greeting
[01:25:47] node and random node. Perfect. Okay. And
[01:25:50] now we're going to add an edge between
[01:25:53] greeting and random. Uh why? Because
[01:25:56] well I've created this edge. You see
[01:25:58] this edge greeting node and random node.
[01:26:00] This edge that's the edge I've created.
[01:26:03] Okay. Now I'm going to create the um the
[01:26:07] conditional
[01:26:08] edges which is done through
[01:26:11] here and I've written some comments here
[01:26:14] as
[01:26:14] well. So uh there will be the source
[01:26:18] node which is the random. So where I
[01:26:21] want the conditional edge to start from
[01:26:23] and then the routing function or this
[01:26:25] tree I should have really written action
[01:26:27] here because is the action I want to
[01:26:29] perform the underlying mechanism or
[01:26:31] function which is going to which we're
[01:26:33] going to um determine which edge to use
[01:26:35] and that's uh implemented by the should
[01:26:37] continue function right and notice how
[01:26:40] again these two edges are the same edges
[01:26:42] here. So if the loop is uh the one which
[01:26:47] um uh is outputed then we need to go
[01:26:51] back into its random the random node
[01:26:54] which we've generate uh which we put
[01:26:56] there and if it doesn't we go to the end
[01:26:58] part. Okay and then obviously we set the
[01:27:01] entry
[01:27:03] point. Okay. So again you don't have to
[01:27:07] set the exit point here uh or the finish
[01:27:10] point because we've already done it
[01:27:11] using end here. Okay, perfect. And then
[01:27:14] we just compile the graph app is equal
[01:27:16] to
[01:27:20] graph.compile and okay, it compiled.
[01:27:22] That's a good sign. But let's see if we
[01:27:26] have got our graph to be the exact
[01:27:29] same. Now I'll put the graph image here
[01:27:32] so I don't keep scrolling back and
[01:27:34] forth. But you can see we have the start
[01:27:36] point and the end point. We have the
[01:27:37] greeting and the random. And then we
[01:27:39] have our two condition edges. So we have
[01:27:42] the loop going back into the random node
[01:27:45] as we wanted and the exit which you can
[01:27:47] see. So take a moment and you can see
[01:27:50] compare and contrast. Okay, let's
[01:27:54] continue. Okay, now I have this
[01:27:57] code. So I've given a name my name uh a
[01:28:01] r um a completely brand new list and
[01:28:04] I've set counter to minus
[01:28:06] one. And as you can see it enters loop
[01:28:08] one, loop two, loop three, loop four
[01:28:11] because these are print statements we
[01:28:12] printed. Uh it says hi there v which is
[01:28:15] my name. Uh number 10 21026 just
[01:28:19] randomly generated and you can see the
[01:28:20] counter value is five. Now remember what
[01:28:23] I was saying over the counter. We set
[01:28:25] the counter value to zero here to make
[01:28:26] it more robust. If we had not done that
[01:28:28] well it would have generated six times.
[01:28:31] And now I can set this to minus 100. it
[01:28:33] will still obviously give me different
[01:28:35] random values but um the code is largely
[01:28:39] the same. So that's really the way which
[01:28:42] I personally use to create loops in
[01:28:46] langraph it's pretty easy right but um
[01:28:49] obviously with practice you might even
[01:28:51] find some other ways if you do find
[01:28:53] other ways like obviously uh do let me
[01:28:55] know uh there's more than one way again
[01:28:58] you can send me a message on LinkedIn or
[01:29:00] Instagram or whatever but um yeah so
[01:29:03] this is finally finally uh we have
[01:29:07] implemented the code for our final graph
[01:29:09] of the section
[01:29:10] So just complete the graph 5 exercise
[01:29:13] please and yeah we should be good to go
[01:29:16] to make AI agents. So I'll see you at
[01:29:19] this codes exercise. Okay
[01:29:22] cool. Okay good job on that. Now for the
[01:29:25] exercise for this last graph uh you need
[01:29:28] to implement this graph on the right. So
[01:29:31] you need to implement an automatic
[01:29:33] higher or lower gain. So for context,
[01:29:36] you need to set the bounce which we can
[01:29:38] guess between 1 to 20 integers of course
[01:29:41] and the graph has to keep guessing where
[01:29:43] the max number of guesses is 7 where if
[01:29:46] the guess is correct it stops but if not
[01:29:49] we keep looping until we hit the max
[01:29:51] limit of seven. Now please note we don't
[01:29:54] have to pass any inputs the actual graph
[01:29:57] should automatically guess by itself. So
[01:29:59] there should be no human in the loop
[01:30:01] human intervention at all. So each time
[01:30:03] a number is guessed the hint node aka
[01:30:06] this node should say either higher or
[01:30:08] lower and the graph should account for
[01:30:10] this information and guess the next
[01:30:12] guess according accordingly. So for
[01:30:15] example the input should be something
[01:30:17] like the player name student. The guess
[01:30:19] should just be an empty list cuz we're
[01:30:20] initializing the list. Attempts should
[01:30:22] be set to zero and the lower bound and
[01:30:24] upper bound should be 1 to 20. Now the
[01:30:27] reason I've also passed these as inputs
[01:30:29] is because uh if you wanted to expand
[01:30:32] this to maybe 1 to 50 numbers or
[01:30:34] whatever you can. It's quite easy to do
[01:30:37] that. So just as a hint uh it will need
[01:30:40] to adjust it its bounds after every
[01:30:43] guess based on the hint provided by the
[01:30:45] hint though. So once you've completed
[01:30:47] this exercise you would have fully
[01:30:49] reinforced uh your understanding about
[01:30:51] loops in langraph. So once you've
[01:30:54] completed this, cross reference it.
[01:30:56] Cross reference the answers on GitHub. I
[01:30:58] will see you in the next section where
[01:31:00] we finally begin AI agents. See you
[01:31:04] there. Okay people. So welcome back to
[01:31:08] this brand new section where we actually
[01:31:10] start learning about AI agents. Now we
[01:31:13] finally are upgrading our ability in
[01:31:16] Langro. I even upgraded my clothing
[01:31:18] sense. Not really. But this is exciting
[01:31:21] times cuz we actually finally build AI
[01:31:23] agents. So, we're going to build a lot
[01:31:25] of AI agents in this section. And
[01:31:28] starting off with the first agent. Well,
[01:31:30] technically it's not really an agent,
[01:31:32] but I just named it that because it
[01:31:34] sounds cool. But um technically it's not
[01:31:37] though. But let's see what we're going
[01:31:40] to actually learn in this section in
[01:31:41] this subsection. So, we're going to
[01:31:43] build a simple bot. That's it. And these
[01:31:46] are the objectives. So we're going to
[01:31:48] define a state variable uh state
[01:31:50] structure which we're going to have a
[01:31:52] list of human message objects and I
[01:31:55] briefly uh me uh mentioned what a human
[01:31:58] message was uh a long time ago in the
[01:32:00] course. Uh what it is it's well it's in
[01:32:02] the name it's a message prompt which is
[01:32:05] given by the human aka us to the AI. Uh
[01:32:10] we're going to initialize the GPD40
[01:32:12] model for this uh using lang chain's
[01:32:14] chat open AAI uh uh library. Uh we're
[01:32:17] going to send and handle different types
[01:32:19] of messages. We're going to build and
[01:32:21] compile the graph of the agent. But the
[01:32:22] main goal really is how we can integrate
[01:32:25] LLMs into our graphs. So what is this
[01:32:30] sort of graph we actually going to end
[01:32:31] up building? Now it's very very simple.
[01:32:34] It's going to look like this. And yes,
[01:32:36] this looks exactly like the graph we
[01:32:38] made in the uh first ever graph we
[01:32:41] actually ever made. But um the
[01:32:43] functionality will obviously be
[01:32:44] different cuz now we're actually
[01:32:45] integrating LM. So exciting stuff
[01:32:48] people. Uh okay, I will see you at the
[01:32:50] code
[01:32:52] then. All right, coding time. So now we
[01:32:55] first code our well we code up our very
[01:32:58] first AI agent aka the simple what and
[01:33:02] um I've already imported all the
[01:33:03] necessary libraries we'll need uh to not
[01:33:06] waste time. So while you're uh coding
[01:33:08] these up as well and copying these I'll
[01:33:10] also briefly explain what these are so
[01:33:12] we're at the same level. Okay, so we've
[01:33:15] already imported type dictionary and
[01:33:17] list many times before but um these two
[01:33:21] we haven't sorry these two the lang
[01:33:23] chain codon messages import human
[01:33:25] message so I briefly mentioned this in
[01:33:28] the intro of this section of the
[01:33:30] subsection what a human message is right
[01:33:33] and this is the library we get it from
[01:33:35] and similarly we're going to be using
[01:33:37] openai's lms so that's why we're going
[01:33:39] to use chat openai from the lang chain
[01:33:41] open aai uh library uh the
[01:33:44] langraph.graph. Uh these we were
[01:33:46] familiar with and this is the env. Now
[01:33:50] just a few points. You could have been
[01:33:52] saying okay wait hold on I thought we
[01:33:55] were about to do a langraph stuff. Why
[01:33:56] is the lang chain stuff here? Now you
[01:33:59] must know that langraph is built on top
[01:34:01] of lang chain and lang chain already has
[01:34:05] the sophisticated libraries right so why
[01:34:07] not actually use them that's how
[01:34:09] langraph is designed it's designed to
[01:34:11] use the robust sophisticated libraries
[01:34:14] which lang chain offers right so no I'm
[01:34:17] not a trader we're still doing langraph
[01:34:19] stuff but we're also using leveraging
[01:34:21] lang chain strengths as well okay and um
[01:34:24] now this env file now it's okay if you
[01:34:27] haven't ever um encountered av file
[01:34:29] before. Essentially, it's just a file
[01:34:32] used to store secret stuff like API keys
[01:34:34] or configuration values. So, it's really
[01:34:37] there for security purposes. Now, I have
[01:34:40] my own
[01:34:41] um file stored in my folder structure uh
[01:34:45] so that you don't see my API key uh
[01:34:48] because if you do then I would go
[01:34:49] bankrupt. So, that's why. Now, you might
[01:34:53] also be wondering why do we need an API
[01:34:55] key here? We need the API key because
[01:34:58] we're doing calls to an external LLM. If
[01:35:01] we were using our own LLM like through
[01:35:05] OAMA, then we would um not have an API
[01:35:08] key, right? We would just use like the
[01:35:10] Olama library integration with lang
[01:35:13] chain. So because we're using charges,
[01:35:16] we need an API to communicate with the
[01:35:17] LLM in their cloud servers. Cool. So how
[01:35:21] do we actually load this? So to load our
[01:35:25] um API, we just use a simple Python uh
[01:35:28] code load. Env. All right. So now that
[01:35:31] we're at the same level, let's actually
[01:35:32] code up our AI agent. Cool. So let's
[01:35:36] define the state like we always do. So
[01:35:38] this time class agent
[01:35:40] state type
[01:35:42] dictionary. Perfect. Okay. Now what are
[01:35:46] the attributes we need in this section
[01:35:48] uh in this uh state? Well really just
[01:35:50] one the messages part right so messages
[01:35:53] but what form will it be well it will be
[01:35:55] in the form of a a list of human
[01:35:57] messages right so we'll have list human
[01:36:01] message why because we when we invoke
[01:36:04] the graph we're inputting human messages
[01:36:07] right so to tell the large language
[01:36:08] model that this is a human message I i.e
[01:36:12] Uh this is a message from me the user
[01:36:14] aka human right. Um we need to actually
[01:36:18] mention human message that it's a human
[01:36:20] message type. Cool. Okay. So now we
[01:36:24] actually initial initialize the large
[01:36:25] language model. So we just write lm is
[01:36:28] equal to chat openai. And now we specify
[01:36:32] what model we want. Now I'm going for
[01:36:36] GPD4er. Now yes there's also chat uh
[01:36:39] anthropic. I think there's chat oama. Um
[01:36:42] there's a lot of like in-built um
[01:36:45] libraries which lang chain offers which
[01:36:47] is great. Personally I've used chat
[01:36:50] openai a lot. I've also used chat
[01:36:52] anthropic a lot as well. Uh personally I
[01:36:54] like chat openai cuz it's just really
[01:36:56] simple to use. I've also used tried well
[01:36:59] tried to use chat oama before but really
[01:37:02] there's some difficulty in integrating
[01:37:05] it with lang. So that's why I've opted
[01:37:07] for openi. And if you're worried about
[01:37:10] financial cost, don't worry, it's
[01:37:11] extremely cheap. Uh if you want, you
[01:37:14] could also go for the GPD 40 mini model
[01:37:16] as well if that's a concern. But trust
[01:37:18] me, it's extremely cheap. Like the input
[01:37:21] tokens, output tokens is like in like
[01:37:24] tens of pennies for like a,000 tokens.
[01:37:26] So really, really cheap. Okay. So now
[01:37:29] let's actually define our node through
[01:37:31] our function. So
[01:37:33] process and we obviously define the
[01:37:36] state and then
[01:37:38] return the state like so. Perfect. Now
[01:37:42] how do we actually call the lm? Now lang
[01:37:46] chain and the langraph team really like
[01:37:48] using the word invoke. You might have
[01:37:50] noticed that to call a graph or like to
[01:37:52] make the graph run we've used invoke.
[01:37:54] Similarly to run the lm we use invoke as
[01:37:57] well. So we okay let's store the
[01:38:00] response we get in a variable. So uh
[01:38:03] lm.invoke and what do we invoke? Well,
[01:38:06] you can see from the uh hints here that
[01:38:08] it requires an input of language model
[01:38:11] input. What's that basically saying is
[01:38:13] what what what do you want the LM to do?
[01:38:15] Right? What's your question? Now what is
[01:38:17] our question? Well, that's in the
[01:38:19] messages. So we write state messages. So
[01:38:22] what will happen here is as soon as I've
[01:38:24] written state messages, let's say I have
[01:38:27] written hi or whatever uh we will pass
[01:38:30] this to the LLM through the invoke
[01:38:32] method. The LLM will then generate a
[01:38:35] response from its cloud server through
[01:38:37] our API and it'll get it will give us
[01:38:40] back the um its response and then we'll
[01:38:43] store it in the response section uh the
[01:38:45] response variable. Cool. And um let's
[01:38:48] actually print
[01:38:51] this like so and return the state like
[01:38:55] such. Okay, done. Now we obviously need
[01:39:00] to create the graph like such.
[01:39:02] Okay. So uh what is it saying? Well,
[01:39:06] it's saying that there is we've created
[01:39:08] a node process which is that which where
[01:39:12] the action is the process function. The
[01:39:14] add we've added an edge. We've added an
[01:39:16] edit from the start to the end node end
[01:39:18] point and we've compiled the graph.
[01:39:20] Okay. Um yeah. So let's now ask the for
[01:39:25] the user input. So user input is equal
[01:39:27] to input. We'll say enter
[01:39:32] something. And now we will invoke the
[01:39:36] agent cuz we need to invoke the agent of
[01:39:39] course because we're creating a graph,
[01:39:41] right? And the graph is well like agent
[01:39:44] in this case. Cool. Let's actually run
[01:39:47] this code now. So, Python
[01:39:50] agentbot.
[01:39:52] py and perfect. So, enter. Let's say
[01:39:57] hi. The AI message was hello, how can I
[01:40:01] assist you today? Now, I can reassure
[01:40:03] you I did not pre-code this or hardcode
[01:40:06] this. This is the actual LM. Let's run
[01:40:07] it uh one more time.
[01:40:10] Let's come up with a different message
[01:40:11] like who are
[01:40:15] you and it'll say I'm an AI language
[01:40:18] model created by open AAI called chat
[01:40:19] GBT. So you can this basically pretty
[01:40:22] much confirms that yes this is GBT uh in
[01:40:25] the background. Okay, but
[01:40:27] um why why just stick to one message,
[01:40:31] right? Why not uh be able to run
[01:40:33] multiple message like asking multiple
[01:40:34] messages kind of like a chatbot, right?
[01:40:37] So this is the code which does this and
[01:40:39] I'll walk you through this what's
[01:40:41] happening here as well. So uh like
[01:40:43] before we input our query and now we
[01:40:47] basically say keep iterating through and
[01:40:50] as soon as the user has said like exit
[01:40:52] or something then uh well you exit the
[01:40:55] while loop and that basically signifies
[01:40:57] that well you don't want to talk to the
[01:40:59] ailm anymore. So let's have get run
[01:41:03] this. So python agentbot
[01:41:05] py. Okay let's say hi again. Hello how
[01:41:09] are you? But now we can run it again.
[01:41:11] It's just a simple y loop. It's nothing
[01:41:12] groundbreaking. So like who made
[01:41:15] you? Okay, perfect. What is 2 + 2? 2 + 2
[01:41:20] equals 4. Okay. Uh let's say now, hi, I
[01:41:25] am
[01:41:28] Bob. Okay, now watch this carefully. I'm
[01:41:32] about to ask what did I
[01:41:35] just well or I should say what is my
[01:41:39] name?
[01:41:41] I'm sorry, but I don't have the ability
[01:41:43] to know your name or any personal
[01:41:45] information about you. Why is
[01:41:49] that? Why didn't it know what my name
[01:41:52] is? Well, even though I clearly
[01:41:55] specified it. So, let's quickly
[01:41:57] exit. Okay, now this is important.
[01:42:00] Nowhere in the code have we actually
[01:42:02] created some sort of memory. That's why
[01:42:05] I called this
[01:42:06] subsection simple bot. And that's why I
[01:42:09] kept on saying AI agent because it's not
[01:42:11] even an agent yet. Uh it's just a simple
[01:42:14] like the most basic LLM wrapper you can
[01:42:17] possibly have. But at least now you know
[01:42:20] how to actually integrate
[01:42:22] um LLMs in your graphs, right? And it's
[01:42:26] pretty straightforward. You just you um
[01:42:28] you just uh embed them within your
[01:42:30] functions and then your functions
[01:42:33] obviously act as the actions in your
[01:42:35] notes. And that's it. It's quite an easy
[01:42:37] piece of code. Like it's only what 29
[01:42:40] lines or 25 lines give or take. Uh but
[01:42:43] yeah, pretty simple. Um I don't think
[01:42:46] there'll be any exercise for this cuz
[01:42:48] well there really isn't much to do with
[01:42:50] this. So I will see you in the
[01:42:53] introduction for the second AI agent
[01:42:55] we're going to build. Okay. So I'll see
[01:42:57] you
[01:42:58] there. Cool. Cool. Cool. Okay. So now
[01:43:01] we're going to build our second AI
[01:43:03] system. And we're going to try to fix
[01:43:05] the problems we faced in the last uh AI
[01:43:08] system we built. And what was the
[01:43:11] problem? Well, the problem was it
[01:43:13] doesn't remember what we in what we had
[01:43:15] said before, right? Why? Cuz we were
[01:43:18] calling separate API calls. So now we're
[01:43:20] going to try to create a chatbot with
[01:43:22] some sort of memory. That's why I
[01:43:24] included the brain emoji here. So let me
[01:43:26] walk through the objectives for this uh
[01:43:28] subsection. So, we're going to use
[01:43:30] different message types in particular in
[01:43:33] particular the human message and the AI
[01:43:35] message. We're going to maintain a full
[01:43:37] conversation history using both of these
[01:43:39] message types. We're going to
[01:43:41] particularly use the GPD4 model again
[01:43:44] using the lang chains uh chat open AI
[01:43:47] library and overall we're going to
[01:43:49] create a sophisticated conversation
[01:43:51] loop. So, what is the main goal goal of
[01:43:54] this um subsection? It's really to
[01:43:56] create a form of memory for our agent.
[01:43:59] So if you're ready, let's go to the
[01:44:02] code. All right, awesome people. So
[01:44:05] let's begin coding our simple chatbot
[01:44:07] then. Okay, so like last time, I've
[01:44:10] already imported all of the uh necessary
[01:44:12] libraries and it's largely this exact
[01:44:15] same except now I've added two more uh
[01:44:17] stuff. So the first is the AI message
[01:44:20] and I explained this in the introduction
[01:44:22] of this subsection why we need the AI
[01:44:25] message. And I've also imported the
[01:44:27] union type annotation. Now the union
[01:44:30] type annotation is something we covered
[01:44:31] in the first chapter. So if you if this
[01:44:34] is the first time you are looking at it
[01:44:35] or hearing about it, I would recommend
[01:44:38] you going to the first chapter really
[01:44:39] understanding and watching the first two
[01:44:41] chapters. They're quite short to be
[01:44:43] honest and then coming back. Okay. Now
[01:44:47] that being said, let's actually begin
[01:44:49] the uh coding then. Okay. So like
[01:44:52] always, we define the state. So class
[01:44:55] agent state
[01:44:57] uh typed dictionary. Perfect. Now last
[01:45:00] time what did we define this as? Again
[01:45:02] we're only going to have messages again
[01:45:04] but uh last time we had list human
[01:45:08] message. Okay so that was what we had
[01:45:12] defined as our agent state
[01:45:16] previously. Now this time we also want
[01:45:19] to include the AI message as well. We're
[01:45:21] building a more sophisticated chatbot.
[01:45:23] So how do we do that? Well, one way or
[01:45:26] the naive way is to really have it as
[01:45:30] messages
[01:45:32] AI list AI message or something like
[01:45:35] that. Something like that. And don't get
[01:45:38] me wrong, this is still a valid
[01:45:39] approach. You can still build your graph
[01:45:41] and everything like that, but um I think
[01:45:44] it's a bit longer. So let me tell you
[01:45:47] another way which would actually be
[01:45:49] better. So remove this. Instead, let's
[01:45:53] use the type annotation union like this.
[01:45:56] So,
[01:45:57] union like so. And let's include AI
[01:46:02] message. Now, what has this done?
[01:46:05] Essentially, let me first tell you about
[01:46:07] a bit about human message and AI
[01:46:09] message. Human message and AI messages
[01:46:11] and like all of these like different
[01:46:12] structures are actually data types in
[01:46:14] Langraph and Langchain. That's what the
[01:46:17] developers of these libraries have got
[01:46:19] them to be. And um when I write union
[01:46:23] human message AI message then that
[01:46:26] basically allows me to store uh either
[01:46:29] human messages or or AI messages in this
[01:46:32] uh key in the state the messages. So
[01:46:35] that's what that literally means in a
[01:46:38] nutshell. Now, one important thing which
[01:46:40] I want to mention is this. All of these
[01:46:42] AI agentic libraries like Langchain,
[01:46:45] Langraph, Crew AI, Autogen, they're all
[01:46:48] great, but um you really can make your
[01:46:52] own AI agentic system by writing just
[01:46:55] Python functions. You don't even need to
[01:46:57] use a library. Now that being said, I
[01:47:01] would still recommend using these
[01:47:03] libraries, especially Langraph because
[01:47:05] Langraph, well, because it's a personal
[01:47:07] favorite, no bias at all, but um it's
[01:47:11] Langraph really allows you to control
[01:47:14] much more than other libraries would.
[01:47:17] Obviously, not as much control as if you
[01:47:19] were writing the Python functions
[01:47:20] yourself and everything, but I think
[01:47:22] it's a good balance of how much control
[01:47:24] you have and how much uh unnecessary
[01:47:26] jargon you need to write. Because think
[01:47:27] about it, think about how much of um
[01:47:30] this unnecessary code which you would
[01:47:32] have had to write else otherwise uh
[01:47:35] langraph and lang chain support. So
[01:47:37] that's why I highly recommend using
[01:47:39] these libraries and everything. So again
[01:47:42] human message and AI message are data
[01:47:44] types inbuilt data types within uh lang
[01:47:46] lang graph and lang chain. Cool. Okay.
[01:47:49] Now let's again initialize the large
[01:47:52] language model as we did last time. And
[01:47:53] again we're only we're using GP4.
[01:47:56] Okay, now we're going to create our
[01:47:58] node. Again, it's going to be the exact
[01:48:00] same graph structure, by the way. So,
[01:48:03] state agent state, but obviously the
[01:48:07] actions we perform will be slightly
[01:48:08] different. Now, um let's write a dock
[01:48:11] string. This node will
[01:48:15] um this node will
[01:48:19] uh
[01:48:20] do solve the request you input
[01:48:23] something. Dog strings aren't really
[01:48:25] needed for this AI agent or this
[01:48:28] subsection because we're not going to
[01:48:29] use them. But um again, good habit.
[01:48:32] Okay, cool. Let's invoke
[01:48:36] this. So what have I done here? This is
[01:48:39] exactly the same code which we did in
[01:48:40] the previous subsection. The l we invoke
[01:48:42] the lm uh with the state messages. And
[01:48:45] what are the state messages? Well, it's
[01:48:47] could be either human message or an AI
[01:48:49] message. It's a list of those. Awesome.
[01:48:53] So now we write this piece of
[01:48:56] code. Okay. State messages.appen AI
[01:49:00] message content equal to
[01:49:02] response.content. What on earth is
[01:49:04] happening there? Okay. Let's break this
[01:49:05] down. Response. Well, that's just
[01:49:08] extracting only the content part of the
[01:49:11] response aka the response being the
[01:49:13] answer or the result after we make the
[01:49:15] uh API call from the large language
[01:49:17] model. And it only extracts the content.
[01:49:19] So it only extracts like the important
[01:49:21] stuff, right? It removes all the
[01:49:23] unnecessary jargon which comes with it
[01:49:25] like the amount of tokens you use and
[01:49:26] all that. It removes that and that's uh
[01:49:29] gets stored in that gets converted to to
[01:49:32] an AI message and that's appended to our
[01:49:35] state messages um in the state. Simple.
[01:49:39] Okay. Uh now obviously to make it look
[01:49:43] pretty in the terminal we're going to
[01:49:45] print this and then we're going to
[01:49:46] return the
[01:49:47] state. That's it. That's how simple it
[01:49:50] was.
[01:49:52] Okay, so now we're going to create this
[01:49:55] exact same graph. And that's why I've
[01:49:57] just copied and pasted it because it's a
[01:49:58] time waste of me rewriting the code in
[01:50:00] front of you again and again. So we can
[01:50:02] just reuse the same code because it's
[01:50:04] the exact same graph uh graph structure
[01:50:06] as the previous subsection. Cool. Okay,
[01:50:09] now we're going to now here's where it
[01:50:11] actually starts working differently.
[01:50:14] See, last time we didn't have this the
[01:50:17] conversation history. really this is
[01:50:20] what's going to be our memory in in um
[01:50:23] this uh setup. Okay, so we have now in
[01:50:26] initialized conversation history. Now
[01:50:29] again we're going to ask the user what
[01:50:31] they want, right? What's their request?
[01:50:35] So now we use this Y loop and this Y
[01:50:38] loop was the exact same loop we had in
[01:50:40] the previous subsection as well. uh it
[01:50:44] only exits unless if the user has uh
[01:50:46] inputed well exit obviously but now look
[01:50:49] at this the conversation history is
[01:50:52] appended with the human message and the
[01:50:55] human message is obviously the user
[01:50:57] input the reason I've kept on writing
[01:50:59] content is because well that's the
[01:51:00] parameter in human message as you can
[01:51:02] see
[01:51:03] here okay cool uh and we've invoked the
[01:51:08] agent what is the agent well the agent
[01:51:10] is the compiled version of the graph the
[01:51:12] compiled graph uh with uh the entire
[01:51:15] conversation history. Now this is
[01:51:18] important. The entire conversation
[01:51:20] history is sent, not just the current
[01:51:24] human message. So uh this will make more
[01:51:26] sense. Don't worry, I'm um trying my
[01:51:29] best to explain it right now, but
[01:51:31] obviously it will make much much more
[01:51:33] sense as soon as I start running it.
[01:51:35] Okay? So bear with me if you didn't
[01:51:36] fully understand that. Don't worry.
[01:51:38] Let's remove that for now.
[01:51:41] Uh, and then we replace the conversation
[01:51:43] history completely like wipe it with the
[01:51:46] result messages. Why? Don't worry, it's
[01:51:49] going to make sense as soon as I run it.
[01:51:51] And I think yeah, we should be able to
[01:51:54] run this now. So, let's
[01:51:56] write python memory agent.py, which is
[01:51:59] the name of the
[01:52:00] file. Cool. Okay, let me just quickly
[01:52:02] write a hi just to see if the API is
[01:52:04] working. It is perfect. Okay. Hello. How
[01:52:07] can I assist you today? Uh, now I'll say
[01:52:10] like, "Hi, my name is
[01:52:17] Steve." Hi Steve, it's great to meet
[01:52:19] you. How can I help you today? Okay, now
[01:52:22] remember from last time. Last time if I
[01:52:24] asked it, hey, who am I? It didn't know.
[01:52:27] Do you think it will know
[01:52:31] now? Think about
[01:52:34] it. It does. you are Steve or at least
[01:52:38] that's the name you've chosen to share
[01:52:39] with me. Uh and the rest is yes
[01:52:42] whatever. So it does know about what I
[01:52:45] have said but just looking at this code
[01:52:49] I guess you can try to like pick out
[01:52:51] okay how does it work and everything
[01:52:53] like why everything works like that but
[01:52:57] um I think we can add print statements
[01:53:00] and everything. So let's try to add
[01:53:02] print statements now and see well how
[01:53:05] this is actually working. So let's exit
[01:53:06] the program.
[01:53:10] Okay. Uh let's add a print statement
[01:53:13] here. Let me include this. Cool. So what
[01:53:18] is this saying? So this print statement
[01:53:20] actually kind think of it like a
[01:53:22] snapshot of what the current state is.
[01:53:25] So as soon as it goes into a process
[01:53:27] note as just before it's about to finish
[01:53:29] by returning the state, we also print
[01:53:31] the current state as well. And this will
[01:53:34] literally just output whatever is stored
[01:53:36] in the messages attribute within our
[01:53:39] state. Okay. So let's clear. There we
[01:53:43] go. Let's run this
[01:53:45] again. So hi, nice to meet you.
[01:53:49] Something like
[01:53:50] that. Now take a look at the current
[01:53:53] state. See it outputed hello, nice to
[01:53:56] meet you. How can I see you today? Why
[01:53:58] did it output that? Well, because in our
[01:54:00] process
[01:54:01] function it we've asked it we formatted
[01:54:05] it in a way so it says hey AI which is
[01:54:07] this part and the response or content is
[01:54:10] this part. Okay. Now this response or
[01:54:13] content is also what was stored remember
[01:54:16] how I said it's stored in the um in a
[01:54:18] nice manner and was appended to our
[01:54:20] state messages. Now was it appended to
[01:54:23] the state messages? Yes. How do you know
[01:54:25] that? Because look at the human message.
[01:54:27] The human message was what I wrote which
[01:54:29] was hi nice to meet you. Uh forget the
[01:54:31] additional keyword arguments and
[01:54:32] response metadata cuz I didn't provide
[01:54:34] any. Uh you don't need to worry about
[01:54:35] that. The main part is this part the
[01:54:37] content. And then look at the AI message
[01:54:39] part. Uh it's the content is equals to
[01:54:42] hello nice to meet you. How can I see
[01:54:44] you today? Notice how it's the exact
[01:54:46] same thing as it was
[01:54:50] here. Okay. Now, now we're going to go
[01:54:54] one step ahead and I'm going to ask it
[01:54:56] to
[01:54:57] say my name is Steve again. Now, think
[01:55:03] about how will this current state
[01:55:05] change? Pause the video and try to think
[01:55:08] about
[01:55:12] this like that. Okay. So, now the second
[01:55:16] uh message I sent was my name is Steve.
[01:55:19] Its response for the second message was
[01:55:21] hi Steve. How can I help you today? Now
[01:55:24] look at the current state. It still
[01:55:27] begins with hi, nice to meet you, which
[01:55:28] was the first ever message I inputed
[01:55:30] into this conversation and then its
[01:55:32] respective AI message. And then that
[01:55:34] gets uh appended. Why appended? Well,
[01:55:37] because we had appended the AI message
[01:55:39] and appended the human
[01:55:41] message. So that's why. Okay. And you
[01:55:45] can see the human message is my name is
[01:55:47] Steve which is the most recent uh
[01:55:49] message which I put and then the AI
[01:55:51] message which is hi Steve how can I help
[01:55:52] you
[01:55:53] today? Perfect. And we can just keep
[01:55:56] going and going and going. But uh for
[01:55:58] now I'll
[01:55:59] exit. Now here's the thing. This works
[01:56:03] well relatively well, right? We've got
[01:56:06] it like as a chatbot which is what we
[01:56:08] wanted. it has some recollection of
[01:56:10] memory or or like of what we what we are
[01:56:13] who we are and everything. But there's
[01:56:15] two big problems here. Let's start with
[01:56:17] the first uh massive problem which is
[01:56:21] this. You know how I've exited the
[01:56:24] program right now. Yeah. Okay. I'm going
[01:56:28] to run the exact same program
[01:56:30] again. Now I told it that my name is
[01:56:34] Steve. What is my name?
[01:56:40] and it
[01:56:41] says uh I'm sorry I don't have access to
[01:56:45] your personal data. Okay. And look at
[01:56:47] the current state completely wiped out.
[01:56:50] Again, that's pretty self-explanatory as
[01:56:51] to why you exited the program and that's
[01:56:54] why obviously all the var the data was
[01:56:56] stored in the variables, right? The
[01:56:57] state was stored in the variables
[01:56:58] completely got wiped away. So what is
[01:57:01] the solution? Think about it.
[01:57:06] Well, obviously one potential solution
[01:57:08] would be to store it in a database, like
[01:57:10] a large database, right? Or a vector
[01:57:12] database if you're trying to do some
[01:57:13] ragged applications. For now, I'm just
[01:57:16] going to store it in a very simple text
[01:57:18] file. Why? Cuz it's really easy. And
[01:57:20] I've got the code as well. And usually,
[01:57:23] honestly, I just store it in a text file
[01:57:24] when I'm prototyping. Now, yes,
[01:57:26] obviously, storing it in a vector
[01:57:28] database or a database is much more
[01:57:29] robust and sophisticated, and that is
[01:57:31] what you should do. But when you're
[01:57:33] prototyping and you want to really see
[01:57:35] uh try to build it quickly and fast, uh
[01:57:38] I just tend to use a text file. It still
[01:57:40] works uh still works great and
[01:57:41] everything. So what is the code for the
[01:57:44] text file? Uh it's
[01:57:47] here.
[01:57:50] Okay. So what is this code saying? Well,
[01:57:52] essentially it's saying create me a text
[01:57:55] file called logging as a as a text file
[01:57:58] you see in write mode and a file. Write
[01:58:00] your conversation log. This is just to
[01:58:02] like make it look better and more
[01:58:03] aesthetic. But this is the main part of
[01:58:05] the code which um you should actually
[01:58:07] try and understand for every single
[01:58:09] message in the conversation history.
[01:58:11] Okay. Now note the conversation history
[01:58:14] was this variable which we had like
[01:58:15] initialized the conversation history uh
[01:58:18] stores the AI messages and the human
[01:58:20] messages. So that's where all of the um
[01:58:23] the information outside the graph
[01:58:26] actually is. Right? the state is locked
[01:58:30] in within the graph now and uh the
[01:58:33] conversation history is just another I
[01:58:36] guess you can say a duplicate version of
[01:58:37] the state right because we've you we've
[01:58:40] appended the exact same human messages
[01:58:43] and AI messages and kept on updating it
[01:58:45] through this line cool so what it says
[01:58:49] is that for every single message in the
[01:58:51] conversation history by the way a
[01:58:53] conversation is the duration between my
[01:58:56] first message and the last message I
[01:58:58] sent that entire thing is a
[01:59:00] conversation. A conversation isn't just
[01:59:02] a single API call. It's the entire
[01:59:04] length. Okay? So, just to be mindful of
[01:59:07] that. So, uh it first checks if it's a
[01:59:10] human message, it writes that as you and
[01:59:12] then extracts that content and if it's
[01:59:14] the AI message, it uh puts it under the
[01:59:16] AI stuff. So, let's run this again. So,
[01:59:19] let's exit this. Clear this. Okay.
[01:59:25] Who? Okay, let's say hi, I am Steve.
[01:59:29] Again, I'm using Steve because a
[01:59:31] Minecraft movie just came out, so that's
[01:59:33] why. Okay, now I'm going to
[01:59:35] intentionally make a spelling mistake
[01:59:37] here. Good morning. It should obviously
[01:59:40] morning should have been spelled, right?
[01:59:41] But I'm doing that for a reason. It gets
[01:59:44] no problem. Let's say tell me a joke.
[01:59:46] Just another random thing. Sure. Why
[01:59:49] don't skeletons fight each other? They
[01:59:51] don't have the guts.
[01:59:53] Um, really rubbish. My point is it
[01:59:57] works. Now I'll exit the program. And
[01:59:59] now it says conversation saved to
[02:00:01] login.xt. Now look at
[02:00:04] this. Remove that. Let me remove that.
[02:00:06] Okay, perfect. So this is the
[02:00:08] conversation log. The first message I
[02:00:10] ever sent was, "Hi, I'm Steve." There,
[02:00:11] it's response. Now, good morning. Now,
[02:00:14] why did I spell it like wrong? Why did I
[02:00:17] do that? Because I wanted to show you
[02:00:19] that this is the actual human message,
[02:00:21] my message being stored unaltered. So
[02:00:25] whatever I pass in the state as a human
[02:00:28] message that stays there. So it's
[02:00:30] unaltered. The AI message cannot or or
[02:00:34] anything can really change the previous
[02:00:36] human messages at all. Right? So that's
[02:00:39] why. And you can see tell me a joke.
[02:00:42] Sure. It's it's a rubbish joke is after
[02:00:44] that. And that's the end of the login.xt
[02:00:46] file. So that's a really fast efficient
[02:00:50] way, not the most robust way of course,
[02:00:52] but it is a fast efficient way to be
[02:00:54] able to store your data outside um the
[02:00:57] application if it stops. Perfect. Now,
[02:00:59] what was the second problem that I was
[02:01:01] mentioning? It's
[02:01:03] this. Look at how I initially I say,
[02:01:07] "Hi, I'm Steve." I don't know why I
[02:01:09] printed twice there. Weird, but
[02:01:11] whatever. Look at the current state
[02:01:13] length.
[02:01:15] Okay. Then I pass in another message, it
[02:01:17] becomes longer. I pass in another
[02:01:20] message,
[02:01:22] uh it gets longer. It keeps getting
[02:01:23] longer and longer and
[02:01:25] longer. That's a problem because think
[02:01:28] about it, you will use these uh library
[02:01:31] uh you'll use these like large language
[02:01:32] models whether it's for your own AI
[02:01:34] agentic startup or your own mini Javas
[02:01:36] or your own projects or whatever it is.
[02:01:39] You would obviously want to minimize
[02:01:40] cost, right? But using so many tokens uh
[02:01:45] using so many tokens like input tokens
[02:01:47] especially will really eat away uh your
[02:01:51] uh the amount of money you will uh spend
[02:01:53] like it will drastically increase it and
[02:01:57] that's a huge problem right we want to
[02:01:59] try to be conservative a bit about our
[02:02:01] money and our financial our finances so
[02:02:04] what is one what is a way to solve this
[02:02:07] think about
[02:02:10] that Well, right off the bat, I can give
[02:02:12] you an easy solution to implement which
[02:02:14] is within the code, write it, write some
[02:02:17] code where if the number of human
[02:02:20] messages exceeds five or something like
[02:02:23] that, then you remove the first human
[02:02:26] message in your uh history. Why remove
[02:02:29] the first and not the latest? Well,
[02:02:31] because the latest is most likely to be
[02:02:33] more relevant, right? The first message
[02:02:35] could is most likely to be the one where
[02:02:40] um the one which is well not needed or
[02:02:42] it could have been like it can it has
[02:02:45] more of a chance to be like a bit more
[02:02:47] less of an impact to have been removed.
[02:02:51] So why did I pick five? Well, five is
[02:02:53] just a random number I thought of. You
[02:02:55] could do 10, 15, 20, 25, three,
[02:02:58] whatever. But that's a really easy
[02:03:01] solution to do. Okay, so we learned
[02:03:04] quite a lot there. We learned how to
[02:03:06] integrate human message and AI message
[02:03:08] within a thing. And now we've created a
[02:03:11] somewhat of a sophisticated chatbot,
[02:03:13] right? It has a memory. It still talks
[02:03:16] to us. We if we define uh if we write
[02:03:19] who we are, it remembers that and
[02:03:20] everything and it works great.
[02:03:21] Obviously, it has its flaws, but for
[02:03:23] now, it's pretty good. Okay, so now
[02:03:26] we're going to build our third AI agent.
[02:03:29] And this is going to be a special type
[02:03:30] of an AI agent.
[02:03:32] The technical term for this type of
[02:03:34] agent is called a react agent and react
[02:03:37] stands for reasoning and acting. So this
[02:03:40] is a quite a common type of AI agent
[02:03:43] which you will build. So how does it
[02:03:45] look like? Well, it looks something like
[02:03:47] this. So it's quite simple. There's a
[02:03:51] start point and then it's an end point
[02:03:52] obviously. Then you have your agent and
[02:03:55] then we use a loop where we attach it to
[02:03:58] tools. Now, this could be one tool, two
[02:04:01] tools, a lot of tools. And it's the
[02:04:03] agent's job or the LLM in the background
[02:04:06] to be able to decide which tool to
[02:04:08] select. But not only that, it's all it's
[02:04:10] also its job to be able to decide when
[02:04:13] there's no more tool calling left to do.
[02:04:15] And when that happens, it goes to the
[02:04:17] end part. So that's the general gist of
[02:04:20] what a React agent is. It's a very very
[02:04:23] common and famous type of agent to make
[02:04:24] in Langraph. And that's exactly what
[02:04:26] we're going to be building in this
[02:04:27] subsection. So what are the objectives?
[02:04:30] So to build a react agent, the
[02:04:32] objectives are learn how to really
[02:04:34] create tools in langraph. We're going to
[02:04:37] be creating a react graph. Of course,
[02:04:39] we're going to be working with different
[02:04:40] types of messages such as tool messages.
[02:04:43] See, last subsection we've we covered AI
[02:04:46] messages, human messages, but now we're
[02:04:48] going to look at a lot more types of
[02:04:49] messages. for example, tool messages,
[02:04:52] system messages, base messages, and
[02:04:54] we're obviously going to test our
[02:04:55] robustness um of our graph. So, the main
[02:04:58] goal is to create a robust React agent.
[02:05:02] So, if you're excited, I'll see you at
[02:05:04] the
[02:05:05] code. Okay, people. So, now we're going
[02:05:08] to code up the React agent. And just a
[02:05:11] heads up, this is going to be quite a
[02:05:12] long subsection. So, get ready. You can
[02:05:15] see it's going to be long because of how
[02:05:17] many imports I've done. But because I've
[02:05:19] done so many new imports, I actually
[02:05:20] want to take some time off and really
[02:05:22] explain each line so that we're all on
[02:05:25] the same page. Okay, let's go. So the
[02:05:27] first line is from typing import
[02:05:29] annotated sequence and type dictionary.
[02:05:32] Now we obviously know what a type
[02:05:33] dictionary is, but we haven't come
[02:05:35] across annotated or sequence yet. So
[02:05:37] these are also type annotations. And
[02:05:39] I'll start off by explaining what an
[02:05:41] annotated is. So annotated is a type
[02:05:45] annotation which provides additional
[02:05:47] context to your uh variable or your key
[02:05:50] without actually affecting the type
[02:05:52] itself, the data type itself. Now what
[02:05:55] exactly does that mean? Well, I'll give
[02:05:57] you an example. Let's say I am trying to
[02:06:00] create a type dictionary where there is
[02:06:02] an email key in it. Okay? Now, obviously
[02:06:06] an email is string. So if I was to
[02:06:07] create a type dictionary, I would have
[02:06:09] written email colon string, right? Sl.
[02:06:12] That's how we've been doing it. But
[02:06:14] here's the thing with certain keys like
[02:06:16] email, they have to be a certain uh
[02:06:19] format. But like for example, it has to
[02:06:22] be like
[02:06:23] abcgmail.com for example. But if I pass
[02:06:26] in
[02:06:28] abcd-gmail.com or something like that,
[02:06:31] that's not a valid email format anymore,
[02:06:33] but it's still a string technically. So
[02:06:34] it would pass through. So how do we
[02:06:36] resolve that? Well, that's where
[02:06:38] annotated comes in. And I'll give you an
[02:06:40] example here. Let's say email is equal
[02:06:42] to annotated. I'm not going to create
[02:06:44] the whole type dictionary to save time.
[02:06:46] But for uh the example itself, you first
[02:06:50] pass in what data type you want it to
[02:06:51] be. So we want email to be a string,
[02:06:53] right? That's not changing. But here in
[02:06:55] quotation marks, I provide some more
[02:06:56] additional information, additional
[02:06:58] context. And this is basically adding
[02:07:01] onto the metadata of this key or
[02:07:04] variable. For example, uh let's say this
[02:07:07] has to be
[02:07:09] a valid email
[02:07:12] format. Now, obviously, I should do it
[02:07:15] in more detail, but um that's how uh for
[02:07:18] now, that's fine. So, how how can I
[02:07:22] actually see the metadata? So, if I want
[02:07:25] to, I would write print
[02:07:26] email metadata
[02:07:29] uh like that. And then I would press
[02:07:32] run. And here we go. You can see this
[02:07:35] has to be a valid email format. That's
[02:07:37] the exact same thing which is which we
[02:07:39] wrote here. So that's annotated done.
[02:07:42] But what about sequence? What does
[02:07:43] sequence mean? Well, sequence is also a
[02:07:46] type annotation. And the way I've
[02:07:48] described it is here. It basically
[02:07:50] automatically handles the state updates
[02:07:52] for sequences such as by adding new
[02:07:54] messages to a chat history. Now what
[02:07:57] does that mean? Well, it's really just
[02:08:00] there to avoid any list manipulation to
[02:08:02] the graph nodes. Obviously, like when
[02:08:05] we're using graphs and nodes and all all
[02:08:07] of that stuff and updating the states,
[02:08:08] there's a lot of uh list manipulations
[02:08:10] which we'll have to do. Sequence really
[02:08:12] handles a lot of that. So, that's really
[02:08:14] what it's there for. You don't really
[02:08:16] need to uh worry about it too much.
[02:08:18] Okay. Now, if we continue, we have env
[02:08:22] uh from import loadenv. From last time,
[02:08:26] we know that this is just to store our
[02:08:28] API keys and I've done that here. That
[02:08:30] will load the API keys. But you'll see
[02:08:32] now these three uh imports. We're
[02:08:35] importing some new message types here.
[02:08:37] So we're importing base message, tool
[02:08:39] message, and system message. I'll start
[02:08:41] off with the tool message. So it's
[02:08:43] essentially a type of message where
[02:08:46] where the data is passed back to the LM
[02:08:48] after the tool has been called and like
[02:08:51] the information which is passed is like
[02:08:52] the content itself, the tool call ID. Uh
[02:08:56] that's what tool messages. It's pretty
[02:08:58] self-explanatory. Now for a system
[02:09:00] message, it's the it's a message for
[02:09:02] providing instructions to the LLM. So
[02:09:04] like for example, if you've used uh LLM
[02:09:07] APIs before, you might have written you
[02:09:09] are a helpful assistant. That's exactly
[02:09:11] what a system message is. And don't
[02:09:13] worry, we're going to code this up as
[02:09:14] well. So you'll actually see what they
[02:09:16] are. Now what's a base message? So in
[02:09:19] the comments, you can see that I've
[02:09:20] written the foundational class for all
[02:09:22] message types in Langraph. Now here's
[02:09:25] how this works. Think about the class
[02:09:27] hierarchy. So you know how you have a
[02:09:30] parent class and then you have child
[02:09:31] classes as well. Well the base message
[02:09:34] would be the parent class and these uh
[02:09:37] AI message, human message, tool message,
[02:09:39] system message and all these other types
[02:09:40] of message will be like the child
[02:09:42] classes and they will inherit all the
[02:09:44] properties of the base message cuz
[02:09:46] that's the parent one. I guess you can
[02:09:48] say the uh all father or something but
[02:09:51] the AI message, human message and all
[02:09:53] these child uh classes obviously they'll
[02:09:55] have their own properties, right? For
[02:09:56] example, the tool message has its own
[02:09:58] content and tool call ID and all that
[02:10:00] stuff. So that's what the base message
[02:10:02] is. It's really the foundational class
[02:10:04] for all the message types in
[02:10:06] Langraph. Cool. Okay. So now if we
[02:10:10] continue, you can see we've imported
[02:10:11] chat, openAI. Uh we've done state graph
[02:10:14] and M. These we've come across. We know
[02:10:16] what they are. And we've imported tool
[02:10:19] and tool nodes which we cover in the
[02:10:21] second chapter or second section of this
[02:10:23] course. uh these are different elements
[02:10:25] which we're going to be uh using in
[02:10:26] langraph. Now what about this line from
[02:10:29] langraph dossage import add messages.
[02:10:32] Now what does that mean? So this is a
[02:10:34] little bit um different. This add
[02:10:37] messages is a reducer function. Now if
[02:10:41] this is the first time you're hearing
[02:10:42] that don't panic. It's not that hard. So
[02:10:46] let's let me copy this one second. Okay.
[02:10:49] So a reducer function is essentially
[02:10:52] just a rule that controls how updates
[02:10:54] from nodes are combined with the
[02:10:56] existing state. In simpler words, it
[02:10:58] really just tells us how to merge new
[02:11:00] data into the current state. Now here's
[02:11:03] the thing. If we didn't have some sort
[02:11:05] of a reducer function, uh updates would
[02:11:07] have just replaced the existing value or
[02:11:09] state entirely. And I'll give you an
[02:11:11] example for this.
[02:11:15] So let's say I had a state where it was
[02:11:19] just high. I had one attribute messages
[02:11:21] and high. Now obviously I should have
[02:11:23] created the type dictionary and
[02:11:25] everything and formalize it but just for
[02:11:26] simpler um for times saving purposes
[02:11:29] I've done it like this. Now what if I
[02:11:32] had an update which says nice to meet
[02:11:34] you. If I didn't have a reducer function
[02:11:36] that would completely overwrite it. Now
[02:11:38] in the previous uh graphs and agents
[02:11:41] we've made we've appended it but now
[02:11:43] that we're using so many different
[02:11:45] messages and calls and tool calling and
[02:11:47] what
[02:11:48] whatever we can't really always append
[02:11:50] everything like it will get far too
[02:11:52] complicated. So that's why we need to
[02:11:54] leverage reducer function. So if we
[02:11:56] didn't use a reducer function it would
[02:11:58] just overwrite it completely. But if we
[02:12:00] did like hi nice to meet you it would
[02:12:03] append it. That's the key. So in a
[02:12:06] nutshell, the reducer function really
[02:12:08] just aggregates the uh data in the
[02:12:10] state. This reducer function uh and the
[02:12:12] reducer function which I'm talking about
[02:12:13] is add messages. So once again, add
[02:12:17] messages is a reducer function that will
[02:12:19] really just allow us to append
[02:12:21] everything into the state without any
[02:12:24] overring happening cuz so we want to
[02:12:26] preserve the state. Okay, cool. So now
[02:12:29] let's actually code this uh react agent.
[02:12:32] Okay. All right. Okay. Okay, I've
[02:12:34] cleared the screen now and let's
[02:12:36] actually begin like we how we always
[02:12:38] begin with the uh creation of our state
[02:12:40] of our agent. So, type dictionary like
[02:12:44] such. Okay. And now we we'll only have
[02:12:49] one key in this uh in this example which
[02:12:52] is just messages. And now let's use the
[02:12:55] new type annotations we've learned. So,
[02:12:58] sequence base message and reducer
[02:13:02] function add messages. So again this
[02:13:05] piece of code is saying to preserve the
[02:13:07] state by actually appending it rather
[02:13:10] than overwriting. That's what this
[02:13:11] reducer function does. Okay. All right.
[02:13:15] Okay. Oh, and the sequence of base
[02:13:17] messages is the data type and this
[02:13:20] provides the metadata. That's why we
[02:13:22] have the annotated keyword here. That's
[02:13:25] really it. Okay. Uh now let's create our
[02:13:28] first ever tool. Now how do we do this?
[02:13:30] Some of you who have a um who have come
[02:13:33] from lang chain might know how to do
[02:13:36] this already. We use a decorator and we
[02:13:39] define like this. Now this decorator
[02:13:41] basically tells Python that this
[02:13:43] function is quite is special. It does
[02:13:45] something and well it is special because
[02:13:48] it's a tool which we're going to use. So
[02:13:50] let's define our tool as def. Let's
[02:13:52] create a simple addition tool. Okay. So
[02:13:55] we'll say a integer b integer.
[02:13:59] It's basically going to add two numbers.
[02:14:01] And this is where doc strings actually
[02:14:02] come now. And I'll show you how
[02:14:04] important they are. For now, let's say
[02:14:06] uh this is an addition
[02:14:09] function
[02:14:11] that adds two numbers together.
[02:14:15] Okay. All right. And we just return a
[02:14:18] plus
[02:14:19] b. Simple. Now, how can we actually
[02:14:23] infuse these tools to our large language
[02:14:25] model? Well, first let's create a list.
[02:14:30] Add like such. Now, yes, at this current
[02:14:34] moment, I only have one tool, but in a
[02:14:36] few moments, we'll have multiple tools.
[02:14:37] That's why I'm adding this uh list for
[02:14:39] now. And let's actually create our
[02:14:41] model. So, model is equal to chat
[02:14:45] openai. Model is equal to
[02:14:48] GPT40. Again, I'm using GPD40 because
[02:14:51] I've never had a problem with it to be
[02:14:52] honest. So how can we tell our GPD40
[02:14:56] large language model that these are the
[02:14:58] tools you can use? Well, we can use this
[02:15:00] inbuilt Python um inbuilt function
[02:15:03] called bind tools. Bind tools like that.
[02:15:07] And we pass in the list of tools we
[02:15:08] have. So that's tools. Pretty simple,
[02:15:11] right? Okay. So now large language model
[02:15:14] will have access to all of our
[02:15:16] tools. Okay. So now we need to create a
[02:15:19] node which actually acts as the agent
[02:15:21] within our graph. So how do we do that?
[02:15:24] Let me create just a simple function
[02:15:26] like def model call. We pass in the
[02:15:28] state agent state. Again it needs to
[02:15:31] return the agent
[02:15:32] state.
[02:15:34] Okay. Now I'm going to quickly copy this
[02:15:37] piece of code. Give me a
[02:15:42] second. Okay. So what is this code
[02:15:45] doing?
[02:15:46] uh you can see that we're invoking the
[02:15:49] model aka running the model and this is
[02:15:52] the system message which we are asking.
[02:15:54] So we're explicitly saying the large
[02:15:57] language model that you are my a system
[02:15:59] please answer my query to the best of
[02:16:01] your ability. So that's what the large
[02:16:04] language model's task is to do. Now if
[02:16:07] we want to get technical here, you could
[02:16:09] have written it in a slightly different
[02:16:11] way and that way is through
[02:16:15] this. So remove
[02:16:18] this. We could have said system
[02:16:22] prompt. Okay. So what's going on here?
[02:16:25] Remember how I said system message is
[02:16:26] also something which we imported. Uh so
[02:16:29] the system message like I said is this
[02:16:31] line of uh is this line. You are my AS
[02:16:33] system. Please answer my query to the
[02:16:35] best of your
[02:16:36] ability. Now, either way would have
[02:16:38] worked if we if I had just straight up
[02:16:40] passed this string into here. That would
[02:16:42] have worked as well. Personally, I think
[02:16:44] this way is better. Even though they
[02:16:46] achieve the exact same thing, I think
[02:16:47] this way is better cuz it's more
[02:16:49] readable. Okay? And you're only adding
[02:16:51] just one more import. Okay? So, I would
[02:16:54] prefer you to I would really recommend
[02:16:56] you doing like uh like this so even the
[02:16:59] large language model knows that this is
[02:17:00] a system message. Okay, cool. And this
[02:17:04] is uh just another way of writing like
[02:17:06] the updated state. You know how we've
[02:17:08] been writing state uh brackets messages
[02:17:12] is equal to something something
[02:17:13] something. Well, this is a more compact
[02:17:15] way of updating the state as well. So
[02:17:17] return messages response. So we update
[02:17:20] the messages with the response. No plus
[02:17:22] equal to this this this or adding
[02:17:25] something we just we can simply just
[02:17:27] write it with the updated state. Why?
[02:17:29] because the add messages aka the reducer
[02:17:31] function handles the appending uh for
[02:17:34] us. It doesn't overwrite it. Now, if I
[02:17:37] ran this code and I built the graph and
[02:17:38] everything, would it
[02:17:40] work? No. Why it wouldn't work? Because
[02:17:45] think about it, the response when we've
[02:17:47] invoked the model and we store it in the
[02:17:49] response when we actually invoked it, we
[02:17:52] didn't actually pass in the query. How
[02:17:55] do we pass in the query? Think about it.
[02:17:58] All I passed is my system message. Where
[02:18:01] does the query go? So to be able to add
[02:18:03] the query, I actually have to add like
[02:18:06] this. So state messages. The query it
[02:18:10] will be in the form of a human message.
[02:18:12] And the human message will be stored in
[02:18:14] the messages attribute, right? And now
[02:18:16] that we've passed that into our model as
[02:18:18] well and we can invoke it. And now this
[02:18:21] should work.
[02:18:25] Okay. Okay. Okay, so now we define the
[02:18:28] conditional edge. Now why do we need the
[02:18:29] conditional edge here? I'll put the
[02:18:31] picture of the react agent. Again here
[02:18:34] you can see that the looping part even
[02:18:36] like in the last one in the graph when
[02:18:38] we made the loops for the first time you
[02:18:40] saw that was it was a conditional edge
[02:18:42] which we had to use and now that's
[02:18:44] actually going to come in play here.
[02:18:46] That's why I took so time to build those
[02:18:47] graphs because now the concept is
[02:18:50] coming. So how do we define the
[02:18:53] conditional edge def should
[02:18:59] continue. Okay. So again like always we
[02:19:02] pass in the state and let's do it like
[02:19:09] this like such else
[02:19:14] return continue. Okay. So as you know as
[02:19:18] you um might have guessed end and
[02:19:21] continue will be edges which I'll define
[02:19:23] later in the graph. But what is going on
[02:19:25] here? Well essentially when I'll pass in
[02:19:28] the query uh when we've invoked the
[02:19:30] actual model you will know that we'll
[02:19:33] create a list of tools right so what
[02:19:36] we're going to be doing is we're going
[02:19:38] to be uh getting the last message and
[02:19:40] we're going to see if there's any more
[02:19:42] tools needed to be ran. If there are
[02:19:46] then we'll go into the continue edge aka
[02:19:48] we'll go to the tool node and we'll
[02:19:50] select the tool and we'll do all this uh
[02:19:52] actions and then come back. If there's
[02:19:54] no more tool calling left we will just
[02:19:56] end and we'll just exit the uh graph and
[02:19:59] that'll be the case. You'll get uh uh
[02:20:02] you'll understand more what I what I
[02:20:03] mean when we've actually test we're
[02:20:05] testing and running the graph. Okay. Now
[02:20:08] let's just define the graph. So like
[02:20:11] always we create the graph we initialize
[02:20:13] the graph through the state graph and
[02:20:15] let's call the node R agent. So the
[02:20:17] action will be the model call aka the
[02:20:19] underlying function will be this.
[02:20:22] Okay. Now we create something called a
[02:20:25] tool node which is also what we covered
[02:20:27] in the previous uh in the second section
[02:20:30] or second chapter in this course. The
[02:20:32] tool node essentially is just a singular
[02:20:35] node which contains all of the different
[02:20:37] tools. So we only have one tool. If you
[02:20:39] see what this variable is tools, we only
[02:20:41] have one tool which is add. Don't worry,
[02:20:43] we'll add some more tools like subtracts
[02:20:45] and multiply in a bit. But I just want
[02:20:47] to uh like really solidify your concept
[02:20:50] of how we can add these tools and how
[02:20:52] the graph will work. Okay. Now we
[02:20:55] obviously set our entry point and point
[02:20:57] it to the R
[02:20:58] agent. Now let's add our conditional
[02:21:01] edge. So remember remember how I said
[02:21:04] there's two edges, continue and end.
[02:21:06] again continue and end and if it goes to
[02:21:09] the end we end it. If it goes to tools
[02:21:11] then we go to tool node which is
[02:21:13] tools. Okay. Okay. So yeah this is
[02:21:17] pretty straightforward still. Right now
[02:21:19] we also need to add an edge which goes
[02:21:22] back from our tool to our agent cuz
[02:21:24] that's how we're going to create a
[02:21:25] circular connection.
[02:21:27] Right? You can see that the conditional
[02:21:30] edge only provides a one-way directed
[02:21:33] edge from the from either the agent to
[02:21:36] the tool node or the agent to the
[02:21:38] endpoint. But we need another edge which
[02:21:40] will go back from the uh tool node back
[02:21:43] to the agent. And that's what this um
[02:21:45] that's what this edge does. And lastly,
[02:21:48] we need to uh obviously compile it. So
[02:21:50] we'll just say app is equal to graph
[02:21:54] dompile. Perfect. That's it. Now I've
[02:21:57] just created a a new helper function
[02:21:59] here which this isn't part of langraph.
[02:22:03] I've just written this code because it
[02:22:05] will make every like the tool calling
[02:22:07] and everything uh like output in a much
[02:22:09] better way. So you'll see what I mean in
[02:22:11] just one
[02:22:12] second. Okay. So now we
[02:22:16] actually can begin. So let's say the
[02:22:20] input is uh something like this.
[02:22:24] Let's say I want to add 3 + 4. Okay,
[02:22:28] simple. And this line of code basically
[02:22:31] streams the data. That's all it does.
[02:22:33] So, let's actually run this. Clear. And
[02:22:36] let's do it. Okay. So, remember we wrote
[02:22:39] add
[02:22:41] 3+4. Wow, look at that. So, we've added
[02:22:44] 3+4. It calls the tool and it even knows
[02:22:47] what tool to pick. Add. Um, and it gives
[02:22:51] us the result. The tool message as you
[02:22:52] can see is seven and the AI message the
[02:22:55] final AI message is the sum of three and
[02:22:57] four is seven. That's it. Let's try
[02:23:00] something harder now. Let's write add 34
[02:23:03] + 21. So if we run
[02:23:08] this you can see 55 cuz 34 + 21 is 55.
[02:23:12] And you can also see again all the tool
[02:23:14] calls and everything that's done right.
[02:23:16] I want to show you one two more things
[02:23:18] actually before we add some more tools
[02:23:20] which is this. If I remove this dock
[02:23:22] string here by commenting out for
[02:23:25] now. Let's clear and let's run that
[02:23:30] again. Error. Why? Because the function
[02:23:34] must have a dock string if description
[02:23:36] is not provided. The dock string is
[02:23:39] necessary. That's why included otherwise
[02:23:41] the graph won't work. It's remember it
[02:23:43] tells the LM what that tool is for.
[02:23:46] Okay. So now that we've have uh we've
[02:23:49] got that there, let's try this as well.
[02:23:51] Add
[02:23:54] uh 3+ 4. Again, this time I want both of
[02:23:58] them to be executed. So
[02:24:00] clear now. Do you think this will work?
[02:24:02] Let's
[02:24:05] see. Add 34 + 21. Add 3+ 4. Perfect.
[02:24:09] Brilliant. Okay. So you can see the
[02:24:11] result of adding 34 + 21 is 55. The
[02:24:13] result of adding 3+ 4 is 7. You can see
[02:24:15] how the tool was called twice this time
[02:24:18] and that's the power of the loop which
[02:24:21] we created. Remember we created the
[02:24:23] conditional edge and then we also
[02:24:24] created that directed edge back from the
[02:24:26] tool node to the agent. Let's let's try
[02:24:29] to make it even uh give more um
[02:24:31] complicated stuff. Let's say
[02:24:34] add add 12 + 12 something. So let me
[02:24:38] clear this.
[02:24:40] Clear. Let's see what happens.
[02:24:46] Wow, look at this. If I press enter,
[02:24:50] sorry, I messed up there. But you can
[02:24:53] see the results of the addition as well
[02:24:54] as 34 + 21 is 55 7 24 or and you can
[02:24:58] also see that I called the tool the
[02:25:01] sorry the AI called the tool three
[02:25:02] times.
[02:25:04] Now these tool calls is also an
[02:25:06] indication that the LLM didn't use its
[02:25:09] own like information inbuilt information
[02:25:11] which it was trained on to come up with
[02:25:13] an answer. Right? Remember an LLM
[02:25:15] doesn't know how to do maths. It just
[02:25:16] guesses the next output like through
[02:25:19] probability. But through this we were
[02:25:21] able to actually add the two
[02:25:23] numbers. So an important concept here is
[02:25:27] the LLM actually decides what should be
[02:25:30] passed as the arguments to each tool. So
[02:25:33] 3 + 4 like if I said add 3 + 4 it will
[02:25:36] actually uh create it will actually uh
[02:25:39] input the numbers 3 and four and then
[02:25:40] this tool will handle the uh information
[02:25:42] return it and it will go back to the
[02:25:44] agent and then the AI agent will decide
[02:25:46] what's the answer and everything. So
[02:25:47] that's how it works. Awesome. Okay. Now
[02:25:50] let's make this even more complicated.
[02:25:53] Let's add some more
[02:25:55] tools. Let's add
[02:25:58] subtract and multiply. Okay. And the
[02:26:02] only re change we have to do is instead
[02:26:05] of this one line we just now include
[02:26:09] subtract and multiply as well. That's
[02:26:11] it. Otherwise this line this code
[02:26:14] largely stays the same. Now let's
[02:26:16] actually run this same command and see
[02:26:18] if it gets confused with the different
[02:26:21] um different tools we have it has access
[02:26:24] to. Now let's see. Okay.
[02:26:29] You can see
[02:26:30] again that 55 724. Okay, it didn't get
[02:26:34] confused. Perfect. Let's now give it a
[02:26:36] different command. Let's say something
[02:26:39] like this. One
[02:26:44] second. Add 40 + 12 and then multiply
[02:26:47] the result by 6. So now it has to make
[02:26:49] use of two different tools. Let's see if
[02:26:52] it gets
[02:26:53] that.
[02:26:55] Okay. Wow. Brilliant. So it first used
[02:26:59] the add tool and then used the
[02:27:00] multiplication tool and you can see all
[02:27:02] the queries or all the tool called and
[02:27:04] everything and the final answer is 312.
[02:27:06] So 52 * 6 yes it is 312. Okay. Wow that
[02:27:10] works like brilliantly. So now that we
[02:27:12] know that this is robust what about if I
[02:27:16] add this let's say also tell me a joke
[02:27:22] please. What do you think will happen?
[02:27:24] Do you think this will break? Let's see.
[02:27:28] If I play this and run this. Let's
[02:27:37] see. Wow. Look at
[02:27:40] this. The result of 40 adding 14 and 12
[02:27:43] is 52 multiplying that is by 6 is 312.
[02:27:46] And here's a joke for you. Why don't
[02:27:48] skeletons fight each other? They don't
[02:27:49] have the gun. I swear to God, it's
[02:27:51] always the same dead joke. But you get
[02:27:53] the point. This is so robust. It can
[02:27:55] handle even queries where it doesn't
[02:27:57] even need a tool and that ladies and
[02:27:59] gentlemen is the power of langraph. So
[02:28:01] it's it's so robust even if we don't
[02:28:04] need to use a tool it will still give us
[02:28:06] an answer and the reason it was able to
[02:28:09] do that is once all the tool calling is
[02:28:11] done it passes it to the agent the agent
[02:28:14] checks again oh I need to tell it I need
[02:28:16] to tell the user a joke as well and adds
[02:28:18] that to the final information and then
[02:28:20] ends it that's the power of
[02:28:22] lang okay so after all of that we
[02:28:25] finally now know how to create a react
[02:28:27] agent yes it was a simple react agent
[02:28:30] but the concepts the same. You can
[02:28:32] create your own external tools from now
[02:28:33] onwards and you can create your own
[02:28:35] graph. And that was the whole point of
[02:28:37] this course, right? For you to actually
[02:28:38] understand how we can uh create these um
[02:28:41] how we can use different tools and then
[02:28:43] the rest is up to you. It's up to your
[02:28:45] imagination. Okay, perfect. So now I
[02:28:48] will see you at the next subsection. All
[02:28:51] right, see you there. Okay, people. So
[02:28:55] we've made great progress so far. So
[02:28:57] well done on that. But now we make a
[02:29:00] fourth AI agent. And this time we'll do
[02:29:02] things again slightly differently. Well,
[02:29:05] this time we're going to be making a
[02:29:07] mini project together. So the project's
[02:29:10] name is going to be called Drafter. And
[02:29:12] you'll see why in a minute. So picture
[02:29:15] this. Me and you are working in a
[02:29:18] company together. And our boss comes up
[02:29:20] to us and she has a problem and some
[02:29:23] orders for us. So the problem is this.
[02:29:26] Our company is not working efficiently.
[02:29:28] We spend way too much time drafting
[02:29:30] documents and this needs to be fixed.
[02:29:33] Again, a valid problem. So, what are her
[02:29:36] orders? She says you need to create an
[02:29:38] AI agentic system that can speed up
[02:29:40] drafting documents, emails, etc. The AI
[02:29:44] agentic system should have human AI
[02:29:45] collaboration, meaning the human should
[02:29:47] be able to provide continuous feedback
[02:29:49] and the AI agent should stop when the
[02:29:51] human is happy with the draft.
[02:29:54] The system should also be fast and be
[02:29:56] able to save the drafts. Okay. So then
[02:30:00] me and you start discussing and we are
[02:30:02] going to use land graph obviously and we
[02:30:05] come up with a sketch. Now the sketch of
[02:30:08] our graph is something like this. It
[02:30:11] obviously is going to have a start and
[02:30:13] an end point and it's going to have our
[02:30:14] agent and the agent will have access to
[02:30:17] tools aka the tool node. Now this looks
[02:30:20] similar to a react agent which we
[02:30:22] covered in the last subsection. But
[02:30:24] there's a reason we don't we haven't
[02:30:26] chosen to do that. See we realize that
[02:30:29] one of the tools is the save tool. It
[02:30:31] will save the draft, right? That was one
[02:30:33] of our requirements. But obviously when
[02:30:35] we once we've saved it, the process
[02:30:37] should end, right? But if you remember
[02:30:39] from a React agent, the tools always
[02:30:42] goes back to the AI agent, not directly
[02:30:45] to the endpoint. And we don't want that
[02:30:47] anymore. So that's why as soon as the
[02:30:50] save tool is used because the save tool
[02:30:52] will be within tools right it ends. So
[02:30:56] that is the structure we have chosen to
[02:30:58] go with. So the only thing left is to
[02:31:01] actually code this graph. So let's code
[02:31:04] this together
[02:31:05] then. Okay. So let's actually code up
[02:31:08] this drafter project then. So you can
[02:31:11] see I've already done all the imports
[02:31:12] and I've loaded up my env file. Now all
[02:31:15] of these imports are imports which
[02:31:17] you've already uh encountered before. So
[02:31:19] there's no point in looking at them
[02:31:21] again. But the first thing which I'm
[02:31:23] going to do is I'm going to be defining
[02:31:25] the a global variable.
[02:31:28] Now this global variable yes it's a bit
[02:31:31] odd defining global variables and
[02:31:33] there's a reason which I've done it and
[02:31:35] this will become more apparent as I go
[02:31:37] through the code but just as a heads up
[02:31:40] the reason I've defined a global
[02:31:41] variable in this case is to actually
[02:31:44] pass in a state in tools the the correct
[02:31:48] way to do it in langraph is through
[02:31:50] something called injected state now
[02:31:53] injected state is beyond the scope of
[02:31:55] this uh course so the workound on that
[02:31:58] is to use a global variable and what
[02:32:01] will happen is our tools will uh
[02:32:04] whatever updates are made uh we'll
[02:32:06] update the global variable and then when
[02:32:08] we go on to save it uh the save tool
[02:32:12] will use the contents in this global
[02:32:14] variable and save that into a text file.
[02:32:17] So that's why this is included. Okay. So
[02:32:21] now let's define our agent state again.
[02:32:23] And the way that's done is the exact
[02:32:26] same way we did last time. Uh class
[02:32:28] agent state messages annotated sequence
[02:32:31] base message add message as the reducer
[02:32:33] function. So now we define the tools and
[02:32:37] there will be two tools for this. The
[02:32:39] first tool will be the update tool and
[02:32:40] the second tool will be the save tool.
[02:32:42] So let's start off with the uh update
[02:32:44] tool and I will obviously use the
[02:32:47] decorator and then create def
[02:32:50] update and then we need to pass in
[02:32:55] uh pass in a parameter content. Now just
[02:32:59] as a refresher whatever parameters you
[02:33:01] pass or you request who actually gets
[02:33:05] those parameters? Well, the LLM or your
[02:33:08] model in the background that's uh what
[02:33:10] will automatically pass the parameters
[02:33:13] for this model uh for this tool. So, uh
[02:33:16] in this case the content parameter will
[02:33:18] be uh that will be provided by the lm in
[02:33:21] the background. So, you don't need to
[02:33:22] worry about that. Okay. So, now we need
[02:33:25] the dock string obviously and I've just
[02:33:27] created a simple dock string which just
[02:33:28] updates the document with the provided
[02:33:30] content because that is exactly what it
[02:33:32] does.
[02:33:33] So now we define to interact with the
[02:33:35] global variable in Python, you obviously
[02:33:37] need to uh define it uh you need to code
[02:33:40] it like this and then you need to update
[02:33:45] your document content aka the global
[02:33:47] variable with your current content and
[02:33:50] then you just return again a statement
[02:33:53] to the like the large language model
[02:33:54] telling it that we have successfully
[02:33:56] updated it. So I've written document has
[02:33:58] been updated successfully. The current
[02:34:00] content is this which is the content
[02:34:03] which we store in the thing. Okay. So
[02:34:07] now we define our second tool which is
[02:34:09] the save tool. So again same decorator
[02:34:12] we use uh like
[02:34:14] this. And now we request the llm to give
[02:34:19] us a file name as well. So it will it
[02:34:22] should give us a suitable file name uh
[02:34:24] which will be a suitable file name for
[02:34:25] the text file and uh it will and now
[02:34:28] this save tool will automatically handle
[02:34:30] all the save logic. So uh as a dock
[02:34:35] string I pass like this. So saves the
[02:34:38] current document to a text file and
[02:34:40] finishes the process. And the arguments
[02:34:42] are file name which is the name for the
[02:34:44] text file. Now, I've specifically
[02:34:46] mentioned that we're going to be using a
[02:34:48] text file so that the uh uh the LLM
[02:34:52] knows that the file name which it needs
[02:34:54] to pass has to have a txt in the end of
[02:34:57] it. Now, if it doesn't uh by any means
[02:35:01] to make the uh graph to make the entire
[02:35:03] code more robust, I've also written this
[02:35:05] if statement such that if this file name
[02:35:07] doesn't end with a txt, just put a txt
[02:35:10] there just uh as robust as measure. Now
[02:35:13] again we need to uh call the global
[02:35:15] variable again. So global document
[02:35:19] content. Okay. Now this next bit of code
[02:35:21] that's this is not langraph. This is
[02:35:23] just uh whatever you put in the tool. Uh
[02:35:26] it it doesn't have to it's not going to
[02:35:27] be langraph related. Right. So this
[02:35:31] piece of code is just uh some code which
[02:35:34] allows you to save the uh contents a the
[02:35:38] the content store in in the global
[02:35:40] variable under the file name uh and as a
[02:35:44] text file and I've also added this
[02:35:45] exception uh which is a good thing for
[02:35:48] debugging purposes where it if there's
[02:35:51] an error it will tell me exactly what
[02:35:52] the error is and then we can fix it.
[02:35:55] Okay. So hopefully there won't be any
[02:35:57] errors. Now we create a list of tools
[02:36:00] which uh again will be update and save
[02:36:04] because we only have two tools. And now
[02:36:07] we actually call the uh model and how do
[02:36:10] we call the model like
[02:36:12] such? Now let me ask you a question. Is
[02:36:15] this it for the model definition or do
[02:36:18] we need something
[02:36:19] else? Well, there's a reason I asked
[02:36:22] that question, right? We forgotten to do
[02:36:24] bind tools. So bind tools and tools. So
[02:36:28] that will do. Okay. Now we actually
[02:36:31] initialize the agent itself or the
[02:36:33] function which will cuz remember the
[02:36:36] agent will be a node in our graph. And
[02:36:39] what will be the function behind that?
[02:36:41] It will be this function which we're
[02:36:43] about to define. So let's write this as
[02:36:46] def r agent. And again we need to pass
[02:36:49] in the state the agent state and it'll
[02:36:51] return the agent state.
[02:36:54] And okay so now this doc uh not doc
[02:36:58] string this we need to pass in a system
[02:37:00] message to our llm right now this llm
[02:37:03] this system prompt will be quite large
[02:37:05] so get ready
[02:37:08] uh like such so in this system prompt I
[02:37:11] have specifically said this is a system
[02:37:12] message and the content is this you are
[02:37:15] drafter a helpful writing assistant
[02:37:18] you're going to help the user aka us to
[02:37:20] update and modify documents and I've
[02:37:22] also written some more stuff about what
[02:37:25] the uh update or what what to do if the
[02:37:29] user wants to update. We use the update
[02:37:30] tool. Uh we need to use the save tool to
[02:37:33] save it and to always show the current
[02:37:35] document say after modifications and all
[02:37:38] that stuff. Cool.
[02:37:40] Okay. So, oops. There we go.
[02:37:45] And now it's time for some robustness
[02:37:48] measures. So when we're first
[02:37:50] initializing the graph like when it's
[02:37:52] the first message we're writing
[02:37:54] obviously we're not going to straight up
[02:37:55] say uh how would you like to change the
[02:37:57] document right because we haven't passed
[02:37:58] in a document yet. So if messages uh
[02:38:03] this part if that if there's nothing in
[02:38:06] it we will have to say something like an
[02:38:08] introduction message right. So this is
[02:38:10] how you can do that. So we can
[02:38:15] say if not state messages aka if there's
[02:38:18] nothing in the state messages then we
[02:38:20] can say uh I'm ready to help you update
[02:38:23] a document. What would you like to
[02:38:24] create? and then it collects the user
[02:38:26] input and passes it as a put stores it
[02:38:29] as a a human message in this user
[02:38:32] message variable. Now what if I've
[02:38:34] already passed it uh passed in a message
[02:38:37] or like we are on the process of
[02:38:39] updating our draft or drafting it. Well
[02:38:42] to do that we need this else statement
[02:38:45] and what does this say? Well it says
[02:38:47] what would you like to do with the
[02:38:48] document? So this assume this says that
[02:38:50] there's already stuff in the messages uh
[02:38:52] state a messages key in the state how do
[02:38:55] you want to update it further and then
[02:38:57] we also print it uh under this emoji uh
[02:39:01] in the terminal so the user can also see
[02:39:03] what they've inputed and then this is
[02:39:05] also stored in the user message. All
[02:39:07] right. Okay.
[02:39:10] Now we combine all of this uh all
[02:39:14] messages aka the system prompt which was
[02:39:16] the system message uh and we create a
[02:39:19] list of uh list of the uh state messages
[02:39:22] and the user message the new message
[02:39:24] which we want the aka the update and
[02:39:27] then we just invoke the model and how do
[02:39:29] we invoke the model you just use the uh
[02:39:33] model invoke okay so pretty basic code
[02:39:36] so far there's nothing hard or nothing
[02:39:39] uh extraordinary or something we haven't
[02:39:41] seen before. All of this we have seen
[02:39:43] before. And now the rest of this
[02:39:47] function is just a print statement which
[02:39:50] I've included. This print statement is
[02:39:52] just for uh um making things look
[02:39:55] prettier on the terminal. That's all it
[02:39:57] is. You can see the true print
[02:39:58] statements. There's the AI response
[02:40:00] which will be printed and then there'll
[02:40:02] be the tools uh whatever the tool
[02:40:04] messages are that's also printed. So
[02:40:06] that's the whole point of it. there's
[02:40:07] nothing like to really like talk about
[02:40:09] it here. Uh and then we also need to
[02:40:12] obviously
[02:40:13] return the updated state. Now remember
[02:40:16] last time I showed you that this is also
[02:40:18] a really convenient concise way to uh
[02:40:22] update the states. So from now onwards
[02:40:25] we're only going to update the states
[02:40:26] like this. Okay. Now we create our
[02:40:29] conditional edge function or the
[02:40:30] function behind the conditional edge cuz
[02:40:33] remember let me open this up. So the
[02:40:36] conditional edge which I'm talking about
[02:40:38] will be this this this conditional edge.
[02:40:42] So there from tools there will be either
[02:40:45] the select the uh the choice of going to
[02:40:47] back to the agent or the choice of
[02:40:49] ending it. So we need to create the
[02:40:52] underlying function behind that. So
[02:40:54] let's create that now
[02:40:57] uh under this. So should continue. We've
[02:41:02] done this many times before. it det will
[02:41:04] determine if we should continue or end
[02:41:05] the conversation and remember continue
[02:41:08] or end the conversation. Okay, makes
[02:41:11] total
[02:41:12] sense. Okay, so
[02:41:16] now we do this. So we get the messages
[02:41:21] and if there's nothing in the messages,
[02:41:22] well obviously we'll need to continue,
[02:41:24] right? It won't go to the end part. Uh
[02:41:28] and this is just as like a robustness
[02:41:29] measure to be honest.
[02:41:31] Okay. So now this piece of code
[02:41:35] is basically saying look at the most
[02:41:38] recent tool message or the uh recent
[02:41:41] tool we've used and we need to check if
[02:41:44] this tool uh has used the save tool. Now
[02:41:48] why remember how we have two tools we
[02:41:51] have either the uh update tool or the
[02:41:54] save tool. If we use the update tool,
[02:41:57] well, we will obviously need to use the
[02:41:59] continue branch, right? But if we use
[02:42:01] the uh save tool, well, after you saved
[02:42:05] it, there's nothing else to do, right?
[02:42:07] You finished your draft, you finished
[02:42:09] everything, so might as well end the
[02:42:12] program. That's why this end tool. So,
[02:42:14] for the continue, uh if to go to the
[02:42:17] continue um through the continue edge,
[02:42:19] we have to use the update tool. And to
[02:42:21] go to the end uh edge you need to use
[02:42:24] the uh the save tool. So should make
[02:42:28] sense now but don't worry if it doesn't
[02:42:29] we will do some more print statements so
[02:42:31] you see the workflow. Don't worry. And
[02:42:35] lastly we need to obviously return
[02:42:36] continue because by
[02:42:38] default it's checked here that it's used
[02:42:42] the save tool. The only other tool left
[02:42:44] is the right tool and uh sorry the
[02:42:47] update tool. And the update tool means
[02:42:49] that we have to go to the continue edge,
[02:42:51] right? Okay. And that's that uh function
[02:42:54] done as well. So pretty easy still. Now
[02:42:57] this next function is again I only coded
[02:43:01] this just to make the print statements
[02:43:04] in a more readable message format uh
[02:43:06] when we printed on the terminal. So you
[02:43:08] will see where this comes in play when
[02:43:10] we actually start uh invoking the graph
[02:43:12] and seeing how our process is going.
[02:43:15] Okay, cool. Okay. So now we actually
[02:43:19] init uh create the graph. So how do we
[02:43:22] create the graph? We've done this many
[02:43:23] times. We will initialize it through a
[02:43:26] state graph. And now we will add the
[02:43:30] nodes. So agent and tools. And the tools
[02:43:33] will be a tool node. And again if you
[02:43:36] notice back we had one node, two node,
[02:43:38] the agent node and the tools node.
[02:43:40] I'm keep I'm like reflecting back and
[02:43:43] forth between this diagram and the code
[02:43:45] so I can show you exactly what we're
[02:43:47] coding. Okay. So again agent and tools
[02:43:49] node uh we've
[02:43:51] done now we will set the entry point at
[02:43:54] agent which is the start point aka this
[02:43:57] part
[02:43:59] right and now we're going to add an edge
[02:44:02] between agent and tools. Now we need to
[02:44:05] obviously create this edge because the
[02:44:06] agent needs to go to the tools right and
[02:44:08] then this edge this directed edge and
[02:44:11] this conditional edge creates the loop
[02:44:14] uh which will allow for the human AI
[02:44:16] collaboration. All right. Okay. So now
[02:44:20] we add the conditional edge and that's
[02:44:23] the conditional edge which I was talking
[02:44:24] about the continue at the end aka this
[02:44:27] condition this conditional edge from
[02:44:29] tools. Okay.
[02:44:32] And now the last thing we need to do is
[02:44:35] just compile it because we've finished
[02:44:36] the graph completely, right? There's
[02:44:38] nothing left. We've done the start
[02:44:39] point, we've done the end point, the
[02:44:41] end, this conditional edges done, the
[02:44:43] nodes done, and then this directed edge
[02:44:45] is done and the start point is obviously
[02:44:47] done because we've uh created a
[02:44:49] directed. So you can see the entire
[02:44:50] graph we have created just like that. So
[02:44:53] again, nothing too
[02:44:55] hard. Cool. Okay. So now we actually run
[02:44:59] the program. And to run it, I have just
[02:45:01] written this um function so that
[02:45:04] everything is in a more compact way.
[02:45:06] This is just to invoke the graph. Okay.
[02:45:09] And let's do that. So that was the
[02:45:12] entire code. And this code will allow
[02:45:15] for human AI collaboration. Now, yes, we
[02:45:18] used a global variable. And again, there
[02:45:21] is nothing wrong with using a global
[02:45:22] variable. I know some of you might frown
[02:45:24] upon it, but um again, there's nothing
[02:45:27] wrong with it. If we wanted to use more
[02:45:29] complicated uh form uh complicated uh
[02:45:32] stuff from langraph like the injected
[02:45:34] state or even using something like
[02:45:36] commands and interrupts uh we would have
[02:45:39] to write the code slightly differently
[02:45:41] but because this is a beginner level
[02:45:43] course uh we've just disregarded that
[02:45:46] completely and we found another way of
[02:45:49] performing human AI collaboration.
[02:45:51] Awesome. So let's actually run this now.
[02:45:53] So let's write python draft.
[02:45:57] py and you should be able to see all of
[02:46:00] the things. I made my face cam slightly
[02:46:02] smaller so you can hopefully see
[02:46:03] everything. Perfect. So you currently
[02:46:05] have an empty document. Could you let me
[02:46:07] know what you like to add or create in
[02:46:09] the document? So what would you like? So
[02:46:11] let's say we are writing an email to our
[02:46:14] colleague Tom saying that we can't make
[02:46:16] it to the meeting. So let's say write me
[02:46:20] an email. Let's say uh write me an email
[02:46:22] to Tom saying we I cannot make it to the
[02:46:28] meeting. Let's see what it says. So it
[02:46:31] says
[02:46:34] uh hi Tom I hope this message find you
[02:46:37] well. Please let me know. Okay let's now
[02:46:40] give it some feedback on how we how we
[02:46:43] can improve. So and also you can also
[02:46:44] see that it's used the update tool as
[02:46:46] well. Perfect. So, let's say
[02:46:50] um make sure to also have specified that
[02:46:56] the meeting was supposed to be
[02:47:00] at 1000 a.m. at some random negation.
[02:47:05] Canary
[02:47:07] Wolf.
[02:47:09] Okay. Okay. Let's see the updated thing.
[02:47:11] Hi, Tom. Uh you can see message meeting
[02:47:14] at 10. Uh, can I wolf due to unforeseen
[02:47:18] circumstances? Uh, let's I don't like
[02:47:20] this uh your name part though. So, let's
[02:47:22] say my name is
[02:47:26] V and it will update that as you can
[02:47:29] see. Perfect. Uh, what do what else do
[02:47:32] we want to change? We can also say
[02:47:34] something like uh let's say but tell him
[02:47:40] that I can make it at 12 p.m. in
[02:47:47] um New York, some random location. Okay,
[02:47:51] I'm making this up, but you you get the
[02:47:53] uh plan. Uh the next day. So, let's
[02:47:59] see. And perfect. It's updated it.
[02:48:02] However, I am available to meet at 12:00
[02:48:04] p.m. in New York the next day.
[02:48:06] Obviously, it's complete like rubbish
[02:48:08] like the timings of the location I've
[02:48:09] written. But you can see how we can just
[02:48:13] uh use human AI collaboration here. Uh
[02:48:16] one more thing which I don't like is
[02:48:18] this part. I don't like the fact that
[02:48:19] it's not a new line. So, I mean I'm
[02:48:22] being a bit picky here. We can say
[02:48:24] something like uh
[02:48:27] put the II hope this message finds you
[02:48:36] well. Awesome. And as you can see that's
[02:48:38] done as well. So now let's say I like
[02:48:40] it. Save it please. And what
[02:48:45] happens? You can see that uh it used the
[02:48:50] save tool. The tool results is document
[02:48:52] has been updated successfully. The
[02:48:53] current content is this and the document
[02:48:56] has been saved to unable to attend
[02:48:58] meeting email. Now remember we never
[02:49:00] passed in the file name at all. That was
[02:49:03] all generated by the by the agent
[02:49:05] itself. And to check we need to go on
[02:49:07] unable to attend meeting. So let's see
[02:49:10] here it
[02:49:12] is. And you can see it's the exact same
[02:49:15] meeting uh exact same email we said. So,
[02:49:17] subject, oops, best regards me. All the
[02:49:22] exact same content. Perfect. And we
[02:49:24] don't even need to uh make it so that
[02:49:27] we're drafting emails. We can even drop
[02:49:28] short stories. We can drop whatever we
[02:49:31] want. In fact, we can also pass in uh a
[02:49:35] previous message. So, the reason it
[02:49:37] started off like with nothing is because
[02:49:40] we pass in an empty list. But if you
[02:49:43] wanted to, we could have written
[02:49:45] something over here uh with our pre with
[02:49:48] a already existing email or already
[02:49:51] existing document and then it could the
[02:49:53] model the agentic system would know that
[02:49:55] this is what the content is the current
[02:49:57] content how would you like to uh change
[02:49:59] that and that is exactly how uh we will
[02:50:02] be able to operate on our existing ones.
[02:50:05] So you can see that this is quite a
[02:50:07] robust thing. If we want another
[02:50:09] example, for example, uh let's say
[02:50:11] python drafter.
[02:50:16] py. Okay, now watch this as well. Look
[02:50:19] how robust this is. If I say something
[02:50:22] like write an
[02:50:24] email, it actually gives back questions.
[02:50:28] So sure, what would you like the email
[02:50:30] to say? D. So remember, it didn't even
[02:50:32] go through any tool here. uh using
[02:50:35] langraph we can really make the agents
[02:50:38] quite robust and that's the thing which
[02:50:40] I wanted to show you it doesn't always
[02:50:42] have to pick a tool its own like LLM
[02:50:45] like the agent itself cuz remember the
[02:50:47] agent node has an LLM in the background
[02:50:49] back end the bind tools function allows
[02:50:52] it allows it scope like it increases the
[02:50:55] scope of it uh by providing some tools
[02:50:57] but that doesn't mean it has to use
[02:50:59] those tools if it doesn't feel like the
[02:51:02] need to use the tools it won't and in
[02:51:04] this case it wanted to ask us more
[02:51:06] questions about it. So it would say show
[02:51:08] what would you like this email to say
[02:51:10] because to be fair I only wrote three
[02:51:12] words. Uh but that was what I was trying
[02:51:14] to show you. So let's just clear this
[02:51:16] now cuz we don't need to. And yeah you
[02:51:19] can see perfectly works human AI
[02:51:21] collaboration in langraph and this is
[02:51:24] actually somewhat useful as well. Now
[02:51:26] yes of course you can use GPT4 canvas
[02:51:29] and all of that stuff of course but um
[02:51:31] this is how you would do it in Lagraph.
[02:51:34] All right. So, if you would like an
[02:51:36] extension to this, what you could do is
[02:51:39] add a voice feature as well. So, maybe
[02:51:42] you could add use OpenAI whisper for uh
[02:51:45] speech to text conversion or add 11 laps
[02:51:48] for text to speech conversion and maybe
[02:51:50] you can make it voice based cuz right
[02:51:52] now I'm giving it I'm how am I
[02:51:55] communicating it with text mode? What
[02:51:57] about voice mode? You could also include
[02:51:59] a GUI to this. There's a lot of stuff
[02:52:02] which you can do on you can even have
[02:52:04] your own knowledge base as well and
[02:52:06] include that. So a lot of potential with
[02:52:08] this if you want a homework for this uh
[02:52:11] specific project that there you go. All
[02:52:13] right. Okay. Cool. So that's the end of
[02:52:16] this
[02:52:17] subsection. Awesome. So now let's build
[02:52:20] our fifth AI agent. And some of you
[02:52:22] might have been looking forward to this.
[02:52:24] It's retrieval augmented generation rag.
[02:52:27] So what will the graph look like? It
[02:52:30] will look something like this. Again,
[02:52:32] start point, end point, really similar
[02:52:35] to what a react agent was, right? But uh
[02:52:38] we have two agents in this case. We have
[02:52:39] a retriever agent and we have our main
[02:52:41] agent LLM, right? So, and it will have
[02:52:44] obviously a conditional edge, a loop,
[02:52:46] and everything. Again, we're bringing
[02:52:48] everything we've learned so far and
[02:52:49] merging them into one. And we're also
[02:52:51] going to be learning about a little bit
[02:52:53] about rag. Now, I'll assume you know
[02:52:55] what rag is. I'm not going to go too
[02:52:58] much in detail into like the
[02:52:59] nitty-gritty of it. But again, in the
[02:53:01] surface level, I will obviously explain
[02:53:03] what rag is about and everything. Okay.
[02:53:06] So, if you're excited, let's uh let's
[02:53:08] jump to the
[02:53:09] code. Okay. So, now you can see that
[02:53:12] I've already done all of the imports
[02:53:13] which we'll need. But you'll notice how
[02:53:16] there are these four imports which we
[02:53:18] haven't come across yet. Now, rather
[02:53:20] than explain them from the get- go, I
[02:53:22] will explain them as they come because
[02:53:24] it'll make more sense. uh it'll make
[02:53:25] more intuitive sense that way. Okay. So
[02:53:28] now I'm going to be loading our uh ENV
[02:53:31] file which contains all the API keys.
[02:53:34] And this time I'm going to be
[02:53:37] initializing our LLM differently. Well,
[02:53:39] slightly differently. It's the same LLM,
[02:53:41] but why did I say differently? Because
[02:53:44] I've passed in a new parameter called
[02:53:45] temperature. Now for those of you who do
[02:53:47] not know what temperature is, it's
[02:53:49] essentially a parameter which depicts
[02:53:51] how stochastic the model outputs how
[02:53:54] stoastic you want the model outputs to
[02:53:56] be. So because I've set it to be zero,
[02:53:59] temperature equal to zero makes the
[02:54:00] model output more deterministic.
[02:54:03] Similarly, if I had set the temperature
[02:54:05] to be one, the model output would have
[02:54:07] been more stochastic. Okay. So now we
[02:54:11] create the embedding
[02:54:13] model. And the embedding model uh is
[02:54:16] what's going to convert our text into
[02:54:18] vector embeddings. Right? Uh so this
[02:54:20] will be the layout for it. Now please
[02:54:23] note one important thing which is the
[02:54:25] embedding model has to be compatible
[02:54:27] with the LLM we're using. You can use
[02:54:30] whatever LLM you want but make sure the
[02:54:32] embedding model uh is compatible with
[02:54:35] it. For example uh let's say we're using
[02:54:37] GBD40 uh an open model but the embedding
[02:54:40] model we're using is from Olama some
[02:54:42] random model. Now that they wouldn't
[02:54:45] most likely they're not going to be
[02:54:46] compatible. Why? Because there's so many
[02:54:48] differences between them. One potential
[02:54:50] difference could be the vector
[02:54:51] dimension. So just a rule of thumb. Make
[02:54:54] sure the LLM and the embedding model is
[02:54:57] compatible. Okay. Awesome. So now we're
[02:55:01] going to specify the PDF part. So this
[02:55:03] is the stock market performance 2024
[02:55:05] PDF. And essentially this is just a
[02:55:07] document which I created which contains
[02:55:10] um a lot about the stock market
[02:55:12] performance. Okay. Uh I can show you
[02:55:15] that right now actually. So this
[02:55:17] contains nine pages and is just a
[02:55:20] document containing about some stock
[02:55:22] market details in 2024. Okay. Awesome.
[02:55:26] So now um in case you've specified the
[02:55:31] uh you have put the PDF in a wrong
[02:55:33] directory or if it can't find it uh this
[02:55:36] error will pop up. So again I've just
[02:55:37] put this for debugging purposes if you
[02:55:39] use the code which I provided on GitHub.
[02:55:42] Okay. Now this will load the PDF and you
[02:55:46] can see pi PDF loader is one of the
[02:55:48] imports which we made here. So again
[02:55:51] it's in the name and the common. It just
[02:55:53] simply loads the PDF. Okay. Uh and this
[02:55:58] try and accept command uh just checks if
[02:56:00] the PDF is there. And pages is equal to
[02:56:04] PDF loader.load. So this essentially
[02:56:07] says how many pages are there in the
[02:56:09] document. So you can see there's nine
[02:56:12] pages in our document. So if I run this
[02:56:15] command, if I run this, so clear
[02:56:20] python rag agent.py
[02:56:23] py it should say nine
[02:56:25] pages.
[02:56:27] So there we go. PDF has been loaded and
[02:56:30] has nine pages as expected. Right? Okay.
[02:56:33] Now it's time for the chunking process.
[02:56:35] Now what is chunking? First look at
[02:56:37] this. There are two parameters which
[02:56:39] I've specified. Chunk size which is
[02:56:41] a,000 and chunk overlap which is 200. So
[02:56:45] let's break this down a bit. Going back
[02:56:47] to our document. So chunk size was 1,000
[02:56:50] tokens. So let's say that this was a
[02:56:54] chunk for example. Okay, obviously
[02:56:56] that's not going to be a thousand
[02:56:57] tokens, but just as like uh
[02:57:00] demonstration purposes, let's assume it
[02:57:01] is. So this is saying as soon as you've
[02:57:04] reached 1,000 tokens, you create a new
[02:57:06] chunk. So let's say 1,000 tokens ended
[02:57:08] here. So this would be the start of a
[02:57:10] new chunk like such. Okay. And you keep
[02:57:12] going and going and going until the end
[02:57:14] of the document. But what if the what
[02:57:16] about the second parameter? The second
[02:57:19] parameter is specified overlap and
[02:57:21] that's essentially saying let me use it
[02:57:23] in a different color that your chunks
[02:57:25] consecutive chunks should have some
[02:57:27] tokens um which are which exist in both
[02:57:30] for example because it was 200 the
[02:57:33] second chunk is not going to start from
[02:57:34] here. It's actually going to start
[02:57:37] something like
[02:57:39] this. They're obviously going to be the
[02:57:41] same length uh in terms of tokens but
[02:57:43] they will have some tokens which will be
[02:57:46] in both chunks. So for example, this
[02:57:48] part will be in both cuz that's the
[02:57:50] overlap. 200 tokens to be precise. Okay,
[02:57:53] so that was just a brief overview of
[02:57:55] what chunks are in uh rag. Okay, so
[02:57:59] that's that part done. And again, this
[02:58:01] recursive character text splitter is one
[02:58:04] of the imports we did. Okay,
[02:58:08] so this text splitter um chunking
[02:58:12] process, we now apply it to all of the
[02:58:14] pages, all of our nine pages in our
[02:58:16] document. Okay.
[02:58:18] And this piece of code essentially
[02:58:22] saying this, the chroma vector database,
[02:58:24] we're going to be using a chroma vector
[02:58:26] database to store all of our vector
[02:58:27] embeddings, by the way. But the uh the
[02:58:31] place where we want our chroma vector
[02:58:33] database to be will be specified in this
[02:58:36] file path. And the collection's name
[02:58:38] will be called stock market. Now, you
[02:58:39] can specify it wherever you want
[02:58:41] obviously, but I've just specified it to
[02:58:43] be in the same
[02:58:44] folder. Okay.
[02:58:47] So this is just an if statement to make
[02:58:50] sure that uh if this is the first time
[02:58:53] we're running this command uh if we're
[02:58:55] running this file uh if this collection
[02:58:58] doesn't exist we will create the um
[02:59:02] collection in the specified directory.
[02:59:05] Okay, again not too hard yet. Now here
[02:59:09] comes a try except command u try accept
[02:59:11] block. So this is where we actually
[02:59:14] create the vector embedding uh where we
[02:59:16] create the chroma vector um
[02:59:19] database and these are just parameters
[02:59:21] which I specify. So for example, how I
[02:59:23] want the pages to be split, what
[02:59:25] embeddings to use, where to store it and
[02:59:27] the collection name. The collection name
[02:59:28] being stock market, right? And if there
[02:59:30] is an error, it will throw an error and
[02:59:32] if it's successful, it'll print on the
[02:59:34] terminal. Okay, awesome. So now we
[02:59:37] create something called a retriever. So
[02:59:40] the retriever is quite important in rag.
[02:59:42] It's well obviously the first part of
[02:59:44] rag retrieval augmented generation. So
[02:59:47] the retriever is what actually well
[02:59:49] retrieves the chunks the most similar
[02:59:51] chunks. Um the search type which we're
[02:59:54] going to use similarity. It's just the
[02:59:56] default anyway. Uh you don't really need
[02:59:57] to know how that works to be honest. But
[02:59:59] what you do need to know is this part.
[03:00:03] So in this code I have made sure that
[03:00:06] every time uh it goes the amount of
[03:00:09] chunks it uh outputs back is five. Why?
[03:00:14] Because k here is the amount of chunks
[03:00:16] to be returned. So I've set it as five.
[03:00:19] Now I'm pretty sure if we go to the
[03:00:21] actual documents here the default the
[03:00:24] default is four. Okay. So uh this is
[03:00:28] just a parameter which you can uh set.
[03:00:30] Now you don't want it to be too high of
[03:00:33] course or too low. So you want like a
[03:00:34] good middle ground and 405 is a good
[03:00:37] middle ground in my opinion. Okay. So
[03:00:39] now let's create our tool. So again we
[03:00:42] use decorator tool. And the tool's name
[03:00:45] is going to be this retriever tool. It
[03:00:47] will input it will take in a query and
[03:00:49] it'll output a string. So the dock
[03:00:52] string is as follows. This tool searches
[03:00:54] and returns the information from our
[03:00:56] document. Okay self-explanatory.
[03:01:00] uh and obviously we need to invoke it to
[03:01:03] the retriever. So whatever query we ask
[03:01:06] for example uh what was Apple's
[03:01:09] performance in 2024 that will be the
[03:01:11] query and that will be passed to our
[03:01:13] retriever which will grab all the chunks
[03:01:15] the most the top five most similar
[03:01:16] chunks. Okay. Now if we don't if there's
[03:01:20] nothing similar uh which it finds for
[03:01:22] example if I say something like uh who's
[03:01:26] Bob the builder something like that
[03:01:27] right obviously Bob the builder is not
[03:01:29] in this document uh so it will return as
[03:01:33] I found no relevance information in the
[03:01:35] document and uh this will be passed to
[03:01:37] our LLM agent okay if it does find it
[03:01:41] though what we'll do is we'll create an
[03:01:43] empty list and we will store all of the
[03:01:46] similarity
[03:01:47] um us the all of the chunks which it
[03:01:50] found and then return those results uh
[03:01:53] through this. Okay, still it's quite
[03:01:56] easy still uh and this piece of code
[03:02:00] we've already come across. There is only
[03:02:02] one tool. So we just bind that tool to
[03:02:04] our
[03:02:05] LLM. And this also code we have also
[03:02:10] we've uh done many times. It's the uh
[03:02:14] creation of the agent state. And again
[03:02:16] we're using our add messages reducer
[03:02:18] function. All of this we've covered many
[03:02:20] times so you should be quite familiar
[03:02:22] with it. Okay. So now we create the
[03:02:25] should continue function and the should
[03:02:26] continue function uh is going to be the
[03:02:29] underlying function between our
[03:02:30] conditional edge behind our conditional
[03:02:32] edge. So it will check if the last
[03:02:35] message contains any tool calls. If it
[03:02:37] does then we um proceed. If it doesn't
[03:02:40] then we'll just end
[03:02:44] right. Okay. So now we specify the
[03:02:47] system prompt. Now this system prompt is
[03:02:49] going to be quite big. So let me copy
[03:02:52] and paste it here. Now the reason is
[03:02:54] quite big is I want to specify as much
[03:02:56] information to the LLM so that it knows
[03:02:58] what to do. Right? So I've just said
[03:03:00] you're an intelligent AI assistant who
[03:03:02] answers questions about the document uh
[03:03:04] loaded into your knowledge base. Uh you
[03:03:07] can read the rest if you would like. But
[03:03:09] I've also written this. Please always
[03:03:11] site the specific parts of the document
[03:03:13] you use in your answers. This is really
[03:03:16] just to make sure it's not
[03:03:17] hallucinating. Right? because as we know
[03:03:19] hallucination is quite a big problem
[03:03:20] with LLMs. So this is just to make sure
[03:03:23] um hallucinations are kept to a bare
[03:03:27] minimum. Okay. All right. So now we
[03:03:31] create a dictionary of our tools and we
[03:03:35] now create the underlying function which
[03:03:37] will be our LLM agent. So this function
[03:03:40] will call the LLM with the current state
[03:03:42] and you can see it converts the messages
[03:03:44] to a list passes the system messages and
[03:03:46] passes it to our LLM which is defined
[03:03:49] like this and it will just return the
[03:03:52] messages aka the updated
[03:03:54] state. Okay, this should be like such.
[03:03:59] Okay, awesome. So now we create our
[03:04:02] second agent which will be the retriever
[03:04:03] agent which you saw on the in the graph
[03:04:06] which I showed you in the introduction.
[03:04:08] So the retriever agent executes the tool
[03:04:11] calls from the LLM response. So what is
[03:04:13] this code actually saying? Well, all in
[03:04:17] all, this massive piece of code really
[03:04:20] just says if there is a tool, if the
[03:04:23] tool name is within the is a proper
[03:04:26] specified tool, aka if it's retriever
[03:04:29] tool, then actually run it. If it's not,
[03:04:32] then we will output the result as input
[03:04:35] in incorrect tool name. Please retry and
[03:04:36] select the tool from list of available
[03:04:39] tools. It's just for checking if a if
[03:04:42] the tool which is decided from the LLM
[03:04:44] is valid or not. So that's all what this
[03:04:47] is doing. If it is valid, it will invoke
[03:04:49] it and we will store the results uh like
[03:04:52] this and we will return that. Okay.
[03:04:54] Again this should be agent state like
[03:04:59] such. Okay. So we've created all of our
[03:05:03] our two um AI agents now and now we're
[03:05:07] going to create the graph itself. So
[03:05:09] like how we've done initialize it
[03:05:12] through state graph and then we're going
[03:05:14] to add our two AI agents as nodes with
[03:05:17] their respective
[03:05:19] actions and we are now going to add the
[03:05:22] conditional edge. So which will be llm
[03:05:26] which will be start from l lm and the
[03:05:28] should continue function is the function
[03:05:30] which will be um the underlying function
[03:05:34] and this is a uh true false statement
[03:05:37] and this is the edge the set entry point
[03:05:39] all of this we've covered many times so
[03:05:41] again should be quite familiar to you
[03:05:44] and last but not least compile the graph
[03:05:48] and store it in a ragation okay one last
[03:05:51] thing though uh I've created
[03:05:55] this function and this function is just
[03:05:57] a function which allows us to keep
[03:06:00] asking questions to our graph and keep
[03:06:02] receiving qu uh answers back and if you
[03:06:05] want to exit we can write either exit or
[03:06:07] quit um and it's just a simple while
[03:06:10] loop that's all it is okay and it prints
[03:06:13] the
[03:06:13] answer okay so that's the actual code
[03:06:17] complete now we're going to test it and
[03:06:20] see uh if the if this is reliable or
[03:06:23] not. Okay. Okay. So, let's actually test
[03:06:26] this now um by doing python rag agent.
[03:06:31] py. Let's run this.
[03:06:35] Okay. PDF has been loaded and has nine
[03:06:38] pages. Created chromo vector data uh
[03:06:40] chroma database vector store. So, where
[03:06:43] is this stored? Well, you can see that
[03:06:45] this is uh by the way, this will all be
[03:06:47] on GitHub as well. But this is the
[03:06:49] Chroma database and its respective um
[03:06:52] bin bin files. Okay. And we can even
[03:06:56] view it.
[03:06:57] But it'll look something like that.
[03:07:00] Okay. But because this has been created,
[03:07:02] this is a good sign that everything is
[03:07:04] working. Okay. So, let's ask a simple
[03:07:06] question. Uh let's ask something
[03:07:11] like how was the S&P 500
[03:07:16] uh performing in 2024? Enter. So it's
[03:07:22] calling the retriever tool uh with the
[03:07:24] query this uh its result then puts that
[03:07:27] complete back to the model and the model
[03:07:29] has given us this. In 2024, the S&P 500
[03:07:32] delivered a total return of this with a
[03:07:34] 23% increase late 1990s and all of that
[03:07:37] stuff uh magnificent 7 and has given us
[03:07:39] the uh respective uh citations as well.
[03:07:42] Now, how can we verify this is uh
[03:07:44] correct? Let's
[03:07:45] see. So, notice
[03:07:49] how if you remember this part, the total
[03:07:52] return of approximately 25%.
[03:07:55] Well, the reason I prom I asked it for
[03:07:57] this is because that's exactly what uh
[03:08:00] over here it stated the benchmark
[03:08:02] roughly at 25% 23%. Uh remember this
[03:08:05] late 1990s part that's exactly what this
[03:08:08] is saying here as well and this was
[03:08:12] correctly defined in the first document.
[03:08:14] So this is clearly working now right it
[03:08:17] can't have made up this information. So
[03:08:18] that means our rag is successfully set
[03:08:20] up. Now I can ask as many questions I
[03:08:22] possib as I want now but now let's see
[03:08:26] if there is something which is not
[03:08:28] included in the rag. So for example we
[03:08:31] can say something like how did open AI
[03:08:34] perform in
[03:08:37] 2024 retrieve a tool called back to the
[03:08:40] model. Okay, now look at this. Uh if I
[03:08:46] do it like that, the documents do not
[03:08:48] provide specific information about
[03:08:49] OpenAI stock performance, which is true
[03:08:51] cuz OpenAI is not a publicly traded
[03:08:53] company. Uh and yeah, it got that
[03:08:56] correct. So no hallucination there. So
[03:08:59] you can clearly see that this is working
[03:09:02] uh completely fine. And that ladies and
[03:09:04] gentlemen is how you create a retrieval
[03:09:07] augmented generation graph in Langraph.
[03:09:11] Okay.
[03:09:12] Awesome. All right people. So that
[03:09:15] brings us to the end of this course and
[03:09:17] I hope you liked it and I hope you
[03:09:19] learned a lot about
[03:09:20] Langraph. Now although this course is
[03:09:22] finishing here, your journey in Langraph
[03:09:25] is just beginning. Just think about how
[03:09:27] many cool AI projects, AI agent systems
[03:09:29] you can make now. Maybe your own Javis
[03:09:31] as well. Now, if you have any further
[03:09:34] questions related to the course material
[03:09:37] or just things in general or just want
[03:09:38] to say hi, you can always message me on
[03:09:41] LinkedIn. With that being said, thank
[03:09:43] you so much for watching this course and
[03:09:45] I hope to see you in another course.
[03:09:47] Take care.
<!-- project: github.com/gonzoblasco/workspace_openclaw -->
