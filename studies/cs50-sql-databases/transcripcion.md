# Transcripción — Harvard CS50's Intro to Databases with SQL

- Fuente: https://www.youtube.com/watch?v=WXk7yDqsKxs
- Subtítulos automáticos `en-orig` (json3) vía yt-dlp 2025.10.14, 29.638 eventos crudos → 14.819 cues con timestamps
- Cobertura: último cue 11:08:36 sobre una duración de 11:08:48 (gap 12 s)
- ~107.654 palabras

---

[00:00:00] This course is CS50's introduction to
[00:00:02] databases using a language called SQL.
[00:00:04] This course is from Harvard University
[00:00:07] and is taught by Carter Zeni with help
[00:00:09] from Dr. David J. Men. In this course,
[00:00:12] you'll master the fundamentals of SQL,
[00:00:15] including how to create, read, update,
[00:00:17] and delete data. You'll learn to model
[00:00:19] real world scenarios by designing
[00:00:21] tables, normalizing data to reduce
[00:00:24] redundancy, and joining tables using
[00:00:26] primary and foreign keys. The course
[00:00:29] also covers how to automate queries with
[00:00:31] views, accelerate searches, with
[00:00:34] indexes, and connect your database to
[00:00:36] languages like Python. The curriculum
[00:00:39] begins with the portability of SQLite
[00:00:42] before introducing the scalable power of
[00:00:44] PostQL and MySQL all through assignments
[00:00:48] inspired by realworld data sets.
[00:00:53] [Music]
[00:01:07] Hello world. This is CS50's introduction
[00:01:10] to databases with SQL or SQL. My name is
[00:01:13] David Mailen
[00:01:14] >> and my name is Carter Zeni.
[00:01:15] >> CS50 itself is an introduction to
[00:01:17] computer science and along the way you
[00:01:19] learn about SQL and more. This course
[00:01:21] dives all the more deeply into SQL
[00:01:23] specifically and you can take it before,
[00:01:25] during, or after CS50 itself, whether
[00:01:27] you're a computer scientist, data
[00:01:29] scientist, programmer, or simply someone
[00:01:31] who's interested in databases. Now,
[00:01:33] we'll begin with a software called SQL
[00:01:35] light, which you can use to query a
[00:01:37] table of data, maybe a table of books,
[00:01:40] for instance. You will then graduate and
[00:01:42] work not just with one table, but
[00:01:44] multiple and see how to define
[00:01:46] relationships among them. Afterwards,
[00:01:49] you'll figure out how to design your
[00:01:50] very own database from scratch, learning
[00:01:53] about schemas and data types. And then
[00:01:56] you'll see how to add data to that
[00:01:58] database, how to insert, update, and
[00:02:00] delete some data all together. Soon
[00:02:03] after, you'll see how to write alternate
[00:02:05] views for your data, new ways of
[00:02:07] simplifying your data for yourself and
[00:02:09] for others. And then towards the end of
[00:02:11] the course, you'll see how to optimize
[00:02:13] your queries, how to reduce the time
[00:02:15] that they take, although at the cost of
[00:02:17] some space. And then finally, to cap it
[00:02:20] all off, you'll learn other DBMS's,
[00:02:23] database management systems like MySQL
[00:02:26] and Postgress that you can use to do all
[00:02:28] of this and more at a much bigger scale.
[00:02:31] Now, this is CS50.
[00:02:36] [Music]
[00:02:53] Well, hello one and all and welcome to
[00:02:56] CSA's introduction to databases with
[00:02:58] SQL. My name is Carter Zeni and in this
[00:03:01] course you'll learn how to represent,
[00:03:03] how to organize and manage, and how to
[00:03:06] ask questions of the data that's around
[00:03:07] you in your everyday life. But why learn
[00:03:11] those skills? Well, you may have heard
[00:03:13] it. So, we're living in the information
[00:03:15] age where we generate so much
[00:03:16] information, so much data by virtue of
[00:03:19] interaction with computers and with each
[00:03:20] other over the internet. Uh, you might
[00:03:22] think of, let's say, uh, Google keeping
[00:03:25] track of the sites you click on or the
[00:03:26] sites you search for. You could think of
[00:03:28] maybe the smartphone in your pocket or
[00:03:30] the smartwatch on your wrist, keeping
[00:03:32] track of health information, emails,
[00:03:34] text messages, and so on. You might even
[00:03:37] think of YouTube where you might be
[00:03:38] watching this same video keeping track
[00:03:41] of all the videos on their platform, the
[00:03:43] creators of those videos and even the
[00:03:44] comment you might leave on this video.
[00:03:48] So although we're living in this
[00:03:49] information age where there is so much
[00:03:51] data, so much information, we can use
[00:03:54] these new tools like database and SQL to
[00:03:56] interact with that information to store
[00:03:58] it and manage it. And although we're
[00:04:00] using some of these new tools, some of
[00:04:02] the other concepts we'll learn aren't
[00:04:03] actually so new. So here is a diagram
[00:04:07] from literally a few thousand years ago.
[00:04:10] And notice how this diagram has rows and
[00:04:14] columns. And this seems to store the uh
[00:04:17] stipens for workers at a temple some few
[00:04:19] thousand years ago. So given what you
[00:04:22] know based on your prior knowledge, what
[00:04:25] kind of name might you give this diagram
[00:04:27] with rows and with columns? What could
[00:04:31] we give a name to for this? So I'm
[00:04:34] seeing some ideas of a table, perhaps a
[00:04:37] spreadsheet as well. For our purposes,
[00:04:39] we'll call this a table where a table
[00:04:41] stores some set of information and every
[00:04:45] row in that table stores one item in
[00:04:48] that set where every column has some
[00:04:50] piece of information about that item,
[00:04:52] some attribute of that item. So here for
[00:04:54] example, we do have a table of workers
[00:04:57] at a temple. every row is one worker and
[00:05:00] every column is their stipend for a
[00:05:03] particular month. So I could take this
[00:05:06] idea of a table, this very ancient idea,
[00:05:08] and apply it to a more modern context.
[00:05:11] So let's say I'm a librarian for
[00:05:14] instance, and I want to organize my
[00:05:16] library. Well, here I have book titles
[00:05:19] and authors, and I could certainly use a
[00:05:21] table to store this information, but how
[00:05:23] might you propose I store this
[00:05:26] information? What could I do with my
[00:05:28] rows and with my columns if I have book
[00:05:31] titles and book authors?
[00:05:34] I see one thing I could do is probably
[00:05:36] organize my titles and my authors kind
[00:05:39] of next to each other like this. I could
[00:05:41] take my titles and my authors, put them
[00:05:43] right next to each other. So, I have
[00:05:44] Song of Solomon by Tony Morrison, Good
[00:05:46] Night Moon by Margaret Wise Brown. And
[00:05:48] notice here how each book is one row,
[00:05:51] but every row has two columns where two
[00:05:54] pieces of information for each book. I
[00:05:57] have a title for one column and an
[00:06:00] author for the other. And so together I
[00:06:02] have a table of books where every column
[00:06:05] tells me one piece of information and
[00:06:07] every row tells me one book in this data
[00:06:10] set.
[00:06:12] So thankfully now that we're living in
[00:06:14] this information age, we no longer have
[00:06:17] to use no longer have to use like stone
[00:06:19] tablets or perhaps pencil and paper to
[00:06:21] store our tables. We have software now
[00:06:23] like Apple numbers, Google Sheets and
[00:06:26] Microsoft Excel, but this isn't a course
[00:06:29] on Apple Numbers or Microsoft Excel or
[00:06:32] so on. It's actually a course on
[00:06:34] databases and on SQL. So feel free to
[00:06:37] raise your hand if you'd like. But why
[00:06:39] would we decide to move along from these
[00:06:42] spreadsheet softwares towards a
[00:06:45] database? What might that database give
[00:06:47] us that a spreadsheet might not give us?
[00:06:50] So I'm seeing a few ideas here and among
[00:06:52] them are some simplicity, some ability
[00:06:54] to organize some data. Um but there are
[00:06:57] a few other ideas we think about too for
[00:06:59] why move beyond spreadsheets and go
[00:07:00] towards databases. Now one of these is
[00:07:03] this idea of scale. So let's say you are
[00:07:06] a Google or an Instagram. You're trying
[00:07:08] to store not just tens of thousands of
[00:07:11] users or hundreds of thousands but
[00:07:12] literally millions of users or billions
[00:07:14] of users. And with that kind of scale,
[00:07:17] you might be better served by a database
[00:07:19] to store that much information.
[00:07:22] Another reason to move from spreadsheets
[00:07:24] to databases is this idea of being able
[00:07:26] to update data more frequently. Maybe
[00:07:29] you're a Twitter of the world. You're
[00:07:31] trying to have others tweet multiple
[00:07:32] times per second. Well, a database can
[00:07:35] handle that kind of capacity much better
[00:07:37] than a spreadsheet could alone. And a
[00:07:40] third reason to move beyond this might
[00:07:42] be speed. Let's say I'm trying to look
[00:07:45] up some piece of information in my
[00:07:46] database. Well, I could do that much
[00:07:48] faster with a database than I could with
[00:07:50] a spreadsheet. You could think of
[00:07:51] yourself using command F or control F to
[00:07:53] find a piece of information in your
[00:07:55] spreadsheet, kind of going one by one
[00:07:57] through the rows. A database gives you
[00:07:59] access to more kinds of algorithms you
[00:08:01] could use to search this data much
[00:08:02] faster ultimately. So these three
[00:08:05] reasons among others are those you might
[00:08:07] want to move beyond spreadsheets and
[00:08:09] start using databases.
[00:08:12] Now it's worth thinking first what is a
[00:08:16] database? We'll be talking about
[00:08:17] databases throughout this course. So
[00:08:18] what is a database? Well, a database is
[00:08:21] simply some way to organize your data
[00:08:24] such that you can actually create data,
[00:08:26] update data, read data, and delete data.
[00:08:30] And often these are our four
[00:08:31] interactions that we'll do with a
[00:08:33] database, like adding some data, looking
[00:08:35] at data, deleting data, and even
[00:08:37] updating it along the way. But the
[00:08:39] database isn't the only thing in our
[00:08:41] picture here. We also have a database
[00:08:44] management system, way to interact with
[00:08:47] our database. So you might think of
[00:08:50] perhaps writing a um program on your
[00:08:52] computer. You have some interface with
[00:08:54] which to write that program like VS code
[00:08:56] for instance or you might think of your
[00:08:58] own desktop on your own computer. You
[00:08:59] have icons such that interact with the
[00:09:01] underlying operating system. In the same
[00:09:04] way we can use this software called a
[00:09:06] database management system or a DBMS for
[00:09:09] short to interact with the database
[00:09:11] perhaps using a graphical interface or
[00:09:13] using a textual language too. Now there
[00:09:17] are a few uh varieties of database
[00:09:20] management softwares and these are a few
[00:09:22] of them here my SQL Oracle Postgress SQL
[00:09:26] and SQLite but this is a non-exhaustive
[00:09:28] list so let me also ask again what kinds
[00:09:31] of other database management systems
[00:09:33] have you perhaps heard of in this case
[00:09:36] I'm seeing one for Microsoft Access
[00:09:39] perhaps um MongoDB
[00:09:41] there are other kinds of software other
[00:09:43] companies out there that make these ways
[00:09:45] to interact act with a database. This is
[00:09:47] again a non-exhaustive list. Now, if you
[00:09:50] are a database administrator or maybe
[00:09:52] you're somebody who's making a choice of
[00:09:53] which software to use, you have a few
[00:09:55] trade-offs to consider. Let's say you
[00:09:58] might think of one being proprietary,
[00:10:00] for instance, costing money to work
[00:10:02] with. What you get for that money is
[00:10:04] additional support to actually implement
[00:10:06] your own database. On the other hand,
[00:10:08] you might have open-source software or
[00:10:10] free software to use stuff like
[00:10:12] Postgress SQL, MySQL, and SQLite. But
[00:10:15] the downside is you are then responsible
[00:10:17] for actually implementing that database.
[00:10:21] Another uh thing to consider too is that
[00:10:23] maybe some are going to be heavier
[00:10:26] weight than others more fully featured
[00:10:28] as a consequence but perhaps heavier
[00:10:29] weight requiring more computation to
[00:10:31] run. You could think of those like my
[00:10:33] SQL or post SQL being a little bit
[00:10:35] heavier weight but being more fully
[00:10:37] featured. Whereas SQLite down below will
[00:10:40] be a little lighter weight as the name
[00:10:42] might imply, but allow you to do most of
[00:10:44] the same work that these other softwares
[00:10:46] could allow you to do as well. And in
[00:10:49] this course, we'll actually be using
[00:10:51] SQLite for you to work with your own
[00:10:53] databases, but gradually we'll move on
[00:10:55] to MySQL and Postgress SQL too.
[00:11:00] So
[00:11:02] let me go ahead and talk about then SQL
[00:11:04] in this case. You might notice that in
[00:11:06] each of these MySQL and Postgress SQL
[00:11:08] and SQLite each of them have this idea
[00:11:11] of SQL in them and SQL is that language
[00:11:14] that we'll use to interact with our
[00:11:16] database. Now let me ask what does SQL
[00:11:19] stand for? Perhaps we talk about SQL or
[00:11:22] SQL but what might SQL stand for? So I'm
[00:11:27] seeing it might stand for structured
[00:11:28] query language which is good if you
[00:11:30] already know this but not to worry if
[00:11:31] you don't. So SQL does stand for
[00:11:34] structured query language. As we'll see
[00:11:36] in this course, it is structured. It
[00:11:38] does have some keywords you can use to
[00:11:40] interact with a database. And it is a
[00:11:42] query language. It can be used to ask
[00:11:44] questions of data inside a database.
[00:11:48] We'll see that this is the language we
[00:11:50] can use to create data, to read data, to
[00:11:54] update data, and delete data all with
[00:11:57] SQL in this case. And our next thing
[00:12:01] will be to talk about this idea of
[00:12:03] querying. So SQL is a query language.
[00:12:06] But what can we do with SQL? Well, the
[00:12:09] first thing we can do we'll focus on
[00:12:10] first in this course is writing queries.
[00:12:13] Trying to ask questions of data using
[00:12:16] SQL. Well, what kinds of questions could
[00:12:18] we ask? Well, you might imagine perhaps
[00:12:21] working at an Instagram or a Facebook
[00:12:23] trying to work as an engineer to figure
[00:12:25] out what kinds of posts are the most
[00:12:27] liked on your platform. That's a
[00:12:29] question you can answer with databases
[00:12:31] and with SQL. You might also think of um
[00:12:35] whether your numbers of daily users are
[00:12:36] growing or shrinking if you're working
[00:12:37] at a startup for instance. Even maybe
[00:12:40] might be working for something company
[00:12:41] like Spotify that could ask how could we
[00:12:43] play songs that are like those a user
[00:12:46] just played. This too is a question you
[00:12:48] can answer with databases and with SQL.
[00:12:53] Now, today we'll be focusing on this
[00:12:55] database of books and in particular
[00:12:58] books that have been long listed quote
[00:13:00] unquote for the International Booker
[00:13:02] Prize. The International Booker Prize,
[00:13:04] if you're not familiar, is a award given
[00:13:06] to books written around the world by
[00:13:08] authors from many countries. And it's
[00:13:10] designed to uh award uh books of fiction
[00:13:13] are particularly good in some cases. And
[00:13:15] every year the committee selects 13
[00:13:18] books to include on a long list for
[00:13:20] consideration for this prize. And our
[00:13:23] database then has 5 years worth of long
[00:13:26] lists for the International Booker Prize
[00:13:28] inside of it. We could use this database
[00:13:31] perhaps if we were a librarian trying to
[00:13:32] find books for our library or even as a
[00:13:36] a book reader, an avid reader myself,
[00:13:37] trying to find books to read that I
[00:13:39] could put on my own shelf overall. So,
[00:13:42] we'll look at this database, but we'll
[00:13:44] need a few tools in our toolkit,
[00:13:46] metaphorically, to actually interact
[00:13:48] with this database. And one of them is
[00:13:50] going to be Visual Studio Code. Visual
[00:13:53] Studio Code is an IDE, integrated
[00:13:56] development environment to write code
[00:13:58] and to edit files with. It's also often
[00:14:00] called VS Code. Now in VS Code, we'll
[00:14:05] also be able to use SQLite, this
[00:14:07] database management system or a DBMS for
[00:14:10] short to actually interact with that
[00:14:12] database. So we'll be using these two
[00:14:14] tools combined to work with this
[00:14:16] database of long listed books for the
[00:14:18] International Booker Prize. And although
[00:14:21] we'll be using it here, SQLite is not uh
[00:14:24] just used in this course. It's used in a
[00:14:26] variety of applications. You could think
[00:14:28] too of phone applications or SQLite is
[00:14:30] often used on those um devices that have
[00:14:32] much lower memory. You could think too
[00:14:35] of it being used on desktop applications
[00:14:37] to simplify the process of storing data
[00:14:40] there too. You could even think of it
[00:14:42] being used on websites to help store
[00:14:44] information the user submits via a form
[00:14:47] for example.
[00:14:48] So we'll jump into using SQLite but keep
[00:14:51] in mind that uh not just in this course
[00:14:53] you'll use it but also it's used in a
[00:14:55] variety of applications here too.
[00:14:59] So why don't we just jump right into
[00:15:00] things start using our uh environment
[00:15:03] and start using SQLite. So I'll go over
[00:15:05] here to my computer and I will open up
[00:15:07] let's say VS Code where here you can see
[00:15:11] I have my terminal environment and if
[00:15:13] you're familiar you can type things like
[00:15:15] ls to see the files that are in your
[00:15:18] current folder. So I'll type ls right
[00:15:20] here and I'll see this database called
[00:15:22] longlist db. Again working with books
[00:15:25] that have been long listed or considered
[00:15:28] for the international booker prize. So
[00:15:30] if I want to open up this file, I can
[00:15:34] use this command. Then this command is
[00:15:37] going to be called SQLite 3 or I can
[00:15:41] take some file that I have like long
[00:15:43] list.db and open it using this program
[00:15:46] called SQLite 3. Well, it's called
[00:15:49] SQLite 3 because this is the third
[00:15:50] version of the SQLite software. So let's
[00:15:54] try this in our terminal. I'll go back
[00:15:56] over here and I'll say SQLite 3. SQLite
[00:16:00] 3 long list db. And now I'll hit enter.
[00:16:05] And notice how my terminal prompt
[00:16:07] changes. It's no longer a dollar sign.
[00:16:09] It now says SQLite in front. This means
[00:16:12] I'm inside of my SQLite environment.
[00:16:15] So to clear things up, let me just clear
[00:16:17] my terminal. I can use L for this. And
[00:16:20] now I have just that prompt up top. And
[00:16:24] now a question I want to answer in this
[00:16:26] case first is what data do I actually
[00:16:29] have in my database? What data is
[00:16:32] actually here for me to look at and to
[00:16:34] ask questions about? Now for this
[00:16:37] question, I can use my very first SQL
[00:16:40] keyword which will be called select. So
[00:16:43] select is a way for me to select some
[00:16:46] rows in a table inside of my database.
[00:16:49] Using select I can get back certain rows
[00:16:51] or in this case perhaps all of them just
[00:16:53] to get a taste of what's inside. So
[00:16:56] let's try using select on this database
[00:16:58] to understand what rows we have in our
[00:17:01] table here. Let me go back to my
[00:17:03] computer into my SQLite environment and
[00:17:06] I will try this very first SQL keyword.
[00:17:09] I'll say select and I can use this star
[00:17:13] operator here to say select everything.
[00:17:15] I want every row and every column from
[00:17:19] this table.
[00:17:21] Now, it's not enough for me to simply
[00:17:22] say select star and end my query. I have
[00:17:26] to tell SQL which table do I want to
[00:17:28] select rows from. In this case, I know a
[00:17:31] table is called long list. So, I'll say
[00:17:33] select star from long list quote
[00:17:37] unquote. And to end my query, I'll say
[00:17:40] semicolon. And then finally, I can hit
[00:17:43] enter. And notice how I get a lot of
[00:17:46] data back, right? This is a lot of data
[00:17:48] all at once. But it's because my
[00:17:50] terminal is a little bit small. There's
[00:17:51] a lot of rows and columns here. So I
[00:17:53] could probably simplify this just a
[00:17:54] little bit. Instead of saying select
[00:17:57] star, I could also select a particular
[00:18:00] column from my table. I could say for
[00:18:03] instance, select let's say just the
[00:18:05] title column from my database from my
[00:18:09] table like this. I just know already
[00:18:12] that there is a column called title. So
[00:18:15] now I'll try this instead. Not select
[00:18:17] star, but select title instead. I'll hit
[00:18:19] enter. And now this looks a little bit
[00:18:21] better. I can see the titles inside of
[00:18:25] this table from top to bottom.
[00:18:29] Now the neat thing here is I can select
[00:18:32] more than one column, too. Let's say I
[00:18:34] don't want just the titles. I want
[00:18:36] titles and authors in my search. Well, I
[00:18:38] could do that as well. Let me try this.
[00:18:41] Select not just title quote unquote, but
[00:18:44] then I'll say comma and some new column
[00:18:47] to select. I'll select also the authors
[00:18:50] from this table. And I'll select them
[00:18:53] from the long list table like this. Now
[00:18:56] I'll hit semicolon to end my query. Hit
[00:18:59] enter. And now I'll see a variety of
[00:19:02] columns here. In particular, the title
[00:19:04] and the author column.
[00:19:07] Now, this is going to back all of my
[00:19:08] columns so far, and there is a way for
[00:19:10] me to get back just some of them later
[00:19:12] on that we'll see. But for now, let's
[00:19:15] ask what questions do you have on this
[00:19:18] SQL select statement and how we're
[00:19:20] getting back these rows.
[00:19:22] >> Do I need to use the quotes around the
[00:19:24] words like you are?
[00:19:26] >> Yeah, great question. Do I have to use
[00:19:28] quotes around the words like I am? In
[00:19:31] general, it's a good practice to use
[00:19:33] these double quotes around your table
[00:19:35] names and your column names. These are
[00:19:37] called SQL identifiers. Later on, we'll
[00:19:40] see we'll also have strings in SQL.
[00:19:43] Strings being collections of characters
[00:19:45] we can use. For those, we'll simply
[00:19:47] single quote them to note the difference
[00:19:48] between a string and an actual column
[00:19:51] name. So, good style convention here to
[00:19:54] use double quotes for column names and
[00:19:56] single quotes for string names.
[00:19:59] Other questions, too?
[00:20:01] Okay, I wanted to know uh where did we
[00:20:03] take all this information from? Like uh
[00:20:06] this data I don't know this list of book
[00:20:10] where did we take all this information
[00:20:12] from?
[00:20:13] >> Yeah, great question. Where do we take
[00:20:14] this information from? So some of this
[00:20:16] data is publicly available. In fact, if
[00:20:18] you look at the Booker Prize website,
[00:20:20] you can find a set of long listed books
[00:20:22] over the years. In this case, we have
[00:20:24] books from 2018 to 2023. We'll also see
[00:20:28] later on this table has data on the
[00:20:31] ratings of those books and the number of
[00:20:33] votes that were given to those books.
[00:20:35] That data is from Goodreads, this site
[00:20:37] that aggregates reviews from people like
[00:20:39] you, people like me who rate books
[00:20:41] online. So, we've taken data from a
[00:20:43] variety of sources and combined it into
[00:20:45] one here. Let's take one more question
[00:20:48] too from Vinak.
[00:20:50] >> Yeah. So, I wanted to ask regarding the
[00:20:52] syntax of what you used in the terminal.
[00:20:56] So is the whole SQL light tree is case
[00:21:00] sensitive because while using the syntax
[00:21:02] you used capital letters whereas can we
[00:21:05] use like small case letter as well?
[00:21:08] >> A great question. So here I used capital
[00:21:10] letters for SQL keywords and lowercase
[00:21:13] for my table names and column names. Do
[00:21:15] I have to do that? I in some cases do
[00:21:18] some cases don't. I think I could use
[00:21:20] lowercase for these SQL keywords but
[00:21:22] it's not very good style for instance.
[00:21:24] So let me just show you an example of
[00:21:26] this while I go back to my computer. So
[00:21:28] the question again was can I use
[00:21:31] lowercase for SQL keywords? I think I
[00:21:34] could but the question is should I and
[00:21:36] and probably not. So let me try this.
[00:21:38] I'll say select let's say title from I'm
[00:21:41] in the habit of uppercasing it. So I'll
[00:21:42] say from and lowercase
[00:21:45] long list like this semicolon hit enter.
[00:21:48] And that still works. But the problem
[00:21:51] you might run into is someone who's
[00:21:53] reading your query, particularly a long
[00:21:55] one, might want to know what are the SQL
[00:21:57] keywords and what are your column names
[00:22:00] and other identifiers here. By
[00:22:02] capitalizing your SQL keywords, you can
[00:22:04] make it clear that this is a SQL keyword
[00:22:07] and not some other name overall.
[00:22:11] Okay, so let's keep going. And we saw
[00:22:13] just a little bit ago that we could
[00:22:14] select title from long list and we would
[00:22:18] get back a whole list of titles.
[00:22:20] Literally all the titles that are in
[00:22:22] this database. But it's often maybe good
[00:22:26] practice for me to not look at all the
[00:22:28] data. Like imagine if we had millions of
[00:22:30] rows in this in this column, but only to
[00:22:32] get back some take like a peak of what's
[00:22:34] inside this database. And for that I
[00:22:37] could use this other SQL keyword, this
[00:22:39] one called limit. So limit as its name
[00:22:43] might imply limits the number of queries
[00:22:45] or the number of rows I get back from my
[00:22:48] query. I could say limit three for
[00:22:50] instance or limit five to get back only
[00:22:52] the top three or the top five rows from
[00:22:55] my table. And let me ask folks if I
[00:22:57] wanted to peak in this data set how many
[00:23:00] rows should I try to limit it to?
[00:23:03] I could say select title from let's say
[00:23:06] long list but limit to what number?
[00:23:10] I'm seeing 10. So, let's try 10 first.
[00:23:12] I'll go back to my computer. I'll come
[00:23:14] back over here and I'll say why don't I
[00:23:16] select title,
[00:23:18] select title from long list. But now,
[00:23:22] instead of hitting semicolon, I will
[00:23:25] instead say limit 10 semicolon and I'll
[00:23:29] hit enter. Now, I see only the first 10
[00:23:33] rows in my data set. Handy for peeking
[00:23:36] in at the top of my data set here too.
[00:23:39] Let me try not just 10 but five. So I'll
[00:23:41] say select title from long list limit
[00:23:47] five semicolon. This then gives me just
[00:23:51] the top five titles in my database just
[00:23:55] in whatever order they were added to my
[00:23:57] table. I'll see them in that order here
[00:23:59] too.
[00:24:01] So using limit we can actually um try to
[00:24:04] get back a certain number of rows. But
[00:24:07] this isn't quite that interesting. It's
[00:24:10] good for peing your data set. I think
[00:24:11] we've answered that question of what
[00:24:12] data do we have. But let's say we want
[00:24:15] to make more advanced queries. We want
[00:24:17] to find the books that were nominated in
[00:24:18] 2023 or perhaps books by a certain
[00:24:21] author. Well, for that we could use this
[00:24:23] next SQL keyword. This one called where.
[00:24:26] So where allows me to get back not all
[00:24:31] rows but only some rows where some
[00:24:34] condition is true. So where is often
[00:24:38] combined with other conditions to make
[00:24:40] sure I only get back some rows where
[00:24:43] that condition is true. Let's try
[00:24:46] looking at that in SQLite to get a feel
[00:24:47] for what it can do for us here. So I'll
[00:24:50] go back to my where and I will then go
[00:24:55] back to SQLite here uh control L to
[00:24:58] clear my terminal and I'll then try this
[00:25:00] query. I'll say select title. Select
[00:25:04] title. And why don't we also select
[00:25:07] author along the way. Two columns here.
[00:25:10] And I'll select them from my long list
[00:25:12] table. But I don't want all rows. I only
[00:25:15] want let's say those titles and authors
[00:25:18] that were long listed in 2023.
[00:25:21] So I'll do this. I'll say where the year
[00:25:24] column is equal to 2023.
[00:25:28] And notice here how 2023 is not in
[00:25:31] quotes because it is an actual number,
[00:25:33] an integer. So I don't need to quote it
[00:25:36] like I would a string, some collection
[00:25:37] of characters, or a table or column
[00:25:40] name. So I'll hit enter here. And what
[00:25:43] do I see? Well, I see only those books
[00:25:45] that were nominated in 2023.
[00:25:48] Let's try this again. I might try not
[00:25:51] just 2023. I might try 2022.
[00:25:55] Like this. Hit semicolon. Now I'll see
[00:25:58] those books nominated in 2022. I could
[00:26:01] keep going. I could say why not 2022?
[00:26:04] Why not 2021? Now I have all those books
[00:26:07] nominated in 2021.
[00:26:10] So this is handy. We can set things
[00:26:13] equal to or not equal to to make some
[00:26:15] condition here. And we also have others
[00:26:18] we could use. We saw equals just now,
[00:26:20] but we similarly have not equals. And we
[00:26:23] have this kind of obscure operator down
[00:26:25] here. This one being also equivalent to
[00:26:28] not equals as we'll see in just a
[00:26:30] minute. But let me first ask now what
[00:26:33] questions do we have on how to use where
[00:26:36] or using select so far?
[00:26:38] >> What are the subsets of SQL?
[00:26:41] >> A good question. Are there subsets of
[00:26:42] SQL? So um there are in fact SQL or SQL
[00:26:47] was defined by the I believe it's the
[00:26:49] ANZI like standard corporation. They
[00:26:51] have a whole set of the SQL language
[00:26:53] that is like the official version of it.
[00:26:55] you might be able to use some subset of
[00:26:57] that version with the database
[00:26:59] management system that you actually use.
[00:27:00] So for SQLite, we're using a subset of
[00:27:03] SQL that works with SQLite. Similarly,
[00:27:05] if you were using another software like
[00:27:07] Postgress SQL or MySQL, you could use
[00:27:09] another subset there too.
[00:27:12] Let's take another question from Teaos
[00:27:15] perhaps.
[00:27:16] >> Sir, I want to know that can we add 2022
[00:27:19] and 2021 in a terminal?
[00:27:22] >> Yeah, good question. Could I um perhaps
[00:27:24] try to filter by both and by 2021 and
[00:27:27] 2022? I could do that and we'll see that
[00:27:30] in just a moment here. So let's keep
[00:27:31] going and exploring some other options
[00:27:33] with not equals and then we'll see how
[00:27:34] we can combine conditions using where
[00:27:37] to. So let's go back and let's focus
[00:27:40] first on trying to use these not equal
[00:27:43] operators. We saw the exclamation point
[00:27:45] equals and this greater than less than
[00:27:47] sign put together. So let's try a few of
[00:27:50] those. Let's say I want to find books
[00:27:52] that are written by um a certain author.
[00:27:55] Well, I could use equals for that. But
[00:27:57] let's say I also want to find books that
[00:27:59] are not written in a hardcover format.
[00:28:02] They kind of tend to be more expensive
[00:28:03] and so on. So, I don't want hardcover
[00:28:05] books. Well, I could try a query like
[00:28:07] this. I could say select title and
[00:28:11] format where format is either hard
[00:28:13] coverver or paperback from my long list
[00:28:16] table. And now I'll say where the format
[00:28:21] is not equal to hard cover semicolon. So
[00:28:25] notice here I'm using single quotes for
[00:28:28] hard cover. This is a string. It's not a
[00:28:31] table name or a column name. It is just
[00:28:33] a string. So I'm using single quotes
[00:28:35] here. Everything else though like
[00:28:38] format, long list, title, etc. Those are
[00:28:41] all table names or column names. So
[00:28:44] again I'll hit enter. And now I'll see
[00:28:46] that these are all in paperback
[00:28:49] according to my table. I've omitted
[00:28:51] those that are hard cover. Well, I could
[00:28:54] also use in this case the kind of
[00:28:57] greater than or less than sign put
[00:28:58] together to say not equals as well. Let
[00:29:01] me just hit the up arrow on my computer
[00:29:03] to sort of reveal what I just previously
[00:29:04] typed. I'll then tab back over and say
[00:29:08] not exclamation point equals but less
[00:29:11] than and then greater than. Hit enter
[00:29:14] now and I should see the very same
[00:29:16] results. But all I did was change this
[00:29:18] operator from exclamation point equals
[00:29:20] to less than and greater than. It tends
[00:29:23] to be that the exclamation point equals
[00:29:25] is the more common operator in this
[00:29:27] case, but they do the very same thing.
[00:29:31] Now, one more keyword I could use here
[00:29:33] that's worth mentioning is this keyword
[00:29:36] called not. So here I was able to use
[00:29:39] exclamation point equals or the less
[00:29:41] than or greater than sign to say not
[00:29:43] equals. But I could also negate a
[00:29:45] condition using not. So let's try using
[00:29:48] this one in our SQLite terminal too.
[00:29:51] I'll go back over here and I'll bring
[00:29:55] back my SQLite terminal. I'll say let's
[00:29:58] do not this operator here but instead
[00:30:01] use not. So I might in front of where
[00:30:05] say where not format equals hard cover.
[00:30:11] So I have a condition format equals hard
[00:30:13] cover. But now I'm going to negate it.
[00:30:16] Take the opposite of it and get back the
[00:30:18] very same results here too.
[00:30:22] Okay.
[00:30:24] So to the question earlier how we can
[00:30:26] combine these conditionals. Let's try
[00:30:29] that here in just a minute. So, let's
[00:30:31] say I wanted to find the books that were
[00:30:35] not just written in 2022 or 2023 alone,
[00:30:39] but all the books together. Well, for
[00:30:41] this, I could use a few other SQL
[00:30:43] keywords that might be a little familiar
[00:30:45] to you, too. Let's try looking at some
[00:30:48] of these over here. So, here we have
[00:30:51] these called and, or these parentheses
[00:30:55] here, too. So, using and and or I can
[00:30:58] change condition. I can chain
[00:31:00] conditionals. I can put them together to
[00:31:02] make a more complex conditional, a
[00:31:04] compound condition. And I could also use
[00:31:07] these parentheses to symbolize that this
[00:31:09] condition should come first and then
[00:31:11] some condition should come afterwards as
[00:31:13] well. So let's try these in SQLite as
[00:31:16] well. I'll go back to my computer and
[00:31:18] again our goal is to find not just books
[00:31:20] in 2022 or 2023, but books that work
[00:31:24] across those years as well. So I'll in
[00:31:27] this case say select let's go for title
[00:31:31] and author from my long list table. Now
[00:31:35] I'll say where the year is 2022 as we
[00:31:40] did before or perhaps the year is 2023.
[00:31:46] And notice how my query is kind of
[00:31:48] wrapping around my terminal. I could
[00:31:50] leave it like this or if I backspace
[00:31:53] just a little bit I could hit enter and
[00:31:57] now I'm on a new line to continue my
[00:32:00] query. So here I'll say or the year is
[00:32:04] 2023
[00:32:06] and now my query is done. So I'll hit
[00:32:08] semicolon and I should see those books
[00:32:11] published in or nominated in 2022 or
[00:32:16] 2023.
[00:32:18] Let's try a few more here. Let's try
[00:32:20] using our parenthesis as well. Maybe I
[00:32:23] want not just these books, but also
[00:32:25] those that are formatted in a hard
[00:32:27] coverver format. So I'll say clear my
[00:32:30] terminal, control L again, and select
[00:32:33] title
[00:32:34] as well as let's say format
[00:32:38] from my long list table. And now I'll
[00:32:42] hit my new line to sort of extend my
[00:32:44] query without wrapping it around my
[00:32:46] terminal. I'll hit enter and I'll say
[00:32:48] where the year is 2022
[00:32:52] or the year is 2023. That's one
[00:32:57] condition and I can denote that with a
[00:32:59] single set of parenthesis here. I also
[00:33:02] want it to be true that the format is
[00:33:06] not hard cover.
[00:33:09] So now I'm adding another condition in
[00:33:11] here. Now I'll say semicolon, hit enter,
[00:33:14] and I'll get back only those books are
[00:33:17] published in the paperback format in
[00:33:20] 2022 and 2023.
[00:33:25] Okay, so let me pause again and ask if
[00:33:28] there are any questions so far on how
[00:33:29] we've been using where and select and
[00:33:34] other conditions as well.
[00:33:36] I would like to know about uh the uh we
[00:33:41] can able to list out the top titles
[00:33:43] available
[00:33:45] database like you have mentioned the
[00:33:47] title order where we can know about it
[00:33:51] uh what are the titles available in the
[00:33:53] database using command to know
[00:33:55] >> yeah so here I've been using these
[00:33:57] column names called title and author and
[00:33:59] I think the question is how would I know
[00:34:00] that I have these columns well as we'll
[00:34:03] see in future times together I'll be
[00:34:05] able to actually look at the schema of
[00:34:07] my database. What columns are inside of
[00:34:09] it. For now, just take it on, you know,
[00:34:11] you know, my my own word that I knew
[00:34:13] what was inside this database before I
[00:34:15] actually started querying it. We'll see
[00:34:16] later on how you can take a database,
[00:34:18] understand the columns you have there,
[00:34:20] too. A good question. Let's jump into
[00:34:22] some more queries. Then I'll go back to
[00:34:24] my computer and let's see what else we
[00:34:26] could do with these conditions. Well,
[00:34:29] not only could I try to make compound
[00:34:32] conditions, I could also try to find,
[00:34:35] let's say, which data is missing. So, I
[00:34:38] know in this table I have not just
[00:34:41] authors of books, but translators of
[00:34:44] those books. Often books for the
[00:34:46] international book of Prize were
[00:34:47] translated from some other language into
[00:34:50] English. But some weren't, or at least
[00:34:53] they didn't have a translator that was
[00:34:54] separate from the author. So to think
[00:34:57] about what data is missing from our
[00:34:59] table, we should introduce this new
[00:35:00] idea. This one called null. So I'll walk
[00:35:05] over here and we'll see that we have
[00:35:06] this type called null where this means
[00:35:09] that this value doesn't exist. It's not
[00:35:11] in our database. We can actually put
[00:35:14] together a condition around this idea of
[00:35:17] null, something not being there. We
[00:35:20] could use is null to figure out if a
[00:35:22] value is null. It's not there. It's
[00:35:24] missing from our database. or is not
[00:35:27] null, meaning that it actually is there.
[00:35:30] So, I'll go back to SQLite and show you
[00:35:32] what we could do with some of these um
[00:35:34] concepts here. Let me go back to my
[00:35:36] terminal and let's say I do want to find
[00:35:39] those translators that don't exist in my
[00:35:41] database. Well, I could use select,
[00:35:44] let's say, title and translator from my
[00:35:49] long list. And I want to make sure that
[00:35:52] these translators are null. they don't
[00:35:55] exist. So I'll say where translator is
[00:35:59] null semicolon. Now I'll hit enter and I
[00:36:03] should see two books titles are the
[00:36:05] perfect nine and the enlightenment of
[00:36:06] the green gauge tree. But notice how
[00:36:08] over here this value is null. It doesn't
[00:36:11] exist in my table. I could conversely
[00:36:15] find those books that do have
[00:36:17] translators using is not null. And I
[00:36:19] will try this one again. But in this
[00:36:22] case, I'll say
[00:36:24] where translator is not null semicolon.
[00:36:29] And I'll hit enter. And now let me just
[00:36:32] zoom out just a little bit. I can see
[00:36:35] that I have both titles on the left hand
[00:36:38] side and translators on the right hand
[00:36:41] side. All of these actually exist. These
[00:36:43] are books that did have translators in
[00:36:46] this case. So a good way to find data
[00:36:48] that's missing in your table using null
[00:36:51] or is not null. So let's come back over
[00:36:54] here and figure out what more we could
[00:36:56] do with some of these queries. We've
[00:36:58] kind of exhausted our work with um some
[00:37:01] of our you know conditions like chaining
[00:37:03] them together and using null and so on.
[00:37:05] But one more thing we could do is trying
[00:37:08] to use this idea of matching some kind
[00:37:10] of pattern in my database. So maybe I'm
[00:37:14] a uh you know book reader and I want to
[00:37:16] find a book with the word love somewhere
[00:37:19] in the title. Well, for this I could use
[00:37:21] another keyword. This one called like.
[00:37:25] So like is a good keyword to use when I
[00:37:28] want to roughly match some string in my
[00:37:31] database. Let's say I want to look at
[00:37:33] book titles and find if some word exists
[00:37:36] in that title. I could use like for
[00:37:38] that. And like becomes powerful when you
[00:37:41] combine it with these other operators,
[00:37:43] namely this percent sign and this
[00:37:45] underscore. The percent sign can match
[00:37:48] any character around a string I give it.
[00:37:51] And the underscore can match any single
[00:37:53] character that I pass in with my string.
[00:37:56] It's probably best shown with an
[00:37:58] example. So let me show you some in my
[00:38:00] terminal here. I'll walk back and again
[00:38:03] we'll try to find these books that have
[00:38:05] love somewhere in the title. So I'll say
[00:38:09] in this case select let's say title from
[00:38:12] long list. But I don't want all titles.
[00:38:15] I only want those that have love
[00:38:17] somewhere in this title. So I'll say
[00:38:20] where title like let's say percent love
[00:38:27] percent semicolon. Now before I run this
[00:38:30] let me explain what this is doing. I
[00:38:33] have here a select query asking for the
[00:38:37] title column from my long list table.
[00:38:40] But I'll only get back those rows where
[00:38:43] title is like percent love percent.
[00:38:47] Well, what does that mean? Well, the
[00:38:48] percent remember matches any string of
[00:38:51] characters. It could match ABC 1 2 3. As
[00:38:54] long as it some any string of characters
[00:38:56] comes after and has love, I could match
[00:38:59] that uh value here. Similarly, the
[00:39:01] percent sign after says anything can
[00:39:04] come after love as long as love is
[00:39:07] somewhere in the middle. So, anything
[00:39:09] before, anything after, but so long as
[00:39:11] love is just somewhere in there, I'll
[00:39:13] get it back. So, let me try running this
[00:39:15] query then and come back over here. I
[00:39:18] will hit enter on my query and I'll see
[00:39:21] I get back four books, Love in the Big
[00:39:23] City, More Than Love My Life, and so on.
[00:39:26] So notice how if I come back over here
[00:39:29] that each of these titles has love
[00:39:31] somewhere in it. For this one, I matched
[00:39:34] love up front and then had any string of
[00:39:36] characters coming after it like this.
[00:39:38] For this one, I had more than I love my
[00:39:41] life. Uh some string before it and then
[00:39:43] afterwards any string after it. Love is
[00:39:46] somewhere in the middle. Let me show you
[00:39:49] another example too where we use percent
[00:39:51] in a different way. Let's say I want to
[00:39:54] find only those books that have the at
[00:39:57] the very beginning of the title. Let me
[00:39:59] try this. I'll say select title from
[00:40:03] long list. Then where let's say the
[00:40:08] title is like
[00:40:12] the percent semicolon.
[00:40:15] Now I've changed something up. I have
[00:40:18] not percent in front and behind but only
[00:40:21] after the 'the'. So in this case I'll
[00:40:25] get back not anything that has the in
[00:40:27] the title wherever but now the at the
[00:40:30] very beginning of this string and I see
[00:40:33] perhaps a a style mistake. Let me ask
[00:40:35] the audience what style mistake did I
[00:40:38] just make when I typed in this query. So
[00:40:41] I'm seeing maybe I used double quotes
[00:40:43] when I should have used single quotes.
[00:40:45] So let me come back and fix that first.
[00:40:47] I'll come back over here and again by
[00:40:49] convention we tend to use single quotes
[00:40:52] for our strings. So let me fix that
[00:40:54] right here. And now let me run this
[00:40:56] query to see what we get back. I'll hit
[00:40:58] enter and I'll see only those books that
[00:41:01] begin with the.
[00:41:04] Now let me show this query again though.
[00:41:08] This was our query here. Knowing what we
[00:41:11] know about the percent sign,
[00:41:15] what other titles might I accidentally
[00:41:17] get back by running this query? I have
[00:41:21] the percent, but what other words might
[00:41:24] actually begin these book titles? If I
[00:41:27] were to run this query here, we saw only
[00:41:30] those with 'the', but if I had other
[00:41:31] book titles, what might I get back? So I
[00:41:34] might get back those book titles that
[00:41:36] have not just the at the beginning but
[00:41:38] also let's say there or they or so on.
[00:41:42] There are many uh words that begin with
[00:41:43] th e. And if I have the percent sign
[00:41:45] right after it, I might match one of
[00:41:47] those words like y or re e or so on. So
[00:41:51] I didn't have any of those titles in
[00:41:52] this database, but you could imagine a
[00:41:54] different database where I have that
[00:41:56] kind of data.
[00:41:58] Let's fix this then. I say I want to
[00:42:01] match not just 'the' butthe' in a space
[00:42:04] and match any characters after that to
[00:42:06] make this query better designed in this
[00:42:09] instance.
[00:42:11] Okay. So let me pause here then and ask
[00:42:13] what questions we have on using percent
[00:42:17] along with like.
[00:42:19] >> Can we use 2% signs for between two
[00:42:23] words?
[00:42:24] >> Yeah, I think so. So let me go back to
[00:42:25] my kernel here and let me try to answer
[00:42:27] this question. So, can we use two
[00:42:29] percent signs to say something's between
[00:42:31] two words? So, let me say this. I'll go
[00:42:34] with um select let's say title from long
[00:42:39] list where maybe the title has something
[00:42:45] like maybe it begins with 'the'. So I'll
[00:42:47] say where title like
[00:42:50] uh title like 'the' and then I'll take
[00:42:54] any set of characters afterwards but I
[00:42:57] want to have love also in here too. So
[00:42:59] I'll say love and then I'll take any
[00:43:02] other characters after it percent again
[00:43:06] single quote semicolon. Now I don't know
[00:43:09] if I have any books that actually fit
[00:43:11] this search but I could say the percent
[00:43:16] love percent to mean give me back any
[00:43:18] title that has the at the beginning then
[00:43:20] any words or characters then love then
[00:43:23] any words or characters after that. I'll
[00:43:25] hit enter and I see I don't have any
[00:43:28] books that fit that kind of description,
[00:43:30] but I if I did, I would see them here
[00:43:32] with 'the' at the beginning and love
[00:43:34] somewhere in the title.
[00:43:37] All right, so let's keep going. Let's
[00:43:38] focus not just on this percent sign, but
[00:43:42] also on this underscore. So if I want to
[00:43:44] find let's say I don't know what a
[00:43:47] particular character is in my title I
[00:43:50] could use this underscore to match any
[00:43:51] particular character not any string of
[00:43:54] characters but any single character too.
[00:43:56] So let's try this in our terminal and
[00:43:59] there is a book uh this one called py
[00:44:02] and I actually keep forgetting how it's
[00:44:04] spelled. I don't know whether it's p i e
[00:44:07] or p y r e. It could be either one but I
[00:44:10] want to find it in my database. So let
[00:44:13] me try this. I'll say select let's say
[00:44:15] title from long list where in this case
[00:44:20] title is like well I know that it starts
[00:44:23] with a P and I don't know if this is an
[00:44:26] I or a Y but I'll at least leave it as
[00:44:29] an underscore now to say it could be any
[00:44:31] character here. Then I'll say re
[00:44:36] sing single quote semicolon. And now I
[00:44:39] could try hitting enter and I'll see I
[00:44:41] get back this title called py. So notice
[00:44:45] in this case that the underscore is
[00:44:47] matching literally any single character.
[00:44:50] This could be a y, it could be an i, but
[00:44:52] in this case I have this y here.
[00:44:56] Okay, let me go back and let's actually
[00:44:58] ask in this case what questions we have
[00:44:59] on using like with these single
[00:45:02] underscores if any.
[00:45:04] >> Yeah. So Carter, I wanted to ask you
[00:45:06] that as you use the underscore sign
[00:45:08] here, so can we for multiple characters,
[00:45:11] can we use multiple underscores in order
[00:45:13] to find something in the database?
[00:45:16] >> A great question. Could we use more than
[00:45:17] one underscore to try to find some
[00:45:19] characters in our database? You
[00:45:21] absolutely could. So let me try that
[00:45:22] myself. I'll go back to my terminal and
[00:45:26] let me try to find a book title this
[00:45:27] could work with. I'll say maybe select
[00:45:30] title from long list to get back all the
[00:45:33] books in this table. I'll hit semicolon
[00:45:36] and maybe I will go with h
[00:45:41] um let's try this one uh called till.
[00:45:44] Well, maybe I want to just find the
[00:45:46] titles that have a Y or an I in here,
[00:45:49] but I also don't know if it's one L or
[00:45:52] maybe two L's for instance. Let me go
[00:45:53] back and try this. I'll say select let's
[00:45:56] say title from long list where my title
[00:46:01] is like I know it begins with a T. I
[00:46:04] don't know if this is a Y or an I. And
[00:46:07] maybe I know that it has maybe one or
[00:46:10] two characters after it. So I'll try
[00:46:12] this one. Now I have three underscores,
[00:46:15] single underscores. So match any book
[00:46:17] title that has T and then any three
[00:46:21] individual characters after it. I'll hit
[00:46:23] enter. And I'll see I get back till this
[00:46:26] is the only title that has T and then
[00:46:29] three characters after it. I could try
[00:46:32] to get better with this. I could say
[00:46:34] maybe I'll accept you know five or six
[00:46:35] characters like that. Hit enter and I'll
[00:46:38] see whoops I didn't complete my query
[00:46:40] here. Let me just try it from the top
[00:46:41] again. I'll say select title from long
[00:46:43] list where title is like let's say ty
[00:46:49] hit semicolon. And now I get no matches.
[00:46:54] So there is no book in this database
[00:46:56] that has TY and then let's say three or
[00:46:59] four underscores for any character after
[00:47:01] it.
[00:47:04] Okay, so this covers our use of like,
[00:47:08] but let's keep going and building more
[00:47:10] complex conditions to find even more um
[00:47:12] answers to questions we might have about
[00:47:14] this data. Over here, let me think what
[00:47:17] we should show next. We've seen like
[00:47:20] we've seen some compound conditionals.
[00:47:22] Well, let's go back to trying to find
[00:47:24] books that are in a certain year. So, we
[00:47:27] saw earlier we had this kind of query.
[00:47:30] We could say select title and year from,
[00:47:34] let's say, our long list. Now, I could
[00:47:37] try to find those books that are written
[00:47:39] or nominated in 2022 and 2023. But let's
[00:47:43] say I want to go further. I want those
[00:47:45] from 2019 to 2022. A span of multiple
[00:47:49] years here. So I could try it like this.
[00:47:52] Where year equals let's go ahead and say
[00:47:55] 2019
[00:47:57] or year is 2020
[00:48:00] or year is 2021.
[00:48:04] And let me make a new line again. Or
[00:48:07] year is 2022
[00:48:10] semicolon. Now before I run this query,
[00:48:14] let me ask our audience, what strikes
[00:48:16] you as being not very well designed
[00:48:18] about this query? What could I be doing
[00:48:21] better here? So I'm seeing maybe one
[00:48:24] improvement is that I don't need to
[00:48:27] write out or year is this or year is
[00:48:31] that. I could probably do better with
[00:48:33] this. And let's introduce some new
[00:48:35] keywords for working with ranges in
[00:48:37] terms of our conditions. So here we can
[00:48:42] see some new operators to use. We have
[00:48:45] this greater than sign, this less than
[00:48:47] sign, greater than or equal to, and less
[00:48:50] than or equal to. And we can use these
[00:48:52] to build ranges inside of our queries to
[00:48:55] say I want something to be greater than
[00:48:57] this number or less than this number
[00:48:59] two. And we can combine these with our
[00:49:02] and and our or we saw before to get back
[00:49:04] in this case some set of of rows that
[00:49:07] match our what we intend to find. So let
[00:49:10] me go back and try some of these out.
[00:49:12] I'll try to improve the design of this
[00:49:14] query. Let me first run it and we'll
[00:49:17] see. We do get back 2019 to 2022.
[00:49:22] But I could probably do better. So let's
[00:49:24] try using our new operators here that
[00:49:26] can give us some range capabilities.
[00:49:29] I'll say select title and also select
[00:49:32] year from long list. But now I want
[00:49:36] those rows where the year is greater
[00:49:40] than or equal to 2019
[00:49:43] and the year is less than or equal to
[00:49:46] 2022
[00:49:48] semicolon. I'll hit enter. Notice how I
[00:49:51] get the very same results. So I get all
[00:49:53] those same rows, but now my query is
[00:49:56] much smaller. It's making use of these
[00:49:58] range operators I've seen so far. I
[00:50:02] could even further improve this. I could
[00:50:04] make this a little better designed too.
[00:50:07] Let me go back to some slides and show
[00:50:08] you. We could use these keywords between
[00:50:11] blank and blank where this can be some
[00:50:14] condition or some number. In this case,
[00:50:17] I could say between let's say 2019 and
[00:50:20] 2022. This is inclusive. So if I say
[00:50:24] 2019 and 2022, I'll get back a query
[00:50:28] that includes 2019 and 2022. So let me
[00:50:32] try this one. I'll go back over here and
[00:50:35] I will now try select title from year
[00:50:40] from long list where the year is between
[00:50:44] between 2019 and 2022.
[00:50:48] Same results now, but just a different
[00:50:50] way of writing this same query.
[00:50:54] Now, what else could we do with these
[00:50:56] ranges? Well, as we've said before,
[00:50:59] these books actually have some ratings
[00:51:01] involved. These ratings are crowdsourced
[00:51:03] from Goodreads, the site you can review
[00:51:05] books online. And I want to find maybe
[00:51:08] the books that have a rating of 4.0 or
[00:51:10] higher. Well, I could do that now with
[00:51:12] my ranges. I could say select title and
[00:51:16] rating from my long list and I could say
[00:51:19] where the rating is greater than 4.0
[00:51:23] semicolon. I'll hit enter and I'll see
[00:51:26] now only those books that have a rating
[00:51:29] of 4.0 or higher like this. I could even
[00:51:35] combine conditions. So I know that these
[00:51:38] books have a certain rating, but how
[00:51:40] many votes did they really get? Well,
[00:51:41] let's take a peek. I'll come back over
[00:51:43] here and let me try this one. I could
[00:51:47] say select title.
[00:51:49] Oops. Let me clear my terminal again.
[00:51:51] So, it's back up top. Select title and
[00:51:56] uh rating and the number of votes that
[00:51:59] these books got from let's say our long
[00:52:02] list table. Now, I want to find those
[00:52:06] that have a rating of greater than 4.0
[00:52:09] you know, and let's say a number of
[00:52:12] votes,
[00:52:14] a number of votes is greater than at
[00:52:16] least, let's go with 10,000.
[00:52:19] So, at least we know a good number of
[00:52:20] folks actually voted on these books to
[00:52:22] find the best among them. I'll hit
[00:52:25] enter. And now I'll see we're only down
[00:52:27] to a few books, four in fact, where each
[00:52:31] one has a rating higher than 4.0. And
[00:52:34] indeed each every the vote every every
[00:52:36] vote row has a vote total greater than
[00:52:40] 10,000 in this case. So a good way to
[00:52:43] try to find the top books in our data
[00:52:46] set here.
[00:52:47] Let's keep going with these ranges and
[00:52:50] let's think about one more thing we
[00:52:52] could do. Maybe I want to find books
[00:52:54] that are less than a certain length. So
[00:52:56] I'll try that as well. I'll say select
[00:52:58] let's say title and pages from my long
[00:53:02] list. And now I can make a condition
[00:53:04] based on pages. I'll say where pages is
[00:53:08] less than 300. Hit enter. And now I
[00:53:11] should see that I have all these books
[00:53:13] that are less than 300 pages long when
[00:53:16] they were first published.
[00:53:19] So let's pause here and ask what
[00:53:20] questions we have on these range
[00:53:23] conditions. I just wanted to check if um
[00:53:27] for a for a proper query in this case um
[00:53:31] to be able to run operations they have
[00:53:33] to be integers in the database. Um and I
[00:53:36] my second question is for when we're
[00:53:38] matching a string um is it case
[00:53:40] sensitive or not?
[00:53:42] >> Yeah, two great questions. So the first
[00:53:44] one here is going to be do I have to use
[00:53:46] integers in this case and what types
[00:53:48] maybe should I use and the second one
[00:53:50] being could I match strings like case
[00:53:52] insensitively. So for the first one um
[00:53:55] in this case it'll depend on the design
[00:53:58] of your database. So we'll see later on
[00:54:00] in the course how we can choose the
[00:54:01] types for our columns and how that might
[00:54:03] impact the types we actually use in our
[00:54:06] queries. Um for now I made this database
[00:54:09] so I just know that my my year column is
[00:54:11] an integer. My ratings column is a is a
[00:54:14] real number or a float if you're
[00:54:15] familiar and my votes is an integer. So
[00:54:17] I just know to use those numbers there.
[00:54:19] to the question of uh matching things
[00:54:21] case insensitively. Let's actually
[00:54:23] revisit like just briefly here to show
[00:54:25] you what that can do. So I'll go back to
[00:54:28] my terminal and let's say uh I want to
[00:54:32] find just a book title and I want to
[00:54:34] type it in kind of sloppily. I don't
[00:54:36] want to capitalize it like capital books
[00:54:37] are. So I'll say select let's say title
[00:54:40] from um long list and maybe I'll want to
[00:54:44] find that book p again. So I could say
[00:54:47] where title is like py but all in
[00:54:52] lowercase. Now I'll hit enter and I'll
[00:54:55] see I do get back p. So even though I
[00:54:58] said where title is like lowercase p y r
[00:55:02] e I got back capital p yre e. Now this
[00:55:06] is in contrast to saying where title
[00:55:09] equals lowercase p. Let's try that. I'll
[00:55:12] come back over here and I'll say again
[00:55:16] select title from long list but now
[00:55:20] where oops where title equals quote
[00:55:25] unquote p semicolon I'll hit enter and
[00:55:29] now I see no results so in this case the
[00:55:32] equals is going to be case sensitive
[00:55:34] case matters in this case but like is
[00:55:37] case insensitive
[00:55:41] Okay,
[00:55:43] why don't we keep going then and let's
[00:55:46] take a look at a few other things we can
[00:55:47] do with these SQL keywords for querying.
[00:55:51] Well, earlier we were trying to find a
[00:55:53] way to find the best books in our data
[00:55:56] set. And we did that by filtering them
[00:55:58] based on some ranges, but we could
[00:56:01] probably do that a little bit more
[00:56:03] methodically. In this case, using a new
[00:56:05] keyword, this one called order by. So
[00:56:09] order by allows us to take the results
[00:56:12] of our query and order them as it
[00:56:15] suggests by some column itself. So we
[00:56:19] could put them in alphabetical order or
[00:56:21] in order by number of votes or in order
[00:56:24] by number of ratings. And let's just try
[00:56:27] an example of this to see how order by
[00:56:29] works for us. But in the end we'll see
[00:56:31] it can arrange columns, arrange rows for
[00:56:34] us in a resulting query. So, I'll go
[00:56:36] back to my my computer and let's try
[00:56:39] this question here. I want to try to
[00:56:41] find the top 10 books in my table. So,
[00:56:45] I'll say select
[00:56:47] title and rating from long list. Enter.
[00:56:53] Not on my query yet though. Now, I'll
[00:56:56] say order by the rating.
[00:57:00] And let's only take the top 10. So I'll
[00:57:03] say limit 10 in this instance semicolon.
[00:57:07] So now I've combined some of my prior
[00:57:09] keywords. I'm using select, I'm using
[00:57:12] order by, and I'm still using our old
[00:57:13] friend limit. So let me hit enter here
[00:57:16] and I'll get back. Well,
[00:57:19] not quite the top 10. I see rating of
[00:57:23] 3.05 here and rating of 3.42 down here.
[00:57:28] So based on this, what do you think the
[00:57:32] default ordering of order by is? See it
[00:57:36] might be from least to greatest. So we
[00:57:38] saw here that we have rating being
[00:57:40] pretty small, but we said order by
[00:57:42] rating. So it starts from small and goes
[00:57:45] down to large. So we need to fix this in
[00:57:47] some way. Let's introduce a new addition
[00:57:49] to order by to have us um fix this query
[00:57:53] overall. So let me show you that order
[00:57:56] by does by default sort from least to
[00:58:00] greatest. But let's try some addition
[00:58:03] here. We have not just order by but
[00:58:05] order by some column and then ascending
[00:58:09] or descending. So ascending is the
[00:58:12] default. It means from least to
[00:58:14] greatest. Descending we can specify
[00:58:17] meaning from greatest to smallest. So
[00:58:20] let's try using order by but now with
[00:58:22] this other keyword called deesc for
[00:58:25] descending. Here I'll go back to my
[00:58:28] terminal and let's rewrite this query to
[00:58:31] include deesc. I'll say select title and
[00:58:35] rating from long list. And let me before
[00:58:39] I run this query let me just clear my
[00:58:41] terminal so it's back up at the top.
[00:58:42] I'll backspace this and then a moment
[00:58:45] here I'll press ctr L. Now I'm back at
[00:58:47] the top. I'll say select title, select
[00:58:52] title and rating from long list where
[00:58:57] actually not where we're not filtering
[00:58:59] yet. I'll say order by rating but not by
[00:59:04] ascending by default for going from
[00:59:06] least to greatest. I want greatest to
[00:59:08] least. So I'll say deesc here. Now I can
[00:59:12] say limit 10 semicolon hit enter. And
[00:59:16] now I'll see the top 10 books. Here I
[00:59:18] have The Eighth Life coming in at 4.52
[00:59:22] and the Books of Jacob coming in at
[00:59:23] 4.06.
[00:59:25] So now we're going from greatest to
[00:59:27] smallest.
[00:59:29] Well, I could order by not just these
[00:59:31] ratings, but also by the number of
[00:59:34] votes. Like it seems there's a tie to
[00:59:36] break here. If I look at Stillborn and
[00:59:39] When We Cease to Understand the World,
[00:59:40] those both have a rating of 4.14.
[00:59:43] But presumably one book has maybe more
[00:59:46] votes than the other. So I could try to
[00:59:49] break this tie by ordering not just by
[00:59:52] rating but also by votes. The number of
[00:59:55] votes this book actually received on
[00:59:57] Goodreads. So let's try that then to
[00:59:59] break this tie. I'll come back over here
[01:00:02] and I'll try this query now. I'll say
[01:00:06] again select title and rating from long
[01:00:11] list. Now I'll order by first the rating
[01:00:15] column in descending order. But I also
[01:00:18] want to order by the number of votes
[01:00:20] after I order by rating. So I'm saying
[01:00:23] first order by rating but afterwards
[01:00:26] followed by a comma let's order by the
[01:00:28] number of votes also in descending order
[01:00:32] from greatest to smallest. Now I'll just
[01:00:35] continue my query on the next line and
[01:00:37] I'll say limit 10 semicolon. This then
[01:00:40] gives me, let's see, the books, but now
[01:00:45] they're going to be in the order that
[01:00:46] allows us to see the number of votes.
[01:00:48] Let me just actually refine this. Let me
[01:00:50] say not just select title and rating.
[01:00:52] Let's make sure we can see the votes
[01:00:53] here, too. So, select title and rating
[01:00:56] and votes from long list. Hit enter on
[01:01:00] my query. Now, I'll say order by rating
[01:01:02] and votes. Then I'll say limit 10. And
[01:01:05] here I'm just hitting the up arrow on my
[01:01:07] computer. I'll hit enter and now I'll
[01:01:10] see the votes included. So let me show
[01:01:12] you this on the big screen. Here we see
[01:01:14] that the tie is broken. So when we cease
[01:01:17] to understand the world, these both have
[01:01:19] 4.14 along with um stillborn. But here
[01:01:23] this book has more votes and so is
[01:01:25] higher in our order now that we've
[01:01:28] ordered by multiple columns.
[01:01:31] So let me pause here and ask what
[01:01:33] questions we have on ordering with data.
[01:01:37] ordering by one column or multiple and
[01:01:40] how we can sort data like this.
[01:01:43] >> Sir, I want to know that can we write
[01:01:45] rating to 4.93 to uh 4.9?
[01:01:50] >> Yeah, good question. So, I think if I
[01:01:51] understand correctly, how can we select
[01:01:53] a rating or try to find a rating that's
[01:01:55] like equal to 4, you know, 92 or things
[01:01:57] like that? Let's try that here. So, if I
[01:02:00] want to find a particular rating, I
[01:02:02] could simply use my uh wear friend from
[01:02:05] before. I could say select let's say
[01:02:08] title and rating and maybe I could try
[01:02:11] to find a particular rating for a book
[01:02:13] from long list. I could say then where
[01:02:17] this rating is equal to let's say 4.932
[01:02:21] semicolon this if this book exists it'll
[01:02:24] get it back here. So I'll hit enter and
[01:02:26] I see there's no book with this
[01:02:27] particular rating 4.392.
[01:02:31] But good question for how to find
[01:02:33] particular ratings for our books here.
[01:02:37] Okay, other questions too on how we've
[01:02:40] been able to sort our data and use order
[01:02:43] by. Will desend work on a string on an
[01:02:47] alphabetic basis or do we need to have a
[01:02:50] special conditions for alphabetic
[01:02:53] characters?
[01:02:54] >> Yeah, great question. So, how could we
[01:02:56] use order by with some characters or
[01:02:58] strings or some text in our database?
[01:03:00] Let's try that one out too and see how
[01:03:02] that works with ASC for ascending and
[01:03:04] DEESC for descending. So I'll go back to
[01:03:07] my terminal and I'll demonstrate here
[01:03:09] how we can use this for some text. So
[01:03:12] let's try simply sorting our books
[01:03:14] alphabetically for let's say our
[01:03:16] library. I'll say select title from long
[01:03:21] list. Enter. And I want to order by
[01:03:24] title just plain and simple. And then
[01:03:26] hit semicolon. Let's see what happens.
[01:03:28] I'll hit enter. And now I'll see that
[01:03:31] these books are ordered but they seem to
[01:03:34] be ordered alphabetically. So here we
[01:03:36] have some uh titles lower in the
[01:03:38] alphabet and up here we have titles
[01:03:40] earlier in the alphabet. So by default
[01:03:43] order by seems to order alphabetically.
[01:03:46] If I change that default though from
[01:03:49] ascending to descending. Let's see what
[01:03:51] happens. I'll go back over here and I'll
[01:03:54] try the same query but now using DEESC.
[01:03:58] Select title from long list order by
[01:04:01] title now in descending order. Hit
[01:04:05] enter. And now I'll see these titles in
[01:04:08] reverse alphabetical order. So notice
[01:04:11] how earlier on we have titles that are
[01:04:13] lower in the alphabet, but down below we
[01:04:15] have titles that are earlier in the
[01:04:17] alphabet here. So you can use order by
[01:04:20] with these texts but you then have to
[01:04:23] specify whether you want it in
[01:04:24] alphabetical order or in reverse
[01:04:26] alphabetical order.
[01:04:29] Okay. So let's show a few um other uh uh
[01:04:33] you know concepts here we can use
[01:04:35] alongside of these orderings. One thing
[01:04:38] we could also do is try to find uh more
[01:04:41] information about the ratings of these
[01:04:43] books. So let's say I want not just to
[01:04:45] order these books but try to find the
[01:04:48] average rating or to try to find the
[01:04:50] number of books or try to find let's say
[01:04:52] maybe the sum of my total votes on each
[01:04:55] of my books. Well for this we could in
[01:04:58] we could introduce some new concepts.
[01:05:00] These ones called SQL's aggregate
[01:05:03] functions. These allow us to take a
[01:05:07] whole set of rows and return not each of
[01:05:10] those rows individually but instead in
[01:05:13] this case one number based on the values
[01:05:16] in those rows. You could imagine trying
[01:05:19] to count the number of rows you have or
[01:05:21] take the average of the number of rows
[01:05:23] or take the average of let's say a
[01:05:25] rating for instance finding the minimum
[01:05:27] rating or the maximum rating or finding
[01:05:29] the sum of some votes and we'll see each
[01:05:31] of these in action here. Let's go back
[01:05:34] to our terminal. Try some of these out.
[01:05:37] I will try in this case first um trying
[01:05:41] to find the average rating from my long
[01:05:43] list. Well, I know just from experience
[01:05:46] and as you now know too, I can try to
[01:05:48] find the average of some column by using
[01:05:51] the AVG aggregate function. So, I'll say
[01:05:54] select not just rating in this case, but
[01:05:59] select the average rating from long
[01:06:02] list.
[01:06:03] Notice how in this case I'm using this
[01:06:06] kind of syntax where I take rating my
[01:06:09] column I want to aggregate or to sum up
[01:06:12] or to average like this and I apply the
[01:06:15] function by saying its name followed by
[01:06:18] some parenthesis around that column
[01:06:20] name. So this will return to me not all
[01:06:22] of the rating rows but the average of
[01:06:25] the rating rows in one single cell. Let
[01:06:28] me try this. I'll come back and I will
[01:06:31] then hit enter. And I'll see this is the
[01:06:35] average rating. We have 3.7537179471795.
[01:06:42] So average rating for all of these
[01:06:43] books. But of course, this isn't great.
[01:06:47] What might I want to do if I was going
[01:06:49] to show this to somebody else? I could
[01:06:52] probably improve the presentation of
[01:06:53] this in some way.
[01:06:56] So I could probably round this result.
[01:06:58] Like I have 3.75 371. We could probably
[01:07:02] stop after two decimal points, right?
[01:07:04] Just simply like 3.75.
[01:07:06] So I could introduce some new keyword
[01:07:08] here. This one to round the results. Let
[01:07:11] me show you this one in action. I'll
[01:07:13] come back and I'll try not just select
[01:07:16] average rating, but select the rounded
[01:07:19] average rating. So I'll say select round
[01:07:23] and then take average of rating and
[01:07:27] round to two decimal points from long
[01:07:31] list semicolon. So now this query
[01:07:36] decides to first find the average of the
[01:07:39] rating column then take the result and
[01:07:43] round it using two decimal points.
[01:07:46] Notice how round takes two inputs or two
[01:07:49] arguments. The first one being the
[01:07:51] rating, the average rating. The second
[01:07:53] one being number of decimal points to
[01:07:55] round to. And we complete our query in
[01:07:57] the way we usually do by saying from
[01:07:59] this table. So let's try this one to
[01:08:01] figure this out. I'll come back and I'll
[01:08:03] hit enter. And now we'll see we do get
[01:08:06] back 3.75.
[01:08:08] But there is still one thing to improve
[01:08:10] here. When I write this query, I see
[01:08:13] this ugly title name, round, average,
[01:08:16] rating, 2. I wouldn't send this to my
[01:08:19] boss or somebody else who I work for,
[01:08:21] maybe even a friend, right? I want to
[01:08:22] make sure it's pretty so they can read
[01:08:23] it correctly. So, what could I do then
[01:08:26] to try to make this prettier?
[01:08:29] I could maybe rename this column. I
[01:08:31] could try to take this and make it not
[01:08:33] just this ugly mess of SQL keywords, but
[01:08:36] to give it some name I could use
[01:08:37] instead. So, for this, we'll introduce a
[01:08:40] brand new one. new brand new keyword
[01:08:42] called as. Let's try this one too. I'll
[01:08:45] come back and I'll say select again
[01:08:49] round
[01:08:51] average rating, 2. But now I'll select
[01:08:56] it as let's say average rating. And now
[01:09:01] before I actually finish this query, let
[01:09:03] me try to bring it to the top of my
[01:09:04] terminal. We can see it all in one go.
[01:09:06] I'll backspace this and I'll say select
[01:09:10] select um the rounded version of the
[01:09:14] average rating rounded to two decimal
[01:09:17] points as let's go ahead and call this
[01:09:19] one average rating. Now I'll hit enter
[01:09:22] and I'll say from my long list table
[01:09:26] semicolon. Now I see it's much prettier
[01:09:28] overall. I have no longer these SQL
[01:09:31] keywords but instead just average rating
[01:09:34] as my column name. Okay. So let me pause
[01:09:39] here and ask questions then on using
[01:09:41] average or using um round or using as in
[01:09:46] these cases.
[01:09:48] I'm wondering do these sort of commands
[01:09:49] have like a function like are these
[01:09:53] commands called something like data type
[01:09:56] called something are these commands also
[01:09:58] do have a name?
[01:10:00] >> Yeah. And can I ask are you referring to
[01:10:01] like the AVG like count like sum those
[01:10:04] kinds of things or Yeah. So these
[01:10:07] functions do have a name. They are
[01:10:09] called aggregate functions and aggregate
[01:10:11] means to combine to bring together. So
[01:10:13] they're called aggregate functions
[01:10:15] because they take some number of rows
[01:10:17] like all my ratings for instance and
[01:10:19] bring it down to one single cell like
[01:10:21] the average or the sum or the count. So
[01:10:24] if you look up or read more about SQL
[01:10:26] aggregate functions, you'll see all of
[01:10:28] these and perhaps some more depending on
[01:10:30] the software you're using.
[01:10:33] Okay, so let's keep going then and try
[01:10:36] to start counting um some other rows and
[01:10:38] use our other aggregate functions here.
[01:10:40] I'll go back to my terminal and so far
[01:10:43] we've seen average as well as um we have
[01:10:47] seen round and so on but why don't I try
[01:10:50] to find the maximum or the minimum
[01:10:52] rating in my table I'll say select let's
[01:10:56] say the max rating from my long list
[01:11:00] semicolon hit enter now I see the
[01:11:03] highest rated book was had a rating of
[01:11:05] 4.52
[01:11:07] well what about the minimum rating I
[01:11:09] could use min here too I could say I
[01:11:10] select let's say min of my rating column
[01:11:14] from my long list table I'll hit
[01:11:17] semicolon and I'll see 3.05 05 that is
[01:11:20] the lowest rated book I have in this in
[01:11:23] this set. Well, as we've seen, let me
[01:11:27] try to um view this for you all. I could
[01:11:29] say select um title and votes from my
[01:11:33] long list. It's like title and votes for
[01:11:36] my long list. Here I have many books
[01:11:39] with many user generated votes. Maybe
[01:11:42] people on the internet decided to rate
[01:11:44] this book out of five and maybe uh go
[01:11:47] Went Gone got about let's say 592 votes.
[01:11:50] So I'm curious then how many total votes
[01:11:53] do I have in my data set? Well for that
[01:11:57] I could use the sum aggregate function
[01:11:59] try to count up each one of these rows
[01:12:02] and return it back to me in a single
[01:12:04] cell. So I'll use sum here. I'll come
[01:12:07] back and I'll say I want to find the sum
[01:12:10] of my votes column. I'll say select
[01:12:13] let's say um the sum of my votes column
[01:12:18] from my long list table and then I'll
[01:12:21] just hit enter semicolon enter. And I'll
[01:12:24] see over 600,000 people offered a vote
[01:12:28] for each of these books that were long
[01:12:30] listed for the International Booker
[01:12:32] Prize.
[01:12:34] Now that' be a few more here. So let's
[01:12:36] check out what else we have left to do
[01:12:37] in our aggregate functions. We could
[01:12:40] also try to count up just the number of
[01:12:42] books in our data set. So why don't I
[01:12:45] try to find the number of rows I have.
[01:12:47] For that I could use count. And often to
[01:12:50] find the number of rows in your data
[01:12:52] set, you might use count and star as we
[01:12:55] saw a little earlier. I could say select
[01:12:57] count star from long list. And this
[01:13:01] means again star means give me every row
[01:13:04] and every column give me basically my
[01:13:06] whole table right and if I say count
[01:13:10] star that means count up the number of
[01:13:12] rows that I have in my database. So I'll
[01:13:15] say count star from long list and I get
[01:13:17] back 78 books in this database. Well let
[01:13:22] me try counting up the number of
[01:13:23] translators here. I'll say select let's
[01:13:26] say count of translators from long list
[01:13:30] semicolon hit enter and now I see 76.
[01:13:36] So I have 78 books but if I count
[01:13:41] translators I have 76 of them. So why
[01:13:45] might that be? If you were to raise your
[01:13:47] hand and try to guess at this. Why do I
[01:13:50] have 78 rows but 76 translators?
[01:13:55] >> Um, hello. I actually had raised my hand
[01:13:57] for a question.
[01:13:58] >> Yeah, go ahead.
[01:13:59] >> Also, I wanted to know whether the max
[01:14:01] and the min function can be used for
[01:14:04] finding the longest or the shortest
[01:14:05] string as well or do you have a
[01:14:07] different command for that?
[01:14:08] >> Ah, good question. Could we use max and
[01:14:10] min to find the longest or shortest
[01:14:12] string? That's a a good question. So,
[01:14:14] let's actually pause on this counting
[01:14:15] here and try that out real quick. So,
[01:14:17] I'll come back to my terminal and let me
[01:14:20] try to use max and min with some book
[01:14:22] titles. So, I'll say select um let's
[01:14:26] select the max um title. And at the same
[01:14:29] time, why don't we select the min title
[01:14:32] as well and I'll select these from my
[01:14:35] long list table. I'll hit semicolon. And
[01:14:38] now, let me try this out. I'll get back
[01:14:42] wretchedness and a new name. Septology 6
[01:14:46] through 7. Now, there's a few hypotheses
[01:14:50] here. It does seem that our max title is
[01:14:53] shorter than our min title. So, it's
[01:14:56] probably not that max gives us the
[01:14:58] length of the string. But what do you
[01:15:00] notice? Well, I see min is really early
[01:15:03] on in the alphabet. It has an A here,
[01:15:06] whereas max has a W, pretty low in the
[01:15:09] alphabet. And I would bet if we ordered
[01:15:12] these book titles, we would see a new
[01:15:14] name up at the very top and a
[01:15:17] wretchedness the the book here down at
[01:15:19] the bottom. So max seems to give us the
[01:15:22] lowest alphabetically which is kind of
[01:15:24] contradictory with um titles here or
[01:15:26] strings and min gives us the earliest in
[01:15:29] the alphabet using this a as well.
[01:15:34] Okay, so good question. Let's come back
[01:15:36] to our counting here. So let's go back
[01:15:38] to my terminal and again we had in this
[01:15:40] case 78 rows but only 76 translators. So
[01:15:45] again if I did select count star from
[01:15:48] let's say long list then semicolon I got
[01:15:51] back 78. But if I do select count of
[01:15:55] translators
[01:15:57] translator from long list I get back 76.
[01:16:01] Let me ask again. Why do we have 78 rows
[01:16:05] but 76 translators? You're free to say
[01:16:09] it. Okay. So, I'm seeing maybe we have
[01:16:12] some number of rows 78. But for our
[01:16:16] translators, you remember two of those
[01:16:18] were null values. They didn't exist in
[01:16:20] our table. So, it seems like if we use
[01:16:23] count star, we're counting all the rows.
[01:16:26] But if we use count translator, some
[01:16:28] column that has null values, we're only
[01:16:31] getting back those rows or those values
[01:16:33] that aren't null. So count when given a
[01:16:36] column counts only those that are not
[01:16:38] null or that exist in our table.
[01:16:42] Okay, let's look at one more example
[01:16:43] here for counting. And let's try this.
[01:16:47] Let's say I want to find all of the
[01:16:49] publishers in this database. I'll say
[01:16:52] select count of publisher from my long
[01:16:57] list and I'll hit semicolon.
[01:17:00] So you might think that I have 78
[01:17:03] publishers in this long list, but would
[01:17:06] it be accurate if I were to say I have
[01:17:08] 78 different publishers in this long
[01:17:11] list? Could I say that?
[01:17:16] I'm seeing no, right? I couldn't try to
[01:17:18] count up these publishers and then say I
[01:17:20] have 78 different ones. I might double
[01:17:23] count a publisher along the way. And let
[01:17:25] me show you what we mean here. So I'll
[01:17:27] go back to my table and let me try to
[01:17:30] select from publishers or select the
[01:17:32] publisher column from long list. I'll
[01:17:34] select publisher from long list. Hit
[01:17:38] semicolon.
[01:17:39] Whoops. And now I see something a little
[01:17:41] odd. Let me scroll back up
[01:17:44] and maybe ask for a raised hand here.
[01:17:49] Why
[01:17:50] might I get this odd
[01:17:53] result?
[01:17:55] >> Because of the quotes.
[01:17:57] >> Yeah. So I I think I mistyped some of my
[01:17:59] query here. I said uh it looks like
[01:18:02] publisher instead of publisher. And in
[01:18:05] this case, SQL will give me kind of what
[01:18:07] I asked for. I said select pubser from
[01:18:09] long list. And says okay, here it is.
[01:18:11] But that column doesn't exist. So it
[01:18:13] kind of creates this data for me. So let
[01:18:15] me try this again. I'll go back and I'll
[01:18:17] hopefully type this correctly. Now I'll
[01:18:19] say select let's say publisher
[01:18:24] this one from long list semicolon. And
[01:18:28] now I'll see all of the publishers that
[01:18:30] I have in my table. But what do you see?
[01:18:34] Well, some repeat, right? I have uh
[01:18:36] Harville secker multiple times here. I
[01:18:38] have similarly uh Macose press multiple
[01:18:40] times as well. So if I counted up these
[01:18:43] publishers, I would get each one counted
[01:18:46] one time. But if I want to find the
[01:18:48] distinct ones, the different ones, I
[01:18:50] need a new keyword for this. And for
[01:18:53] this, we'll use this keyword indeed
[01:18:54] called distinct. Trying to find unique
[01:18:56] values from our column. So let's try
[01:19:00] this. I'll go back over here and I will
[01:19:03] now select not just publishers but
[01:19:06] distinct publishers. I'll say select
[01:19:08] distinct
[01:19:10] publisher
[01:19:12] from long list semicolon.
[01:19:15] Now if I scroll through here I should
[01:19:18] see each publisher in here only one
[01:19:21] time. If they have the same name they've
[01:19:24] been filtered out and now they're only
[01:19:26] the same publisher here too. So I will
[01:19:28] then try to say select let's say count
[01:19:31] of publisher
[01:19:33] select count of publisher from uh count
[01:19:37] of distinct publisher for instance count
[01:19:40] distinct
[01:19:42] publisher
[01:19:44] oh typo publisher
[01:19:47] from long list semicolon and I'll see I
[01:19:51] have 33 distinct publishers.
[01:19:55] Okay, so this just about brings us to
[01:19:59] the conclusion of all of these new SQL
[01:20:01] keywords here. We've seen so far we have
[01:20:04] several here to use, but let's figure
[01:20:06] out how to actually exit this prompt. So
[01:20:09] you might be in your SQLite prompt right
[01:20:10] now. If you want to leave it, you could
[01:20:12] also use this commandquit.
[01:20:15] Dotquit is not a SQL keyword. It's a
[01:20:17] SQLite keyword to leave your terminal
[01:20:20] and go back to where you started. So
[01:20:24] just to review then what we've seen so
[01:20:26] far is how to select data from our
[01:20:28] table. We can use select column to take
[01:20:31] some column from our table and give us
[01:20:33] back all of those rows from that table
[01:20:36] for that column. We've seen we can apply
[01:20:39] some aggregate functions to take maybe
[01:20:41] the count of our columns or the average
[01:20:43] or so on. And we could get back not just
[01:20:45] all of our rows but only some of them
[01:20:47] using our wear clause here along with a
[01:20:50] condition. We could have multiple
[01:20:53] conditions having not just one but
[01:20:55] perhaps two like uh like let's say here
[01:20:57] condition zero and condition one and we
[01:20:59] could also use we saw before this idea
[01:21:01] of equals and like to match some pattern
[01:21:04] or to make something exactly equal over
[01:21:06] here. We could again use and and or we
[01:21:09] saw later on how we could order our data
[01:21:11] and use our limit function to get back
[01:21:14] only some number of rows. Now, this then
[01:21:19] is our introduction to querying. And so
[01:21:21] far, we've seen this world of books. And
[01:21:24] the table we've had so far really just
[01:21:26] has books inside of it. But next time,
[01:21:29] what we'll see is how to take this world
[01:21:31] of books and split it into multiple
[01:21:33] tables. How do we find information on
[01:21:35] publishers or books or authors, too, and
[01:21:38] how do we try to put that in a table
[01:21:39] that can represent the relationships
[01:21:40] among all of these different entities?
[01:21:43] We'll talk about all that and more when
[01:21:44] we come back next time, and we'll see
[01:21:45] you there.
[01:21:49] [Music]
[01:22:06] Well, hello one and all and welcome back
[01:22:08] to CSG's introduction to databases with
[01:22:11] SQL. My name is Carter Zeni and last we
[01:22:14] left off, we learned all about querying,
[01:22:17] how to ask questions of data in a single
[01:22:20] table. Today though, we'll take one step
[01:22:22] forward and we'll have databases that
[01:22:24] have not just one table inside of them,
[01:22:27] but actually multiple tables. Tables for
[01:22:29] authors, tables for books and for
[01:22:31] publishers and so on to represent all
[01:22:33] these people who are part of the book
[01:22:35] industry. And you too can apply these
[01:22:37] same skills for whatever you want to
[01:22:39] represent as well. So let's pick up
[01:22:42] where we last left off, which was with
[01:22:44] this database of books. I'll come back
[01:22:46] to my computer over here. And if you
[01:22:49] recall, we had this data set that was
[01:22:51] the books that were long listed for the
[01:22:53] international booker prize. To be
[01:22:55] longlisted means to be nominated for
[01:22:58] some prize in a given year. And the
[01:22:59] international booker prize is awarded
[01:23:01] every year to one book, but 13 are
[01:23:05] nominated. So in this data set, we have
[01:23:08] 13 books for the past five years that
[01:23:11] were nominated for this prize. Now, I'll
[01:23:14] go ahead and open up this database once
[01:23:16] more. And if you remember, we used this
[01:23:18] command last time to open this data set.
[01:23:21] SQLite 3 space the file name where our
[01:23:24] file name was long list. DB. And this is
[01:23:27] one example of our database management
[01:23:29] system. This one called SQLite and this
[01:23:32] one being the third version of SQLite.
[01:23:35] So let's reopen this database and let me
[01:23:37] show you what we have now in store. I'll
[01:23:40] type SQLite. Oops. So I'll type SQLite
[01:23:43] sqlite 3 and then long list db and I'll
[01:23:48] hit enter. Now my prompt changes. I no
[01:23:51] longer have this dollar sign. I now have
[01:23:53] the SQLite prompt. And here's where we
[01:23:55] saw last time I could write my SQL
[01:23:58] queries. Well, before we start, let's
[01:24:01] see the changes to this database. So if
[01:24:04] I want to get a feel for the tables that
[01:24:06] are inside of this database, I can use a
[01:24:10] command. this one called tables. Notice
[01:24:13] this is not a SQL keyword. This is a
[01:24:16] command particular to SQLite to show me
[01:24:18] what tables are inside this database. So
[01:24:21] I'll type enter here. And now I see I
[01:24:24] have more than one table. I have a table
[01:24:26] for authors, a table for books, for
[01:24:29] publishers, and even more. And now that
[01:24:32] we're working with not just one table,
[01:24:35] but multiple, we're actually moving into
[01:24:37] this idea of a relational database. So
[01:24:41] no longer do we have a database with
[01:24:42] only one table inside of it. We now have
[01:24:45] multiple. And these tables presumably
[01:24:48] have some kind of relationship among
[01:24:50] them. You could think, for instance, of
[01:24:52] an author writing a book or a publisher
[01:24:55] publishing a book or even a translator
[01:24:58] translating a book. So we'll have these
[01:25:00] tables and these relationships among
[01:25:02] them. So let's look at one example of
[01:25:05] this kind of relationship among tables.
[01:25:08] I could have a table of authors and a
[01:25:11] table of books. This simplified for now
[01:25:13] to one column in every table. Well, my
[01:25:16] author's table I have names. In my book
[01:25:18] uh table I have titles. And we seem to
[01:25:21] be moving in the right direction. I
[01:25:22] could store more information about
[01:25:24] authors and books. But I've also created
[01:25:27] some problem like how do I know now who
[01:25:30] wrote which book? Like earlier we saw
[01:25:34] that you know maybe Eva is right next to
[01:25:36] Boulder in a single table for authors
[01:25:38] and books and we know that Eva wrote
[01:25:40] Boulder that way. But now if I look at
[01:25:43] authors I only see Eva and no
[01:25:45] information about books. So we seem to
[01:25:47] have this problem here. Well one
[01:25:50] solution uh might be something like the
[01:25:53] honor system. I mean, I'm honest and so
[01:25:55] are you. We could say that, well, maybe
[01:25:57] the first row in authors will always
[01:26:00] correspond to the first row in books.
[01:26:02] So, we always know Eva wrote Boulder
[01:26:04] because Eva is first in the author's
[01:26:06] table and Boulder is first in the books
[01:26:08] table. Similarly, let's say Han wrote
[01:26:11] the white book because Han is in the
[01:26:13] second row and the white book is in the
[01:26:15] second row in books.
[01:26:18] But I have to imagine, I mean, as good
[01:26:20] as I am at being honest and transparent,
[01:26:22] maybe I make a mistake. Maybe I add a
[01:26:24] row to books but not to authors. Or
[01:26:26] maybe I add a row to authors and not to
[01:26:28] books. I could change data and not
[01:26:30] update it to adhere to that standard. So
[01:26:34] let's actually take a step back and
[01:26:36] maybe think, well, is it better then to
[01:26:38] have this kind of situation where we did
[01:26:41] have one table with authors and books?
[01:26:45] It might be. But let's think. I mean,
[01:26:48] this could work for a while. But let's
[01:26:49] say Olga is a prolific author. They like
[01:26:52] to write not just one book, but two.
[01:26:55] They wrote not just flights, but also
[01:26:56] the books of Jacob. Well, let's say Olga
[01:27:00] writes another book or another one too.
[01:27:03] What might be the problem with this
[01:27:06] arrangement now? And feel free to raise
[01:27:08] your hand too with your ideas. Why run
[01:27:10] into some issues here? If we only have
[01:27:12] one table of authors and books,
[01:27:16] >> there is some redundancy, some
[01:27:18] repetition.
[01:27:20] >> Yeah, a good idea. So, you might notice
[01:27:21] there's some redundancy here. I mean,
[01:27:23] Olga is in here twice, which is maybe
[01:27:26] okay if Olga wrote two books, but again,
[01:27:28] let's say Olga wrote three or four or
[01:27:30] five. Olga will be in here that many
[01:27:33] times. And so, we could probably do a
[01:27:35] bit better than this. And let's actually
[01:27:38] just say this isn't going to be the most
[01:27:40] efficient idea for us, let's go back to
[01:27:42] these multiple tables here and think
[01:27:44] about how we could relate these two
[01:27:46] tables one to the other. Now, before we
[01:27:50] get into the details of how we might do
[01:27:51] this technically, let's think about the
[01:27:54] kinds of relationships we could have
[01:27:55] between authors and books. Well, maybe
[01:27:58] in our world, we have one author that
[01:28:02] writes one book. And maybe we could say
[01:28:04] every author only writes one book. And
[01:28:07] similarly, one book is always written by
[01:28:10] one author. This could be true for some
[01:28:13] books and some authors. But arguably,
[01:28:16] it's not the best assumption, right? We
[01:28:18] probably have authors writing more than
[01:28:20] one book or books being written by more
[01:28:22] than one author. So, as it stands now,
[01:28:25] we could call this kind of relationship
[01:28:27] a oneto-one relationship. If this is our
[01:28:30] idea of authors and books, one author
[01:28:32] writes one book and one book is written
[01:28:34] by one author. This is a oneto-one
[01:28:38] relationship.
[01:28:40] Well, as we know, authors can write more
[01:28:43] than one book. Olga, for example, didn't
[01:28:46] write just flights, they also wrote
[01:28:48] another book. And so, we could say,
[01:28:50] well, Olga wrote not just this book up
[01:28:53] top, they also wrote this book down
[01:28:55] below. And now we're moving from a one
[01:28:58] to one relationship to what we'll call a
[01:29:01] one to many relationship. There are many
[01:29:04] books that one author could write.
[01:29:08] But of course, is this the full picture,
[01:29:10] too? I mean, some books are only written
[01:29:14] by one author, but presumably some books
[01:29:17] are written by multiple authors. So, we
[01:29:19] need to enhance our picture even
[01:29:21] further. Let's try that. Let me add
[01:29:24] another author into the mix here. This
[01:29:26] author wrote this book along with Olga,
[01:29:30] let's say. So notice how here we have
[01:29:33] one author writing more than one book.
[01:29:36] And we also have one book being written
[01:29:39] by more than one author. Well, this is
[01:29:42] called a many to many relationship. And
[01:29:45] it's called that because we have many
[01:29:48] books that could be written by many
[01:29:50] authors. So these in general are the
[01:29:53] kinds of relationships we'll have
[01:29:54] amongst our tables in a relational
[01:29:57] database. One to one, one to many, and
[01:30:00] many to many.
[01:30:03] Now thankfully there are some tools we
[01:30:05] can use to visualize these kinds of
[01:30:07] relationships. We have at our disposal
[01:30:10] something called an entity relationship
[01:30:12] diagram. Something a bit like this. It's
[01:30:15] also called an ER diagram for short. And
[01:30:19] let me propose just for now that this is
[01:30:21] the diagram for our database. We have
[01:30:24] authors and publishers and translators,
[01:30:27] books and ratings. These are our
[01:30:30] entities in our database. The things
[01:30:32] we're trying to represent.
[01:30:35] Now, you'll notice though that there's
[01:30:37] something more than just these boxes
[01:30:39] that have author, publisher, translator,
[01:30:42] and so on. There are all these lines
[01:30:44] among them and they have verbs like
[01:30:46] wrote and published and translated. And
[01:30:49] maybe that makes sense to you, but at
[01:30:51] first glance, like there's one line here
[01:30:53] that has three lines coming off of it,
[01:30:55] one line going across. This one has a
[01:30:57] circle on it. I mean, what does all that
[01:30:58] mean, right? This is kind of confusing
[01:31:00] at first glance. Well, this actually has
[01:31:03] some order to it, some rules that we can
[01:31:06] use. And let me show you what those
[01:31:07] rules are. So here we have what's called
[01:31:11] a crow's foot notation. A way of trying
[01:31:14] to represent one to one, one to many or
[01:31:17] many to many relationships using just
[01:31:19] lines and in some cases circles. So here
[01:31:23] if you ever see this line with a circle
[01:31:25] on it, you could think of zero. This
[01:31:27] doesn't have to have anything related to
[01:31:29] it. You could think of this one with a
[01:31:31] bar going perpendicular as one.
[01:31:34] something with this arrow has to have at
[01:31:36] least one thing that relates to it in
[01:31:38] some other table. And this one down
[01:31:40] below, the one that looks like a crow's
[01:31:42] foot, well, this one means that some
[01:31:44] entity has many that could be related to
[01:31:46] it in some other table. So, let's try
[01:31:50] this with an example. Here we have again
[01:31:54] our authors and our books. And here we
[01:31:56] can say that an author wrote one book.
[01:32:00] We read this left to right. In this
[01:32:02] case, one author can have one book
[01:32:05] associated with them. We know it's one
[01:32:06] because we see this bar over our line
[01:32:09] here. Now, we know too that books, at
[01:32:13] least in our world, could be written by
[01:32:15] one author. They must be written by at
[01:32:17] least one author. So, let's try this.
[01:32:19] I'll include that arrow on the other
[01:32:21] side, too. And I'll read this right to
[01:32:24] left. A book has to have at least one
[01:32:27] author.
[01:32:30] Now I could add in more symbols too. We
[01:32:33] know that books could have more than one
[01:32:35] author and an author could write more
[01:32:38] than one book. So let's try enhancing
[01:32:39] our diagram even further. I could say
[01:32:42] adding in these crows foot notation with
[01:32:45] the multiple multiple lines here. Now I
[01:32:47] could read it like this. An author going
[01:32:49] from left to right can write at least
[01:32:51] one book but they could write many
[01:32:54] books. They could write one or many
[01:32:56] books. And similarly, a book could be
[01:32:59] written by at least one author, but
[01:33:02] certainly also multiple too.
[01:33:05] So this is one example of an er diagram
[01:33:09] for our database. And hopefully now you
[01:33:12] can see uh a bit more of this making
[01:33:14] sense to you. So we see that authors
[01:33:16] here could write many books. Book could
[01:33:18] be written by many authors. Books
[01:33:21] actually don't need to have a
[01:33:22] translator. They could have zero to many
[01:33:25] translators for their book here. But in
[01:33:28] general, a translator should write or
[01:33:30] should translate at least one book or
[01:33:32] possibly many of them too. So let me
[01:33:36] pause here and ask what questions do you
[01:33:39] have on these table relationships and
[01:33:42] these diagrams that we call ER entity
[01:33:45] relationship diagrams?
[01:33:48] >> Yeah. So K I want to ask that for any
[01:33:50] given database how can we predetermine
[01:33:53] whether how the relationship between the
[01:33:55] tables are going to be because here we
[01:33:57] know that the author has some
[01:33:59] relationship to the books but how can we
[01:34:01] determine whether those relationships
[01:34:04] are existent in the for first place
[01:34:07] >> a great question if we have some
[01:34:08] database how do we know the
[01:34:10] relationships among those entities or
[01:34:12] those things that are stored inside of
[01:34:14] it well part of this is really up to you
[01:34:17] I mean when you're designing designing a
[01:34:18] database. As we'll see in a future week
[01:34:19] of this course, you have decisions to
[01:34:21] make. Do you want an author to be able
[01:34:23] to write only one book or multiple? For
[01:34:26] instance, often when I design a
[01:34:28] database, I might write a diagram like
[01:34:31] this. So, I could show this to somebody
[01:34:33] else who can know what tables I have and
[01:34:36] how they're related to one another. So
[01:34:38] if you're designing, you have the
[01:34:40] choice. But if you're taking data from
[01:34:41] someone else, you could ask for a
[01:34:43] diagram like this that could show you
[01:34:45] those relationships among those tables.
[01:34:48] Let's see what other questions do we
[01:34:50] have too on these tables and their
[01:34:54] relationships.
[01:34:55] >> How do we determine that relationship? I
[01:34:58] mean we know that it exists but how we
[01:35:00] assign which author wrote which book or
[01:35:04] multiple books or which book were
[01:35:06] written by what authors.
[01:35:09] >> Yeah, great question. So how do we try
[01:35:11] to assign then these relationships
[01:35:13] perhaps in our database? Like we know
[01:35:15] that an author could write multiple
[01:35:16] books but how do we present that in our
[01:35:19] table? Let's say um well for this let me
[01:35:21] just transition to the next part of what
[01:35:23] we'll talk about which is going to be
[01:35:24] this idea of a key. So keys are this
[01:35:27] fundamental idea in databases that can
[01:35:30] help us relate tables one to the other.
[01:35:32] And for this, let's actually do a bit of
[01:35:35] a an example, a bit of a roleplay here.
[01:35:37] So I will be your librarian today. And
[01:35:40] let's say that you're looking for a
[01:35:42] book. This one is called The Birthday
[01:35:44] Party. And I say, "Okay, I'll find you
[01:35:47] this book. I'll go to my computer here
[01:35:48] and I will try to find you the birthday
[01:35:51] party." Here though, I have two options.
[01:35:54] I seem to have The Birthday Party by
[01:35:55] Wendy Danfield and The Birthday Party by
[01:35:58] Lauren Movenier. So, let me ask you, if
[01:36:00] we're on the phone perhaps, which one do
[01:36:04] you want?
[01:36:07] Hearing feel free to to vote. Which book
[01:36:10] should we search for? The one by Wendy
[01:36:12] or the one by Laurent?
[01:36:16] I'm hearing maybe going for Laurent. So,
[01:36:20] let's try Laurent over here. We'll
[01:36:21] search for the one by Lauren. So, The
[01:36:23] Birthday Party by Lauren Movenier. Okay.
[01:36:24] Okay. Let me find you that book. But,
[01:36:27] well, now there are still two books I
[01:36:29] could choose from. Do you want it in
[01:36:30] hardcover or paperback? And so, I could
[01:36:33] ask you again, well, which one do you
[01:36:35] want? Do you want it in hard coverver or
[01:36:38] paperback? And again, feel free to vote.
[01:36:40] Which book do you want?
[01:36:44] Okay, I'm hearing
[01:36:46] we're going for I think closer to
[01:36:50] paperback. Let's try that one. So, I'll
[01:36:52] search for The Birthday Party by Laurent
[01:36:54] Movenier in paperback. And there are
[01:36:58] still two of them. Like, which one do
[01:37:00] you want? We have first edition and we
[01:37:02] have second edition. So, I would ask you
[01:37:04] again, which book do you really want?
[01:37:06] And you could keep voting here, but for
[01:37:08] the sake of just keeping this going, I
[01:37:10] mean, let's pause here and think of a
[01:37:12] better way to do this, right? My life as
[01:37:15] a librarian would be much easier if you
[01:37:18] had given me a simple number. This
[01:37:21] number is called an ISBN.
[01:37:25] And it turns out that every book has a
[01:37:28] unique identifier called an ISBN.
[01:37:32] Now, what is an ISBN really? Well, if
[01:37:35] it's the case that every book has a
[01:37:37] unique ISBN and I can only find one book
[01:37:41] if I have an ISBN, this is what we call
[01:37:44] in database terms a primary key,
[01:37:47] something that is going to be unique for
[01:37:50] our book or for any item that we have in
[01:37:53] our table. Now, here's one example of an
[01:37:55] ISBN. Notice how we have 978-1-840,
[01:38:00] whatever it is. We could use this to
[01:38:02] uniquely identify at least our books,
[01:38:05] but we could extract this away and use
[01:38:07] this in more than one place. Not just
[01:38:08] for books, but for publishers, for
[01:38:11] translators, for authors as well, giving
[01:38:13] them each some ID that uniquely
[01:38:16] identifies them. So, here's one example
[01:38:18] of our table. Let's say that I have a
[01:38:20] table of books and I used to only have
[01:38:23] titles, but now I actually have more
[01:38:25] than a title. have an ISBN to uniquely
[01:38:29] identify each of these books. And this
[01:38:32] is handy for me if I wanted to look up
[01:38:34] some book and know exactly which one I
[01:38:36] was talking about. Now, these are all
[01:38:39] fine and good in tables. They're very
[01:38:41] helpful. But we could do a little more
[01:38:44] with them. We could get to this question
[01:38:45] of how do we actually relate these
[01:38:47] tables together? We could use these
[01:38:49] primary keys for that. Now a primary key
[01:38:52] becomes useful for that kind of work
[01:38:54] when we treat it as a foreign key let's
[01:38:57] call it. Well what is a foreign key?
[01:39:00] Well a foreign key is simply taking a
[01:39:03] primary key from one table and including
[01:39:06] it in the the column of some other
[01:39:08] table. So here we have in the ratings
[01:39:11] table the ISBN column still this is the
[01:39:15] primary key for the books table but now
[01:39:18] notice how it's inside the ratings
[01:39:20] table. This is now a foreign key because
[01:39:23] it is outside of this books table and
[01:39:25] inside the ratings table. And what could
[01:39:28] I do with this? Well, I now see if I
[01:39:30] want to find all of the individual users
[01:39:33] ratings for for Boulder, I could look
[01:39:36] what is the ISBN of Boulder and then
[01:39:39] which ratings correspond to that ISBN in
[01:39:43] some other table. So this is an example
[01:39:46] how I could represent these one to many
[01:39:48] relationships. I have here a table that
[01:39:52] has an ISBN or a list of ISBNs and I
[01:39:55] have another table that can tell me
[01:39:57] which ratings correspond to this ISBN
[01:40:00] this primary key in this other table
[01:40:02] here.
[01:40:04] Well, that solves one picture here. How
[01:40:07] can I represent these one to many
[01:40:09] relationships? But we could also think
[01:40:11] about how we do the many to many
[01:40:13] relationships as well. And for this
[01:40:15] we'll need to think about how do we can
[01:40:17] improve our primary key here. So let me
[01:40:22] ask this is an ISBN but if I want to put
[01:40:26] this inside of a computer like over and
[01:40:28] over and over again as a primary key the
[01:40:32] unique identifier what problems do you
[01:40:34] think I might run into here if any?
[01:40:37] What problems would I get by using this
[01:40:39] ISBN as my primary key? you would like
[01:40:43] run out of memory.
[01:40:44] >> Run out of memory. It's a good guess.
[01:40:45] Like if I had a lot of ISBNs, let's say
[01:40:48] I had not just 78 books, but I had
[01:40:50] literally millions of books. I mean,
[01:40:52] this is a lot of data to store. If you
[01:40:55] treated each of these as an individual
[01:40:57] character, that's about one bite, eight
[01:41:00] bits per character. That's, let's say,
[01:41:02] 13 plus four dashes, 17 bytes per per
[01:41:06] ISBN, which takes up a lot a lot of
[01:41:08] space. So, what if I instead said I'll
[01:41:11] remove the dashes like we did before and
[01:41:13] I'll treat it as a number. Well, in that
[01:41:16] case, I might also have a problem. Like,
[01:41:19] let's say an ISBN begins with zero. And
[01:41:21] if I convert that to a number, I'll lose
[01:41:24] that beginning zero because it doesn't
[01:41:26] really mean anything in the context of
[01:41:28] being a number. And now I've lost my
[01:41:29] unique identifier. So, we could improve
[01:41:33] this even further and we could actually
[01:41:34] construct our very own primary key. This
[01:41:37] one, let's just say, will be called one
[01:41:40] for this book. And some other book we
[01:41:42] could call it uh two. Some other book
[01:41:45] maybe three. And it doesn't quite matter
[01:41:48] what number we choose so long as this
[01:41:51] number uniquely identifies the book that
[01:41:54] we choose. And we don't use that number
[01:41:56] for any other book as well. So let's
[01:41:59] actually rethink this relationship of
[01:42:00] one to many here. Let's say let's not
[01:42:03] just use ISBN. This is a lot of space to
[01:42:05] use. to someone point earlier. Let's go
[01:42:08] ahead and use the ID. Let's make our own
[01:42:11] primary key in our books table and use
[01:42:13] that as the foreign key in ratings. So,
[01:42:16] we freed up a good amount of space here.
[01:42:19] And notice, too, that maybe Boulder has
[01:42:22] the primary key, the ID of 1. The white
[01:42:24] book has the ID of 74. Well, doesn't
[01:42:27] matter if it's 1 2 3 or four. It
[01:42:30] doesn't. As long as 74 uniquely
[01:42:33] identifies the white book, we're okay.
[01:42:36] So here we have an example of a one to
[01:42:39] many relationship, but now improved.
[01:42:43] And with this improvement, we could then
[01:42:46] think about many to many relationships
[01:42:49] as well. I could take the same idea and
[01:42:52] use it to relate authors and books. So
[01:42:55] let's think about this relationship. Now
[01:42:57] here too
[01:42:59] let's say I have a table of authors and
[01:43:02] a table of books and notably each has a
[01:43:05] primary key. So I could use that primary
[01:43:08] key for authors and for books and
[01:43:11] perhaps put it in some new table. This
[01:43:13] one let's say is called authored and
[01:43:16] I'll have one column for author ID and
[01:43:19] one column for book ID. And based on the
[01:43:22] context clues here, what might it mean
[01:43:25] if I looked at the authored table and
[01:43:28] saw 23 next to one where 23 is in the
[01:43:31] author ID column and one is in the book
[01:43:34] ID column to raise your hand. What would
[01:43:37] it mean for me to see those two numbers
[01:43:40] next to each other?
[01:43:44] Yeah, it would mean that uh the author
[01:43:47] that is that has the ID of 21 uh 23 has
[01:43:50] authored the book one.
[01:43:52] >> Yeah, a great instinct here. So if I
[01:43:54] look at author ID, I see 23. Well, I
[01:43:56] could consider that maybe the author
[01:43:58] with the ID of 23 wrote the book with
[01:44:01] the ID of one. And I'll concede there's
[01:44:04] some extra work here. Like I have to
[01:44:06] figure out now who has this author ID of
[01:44:08] 23. Well, turns out if you look in the
[01:44:10] author's table, it's Eva. Similarly, for
[01:44:13] the book ID, I now have to go through
[01:44:15] the process of figuring out, okay, well,
[01:44:17] the book ID is one. What then is the
[01:44:21] book title? And I'll look for that in my
[01:44:24] books table over here. So, it brings in
[01:44:26] a bit more work for me, but ultimately I
[01:44:27] think we've solved our problem from the
[01:44:29] very beginning of lecture trying to
[01:44:31] relate authors and books. We can now do
[01:44:33] that using both primary keys and foreign
[01:44:36] keys. So let me ask then what questions
[01:44:40] do we have on these keys and how to use
[01:44:43] them?
[01:44:46] >> So if the I can the ID of the author and
[01:44:49] the book ID be the same? For example,
[01:44:52] can there be a author ID of one and a
[01:44:55] book ID of one or will they be mixed
[01:44:57] together?
[01:44:59] >> A really good question and good thinking
[01:45:00] here. So let's consider that maybe an
[01:45:04] author ID matches a book's ID like both
[01:45:07] authors both the author and the book
[01:45:10] have this ID of one that's actually I
[01:45:13] would say okay in our case because we
[01:45:16] know that at least one refers to authors
[01:45:19] and one refers to books as we'll see in
[01:45:22] future lectures too when I make this
[01:45:25] join table also called a joint table or
[01:45:27] junction table an associative entity I
[01:45:30] could claim that this column called
[01:45:32] author ID references the primary key
[01:45:35] column in authors and that primary key
[01:45:38] only. I could do the same thing for the
[01:45:40] book side. I could say the numbers in
[01:45:43] here reference the primary keys in the
[01:45:45] books table and those IDs only. So I
[01:45:48] could actually have authors and books
[01:45:50] with the same ID so long as my tables
[01:45:53] know that if I have this column I'm
[01:45:56] looking for author IDs. This column I'm
[01:45:58] looking for book IDs. Great question.
[01:46:00] Let's go to one more here. Um,
[01:46:04] >> I was wondering, it feels like having
[01:46:06] more and more tables because once you do
[01:46:08] this on a big scale, it adds up would
[01:46:10] use up a lot of space as well. How does
[01:46:13] it uh how do you deal with the
[01:46:15] tediousness of it adding up?
[01:46:17] >> Yeah, good question here. So, if we had
[01:46:19] a lot of these kinds of tables, wouldn't
[01:46:21] that take more space? And I think your
[01:46:23] answer the answer to that question is it
[01:46:25] would, but we do gain some things by
[01:46:27] being able to do it this way. Okay, so
[01:46:29] for example, let me go back to my
[01:46:30] authors and books table. Um, in our
[01:46:33] database, we'll see we have not just
[01:46:35] author names, but also the year they
[01:46:37] were born, the city they were born in,
[01:46:39] the place that they were um, living in
[01:46:41] certain periods of their life and so on.
[01:46:42] So, we could have much more information
[01:46:44] in these tables that we couldn't store
[01:46:46] as one table earlier because of these
[01:46:48] redundancies we saw a little bit
[01:46:50] earlier. So I think although this might
[01:46:52] take up a little more space, use a
[01:46:54] little more um tables, we can get around
[01:46:57] that as we'll see later on with some
[01:46:59] creativeness with our queries too to um
[01:47:01] address that that downside. But a good
[01:47:03] question, a good thought for trade-offs
[01:47:05] here. Let's go to one more here.
[01:47:10] >> Uh so my question is that can the ID be
[01:47:13] updated and if so does it automatically
[01:47:15] get updated in the one that has both the
[01:47:18] ids together?
[01:47:20] Yeah, good question. So, maybe we want
[01:47:22] to change the ID of some book or author.
[01:47:25] Could we do that? Uh, I would say you
[01:47:27] could, but it's kind of a dangerous
[01:47:29] game. I mean, if I changed Eva from 23,
[01:47:33] let's say, to uh let's so we change 27.
[01:47:37] Well, I could get EVA confused with
[01:47:40] gauze. And I need to be doubly sure that
[01:47:43] when I'm changing these IDs, I'm making
[01:47:45] sure that I'm not making an ID nonique.
[01:47:50] I'm not making it an ID that somebody
[01:47:51] else already has. And so for that
[01:47:54] reason, we very rarely change IDs. In
[01:47:56] fact, we tend to just abstract them
[01:47:58] away. So we don't actually know the ID
[01:48:00] of any particular author or the ID of a
[01:48:02] particular book. We just use them in our
[01:48:04] queries as we'll see in just a moment.
[01:48:07] So wonderful questions here. What we'll
[01:48:09] do is take a very short break and come
[01:48:11] back to see how we can use these same
[01:48:13] tools of keys to not just relate tables,
[01:48:16] but to query them too and find answers
[01:48:19] to our questions across these tables.
[01:48:22] We'll be back in just a minute. Well,
[01:48:24] we're back and what we saw before was
[01:48:26] how to relate our tables using keys. We
[01:48:29] saw that we could have tables of authors
[01:48:32] and translators and books related to
[01:48:34] each other using primary keys and
[01:48:37] foreign keys. So what we'll do now is
[01:48:39] figure out how we can query these tables
[01:48:42] using different techniques to that in
[01:48:44] this case might actually use primary
[01:48:46] keys and foreign keys within those same
[01:48:49] queries. Now one technique we could use
[01:48:51] is this one called sub queries also
[01:48:54] called nested queries too that basically
[01:48:56] put one SQL query inside of another. And
[01:49:00] they're useful in a few different cases
[01:49:02] but let's say I have one case of a one
[01:49:05] to many relationship. Maybe I have
[01:49:07] publishers that are publishing many
[01:49:09] books, for instance. Well, I could use
[01:49:11] sub queries to help me answer questions
[01:49:13] about these kinds of relationships in my
[01:49:16] table. To make it more concrete, let's
[01:49:18] say I have a table of books and I want
[01:49:22] to figure out which of these books were
[01:49:25] published by Fitz Caraldo editions, my
[01:49:28] favorite publisher. Let's say what's the
[01:49:31] problem here? I want to find the books
[01:49:34] published by Fitz Auto editions, but
[01:49:36] what am I missing? Feel free to raise
[01:49:39] your hand and answer.
[01:49:42] >> Well, we don't have the name of the
[01:49:44] publisher in the same table and we
[01:49:46] haven't made the relationship with the
[01:49:48] other table to know the name of
[01:49:50] publisher.
[01:49:51] >> Yeah, good observation. So, I want to
[01:49:54] find the books that are published by
[01:49:55] Fitz Caraldo editions. And as you noted,
[01:49:58] well, there's no publisher name. There's
[01:50:00] just the ID. So, I need to have some way
[01:50:03] of knowing what these IDs correspond to.
[01:50:06] And and thankfully, I do have a way of
[01:50:08] knowing that. I have a table called
[01:50:10] publishers. And this has a a column
[01:50:12] called ID and a column called publisher.
[01:50:15] And what do I notice? Well, I notice
[01:50:16] that Fitz Caraldo editions has the ID of
[01:50:20] five. So, I could probably solve this
[01:50:23] problem. But let me ask again, what
[01:50:26] queries might I need to answer this
[01:50:29] question? And there are two queries that
[01:50:31] I need to do to answer the question of
[01:50:33] which books were published by Fitz Carlo
[01:50:35] auditions. What two queries are they?
[01:50:40] >> I think it's select and where did you
[01:50:43] mean keywords or queries?
[01:50:46] >> Yeah. So keywords would be great. So I
[01:50:48] need to have some kind of select
[01:50:49] involved. I need to probably select
[01:50:51] something from publishers and something
[01:50:54] from books. So could I ask you what
[01:50:56] would I select from publishers and what
[01:50:58] would I select from books then
[01:51:02] let's take either another hand or
[01:51:04] following up here.
[01:51:06] >> Okay. So we would take the publisher. So
[01:51:08] select publisher ID from uh where
[01:51:11] publisher equals the publisher name
[01:51:13] we're looking for. And then uh we would
[01:51:16] nest this query inside the other one. So
[01:51:20] we can find the the name of the book
[01:51:22] published by this publisher since we
[01:51:25] found the ID.
[01:51:26] >> Yeah, some good ideas here. And let me
[01:51:28] propose to do it a bit visually here
[01:51:30] first. So I want to figure out first
[01:51:33] what is the ID of Fitz Caraldo editions?
[01:51:36] Well, I could write a query to find that
[01:51:37] and I'll say get back five for Fitz
[01:51:40] Caraldo editions. Well, that's one step.
[01:51:43] But my next step is then to say what
[01:51:45] books fit that publisher ID. So I'll
[01:51:49] write another query this one to
[01:51:51] determine which titles have a publisher
[01:51:53] ID of five and I'll get back let's say
[01:51:56] minor detail and paradus. So let's make
[01:51:59] this more concrete as you were doing
[01:52:01] yourself John Paul and let's write these
[01:52:03] queries out. Let's say I have this first
[01:52:05] one to determine what is the ID of Fitz
[01:52:08] Caraldo editions. I could say select ID
[01:52:12] from publishers where the publisher is
[01:52:14] Fitz Caraldo additions and I'll get back
[01:52:18] from this query the number five. Well, I
[01:52:21] could use that number in my next query.
[01:52:24] As we saw visually here, I could then
[01:52:25] say select title from books where the
[01:52:30] publisher ID is five and I would get
[01:52:33] back many titles here. But here's
[01:52:36] another question. Why is this not very
[01:52:39] well designed? At least in the query I
[01:52:42] have here, what could I improve about it
[01:52:45] or what kind of smells wrong about it
[01:52:47] for you?
[01:52:50] >> They are not connected.
[01:52:51] >> Yeah. So, Jean Paul, as you said too,
[01:52:53] they're not connected. And here I have
[01:52:55] this ID of five, but I mean I don't want
[01:52:58] to remember this number. I mean, I don't
[01:53:01] want to have to keep it in my mind and
[01:53:02] like use it later on in my queries. I
[01:53:04] ideally could use some other query to
[01:53:07] find this number for me more
[01:53:09] dynamically. And so SQL supports this
[01:53:12] idea of writing a sub query, a query
[01:53:15] within a query. For example, I'll take
[01:53:18] this and I'll convert it to the query we
[01:53:21] had before. I'll select title from books
[01:53:25] where the publisher ID is equal to well
[01:53:29] the result of this query here. And
[01:53:31] notice how I have parenthesis. This
[01:53:34] means the query furthest inside the
[01:53:36] parentheses will be run first. So first
[01:53:39] this query is run. I get back five. Then
[01:53:42] I could finish out my query and say
[01:53:44] select title from books where publisher
[01:53:46] ID is equal to five.
[01:53:50] So let me pause here before we do some
[01:53:52] practice in our SQLite terminal. What
[01:53:55] questions do we have on these kinds of
[01:53:58] sub queries so far?
[01:54:02] I was wondering what would happen with
[01:54:04] um those records that don't match in the
[01:54:06] subquery.
[01:54:07] >> Yeah, good question. So if the ID
[01:54:10] doesn't match, is that what you're
[01:54:11] asking?
[01:54:15] Yeah, I'm hearing yes. So if the ID
[01:54:17] doesn't match, um that's a good
[01:54:18] question. So we can treat it as we would
[01:54:20] a regular old SQL query that we learned
[01:54:23] about um in last week. So we said select
[01:54:25] title from books where publisher ID is
[01:54:29] equal to let's say some value and we'll
[01:54:32] then filter out all of those that don't
[01:54:34] have that particular value. So if we
[01:54:37] have a publisher ID of six or of three
[01:54:39] those won't be included anymore because
[01:54:41] we said where publisher ID is equal to
[01:54:44] five. And now looking at this query too.
[01:54:48] Well, let's say I might write select ID
[01:54:50] from publishers where publisher is or
[01:54:52] equal to Fitz Caraldo editions. Maybe
[01:54:55] that publisher doesn't exist. There's no
[01:54:58] publisher with that name. Well, in that
[01:55:00] case, this query would return nothing
[01:55:03] and therefore the next would also return
[01:55:06] nothing. So, we have queries dependent
[01:55:07] on the results of the other queries
[01:55:09] here. So let's actually try this using
[01:55:12] our SQLite terminal to get a better feel
[01:55:14] for what we can do with this kind of um
[01:55:17] structure for our queries. I'll go back
[01:55:19] to my computer and I'll hop into my
[01:55:22] SQLite environment. Let's say here I
[01:55:25] want to do a similar query but I want to
[01:55:27] find those books that were published by
[01:55:30] Maclo editions or Maclo press rather. So
[01:55:33] let me try to attempt this one by one
[01:55:36] going one step of the way and then
[01:55:38] finally combining my queries into one I
[01:55:40] could use more dynamically. So to our
[01:55:43] point earlier we have to first find the
[01:55:46] ID of Macose press. Let me try to find
[01:55:49] that. I'll say select let's say ID from
[01:55:54] publisher where the publisher is equal
[01:55:57] to none other than Macose press like
[01:56:01] this. and my quotes semicolon hit enter
[01:56:05] and hopefully oh I will see see an error
[01:56:09] and based on this error let me ask our
[01:56:12] group here what did I do wrong
[01:56:19] >> judging by the error I think you just
[01:56:22] mistyped the table name
[01:56:25] >> yeah so I probably mistyped the table
[01:56:26] name and we could probably parse this if
[01:56:28] I look at the error itself so it says
[01:56:30] parse error no such table publisher and
[01:56:34] that's true there is no table called
[01:56:36] publisher so let me fix this and run it
[01:56:37] again I'll say select let's say ID from
[01:56:42] the publishers
[01:56:44] table plural and we'll say um where the
[01:56:50] publisher is equal to Macly hose press
[01:56:54] like this and I'll hit a semicolon here
[01:56:57] and now fingers crossed this should work
[01:56:59] I do see an ID of 12. Okay, so Macose
[01:57:03] press the ID is 12. Now I want to find
[01:57:05] the books that were published by this
[01:57:08] ID. So let me go to my book table. I
[01:57:12] will say select title from books in this
[01:57:17] case where the publisher ID is equal to
[01:57:22] 12 as we saw before semicolon. Now I'll
[01:57:25] hit enter and I'll see these are the
[01:57:28] books that Maclost Press has published.
[01:57:31] But again as we saw before I could
[01:57:33] improve this. I could make this better,
[01:57:35] more dynamic by nesting my queries
[01:57:38] having a subquery a query inside of a
[01:57:42] query. So let's redo this. I'll start at
[01:57:45] the end. Essentially, I'll say select
[01:57:48] title. Select title from my book table
[01:57:52] where the publisher ID is or is equal to
[01:57:58] what? Well, let's say I don't know it's
[01:58:00] 12. I have to write another query here.
[01:58:02] So, to do that, I could open up some
[01:58:04] parenthesis. Is equal to a parenthesis.
[01:58:07] And then I'll hit enter to continue my
[01:58:10] query. I'll uh indent four spaces. space
[01:58:14] space space space just a style
[01:58:16] convention to keep things clean for me
[01:58:17] to show this query is inside of this
[01:58:20] other query. What I'll then do is finish
[01:58:23] out this query. I want to select I want
[01:58:26] to select the ID from the publishers
[01:58:31] table where let me just indent again
[01:58:34] where the publisher is equal to uh not
[01:58:39] fit scroll auditions is equal to Mac
[01:58:41] leos press end quote and now let me
[01:58:46] close my parenthesis I have an open one
[01:58:48] here that I should close to show this
[01:58:50] subquery is done I'll hit enter close my
[01:58:54] parenthesis. And now my entire query is
[01:58:57] done. I can hit semicolon, hit enter
[01:59:00] again, and now I'll see the very same
[01:59:02] results, but more dynamic. No longer do
[01:59:04] I have to hardcode the ID. I can make it
[01:59:07] more dynamic, and I can actually find it
[01:59:09] using my very own query here. Let's try
[01:59:13] a different context, too. Maybe I want
[01:59:15] to find all of the ratings for this book
[01:59:19] called In Memory of Memory. Well, maybe
[01:59:22] I'll try it step by step. And what I'll
[01:59:25] first do is try to find the ID for in
[01:59:28] memory of memory. I'll say select ID
[01:59:31] from uh let's go from the books table
[01:59:34] and let's say where the title is in
[01:59:39] memory of memory memory of memory end
[01:59:45] quote semicolon. Hit enter and we'll see
[01:59:48] 33. So this book has the ID 33.
[01:59:53] Okay. Let's now look in our ratings
[01:59:55] table for this ID. I'll say select let's
[01:59:58] go for select rating from my ratings
[02:00:02] table where the book ID is equal to 33 I
[02:00:07] believe it was. So now I'll hit enter.
[02:00:10] And now I should see all of the ratings
[02:00:13] for this book. And there are quite a few
[02:00:15] that people have left on this book on
[02:00:17] the Goodreads website. So let me again
[02:00:21] try to improve this and make it just a
[02:00:22] little bit better. I'll be more dynamic
[02:00:24] about it and try to nest these queries.
[02:00:26] I'll say select rating from ratings.
[02:00:30] We'll start at the beginning. We
[02:00:32] ultimately want ratings. Well, I want
[02:00:34] those ratings where the book ID is equal
[02:00:38] to some number, but I don't know what
[02:00:41] number yet. So I have to write my own
[02:00:43] nested query. I'll I'll create a
[02:00:46] parenthesis like this. Enter. I'll
[02:00:48] indent four spaces. Space space space.
[02:00:52] And then I'll say I want to find the ID
[02:00:55] from the books table. From the books
[02:00:58] table um where this title is equal to in
[02:01:03] is equal to in memory of memory. And
[02:01:07] that is my sub query now. So, I'll close
[02:01:11] this out. I'll hit enter. Close my
[02:01:13] parenthesis. Now have a semicolon and
[02:01:16] hit enter. And I see those very same
[02:01:19] ratings. Well, I could probably not get
[02:01:22] back the individual ratings. I want to
[02:01:23] kind of average them over time. So,
[02:01:25] let's try that, too. I'll say the same
[02:01:28] thing. Select rating from ratings. But
[02:01:30] now, no longer do I want to select all
[02:01:32] the ratings. I want to average them. So,
[02:01:34] I'll say select the average rating of
[02:01:36] this book from ratings. And now let me
[02:01:40] go back over to my nested query and I
[02:01:42] will hit enter again and I will hit the
[02:01:44] up arrow to get back access to my
[02:01:46] earlier parts of my um my SQLite
[02:01:49] environment. I'll hit enter here. Close
[02:01:51] it out. Semicolon. And now I should see
[02:01:54] the average rating for this book.
[02:01:58] Okay. So this is very handy for us.
[02:02:01] We're able to kind of replicate those
[02:02:02] queries we would have done with a single
[02:02:04] table but now using sub queries. And so
[02:02:07] far we've seen this working for a
[02:02:10] relationship that is one to many. We
[02:02:13] could also use sub queries with many to
[02:02:15] many relationships. These tables that
[02:02:17] have many items over here and many items
[02:02:19] over there that relate in some way.
[02:02:22] Let's try it let's say with authors and
[02:02:25] books. And I want to figure out let's
[02:02:28] say which author wrote flights. Which
[02:02:31] author wrote flights? So, let me ask
[02:02:36] what should I figure out along the way
[02:02:39] to get to the author who wrote flights?
[02:02:41] Could you walk me through what I might
[02:02:43] need to know for that query?
[02:02:46] >> Uh, you need to know ID of author and of
[02:02:49] that book and based based on that
[02:02:54] relation you have to join all three
[02:02:57] tables together.
[02:02:59] Yeah, I have to know ids and I have to
[02:03:02] kind of walk across these three tables
[02:03:03] as you're saying. So, let's go back to
[02:03:06] our tables and I want to know who wrote
[02:03:09] flights. Well, a good place to start to
[02:03:11] your point is to say let's start at
[02:03:13] flights and find the ID. Well, the ID of
[02:03:16] this seems to be 78. Okay, let me then
[02:03:20] look in our authored table and let me
[02:03:22] try to find the author ID that
[02:03:24] corresponds with 78. Well, I find 78
[02:03:27] here. What's next to it? Well, 58. Okay,
[02:03:30] so the author ID who wrote flights is
[02:03:33] 58. Well, who is 58? I'll look in the
[02:03:36] author's table and I'll see this is none
[02:03:38] other than Olga. Okay, so let's walk
[02:03:42] through trying to make this query
[02:03:44] happen, but now using SQL keywords. I'll
[02:03:48] start first with trying to find the ID
[02:03:50] of flights. I'll select the ID from the
[02:03:53] books table where the title is equal to
[02:03:55] flights. Okay, that's fair enough. Now,
[02:03:58] I could nest this query, put it inside
[02:04:02] another query to find the author ID of
[02:04:05] the person who wrote flights. I'll do a
[02:04:07] bit like this. I'll select author ID
[02:04:10] from authored where the book ID is equal
[02:04:13] to my prior query. Select ID from
[02:04:16] flights where title is equal to or from
[02:04:19] books where title is equal to flights.
[02:04:21] And now I could go one step further. I
[02:04:24] could say I want to find the name of the
[02:04:26] person who has this author ID. Let me
[02:04:28] nest again. Let me put this query select
[02:04:31] name from authors where ID equals and
[02:04:34] put all the rest of it inside of the uh
[02:04:37] nested query here. So to be clear, I'll
[02:04:40] start from the middle, find the ID of
[02:04:42] flights, then I'll find the author ID
[02:04:45] for that book ID, and then I'll find the
[02:04:48] name of the author who wrote that book.
[02:04:52] Okay, so a good number of steps here,
[02:04:55] but let's try it out ourselves in our
[02:04:57] SQLite terminal. I'll come back to my
[02:04:59] computer and here maybe I want to find
[02:05:02] all of those books or maybe not all
[02:05:04] those books. I want to find the author
[02:05:05] of a particular book you might be
[02:05:07] familiar with called the birthday party
[02:05:09] from our librarian conversation a little
[02:05:10] earlier. Let me say I want to first find
[02:05:13] the ID of the birthday party. I'll say
[02:05:16] select ID from books where title is
[02:05:21] equal to the birthday party semicolon
[02:05:26] enter. Now the ID is 8. Okay, let me
[02:05:32] keep that in mind and actually I don't
[02:05:34] quite need to know this. Let me try to
[02:05:36] nest this query inside some other query
[02:05:39] to keep going towards my goal of finding
[02:05:41] the author of the birthday party. So the
[02:05:44] next thing to figure out as we saw
[02:05:45] before is finding the author ID. I'll
[02:05:48] say select let's say the author ID from
[02:05:52] the authored table. That table of
[02:05:55] authors who have written books and I'll
[02:05:57] say where the book ID where the book ID
[02:06:01] is none other than the one I got back
[02:06:04] from this prior query. Let me indent and
[02:06:06] say select ID from books where title is
[02:06:10] equal to the birthday party quote not a
[02:06:15] semicolon yet my parenthesis semicolon
[02:06:19] hit enter and now I see 44.
[02:06:22] So we're getting there but now I have to
[02:06:24] figure out who has the ID of 44 in my
[02:06:28] author's table. Let's keep going. Let's
[02:06:30] clear our terminal using control L. And
[02:06:33] I will then say select the name from the
[02:06:36] author's table. We're going to start at
[02:06:38] the be or going to yeah start at the
[02:06:39] beginning the place we want to actually
[02:06:40] get to. Then I'll say where the ID or
[02:06:44] the ID of that author is equal to the
[02:06:47] result of this query. What is the author
[02:06:50] ID associated with the book I want to
[02:06:53] find? So I'll select author ID from
[02:06:56] authored from authored and I'll say
[02:07:00] where the book ID
[02:07:02] is equal to another subquery here I'll
[02:07:06] indent four times and four again. Now
[02:07:08] I'm nesting twice. Right? So I'll then
[02:07:11] say select ID from books and I'll hit
[02:07:15] enter just to kind of keep me on um some
[02:07:18] good style here. I'll indent eight times
[02:07:20] total or and then I'll say um where
[02:07:25] where let me make sure I'm doing the
[02:07:27] right thing. Where the title is the
[02:07:30] birthday party.
[02:07:32] Okay, that was a lot. Now we'll close
[02:07:34] out our queries. I'll hit enter space
[02:07:37] again semicolon or uh parenthesis enter
[02:07:40] again parenthesis semicolon. And
[02:07:42] hopefully after all this typing we'll
[02:07:44] get back what we want. we see our friend
[02:07:47] Lauren Movenier. So this is an example
[02:07:50] of trying to find the author who wrote a
[02:07:53] particular book although it's a bit
[02:07:54] long-winded using these kinds of
[02:07:56] subqueries.
[02:07:57] So let me pose questions then we've seen
[02:08:02] how to use these subqueries for one to
[02:08:05] many relationships and also many to
[02:08:07] many. What questions do you have about
[02:08:09] how to use these queries?
[02:08:12] I remember you talking about books with
[02:08:14] the same name and fact they can have
[02:08:15] different versions and etc. How would
[02:08:18] you get the ID for the different
[02:08:20] versions if they are titled the same as
[02:08:22] I'm guessing you wouldn't
[02:08:25] I I'm guessing you would set the for you
[02:08:28] wouldn't set the foreign key to a title
[02:08:29] instead of be primary or is it done
[02:08:31] differently?
[02:08:32] >> A good question here. So you could
[02:08:34] imagine a database that has um more than
[02:08:37] one edition of a book inside of it. like
[02:08:39] maybe I have two editions of the
[02:08:40] birthday party or the hard coverver and
[02:08:42] the paperback and all these other
[02:08:43] editions, right? Well, in that case,
[02:08:46] what I might do is try to actually this
[02:08:49] is a good segue. I might have multiple
[02:08:52] IDs that I'm searching for. Like let's
[02:08:53] say I don't care if it's the um hard
[02:08:55] cover or paperback version. Well, I
[02:08:57] could look for the ID of like 55 and 56
[02:09:00] and try to find um the author of both of
[02:09:02] those. So, let's actually keep going
[02:09:04] here. Let me show you a new keyword to
[02:09:05] use for those kinds of questions if you
[02:09:08] don't mind. Um, let me come back to my
[02:09:10] computer and let's introduce this new
[02:09:13] keyword that can help us find the author
[02:09:16] of not just one book but perhaps
[02:09:18] multiple books or different versions of
[02:09:20] the same book. Let me introduce this
[02:09:22] one. This one is called in. Very simple,
[02:09:25] just i. And I can use in to say well
[02:09:29] maybe some key or some column is in some
[02:09:33] set of values not just equal to one but
[02:09:36] in some set of values. So let's see an
[02:09:38] example here. We're back at our authors
[02:09:41] books and authored tables. And maybe I
[02:09:45] want to find the books written by these
[02:09:48] two authors gauze and Olga. Well I could
[02:09:51] select their IDs. I could say get back
[02:09:54] 27 and 58. Now I have two ids. So I
[02:09:58] could look in authored and I could say
[02:10:00] give me back all of the book IDs that
[02:10:04] have an author ID of 27 and 58. Okay,
[02:10:08] I'll look here and I'll get back both
[02:10:10] four and 78. So notice how earlier I was
[02:10:14] asking show me the book IDs where author
[02:10:18] ID is equal to some single value. Here
[02:10:21] I'm asking find me the book ids where
[02:10:24] book ID has where the author ID is in
[02:10:28] some set of values more than one. Now
[02:10:31] and similarly let me look at my books
[02:10:33] table. Let me say okay I want to find
[02:10:35] the titles for these books. Well I'll
[02:10:37] find the titles that have that have book
[02:10:40] ids in this set of ids four and 78. So
[02:10:45] let's see this in action in our SQL
[02:10:48] terminal. I'll come back over here and
[02:10:51] I'll write this query to find all of the
[02:10:54] books by a particular author named
[02:10:56] Fernanda Melor. So I'll go back to my
[02:10:59] terminal and Fernanda is more prolific
[02:11:02] than most. She's written actually two
[02:11:04] books that are on the long list for the
[02:11:06] Booker Prize. So I'll say select ID from
[02:11:11] authors where the name is equal to
[02:11:16] Fernanda Fernanda Melor semicolon and
[02:11:20] this now is Fernanda's ID 24. Okay, let
[02:11:24] me find the ids of books that Fernanda
[02:11:27] has written. I will now say select uh
[02:11:31] book ID. Select book ID. If I can type
[02:11:35] like book ID from the authored table
[02:11:38] where the author ID is equal to the
[02:11:42] result of this query 1 2 3 four spaces
[02:11:45] here and I'll say select ID from authors
[02:11:48] where the name is equal to Fernanda
[02:11:51] Melor
[02:11:54] parenthesis semicolon and I'll hit enter
[02:11:57] and I'll get back not one book ID but
[02:12:00] two. So if I want to find these titles,
[02:12:03] I should say find me the titles where
[02:12:06] the book ID is not equal to but is in
[02:12:09] this set of ids. So let's try that. Let
[02:12:13] me say select title
[02:12:16] from books where the ID is in some set
[02:12:20] of values is in those two ids we saw
[02:12:23] earlier. So I'll say in enter 1 2 3 four
[02:12:27] spaces and then I'll say select the book
[02:12:31] ID from authored where let me actually
[02:12:35] um space this again where the author ID
[02:12:39] is equal to the result of this subquery.
[02:12:42] We can use equals here because there's
[02:12:44] only one author ID we care about. I'll
[02:12:47] hit enter. Then I'll do space space
[02:12:49] space four spaces for one indentation
[02:12:53] and now four more spaces 1 2 3 four to
[02:12:55] indent again to my next nested query.
[02:12:59] I'll then say select let's say the ID
[02:13:02] from authors from authors where the name
[02:13:06] is equal to Fernanda Melor. And now let
[02:13:11] me close out my queries. I'll hit enter
[02:13:14] space space again. And now I'll use
[02:13:16] parenthesis to close out my middle
[02:13:18] subquery. I'll do the same. I'll hit
[02:13:21] enter and then I'll do another
[02:13:22] parenthesis and then semicolon here. Hit
[02:13:25] enter. And now I should see finally
[02:13:28] Fernandanda's two books.
[02:13:31] Okay. So this is one example of using
[02:13:35] in.
[02:13:37] What questions do you have on how to use
[02:13:40] this syntax? Actually my question was
[02:13:43] not regarding n but actually the
[02:13:45] indentation you use regarding the
[02:13:47] subqueries because while you were using
[02:13:50] the subqueries you mentioned that you
[02:13:52] are giving four spaces. Is there any
[02:13:54] necessity of using like such kind of
[02:13:56] indentation while we are using
[02:13:57] subqueries?
[02:13:59] >> Yeah great question about style here and
[02:14:00] let me try to pull up some slides that
[02:14:02] have um an example of that style so we
[02:14:04] can talk about it. Let me try to find an
[02:14:07] example of our nested query. I'll pull
[02:14:10] this one up. And as you might remember,
[02:14:14] we had three queries here. And I tried
[02:14:17] to keep track of them by indenting them
[02:14:19] more and more and more. This isn't
[02:14:22] required. You could um I mean, don't do
[02:14:25] this, but you could put it all on one
[02:14:27] line, which would just be crazy long to
[02:14:29] read. What we do instead is we'll often
[02:14:31] try to hit enter when it feels nice to
[02:14:33] have a break in the reading um length
[02:14:36] and we'll then indent some spaces to
[02:14:38] show that this query is a subquery of
[02:14:41] the prior one. The exact amount to
[02:14:43] indent might vary but the idea of trying
[02:14:46] to break up your lines and trying to
[02:14:48] indent is going to be a good one for
[02:14:51] your own sake and for those who read
[02:14:53] your code.
[02:14:55] Let's take one more too. when do we need
[02:14:58] to use in in wear clause when we are
[02:15:00] doing you know subquerying I suppose
[02:15:02] that we can also use subquerying without
[02:15:05] in as well
[02:15:07] >> you're right so we saw an example using
[02:15:09] equals and we also saw an example using
[02:15:12] in general if you want just a you know
[02:15:15] rule of thumb to follow if you're
[02:15:17] looking to see if some ID is part of a
[02:15:21] list of IDs or part of a set of ids that
[02:15:23] is more than one you should use in in is
[02:15:26] good for checking if something is inside
[02:15:28] of more than one um item. Let's say
[02:15:32] equals though is good if you know you
[02:15:34] have only one ID. Let's say I have an ID
[02:15:37] equal to 23 or equal to 25. That's a
[02:15:41] good place for equals. If though I had
[02:15:43] 23 or 25, I might use in to match either
[02:15:47] or of those in that set. But good
[02:15:50] question. Let's take one more here too.
[02:15:52] >> We have seen many to one to many
[02:15:55] relationships. one to one relationships
[02:15:57] and many to many relationships. So how
[02:15:59] would many to one relationships be
[02:16:01] tackled? Suppose one book has three
[02:16:03] authors. Then how would that be
[02:16:05] represented in the tables?
[02:16:08] >> Yeah, let's look at the example of one
[02:16:10] book having three authors for instance
[02:16:12] and let's look at our authored table. So
[02:16:15] let me pull up that slide for you and
[02:16:16] we'll talk about it in just a minute.
[02:16:18] I'll come back over here and I will pull
[02:16:21] up our example of having authors and
[02:16:25] books and the authored table in the
[02:16:27] middle. And to your question of how
[02:16:29] could I have let's say a book written by
[02:16:32] three authors. Well, we could imagine
[02:16:34] that this table um let's say um let's
[02:16:37] talk about Boulder for instance. So
[02:16:38] Boulder has the ID of one. Let's say
[02:16:41] three people wrote Boulder. Well, in
[02:16:43] this case we could adjust this. I could
[02:16:45] say this is no longer 74. This is one.
[02:16:47] And same thing here. This is not four.
[02:16:49] This is one. We have the book ID one in
[02:16:53] here more than once. It's in here 1 2 3
[02:16:55] times. But what we're saying each time
[02:16:58] is that well 23 was an author of one. 31
[02:17:02] was an author of one as well. And so was
[02:17:05] 27. So I would not be afraid to have
[02:17:08] multiple um instances of your foreign
[02:17:12] key inside of this table. What I
[02:17:14] wouldn't do is have it more than once in
[02:17:16] your primary key here. Here it actually
[02:17:19] has some information who authored which
[02:17:21] book. Here it is strictly a unique ID
[02:17:24] that should be only a one to one
[02:17:26] relationship. Every key has to be unique
[02:17:28] for the items in that table.
[02:17:31] Good questions.
[02:17:34] Okay, so we've seen sub queries, but
[02:17:37] there is one more technique we could use
[02:17:40] to solve some of these problems of
[02:17:41] quering across tables. And this one is
[02:17:44] going to be called a join. So let's dive
[02:17:46] into joins. And the whole idea behind
[02:17:49] joins is trying to take a table and
[02:17:53] combine it with some other table. And
[02:17:56] actually for this we have uh some I
[02:17:58] don't know maybe guests for our class.
[02:18:00] We have these very cute sea lions. And
[02:18:02] we'll use a database of sea lions to
[02:18:04] understand how joins actually work. So,
[02:18:07] if you're not familiar, sea lions are
[02:18:09] sometimes native to the coast of
[02:18:10] California, and they like to travel.
[02:18:12] They like to travel really far. They go
[02:18:15] from the southern part of California all
[02:18:17] the way up to Washington State. This is
[02:18:19] many, many miles of traveling for these
[02:18:22] adorable sea lions. So, there are data
[02:18:25] sets that involve sea lions and their
[02:18:28] migration patterns. Here's one, for
[02:18:30] example. Here we have a table of sea
[02:18:34] lions. And here we have a table of their
[02:18:36] migrations. A distance column tells us
[02:18:39] how far they went in miles. And a days
[02:18:42] column tells us how long it took them to
[02:18:44] travel, of course, in days. Well, here,
[02:18:48] if we're researchers, maybe we're
[02:18:50] keeping track of some number of sea
[02:18:52] lions. We're keeping track of Ya and
[02:18:54] Spot and Tiger, Mabel, Rick, and Jolie,
[02:18:56] but we have data on many sea lions,
[02:18:59] perhaps some we aren't even tracking
[02:19:01] anymore. This would be our migrations
[02:19:03] table. Now, it could come to pass that I
[02:19:06] want to figure out, well, how far did
[02:19:08] Spot travel and how far did Tiger
[02:19:11] travel? And what I could do is I could
[02:19:13] use nested queries for this. But perhaps
[02:19:15] better yet, I could try to join these
[02:19:18] tables to see the data all in one table.
[02:19:21] Now, to do that, how could I try to take
[02:19:25] a row from this side and kind of attach
[02:19:29] it to or extend the row here? What idea
[02:19:34] could I use to put the right rows
[02:19:37] together in this case?
[02:19:40] >> Could you use the uh primary key, the ID
[02:19:43] to kind of join them together using the
[02:19:44] primary key and the foreign key?
[02:19:46] >> Yeah, a good idea. So, you might notice
[02:19:48] that we actually have two columns here,
[02:19:51] both called ID, which is handy for us.
[02:19:54] And notice how we have them kind of sort
[02:19:57] of matching. and matching in the sense
[02:19:59] that some of these IDs are actually
[02:20:01] inside of this column too. So we could
[02:20:05] use the primary key in really both
[02:20:08] tables here and try to match it together
[02:20:11] to figure out how these rows could be
[02:20:13] extended to add more columns. We could
[02:20:16] join these tables together to make this
[02:20:18] table ultimately showing us where ya has
[02:20:21] um traveled and how long it took them to
[02:20:23] get there. So the keyword for doing
[02:20:26] these kinds of manipulations with data
[02:20:29] in SQL is called join. Kind of
[02:20:32] straightforward. But let's take a peek
[02:20:33] at what join can do for us inside of
[02:20:36] this database. So I'll go to my computer
[02:20:38] here and I'll pull up this database of C
[02:20:41] lines that I prepared for us today. I
[02:20:44] will clear my terminal. I'll typ
[02:20:48] and I'll get out of my long list
[02:20:50] database. To do that I can typequit a
[02:20:53] SQLite command to leave this
[02:20:55] environment. I'll hit enter. And then
[02:20:57] what I can do is I can type SQLite 3
[02:21:01] space C_lions.
[02:21:04] DB. That is just the name of this
[02:21:06] database. Okay. I'll hit enter. Now to
[02:21:10] make sure I'm in the right place, I
[02:21:12] could type to see what tables are inside
[02:21:15] of this environment. Tables. Enter. I
[02:21:19] see both tables, migrations and sea
[02:21:21] lions, which is promising for me here.
[02:21:24] So, we could see what data is inside of
[02:21:26] these tables. I could say select star
[02:21:29] from C Lions,
[02:21:33] uh, semicolon, hit enter. Now, I see all
[02:21:36] of these adorable sea lions inside of
[02:21:38] this lovely table. What if I wanted to
[02:21:40] find migrations? Well, I could do that,
[02:21:42] too. I could say select star from
[02:21:46] migrations semicolon enter. Now I see my
[02:21:49] data on migrations. And notice how again
[02:21:53] some sea lions are in the sea lions
[02:21:55] table. And we have some ids in our
[02:21:57] migrations table that actually aren't in
[02:21:59] our sea lions table. So we're keeping
[02:22:01] track of only a subset of sea lions. And
[02:22:03] this might have some uh seions we keep
[02:22:05] track of in the past. So not all of them
[02:22:06] as well. Okay. So let's try joining
[02:22:10] these tables to determine where have our
[02:22:13] sea lions been in our sea lions table.
[02:22:16] I'll say select
[02:22:18] uh star from sea lions. But now I don't
[02:22:22] want to end this query here. I want to
[02:22:25] expand this table with the data inside
[02:22:28] of the migrations table. So what could I
[02:22:30] do? I'll hit enter just as as a style
[02:22:33] thing here to now consider how I can
[02:22:36] make a query a bit longer. I'll want to
[02:22:39] join the migrations table to the sea
[02:22:42] lions table. And to do that, I can type
[02:22:44] join. I'll say join then space. And I
[02:22:48] want to say the table I want to join. In
[02:22:50] this case, the table is called
[02:22:52] migrations. I'll say migrations. And I
[02:22:56] have to tell it one more thing. I have
[02:22:59] to tell it what we saw visually earlier,
[02:23:01] which is that the ID column in sea lions
[02:23:04] matches the ID column in migrations. I
[02:23:07] have to tell SQL which two columns to
[02:23:10] try to join these tables by. So let me
[02:23:13] do that. I'll say join migrations on
[02:23:16] which is a SQL keyword what two columns
[02:23:19] should correspond. I'll now say
[02:23:21] migrations.
[02:23:23] ID. This means the ID column inside of
[02:23:26] migrations table is equal to or is going
[02:23:30] to be joined with this sea lions table
[02:23:34] and the ID column within that. Again,
[02:23:38] these two columns should have some
[02:23:40] matching values that we could use to
[02:23:42] make these rows longer with more
[02:23:44] columns. Let me then hit semicolon here
[02:23:47] and hopefully we'll see all of our data
[02:23:51] now combined. I can tell you how far
[02:23:54] Tiger went and how many days it took
[02:23:56] them to do it because I've joined these
[02:23:58] two tables together.
[02:24:01] So in doing this kind of join, just
[02:24:03] regular old join, what we're really
[02:24:05] doing is part of this family of joins
[02:24:09] are called an inner join. You may have
[02:24:11] seen this idea of an inner join or an
[02:24:14] outer join. The usual join, at least in
[02:24:17] SQLite, is going to be an inner join.
[02:24:20] And what do we mean by inner join? Well,
[02:24:23] let's visualize it a little more slowly
[02:24:26] here and see the process of which we
[02:24:28] might use to understand this join. I'll
[02:24:30] have again my two tables, but now
[02:24:33] simplified. I have name and ID and just
[02:24:37] distance and ID. And to join these, I
[02:24:40] could literally kind of nudge them
[02:24:41] together and draw a line down the middle
[02:24:44] a bit like this. But what do you notice?
[02:24:48] I mean, this one seems to match this ID.
[02:24:51] And this ID seems to match this ID. But
[02:24:54] these two, well, they don't match. I
[02:24:56] mean, poor Jolie down here. We don't
[02:24:57] know how far Jolie went. And if we don't
[02:25:01] know this data, if these IDs don't
[02:25:04] match, if we can't find a match for this
[02:25:07] ID or for this ID, well, let's sadly
[02:25:10] just get rid of the row. Like, it's not
[02:25:11] part of our join table anymore. It's
[02:25:13] gone from our memory. We now have only
[02:25:16] these tables or these rows that we could
[02:25:19] actually join together with the row and
[02:25:22] the other table here.
[02:25:25] So this is our example then of an inner
[02:25:28] join. Let me ask what questions do you
[02:25:31] have on these joins so far?
[02:25:35] >> So the confusion for me right now is
[02:25:37] where were the IDs generated? Was it on
[02:25:39] the C lion table or on the migration
[02:25:42] table? And what kind of problem can that
[02:25:43] pose like maybe in real world? So that's
[02:25:45] the question I have maybe not directly
[02:25:47] to joint itself.
[02:25:48] >> No, that's a great question and good to
[02:25:50] clarify. So um we have sea lions with
[02:25:53] some ID and we see here that you know
[02:25:56] one ID is 10484 another ID is 11728 and
[02:26:00] to your good question which is how do we
[02:26:02] get these IDs? Well, these actually came
[02:26:05] to us from researchers perhaps who are
[02:26:07] researching sea lions. And if you're not
[02:26:09] familiar, let me go back to our slide
[02:26:10] with sea lion migrations on it.
[02:26:13] Researchers might often want to keep
[02:26:14] track of where sea lions have been. And
[02:26:17] to do so, they will aum non-invasively
[02:26:20] apply some tag to this animal that has
[02:26:22] some unique ID on it. And they'll track
[02:26:25] where that tag goes to understand where
[02:26:28] this particular sea lion went. So they
[02:26:30] will make up their very own primary
[02:26:32] keys, their very own unique IDs to
[02:26:35] identify these sea lions. We can then
[02:26:38] use those same IDs in our table to
[02:26:41] understand where these sea lions are
[02:26:43] going. And just to be clear, too, let me
[02:26:45] find our full data set here. Here we
[02:26:48] have those sea lions that we're now
[02:26:50] interested in. Those were now tracking.
[02:26:53] But you could imagine that we also have
[02:26:55] some sea lions that, you know, we no
[02:26:57] longer track. and you know maybe they've
[02:26:59] you know gone on they're doing something
[02:27:01] else now they're not part of our data
[02:27:02] set so that's why we might see some over
[02:27:04] here but not over here I hope that helps
[02:27:08] answer your question about the sources
[02:27:09] of this data so let's take one more when
[02:27:14] we join together the two migration and
[02:27:16] seell the ID table is repeating so I
[02:27:20] just want uh days and the travel
[02:27:24] distance I don't want to repeat the
[02:27:26] table of ID is that possible
[02:27:29] Yeah. And I think if I'm understanding
[02:27:30] correctly, we want to try to um not just
[02:27:33] join these tables, but maybe remove the
[02:27:36] duplicate ID in them. Like if I showed
[02:27:38] you this joined table right here, ID
[02:27:41] appears in here twice. There is a way to
[02:27:43] do this, and we'll see it towards the
[02:27:45] end of our exploration of joins. We'll
[02:27:47] come back to that in just a minute.
[02:27:50] Okay. So, we've seen inner joins so far.
[02:27:53] are this way of combining tables and
[02:27:55] only keeping the data that actually
[02:27:57] matches between them. Well, let's try a
[02:28:00] new uh way of joining. This one that
[02:28:02] might not be so strict. We have a few
[02:28:05] options here. We have what we're going
[02:28:07] to call a left join, a right join, and a
[02:28:12] full join. And you could imagine based
[02:28:15] on the names here, what each one might
[02:28:18] do. You could think of our tables, one
[02:28:20] being on the left, one being on the
[02:28:22] right, and trying to join them,
[02:28:24] prioritizing either the left table or
[02:28:27] the right table, or maybe even both per
[02:28:30] a full join. So, let's get a feel for
[02:28:33] what kinds of tables we get back from
[02:28:35] these different commands, and we'll talk
[02:28:37] about we'll visualize how this is
[02:28:39] actually happening underneath the hood.
[02:28:42] Let's go back to our computer here and
[02:28:44] let's try to do a left join using our
[02:28:47] two data sets. Now, a left join will
[02:28:51] prioritize, so to speak, the data on my
[02:28:54] left table. Left being quote unquote
[02:28:56] because there is no left or right in a
[02:28:58] database, but left here means the first
[02:29:00] table that I start with. So, let's try
[02:29:03] this. I'll say select um star. Select
[02:29:07] star. And let me just make sure I'm
[02:29:09] typing the right things here. Let me try
[02:29:12] select star from the sea lions table.
[02:29:17] And now I don't want to just do a
[02:29:19] regular old join. I want to do a left
[02:29:22] join. I want to no matter what always
[02:29:25] have the data on my left table. This sea
[02:29:28] lions table here. Left join. And I'll
[02:29:32] join migrations. I have to say the same
[02:29:35] thing. Which column in migrations
[02:29:37] corresponds to which column in se lines?
[02:29:40] I'll say left join migrations on
[02:29:42] migrations
[02:29:44] id equals sea lions
[02:29:48] id as well. Now I think that's just
[02:29:51] about it for my join. So I'll say
[02:29:52] semicolon enter. And notice the
[02:29:55] difference here. Let me walk to this
[02:29:57] board so we can see it in its entirety.
[02:29:59] I have all of my sea lions now in this
[02:30:04] table. where we left off Jolie earlier.
[02:30:06] We've now kept Jolie in even though
[02:30:09] Jolie doesn't have a distance or number
[02:30:12] of days. We actually haven't tracked
[02:30:14] that data yet for Jolie, but we still
[02:30:16] see them in this table.
[02:30:19] Let's now try a right join to see the
[02:30:22] difference between this and the right
[02:30:24] join. I'll come back over here and let's
[02:30:27] try prioritizing our rightmost table.
[02:30:30] This one perhaps being the migrations
[02:30:32] table. So I'll say select star from sea
[02:30:36] lions. This will again be our left quote
[02:30:39] unquote table just because it comes
[02:30:41] first. Now I'll say join uh not just
[02:30:44] join I'll say write join migrations
[02:30:48] on again migrations ID equals let's say
[02:30:53] sea lions.
[02:30:55] I semicolon. Now let's see the
[02:30:59] difference here. Well, what have we
[02:31:01] done? We've actually left off a few sea
[02:31:04] lions. Now, we only have those whose ids
[02:31:07] were in the right table. Again, the
[02:31:10] right table being that second one we
[02:31:12] used. And even if we don't have any
[02:31:15] names for these sea lions, we'll still
[02:31:17] include them in our data set. We can see
[02:31:20] though that this data is missing and
[02:31:22] that as we'll see, it has some special
[02:31:23] value called null. So, we have a left
[02:31:27] join and a right join. A full join
[02:31:30] though allows us to see the entirety of
[02:31:33] both tables and which values are
[02:31:35] missing. Let's try that now. I'll come
[02:31:37] back over here and I'll do a full join.
[02:31:40] I'll say select star from sea lions full
[02:31:45] join migrations on full join migrations
[02:31:49] on migrations
[02:31:53] migrations. ID
[02:31:55] is equal to sea lions do ID semicolon
[02:32:00] enter. And now what do we see? Well, we
[02:32:02] see both tables in their entirety. We
[02:32:06] have Jolie in here still even though
[02:32:08] Jolie doesn't have a distance or some
[02:32:11] number of days. We also have our sea
[02:32:14] lions, our mystery sea lions down below
[02:32:16] who don't have any name but are still
[02:32:17] included in our migration table too. So
[02:32:21] left join, full join and right join.
[02:32:25] So let's then visualize this to
[02:32:27] understand what's happening along the
[02:32:28] way. I'll go back to some slides here.
[02:32:31] Let's look first at these um left joins
[02:32:34] as well. So really all of these left
[02:32:37] join, right join and full join. These
[02:32:40] are all part of this family called an
[02:32:42] outer join. An outer join lets you keep
[02:32:45] some data even if the join is not going
[02:32:49] to quite work out for you as much as you
[02:32:51] would want it to in an inner join. By
[02:32:52] that I mean you might have some null or
[02:32:55] empty values in this join after you run
[02:32:58] it. So let's visualize it. Here I have a
[02:33:01] left outer join and I want to combine
[02:33:04] this left table with this right table.
[02:33:07] I'll do a left outer join. I'll put them
[02:33:09] together. And notice how these two don't
[02:33:12] match. Well, because they don't match,
[02:33:15] I'll fill in these values with the value
[02:33:18] that signifies empty or null. In this
[02:33:20] case, it is literally null. There's
[02:33:22] nothing here. So, because I did a left
[02:33:25] join, what I should do is prioritize
[02:33:28] this left table's data. Even if this
[02:33:31] doesn't have any match here, I'll still
[02:33:33] keep this row. But notice down below
[02:33:36] that this ID has no match in the left
[02:33:39] table. I'll omit that and in the end
[02:33:42] I'll delete this bottom row but be left
[02:33:44] with Jolie who might or may not have
[02:33:47] data in the right table. Let's try the
[02:33:50] right join. Right outer join. I'll do
[02:33:53] the same thing. Combine them and they'll
[02:33:55] do the same exact kind of orientation. I
[02:33:58] have some null values here that I don't
[02:34:00] quite know how to match up. What I can
[02:34:03] do instead is say, well, I want to
[02:34:04] prioritize the data on this rightmost
[02:34:06] table, even though this ID has no match.
[02:34:10] I want to keep it because it's inside
[02:34:12] this right table. Okay, let me delete
[02:34:14] this row because it has no match in my
[02:34:16] right table. And I'll be back to this
[02:34:19] type of join, keeping every ID in the
[02:34:22] right table. A full join, a bit more
[02:34:24] simple. I'll take the same data, join it
[02:34:27] together, and I'll simply say I don't
[02:34:29] care if there are null values involved.
[02:34:32] I'll leave them be.
[02:34:35] Okay, so this is a lot of visualizing.
[02:34:38] Let me ask what questions do we have on
[02:34:42] these joins?
[02:34:44] Could I somehow work with multiple
[02:34:46] tables? Uh is there, you know, if I have
[02:34:49] like three tables, which one is the left
[02:34:51] one, which one is the right one, and
[02:34:52] what's the third one?
[02:34:54] >> Yeah. A good question. So, we've seen
[02:34:56] two tables so far and this was
[02:34:58] deliberate kind of pedagogically. It' be
[02:35:00] a lot to see three joins all at once.
[02:35:02] Um, if you're thinking about joining
[02:35:04] three tables though and you're asking
[02:35:06] which one is your left table, which one
[02:35:08] is your right table, always it will be
[02:35:10] that the table that comes first before
[02:35:13] your join command, your keyword will be
[02:35:15] the left table and the table that's
[02:35:17] involved in your join keyword like join
[02:35:19] migrations, let's say, that will be your
[02:35:22] right table. And so you can imagine
[02:35:24] three tables um where for like the first
[02:35:26] two, the first one's on the left, the
[02:35:28] first one's on the right. For the next
[02:35:30] two though, the middle one's on the left
[02:35:31] and the next one's on the right. If that
[02:35:33] helps you visualize without having much
[02:35:34] on the board here. Good question. Let's
[02:35:38] take one more.
[02:35:40] When we perform the join function, do we
[02:35:42] get under the hood, do we have like a
[02:35:44] separate table that's created which we
[02:35:46] can reference later down in the code or
[02:35:48] like do we need to write that entire
[02:35:50] join command again? Yeah, good question.
[02:35:52] And so I believe you're asking, do we
[02:35:54] get back a separate table that we could
[02:35:56] use? Um, for this I might want to
[02:35:58] doublech check myself, but just to kind
[02:36:00] of show you what we've been doing so
[02:36:01] far, go back to my um SQLite terminal
[02:36:04] here and I will ask like select star
[02:36:09] from um let's say sea lions and let's uh
[02:36:14] do a full join with migrations on
[02:36:17] migrations. ID is equal to um sea lions
[02:36:23] id. And I think what you're asking is do
[02:36:24] we get back like a separate kind of
[02:36:26] table here. Um we could
[02:36:29] consider it as a kind of separate table
[02:36:31] like if I hit enter here is this is kind
[02:36:34] of something we're going to call a
[02:36:35] temporary table which you could also
[02:36:37] call a result set. We can use this table
[02:36:40] for the duration of our query. What we
[02:36:42] haven't done though is made this table
[02:36:45] accessible in our database itself. like
[02:36:48] this is only there for the duration of
[02:36:50] this query. So hopefully that helps
[02:36:53] answer it with a bit of um factchecking
[02:36:55] if you need to as well.
[02:36:58] Okay, let's show one final type of join
[02:37:00] here. This one called a natural join. A
[02:37:03] natural join kind of allows me to omit
[02:37:06] the part of the my previous joins where
[02:37:08] I was saying migrations ID equals sea
[02:37:11] lions id like natural join says both
[02:37:14] these columns are called ID. I could
[02:37:17] just assume that I want you to join by
[02:37:19] these two columns. So, let's try a
[02:37:21] natural join and see what we get back.
[02:37:24] I'll come back over here and we'll try a
[02:37:27] natural join with our sea lions table
[02:37:30] and our migrations table. I'll say
[02:37:33] select let's say star from sea lions.
[02:37:37] Then I'll natural join migrations here.
[02:37:41] And I no longer need to say migrations
[02:37:44] ID equals sea lions do ID. I can just
[02:37:47] hit semicolon. And now I can hit enter.
[02:37:50] So we'll see that the join worked just
[02:37:53] as we wanted it to. And we didn't even
[02:37:56] specify which ID column corresponded to
[02:37:58] which other ID column because these were
[02:38:01] named the same column name ID. Notice
[02:38:05] too, we don't get a duplicate ID column.
[02:38:08] In some prior joins, we had an ID column
[02:38:10] here and an ID column here. Now, we've
[02:38:13] just combined them into one single
[02:38:16] column or really only kept one column
[02:38:18] among this join here. So, many kinds of
[02:38:23] joins to use, many ways to query our
[02:38:26] tables. What we've seen so far is how to
[02:38:29] organize our data, build connections
[02:38:31] between them, and now how to query this
[02:38:34] data using both subqueries and joins.
[02:38:37] We'll take a quick break here and come
[02:38:38] back to see how we can use sets and
[02:38:40] groups to again kind of refine our
[02:38:43] queries and ask more interesting
[02:38:45] questions too. Well, we're back and now
[02:38:48] we're going to focus on this idea of
[02:38:50] sets in SQL. So, when you run a query,
[02:38:54] you get back some results and those
[02:38:56] results are often called a result set.
[02:38:59] Some set of values that you've gotten
[02:39:01] back from your table. So let's take a
[02:39:03] look at what sets are and how we could
[02:39:06] use them to refine our queries and to
[02:39:08] find relationships among different
[02:39:10] groups of people, places or even things.
[02:39:13] So let me ask a question of you. Maybe
[02:39:16] in this world we have authors and we
[02:39:18] have translators at least in the
[02:39:20] publishing industry, right? If you're in
[02:39:22] this set, you are an author. If you are
[02:39:26] in this set, then you're a translator.
[02:39:30] But what would it be then if you were in
[02:39:33] this set? What does this set mean?
[02:39:39] >> It means that uh you are both the author
[02:39:42] and the other one. So translator.
[02:39:44] >> Yeah, you're right. So this means you
[02:39:46] are both an author and a translator.
[02:39:49] You're in the middle of these two
[02:39:51] overlapping circles. In SQL, we could
[02:39:54] represent this kind of relationship
[02:39:56] using our intersect operator, which
[02:39:58] we'll see in just a moment. We'll take
[02:40:00] authors perhaps and intersect them with
[02:40:02] those who are translators and find those
[02:40:05] who are both authors and translators.
[02:40:08] Let's do another one then. Let's think
[02:40:10] of this set. Who are you? Or at least
[02:40:14] what does the set represent as a whole?
[02:40:18] >> It means that you're either an author or
[02:40:20] a translator.
[02:40:21] >> Nice. You're either an author or a
[02:40:24] translator. You could be both, too, but
[02:40:26] you're in either camp. You're either an
[02:40:28] author or a translator. And for this, we
[02:40:31] could use a SQL keyword called union.
[02:40:34] I'll take my set of authors and combine
[02:40:37] them with my set of translators and get
[02:40:39] back, in this case, the entirety of
[02:40:41] these two sets. Let's look at this one,
[02:40:44] too. If you are in this set, who's
[02:40:49] included there?
[02:40:53] Only authors will be included. Authors
[02:40:56] which are also translators will not be
[02:40:57] included here.
[02:40:59] >> Yeah, good. So here only authors are
[02:41:02] included. We see that those who are also
[02:41:04] translators aren't included. In fact, if
[02:41:07] you are an author and only an author,
[02:41:10] then you are in this set. And to get
[02:41:12] this kind of result, we would use our
[02:41:15] SQL keyword called accept. I'll take my
[02:41:18] set of authors but subtract or remove or
[02:41:21] accept my set of translators. Similarly,
[02:41:25] I could say take my set of translators
[02:41:28] and accept the set of authors. Subtract
[02:41:30] them, remove them. And I could do that
[02:41:32] with translators except authors. We'll
[02:41:35] see these keywords in just a moment.
[02:41:38] Now, I have one final question here,
[02:41:41] which is how could you represent this
[02:41:45] one? I mean, who are you if you are in
[02:41:48] either this set or this set? And how
[02:41:51] would you get that kind of set? I'll
[02:41:53] actually save that one for you to do as
[02:41:54] homework, if I may, before we move on to
[02:41:56] seeing these in our actual terminal
[02:41:59] environment. So, let's take this idea of
[02:42:01] sets and apply it to authors and
[02:42:02] translators this time in our database.
[02:42:06] I'll come back over to our SQLite
[02:42:08] terminal and let me now leave our
[02:42:11] database of C lines. Sadly, I'll
[02:42:13] typequit and go back to my regular old
[02:42:16] terminal. Now, I want to open back up
[02:42:19] our longlist db database. Long list db.
[02:42:23] Hit enter. And now I'm back in the place
[02:42:26] where I have authors and books and
[02:42:28] publishers inside of this database. I'll
[02:42:32] type L to clear my terminal. And let's
[02:42:34] first try to find all of those who are
[02:42:37] either translators or authors. Well,
[02:42:41] what could I do? I could try this. Let
[02:42:43] me try select select name from
[02:42:47] translators like this or my translators
[02:42:49] table. Semicolon enter. These are all of
[02:42:52] my translators.
[02:42:54] Now I want to find authors. I could then
[02:42:57] say select name from select name from
[02:43:02] authors semicolon. Hit enter. Now I have
[02:43:05] all of my authors. If I wanted though to
[02:43:09] combine these results, these result
[02:43:11] sets, I could do so using union. So
[02:43:15] let's try it. I'll say select name.
[02:43:19] Select name from translators
[02:43:22] and not finish my query yet. I'll hit
[02:43:25] enter just for style sake. And I'll say
[02:43:28] union union with some other result I'll
[02:43:32] get back from some separate query. I'll
[02:43:34] hit enter. Now I'll say select let's say
[02:43:37] name from let's go for authors now end
[02:43:41] quote semicolon hit enter and now I'll
[02:43:45] see both authors and translators and we
[02:43:49] should see here that every author and
[02:43:52] every translator is in here only once.
[02:43:55] We can assume that we have unique names
[02:43:57] for these authors and translators. And I
[02:44:00] could scroll through and figure out who
[02:44:02] is either an author or a translator.
[02:44:04] Actually see them both in the same set.
[02:44:07] If I wanted, I could distinguish between
[02:44:10] authors and translators by adjusting my
[02:44:12] query just a little bit. I could say
[02:44:14] select um let's go for select uh author
[02:44:20] the string as profession and also select
[02:44:25] name from the author's table semicolon.
[02:44:29] This will give me back not just one
[02:44:30] column of names but also a another
[02:44:34] column called profession that has just
[02:44:36] author inside of it. I'll hit enter and
[02:44:39] I'll see I indeed have this column if I
[02:44:42] scroll all the way up called profession
[02:44:44] and I have the value being author. Okay,
[02:44:48] let's combine these. Let's union this
[02:44:50] set with the set of translators and give
[02:44:52] them their profession too. I'll say
[02:44:55] select author as profession
[02:44:59] and then also name from
[02:45:03] the author's table and now I'll hit
[02:45:05] enter and I'll say union that set with
[02:45:09] the set of translators. I'll say select
[02:45:12] translator the string as the column
[02:45:16] profession. Then I'll say name from the
[02:45:19] translators name from the translators
[02:45:22] table quote unquote semicolon. Hit
[02:45:25] enter. And now I could actually see who
[02:45:27] is a translator and who is an author. If
[02:45:30] I scroll through here I'll see
[02:45:31] translators and now I'll also see
[02:45:34] author. So I've combined these two sets
[02:45:37] into one that works for me here. Okay.
[02:45:41] So this is how to union or combine our
[02:45:43] sets. But what if we wanted to find only
[02:45:45] those who are authors and translators?
[02:45:49] Kind of a unique niche group of folks.
[02:45:51] But who is part of this set? Well, let's
[02:45:54] try to find out. I could select names
[02:45:57] from the author's table as I did before.
[02:46:01] Now, instead of union, let me intersect
[02:46:04] these names with those that will be in
[02:46:07] the translators column. I'll say
[02:46:09] intersect.
[02:46:10] intersect and select name from
[02:46:14] translators.
[02:46:16] And now I'll hit semicolon enter. I'll
[02:46:20] see one his name is Goi who is both an
[02:46:22] author and a translator. They translated
[02:46:25] their own book into English for the
[02:46:27] international booker prize. Okay. So
[02:46:31] let's try now to find those who aren't
[02:46:34] just translators and authors but only
[02:46:38] those who are perhaps translators or
[02:46:39] only those who are um authors. So let's
[02:46:43] try this. I'll say select name from
[02:46:46] authors. Hit enter. And now I want to
[02:46:50] exclude those who are also translators.
[02:46:52] I'll say except in this case select name
[02:46:56] from select name from translators. Hit
[02:47:01] semicolon. And now I should see if I pay
[02:47:04] close enough attention that Goi is not
[02:47:07] in this list. They are an author and
[02:47:10] they were in the author set of names,
[02:47:13] but because they're also a translator,
[02:47:15] they're not inside this set of list.
[02:47:19] So this is fine and good for finding
[02:47:21] who's in one list, who's in some other
[02:47:23] list, and who's in between them. But
[02:47:25] it's also nice for trying to find books
[02:47:28] people have collaborated on, let's say.
[02:47:30] Maybe I want to find the books that both
[02:47:32] Sophie Hughes and Margaret Costa have
[02:47:35] written together jointly. So I could try
[02:47:38] to find first the books that Sophie
[02:47:40] Hughes has translated. Let's say select
[02:47:44] um select book ID
[02:47:47] from the translated table. This table
[02:47:50] that has translated has translators and
[02:47:52] books inside of it. And then I'll say
[02:47:55] where the translator where the
[02:47:58] translator ID is equal to this subquery.
[02:48:03] I'll find Sophie Hughes's ID as a
[02:48:06] translator. I'll say select ID from
[02:48:09] translators
[02:48:11] from translators
[02:48:14] where the name is Sophie Hughes. Okay.
[02:48:18] Semicolon to end. And these are the book
[02:48:21] IDs that Sophie Hughes has translated
[02:48:23] because Sophie Hughes is a translator.
[02:48:26] Well, let's see. Maybe they have
[02:48:29] translated some books with Margaret
[02:48:30] Costa as well. I could try to find out.
[02:48:33] I'll say select
[02:48:35] say select book ID. We'll try to find um
[02:48:39] Sophie's books again. I'll say select
[02:48:41] book ID uh from trans from translated
[02:48:47] where the translator
[02:48:50] ID is equal to again Sophie Hughes's
[02:48:53] translator ID select ID from translators
[02:48:57] where let's say the name is Sophie
[02:49:01] Hughes like this now I'll close out this
[02:49:05] part of my query but I want to find the
[02:49:08] intersection the set of book ID keys
[02:49:10] that are the same between Sophie
[02:49:11] Hughes's translated works and Margaret
[02:49:13] Costa's translated works too. So I'll
[02:49:16] continue. I'll say intersect intersect
[02:49:20] this result with some other query. All
[02:49:22] right. Now let me select the book ids
[02:49:26] from the translated table where the
[02:49:29] translator
[02:49:30] the translator ID is equal to a
[02:49:34] different kind of query. This one will
[02:49:36] get back the ID for Margaret Costa. I'll
[02:49:39] say select ID from translators and where
[02:49:43] the name is equal to and I believe in
[02:49:46] this particular case they go by Margaret
[02:49:49] Ule Costa like this. Now I'll hit enter
[02:49:54] close out this subquery and finally I
[02:49:56] can hit semicolon. This is the end of my
[02:49:59] query. Semicolon here and now I'll see
[02:50:02] the book ID they have collaborated on.
[02:50:05] You could imagine going beyond this to
[02:50:08] find the title of this book ID using
[02:50:11] another nested query, but I won't spend
[02:50:13] time on that at least for now because I
[02:50:15] have to write all this text back out for
[02:50:17] you. So, we've seen union, we've seen
[02:50:21] except, we've seen intersect. What
[02:50:24] questions do you have on these sets and
[02:50:27] how they work?
[02:50:29] >> You've got three joints. I just wondered
[02:50:30] if there was a default that you chose if
[02:50:32] you didn't know what the situation was
[02:50:33] like which one to use.
[02:50:35] >> Yeah. So we saw different kinds of
[02:50:37] joins. Um we saw uh we saw left join,
[02:50:40] right join, full join, right? And the
[02:50:43] default as we saw a little before is
[02:50:44] just a simple join. And that join is an
[02:50:47] example of an inner join. It'll only
[02:50:49] take those rows where the ids actually
[02:50:52] match up. You could get more specific
[02:50:53] and have a left or right join or a full
[02:50:55] join, but we'll leave that um for you to
[02:50:58] try out on your own and see the results
[02:50:59] of as we did before too. But great
[02:51:01] question.
[02:51:02] >> You mentioned that the ids from both
[02:51:05] tables were used automatically to merge
[02:51:07] the two tables and we didn't have to
[02:51:09] bother with the duplicate um duplicate
[02:51:12] column for an ID. So I was wondering in
[02:51:14] a situation whereby the primary key are
[02:51:17] actually like foreign keys. Let's say
[02:51:18] you're trying to join with another table
[02:51:20] where your ID is actually like a foreign
[02:51:22] key. How would you go about doing that?
[02:51:24] Because it seems we didn't specify the
[02:51:26] ids where wanted to like make the joins
[02:51:28] on with a natural join. So I just wanted
[02:51:30] to needed some clarification on that
[02:51:32] front.
[02:51:33] >> Yeah. And let me make sure I'm
[02:51:34] understanding correctly. So I think
[02:51:35] you're trying to think about how you
[02:51:36] would um join a table that has a
[02:51:38] different kind of column name from the
[02:51:41] other one. Um, and for that you could
[02:51:42] use the equals there and you could say
[02:51:45] um, we said migrations id equals sea
[02:51:48] lionsid. But let's say the sea lions ID
[02:51:51] was actually called um, sea lions ID
[02:51:54] like the full thing spelled out. I could
[02:51:56] say join um, migrations on migrations
[02:52:00] equals sea lions. Lions ID to spell out
[02:52:04] the column name for SQL. Good question
[02:52:07] too. Can I use intersect and the union
[02:52:10] together between more than two tables,
[02:52:12] three tables or four tables? Yeah, could
[02:52:16] you use intersect more than once? Let's
[02:52:17] say to intersect more than one set. You
[02:52:20] absolutely could. And here I don't have
[02:52:23] a good example planned for this, but you
[02:52:25] could have one query that does one
[02:52:27] thing. Gives you some set and you type
[02:52:29] intersect after it. Then you get back
[02:52:31] the next query and you find the
[02:52:32] intersection of that. You could then
[02:52:34] type intersect again to get the
[02:52:35] intersection of all of these three sets.
[02:52:37] you keep going going as you'd like to.
[02:52:40] The key thing here though is that in
[02:52:43] your intersects or in your unions or in
[02:52:45] your excepts, you always have to have
[02:52:47] the same number and the same type of
[02:52:51] columns. So if I was trying to combine,
[02:52:53] let's say, author names with um book
[02:52:56] titles, I can't intersect or union those
[02:52:59] quite well because they have different
[02:53:01] kind of meanings, right? They're
[02:53:02] different kinds of things. So if you're
[02:53:04] trying to join multiple thing, trying to
[02:53:06] join multiple tables or interact
[02:53:07] multiple tables, make sure you always
[02:53:09] have those same column names and those
[02:53:11] same column types, the type of data
[02:53:13] that's stored inside.
[02:53:17] Okay, so we've seen sets now and we're
[02:53:20] going to conclude by looking at this
[02:53:22] idea of groups. Well, groups will allow
[02:53:25] us to recreate some of what we tried to
[02:53:27] do a little bit of last week, trying to
[02:53:30] um understand the average rating of some
[02:53:33] books. Let's take a look at groups now.
[02:53:36] Well, you could imagine that I have my
[02:53:38] ratings table. And in this ratings
[02:53:40] table, I have book IDs and I also have
[02:53:44] ratings. Here, I see that the book ID of
[02:53:48] one has several ratings for people who
[02:53:50] gave the book a rating. It has four,
[02:53:52] three and four. And similarly, book ID
[02:53:55] with two has two ratings from folks two
[02:53:58] and three. Now I want to find the
[02:54:01] average rating across these ratings for
[02:54:04] each book ID. So let me try that in my
[02:54:08] terminal. Come back over here and let me
[02:54:11] first try to find the average rating for
[02:54:13] each of these books. So I'll go back and
[02:54:16] I'll say why don't I select the average
[02:54:19] average rating. It's like the average
[02:54:21] rating from my ratings table. And I
[02:54:25] think this should be good enough. So
[02:54:26] I'll hit semicolon. And I'll see well
[02:54:29] 3.83644.
[02:54:32] And this seems to be an average, but I
[02:54:35] wanted the average of each book. So what
[02:54:39] did I do wrong here? What am I actually
[02:54:42] seeing in this case?
[02:54:46] Is that an average of all books in the
[02:54:49] entire table?
[02:54:51] >> Yeah, good instinct. So, let me try to
[02:54:52] put back our table here. We can see
[02:54:54] what's actually going on. I'll come back
[02:54:57] over here and I will show us again this
[02:55:00] table. So, we had a table of ratings,
[02:55:03] right? And we had the rating column that
[02:55:06] has individual ratings inside of it.
[02:55:08] When I say select the average rating
[02:55:11] from this table, well, what am I
[02:55:13] getting? I'm getting the average of all
[02:55:16] of these ratings, not grouped by book
[02:55:19] ID. So, if I want to find the average
[02:55:23] rating for each book, I need to employ
[02:55:26] this idea of groups. And I mean,
[02:55:28] wouldn't it be nice if I could do
[02:55:29] something like this? I could kind of
[02:55:31] highlight the rows that are part of each
[02:55:33] group and then try to average those. I
[02:55:35] could say, take all the books with ID 1
[02:55:38] and all the books with ID2 and just
[02:55:40] collapse their ratings like this. And
[02:55:42] once you do that, find the average for
[02:55:45] me and give me that back as a table.
[02:55:48] That'd be kind of nice. And luckily, we
[02:55:50] actually have the capacity to do that
[02:55:52] with SQL using this group by keyword.
[02:55:55] So, we'll see this in action. I'll come
[02:55:58] back over here and let's try to redo
[02:56:00] this query to find the right answer.
[02:56:03] I'll come back and I'll say let's select
[02:56:06] let's select in this case the book IDs
[02:56:11] and also their average rating. I'll
[02:56:15] select book ID that's one column I want
[02:56:17] and I also want the average rating from
[02:56:21] this column from this table. Now I'll
[02:56:25] say let me title this perhaps as average
[02:56:28] rating. So, I'll get the average rating
[02:56:30] and just title that column average
[02:56:32] rating. Exactly. I want to select this
[02:56:35] from the ratings table.
[02:56:38] Okay. But now I don't want to simply hit
[02:56:42] enter. I'll get back the same thing I
[02:56:44] did before, which is the average of all
[02:56:46] the ratings in the ratings table. What I
[02:56:49] want is for these ratings, the average
[02:56:51] ratings to be grouped by the book ID. So
[02:56:54] I'll say group by book ID semicolon hit
[02:56:59] enter. And now I should be able to see
[02:57:03] the results I wanted. Let me scroll to
[02:57:06] the top and notice how using group by I
[02:57:10] was able to take each book ID collapse
[02:57:14] the rows the ratings were associated
[02:57:16] with this book and find the average of
[02:57:18] that rating 3.77 3.97 3.04 4 for each
[02:57:24] book. So, kind of handy here. Let me try
[02:57:28] to improve this and show you one
[02:57:30] additional thing we could do as well.
[02:57:32] I'll come back and why don't I try to
[02:57:37] replicate what we did last time, which
[02:57:38] was find the books that have a certain
[02:57:40] rating or higher. Let's try that. I'll
[02:57:44] say select let's say the um book ID and
[02:57:50] let's get now the rounded rating the
[02:57:53] rounded average rating. I'll round the
[02:57:55] average rating to two decimal places and
[02:57:59] I'll call this average rating as a
[02:58:02] column. Okay, I'm going to select this
[02:58:05] from my books table from my ratings
[02:58:09] table, sorry. And now I want to group by
[02:58:13] the book ID to find the average rating
[02:58:17] for each book ID.
[02:58:20] Now though, let's say I only want those
[02:58:23] books that are pretty well rated,
[02:58:25] greater than 4.0 out of five stars. To
[02:58:28] include a wear clause, I could try
[02:58:31] following up on this group by. And you
[02:58:33] might think I could say, well, where the
[02:58:36] average where um average rating that new
[02:58:39] column I created is greater than or
[02:58:40] equal to 4.0.
[02:58:43] But I can't because these are now not
[02:58:46] individual rows, they are groups. SQL
[02:58:49] uses a different keyword for conditions
[02:58:52] on groups than for conditions on
[02:58:54] individual rows. And this keyword is
[02:58:56] called having. H A V I N G. Let me try
[02:58:59] that. H A V I N G. I want to group by
[02:59:03] the book ID and only keep those that
[02:59:05] have an average rating of greater than
[02:59:08] 4.0. I will scroll over here and I'll
[02:59:11] hit enter. And now I should see a much
[02:59:14] smaller list. I see book ID 5 has a
[02:59:17] 4.06, 10 has a 4.04 and so on. And now
[02:59:21] the next step is you could imagine me
[02:59:23] perhaps joining these book IDs with
[02:59:26] another table that has titles inside of
[02:59:28] it too to find the average rating given
[02:59:31] some title as well. So groups allow us
[02:59:35] to take these columns collapse some rows
[02:59:38] and find aggregate statistics across
[02:59:41] each of those groups. Let me ask then
[02:59:44] what questions we have on groups.
[02:59:48] What if I don't want to see the rate the
[02:59:51] average rating of a book, but how many
[02:59:54] ratings does it have?
[02:59:56] >> Oh, good one. So, I want to know not the
[02:59:58] average rating, but the number of
[03:00:00] reviews. Let's say the number of ratings
[03:00:02] it was given in my table. Well, for
[03:00:04] that, I could just modify my query a
[03:00:06] little bit. I could change average to
[03:00:09] count because count counts up the number
[03:00:11] of rows that I have. So, let me try that
[03:00:13] here. I'll come back to my laptop and
[03:00:16] let me try this one. I will select book
[03:00:20] ID and I will also select the count of
[03:00:24] book ID um in my no also select the
[03:00:28] count of ratings how many ratings there
[03:00:29] are inside my ratings table. Count of
[03:00:32] rating from let's say the um ratings
[03:00:36] table like this. Now I want to group
[03:00:40] this data group the counting by book ID.
[03:00:43] So I'll say group by book ID. Give me a
[03:00:46] count of the ratings for each book ID.
[03:00:49] And now I could just hit semicolon and
[03:00:52] enter. And now I'll see how many ratings
[03:00:56] each book actually has. Let me go to the
[03:00:58] top here. And I'll see book ID 1 has
[03:01:02] 2779 ratings. Book ID 2 has 175 ratings
[03:01:06] and so on. A good question. Let's take
[03:01:10] one more too.
[03:01:12] So considering this new having syntax,
[03:01:14] how could we couple that with the order
[03:01:16] by?
[03:01:18] >> Yeah, where does it fit in with order
[03:01:19] by? Like let's say I want to sort this
[03:01:21] data to at the end of the day. Well, I
[03:01:23] could do that as well. Let me show you
[03:01:25] one example. I'll come back to my
[03:01:27] terminal and I could try this. Let me
[03:01:31] come back to uh finding average ratings.
[03:01:34] So I'll say select book ID and the
[03:01:38] rounded average rating to two decimal
[03:01:42] places calling that column average
[03:01:46] rating. And I'll select this from the
[03:01:50] ratings table. Well, now we want not
[03:01:53] just to find the average rating, we also
[03:01:56] want to sort by that column too. And in
[03:01:59] fact use having to only find those books
[03:02:01] that have 4.0 know or higher. Well,
[03:02:04] let's try this. I'll say from ratings
[03:02:06] and I'll still group by book ID.
[03:02:11] Now, I'll say I only want to filter to
[03:02:14] those groups that have a average rating
[03:02:18] of greater than 4.0. And finally, after
[03:02:22] I've filtered out all of these rows, I
[03:02:25] want to order them. I want to sort them.
[03:02:27] So, I'll order them by average rating.
[03:02:31] this column I made up top and I'll say
[03:02:34] order them descending order. I want
[03:02:37] biggest to smallest and fingers crossed
[03:02:39] I'll hit enter and we'll see our ratings
[03:02:43] sorted for us. So great question here to
[03:02:47] reimplement much of what we did last
[03:02:50] time. And now indeed we've kind of come
[03:02:54] full circle here. We've taken these
[03:02:56] ideas and we've seen them in single
[03:02:58] tables as we did last week. We this week
[03:03:01] took our tables and expanded them into
[03:03:03] multiple tables, different authors,
[03:03:05] different publishers, different ratings
[03:03:06] and so on. And we learned how to query
[03:03:09] those tables using subqueries and using
[03:03:12] joins. What we'll see next time is
[03:03:14] putting you in the driver's seat, having
[03:03:16] you actually create your own tables,
[03:03:18] define your own relationships, and build
[03:03:20] a database to your own liking. So, all
[03:03:23] that and more next time. We'll see you
[03:03:25] there.
[03:03:28] [Music]
[03:03:45] Well, hello one and all and welcome back
[03:03:48] to CS50's introduction to databases with
[03:03:50] SQL. My name is Carter Zeni and last we
[03:03:53] left off we learned about relating. That
[03:03:55] is how to have multiple tables in our
[03:03:57] database for people, places, and things
[03:04:00] and how to have them relate to one
[03:04:02] another in the way we might do in the
[03:04:03] real world. Now today we'll take a step
[03:04:06] forward and we'll talk about how to put
[03:04:08] you in the driver's seat designing your
[03:04:10] very own database schemas to organize
[03:04:13] your data. Now we'll pick up where we
[03:04:15] last left off which was with this
[03:04:16] database of books. So we had this
[03:04:19] database that was full of books that
[03:04:21] have been long listed for the
[03:04:23] international booker prize. To be long
[03:04:26] listed means to be nominated for some
[03:04:28] prize let's say. So we had the past five
[03:04:31] years of books in this database and we
[03:04:33] worked on improving this database over
[03:04:36] time from week zero to week one. Now
[03:04:39] this week we'll actually take a look
[03:04:40] underneath the hood and see what
[03:04:42] commands we had used to create these
[03:04:45] very databases. So let's reveal now what
[03:04:48] we had done all along. I'll go back to
[03:04:51] my terminal here. And if you remember, I
[03:04:53] could use a command to open up a
[03:04:55] database file, which was this command
[03:04:57] here, SQLite 3, and then the name of the
[03:05:00] file I want to open. So, let's try this.
[03:05:04] I'll go back to week zero to my week
[03:05:06] zero folder like this, and I'll open up
[03:05:08] my longlist database, week zero
[03:05:11] longlist. DB. Okay, I'll hit enter. Now
[03:05:16] I'm in my SQLite prompt. So I could work
[03:05:18] on typing some SQL commands, SQL
[03:05:21] statements or queries inside of this uh
[03:05:24] terminal prompt here. So if I want to
[03:05:27] get a feel for what's inside this
[03:05:29] database, we saw I could use a command
[03:05:31] called select. So I'll select now some
[03:05:34] rows from this table. I'll say select
[03:05:37] let's say the title and also the author
[03:05:42] columns from my long list table
[03:05:45] semicolon and enter. Now I'll see all
[03:05:49] the titles and all the authors that were
[03:05:52] inside of this long list table. But I
[03:05:56] only want to peak here. I only want to
[03:05:58] see roughly what kind of data is inside.
[03:06:01] So I could probably improve this command
[03:06:03] here. I could instead say select the
[03:06:07] author and title columns from long list
[03:06:12] from long list but limit now to the
[03:06:15] first five rows we saw before semicolon
[03:06:19] and I'll hit enter on this query and now
[03:06:21] I'll see only the top five rows. So I'm
[03:06:25] able now to see what kind of data is
[03:06:28] inside my database.
[03:06:31] But what I can't yet see is what command
[03:06:34] was used to create this table and what
[03:06:37] kind of data could be stored inside of
[03:06:40] it. So let's reveal now what was going
[03:06:42] on underneath the hood all this time.
[03:06:44] I'll say this new command a SQLite
[03:06:47] command not a SQL keyword but a SQLite
[03:06:49] command called schema
[03:06:52] schema. Now if I hit enter, I'll see the
[03:06:55] following. The command, the statement,
[03:06:58] the query that was used to create this
[03:07:01] long list table. And notice how I have
[03:07:04] many columns inside this table. I have
[03:07:06] an ISBN column, a title column, an
[03:07:09] author column, and so on. And each
[03:07:12] column seems to have some kind of data
[03:07:15] that could be stored inside of it like
[03:07:17] text or integers or real for
[03:07:20] floatingoint values or decimals if
[03:07:22] you're familiar.
[03:07:24] So this is how we created the very first
[03:07:27] version of longlist db. But let's also
[03:07:30] see how we created the second. So I'll
[03:07:33] type doquit to leave this version of
[03:07:36] longlist db. And now let me open up the
[03:07:39] next version we had created which is
[03:07:41] more relational. It had tables inside of
[03:07:43] it that could relate to one another. So
[03:07:46] let me type SQLite 3 then long list the
[03:07:49] SQLite 3 and go to week one and then
[03:07:52] type long list db. I'll hit enter. Now
[03:07:56] in my next version of long list db. Well
[03:08:00] what could I do? I could type select and
[03:08:02] look at some of the uh tables in here to
[03:08:04] see what kind of data is inside. I could
[03:08:07] perhaps say select maybe the names from
[03:08:11] the author's table here from the
[03:08:13] author's table and hit semicolon. Now
[03:08:17] I'll see all the names of authors that
[03:08:19] are inside of the author's table. I
[03:08:22] could do the same thing for books. I
[03:08:24] could maybe look at the titles of books.
[03:08:26] I could say select title from the books
[03:08:30] table semicolon and enter. Now I see all
[03:08:34] of the titles that are inside my books
[03:08:37] table. But what I haven't seen yet is
[03:08:40] the schema of this database. It is the
[03:08:43] way it is organized and the commands
[03:08:45] that were used to create these tables.
[03:08:48] So let me work on that. Now I'll clear
[03:08:50] my terminal using ctr L. And now let me
[03:08:54] type dots schema again. I'll type dots
[03:08:57] schema to see what commands were used to
[03:09:00] create this database. Hit enter. And I
[03:09:04] can see I mean there are quite a lot of
[03:09:07] commands here. Now this feels
[03:09:08] overwhelming. I mean I'd be right there
[03:09:10] with you, right? This is a lot of
[03:09:11] commands to parse through and read. So
[03:09:14] there's probably a better way to do
[03:09:17] this. And one way to try is to type
[03:09:21] schema and then give it some table name.
[03:09:24] Let's say I want to understand the
[03:09:25] schema for just the books table like
[03:09:27] just that for now. So I'll say dots
[03:09:30] schema and then the table name books in
[03:09:33] this case. Then I can hit enter. Now
[03:09:36] I'll see the schema, the organization,
[03:09:39] the command that we used to create the
[03:09:42] books table in this case. And notice
[03:09:44] again we have several columns ID, ISBN,
[03:09:48] title, publisher ID and so on. Each one
[03:09:51] has their own kind of data they could
[03:09:53] support or take into this column like
[03:09:56] integers, text and so on. So again, what
[03:10:00] we'll do today is have you all learn how
[03:10:02] to write your very own create table
[03:10:05] commands to build your very own
[03:10:07] databases that represent what you want
[03:10:09] to represent in the real world. So, let
[03:10:13] me exit this prompt here and let me
[03:10:17] propose that we'll have a bit of a
[03:10:18] design challenge today to actually try
[03:10:20] to represent a real world entity with
[03:10:23] some database here. And if you're not
[03:10:25] already familiar, uh Boston is perhaps
[03:10:28] famous for being among the first cities
[03:10:30] to have a subway system in the United
[03:10:33] States. So, here is a picture from the
[03:10:36] late 1800s of a subway being built in
[03:10:38] Boston's city streets. underneath the
[03:10:41] streets here. There would be trolley
[03:10:43] cars would go and transport people
[03:10:44] across Boston. Here's another picture of
[03:10:47] a trolley actually working underneath
[03:10:49] the streets. So, people would go down
[03:10:51] underneath. They would hop on a trolley.
[03:10:53] They'll be able to go to different parts
[03:10:55] of Boston, perhaps from Harvard to MIT
[03:10:58] or downtown up to, let's say, Brainree
[03:11:01] or down to Brainree, which is more south
[03:11:02] of Boston, for example. One of the
[03:11:05] famous stops is the Park Street stop
[03:11:07] which is right down in the middle of
[03:11:09] Boston, one of the central hubs of this
[03:11:12] subway system. And now these photos are
[03:11:15] all from, let's say, the early 1900s,
[03:11:18] late 1800s, and so on. But the subway's
[03:11:20] gotten a lot more modern since then. And
[03:11:22] actually now we have several lines that
[03:11:24] span the entire city and beyond. So here
[03:11:27] we have the red line of which Harvard
[03:11:29] and MIT are a part. We have the green
[03:11:32] line which brings you kind of west to
[03:11:33] east, the blue line, the uh orange line
[03:11:37] and so on. So many more lines and
[03:11:40] stations have been added to this system.
[03:11:43] It's a big design challenge to represent
[03:11:45] all of these stations, all of these
[03:11:47] lines and all these people who might
[03:11:50] ride this subway too. So the question
[03:11:53] then becomes how can we create a schema
[03:11:58] for this data? And again by schema we
[03:12:01] mean what kinds of tables should we
[03:12:03] have? What kinds of columns might those
[03:12:06] tables have? And what kind of data
[03:12:09] should we put in each of those columns
[03:12:11] for instance? So let me propose this.
[03:12:14] Let's say we start just first with names
[03:12:17] and stations. So Charlie here, our very
[03:12:19] first rider on this system is going to
[03:12:22] be at the Kendall and MIT station. So
[03:12:25] this is what this table represents now.
[03:12:27] But what more could we have? Well, we
[03:12:30] might also want to have maybe what
[03:12:32] Charlie is doing at that station. Maybe
[03:12:34] he's entering the station, for instance.
[03:12:37] And if you're familiar with the subway
[03:12:39] system, you often have to pay to get
[03:12:42] onto a a train or get onto the station
[03:12:45] itself. So, let's say Charlie pays some
[03:12:48] fair to enter into the Kendall MIT
[03:12:51] station. Well, back in the mid 1900s,
[03:12:53] the fair was only about a dime. It was
[03:12:55] 10 cents. So, we'll say Charlie paid 10
[03:12:58] cents to enter the Kendall MIT station.
[03:13:02] And now, this seems pretty good, but if
[03:13:05] I am the transit authority, the person
[03:13:08] who runs the subway system, I probably
[03:13:10] want to know, does Charlie have enough
[03:13:12] money to get on the train? And if so, I
[03:13:15] want to make sure that, okay, well,
[03:13:16] Charlie actually could get on this
[03:13:18] train. So, let's say not only does
[03:13:20] Charlie pay a fair, he has some
[03:13:22] remaining balance afterwards. So Charlie
[03:13:25] here has gotten onto the Kendall MIT
[03:13:28] stop. He's paid the fair of 10 cents and
[03:13:30] has five cents left.
[03:13:33] Okay. So here's a bit of a table. We
[03:13:37] probably add more information to it.
[03:13:39] Let's say Charlie then leaves at the
[03:13:42] Jamaica plane stop. And the fair to
[03:13:44] leave is about a nickel, 5 cents. And
[03:13:47] now Charlie has no cents left over. So
[03:13:50] again, Charlie paid 10 cents to get on,
[03:13:53] had 5 cents left, paid 5 cents to get
[03:13:55] off, and now has no remaining balance
[03:13:58] here anymore. Okay, so that's Charlie's
[03:14:01] story. Let's look at Alice, though.
[03:14:04] Let's say Alice gets on at the Harvard
[03:14:06] stop. They too pay 10 cents to get on at
[03:14:09] the Harvard stop, and they have a
[03:14:11] remaining balance of 20 cents. Alice
[03:14:14] will go, let's say, to Park Street, get
[03:14:16] off at Park Street, pay the nickel to
[03:14:19] leave, and now they'll have a balance of
[03:14:21] 15 cents at the end. Let's go to Bob.
[03:14:25] Bob enters the alewife station. They pay
[03:14:28] 10 cents. They have a remaining balance
[03:14:30] of 30 cents. And let's say they leave at
[03:14:33] Park Street and have a fair of 10 cents
[03:14:36] to leave because it's a further
[03:14:37] distance. Now, they'll have a remaining
[03:14:39] balance of 20 cents overall.
[03:14:42] So this table
[03:14:45] is okay, I might admit. I mean, last
[03:14:48] time we learned about having we called
[03:14:50] primary keys and foreign keys. So seems
[03:14:53] like that's missing here. Let's go ahead
[03:14:55] and add that here. I'll give each row a
[03:14:58] unique ID so I can know who entered, who
[03:15:00] exited, and so on. And give that a
[03:15:02] unique ID here. But I might even say
[03:15:05] that this table could really be improved
[03:15:09] substantially. And I want to ask you,
[03:15:12] what redundancies or inefficiencies
[03:15:16] do you see here? We're trying to
[03:15:18] represent riders and stations. What
[03:15:21] could we improve about this design?
[03:15:25] >> Hello. So, uh probably the redundancy
[03:15:27] will be the names and the stations too.
[03:15:30] For example, the Charlie will uh go to
[03:15:34] the train daily. Then he will become
[03:15:37] most of the names in the data. Yeah,
[03:15:40] good point. If I'm hearing what you're
[03:15:41] saying, Lauren, let me show you some
[03:15:42] examples that I highlighted here. You
[03:15:45] know, one example could be to your point
[03:15:46] about these names. Like these names seem
[03:15:50] to be telling us the name of a person.
[03:15:53] But here we have only three names,
[03:15:56] Charlie, Alice, and Bob. Well, my name
[03:15:59] is Carter. And what if somebody else
[03:16:02] named Carter also tried to get on and
[03:16:05] leave at some stop? Well, I wouldn't be
[03:16:06] able to know which Carter was which or
[03:16:09] which Charlie was which or which Alice
[03:16:10] was which and so on. So, we probably
[03:16:12] need a way to represent people and their
[03:16:15] names a little better here too.
[03:16:18] What other ideas do we have for how to
[03:16:20] improve the design of this table?
[03:16:24] >> Yes, I think we can have uh a singular
[03:16:27] ID for a singular person. That way,
[03:16:29] we'll be better able to track their
[03:16:30] activities.
[03:16:31] >> Nice. So, we could probably have an ID
[03:16:33] for each person. A bit of what we
[03:16:36] learned about last week, right? Putting
[03:16:37] people in their own table and giving
[03:16:39] them their own unique ID, a primary key.
[03:16:43] Let's show that here. I'll go to some
[03:16:46] slides and I'll pick out one that shows
[03:16:48] us just riders. So, to your point,
[03:16:50] Sukanya, we could try to have maybe a
[03:16:52] table for just riders. And maybe to
[03:16:54] simplify, this table has only two
[03:16:57] columns. It has a column for ID and a
[03:17:00] column for name. So here we have
[03:17:01] Charlie, Alice, and Bob all in their own
[03:17:05] table. Well, let me pros too. We could
[03:17:08] do the same thing for stations. Like
[03:17:10] let's say we have a table of stations
[03:17:12] now and we give each one their very own
[03:17:15] ID as well. Our own primary key for this
[03:17:18] table. We have Harvard, Kendall, and
[03:17:20] Park Street. We can differentiate
[03:17:21] between them using their IDs here. So a
[03:17:26] few improvements could be made. And as
[03:17:29] we're making these improvements,
[03:17:30] splitting one table into many and
[03:17:33] debating what kind of data to store in
[03:17:35] each table, the process we're going
[03:17:37] through is one called normalizing. We're
[03:17:40] normalizing our data. To normalize means
[03:17:44] to reduce redundancies effectively to
[03:17:46] take a table uh take one table for
[03:17:48] instance, split up into multiple and
[03:17:50] have each entity be part of its very own
[03:17:54] table. Some academics in the world have
[03:17:57] named different normal forms quote
[03:17:59] unquote. There's like first normal form,
[03:18:01] second normal form, third normal form.
[03:18:04] This progression of making your data
[03:18:06] more and more efficient. You can use
[03:18:08] those as heruristics. At the end of the
[03:18:10] day, a few principles might apply.
[03:18:12] First, take your entities like in this
[03:18:14] case stations and riders and put them
[03:18:17] each in their own table. And if you add
[03:18:21] more data, make sure that if I were to
[03:18:24] add a column, let's say to riders, it is
[03:18:26] only a data point about riders, not
[03:18:29] about stations, not about fairs, only
[03:18:32] about riders. And that process can help
[03:18:35] us make a data set that is more dynamic,
[03:18:38] more easy to reproduce and more easy to
[03:18:40] write queries on. So that is the process
[03:18:43] here of normalizing.
[03:18:46] Okay. So if we have now riders and
[03:18:50] stations, we want to represent them in
[03:18:53] our table. Well, we could use what we
[03:18:55] learned about relating last week to ask
[03:18:57] how could we actually represent these
[03:18:59] riders and these stations. So let's say
[03:19:02] here I again have riders and stations. I
[03:19:05] want to make sure that I have the right
[03:19:07] relationship between them. Well, if
[03:19:09] you're familiar with subways, we might
[03:19:11] say that a rider goes to one station.
[03:19:14] And this big T here is the symbol for a
[03:19:17] station here in Boston for the T's that
[03:19:19] we call it for the subway. So a rider
[03:19:22] might go to one station, but of course
[03:19:25] that might not be the full picture. A
[03:19:27] rider also gets off at some station
[03:19:29] later on. So a rider could be associated
[03:19:31] with not just one station, but multiple.
[03:19:35] And if you're familiar, at least with
[03:19:37] any subway system, really the Boston one
[03:19:38] too, it can often get pretty busy. And
[03:19:41] so riders might not just go to of course
[03:19:44] one station or two stations could also
[03:19:46] have multiple riders that are on a
[03:19:49] particular station here. So to recap,
[03:19:52] one rider might be associated with more
[03:19:55] than one station. They might get on at
[03:19:58] this first one and get off at this later
[03:20:00] one. But each station could presumably
[03:20:03] have more than one rider. Each station
[03:20:06] here could have rider A or rider B, the
[03:20:09] rider up here or the rider down below
[03:20:11] and even many more than that as well. So
[03:20:15] to put it in the language of our ER
[03:20:18] diagrams, our entity relation diagrams
[03:20:20] from last week, we could look at a bit
[03:20:22] like this where we have riders and
[03:20:25] stations. Riders visit stations and
[03:20:28] they're associated like this. A rider
[03:20:32] must have at least one station
[03:20:35] associated with them. That's what this
[03:20:36] horizontal line means. If they aren't at
[03:20:38] a station, they aren't really a rider,
[03:20:40] right? A rider though could have many
[03:20:44] stations associated with them. That's
[03:20:45] what this three prongs down here means.
[03:20:47] They could have one, two, three, four.
[03:20:50] They could have many stations they get
[03:20:52] on and get off of. Now, a station could
[03:20:56] have anywhere between zero riders, if
[03:20:59] it's maybe out of commission or isn't
[03:21:01] very popular, upwards to many. It could
[03:21:04] have two, three, four, five, even
[03:21:06] hundreds of riders associated with this
[03:21:09] particular station. So, here is our
[03:21:12] entity relation diagram for these
[03:21:14] particular riders and these stations
[03:21:17] here. So let me ask what questions do we
[03:21:21] have on these relationship between
[03:21:23] riders and stations and how to design
[03:21:26] this table so far.
[03:21:28] >> Sir I want to ask that you have used the
[03:21:30] safe ID for stations and riders. So uh
[03:21:33] that maybe uh give us problem in coding.
[03:21:37] >> Yeah a good observation. And so you
[03:21:39] might have noticed that in the riders
[03:21:40] table and in the stations table I gave
[03:21:44] the same kind of ID like I had 1 2 3 for
[03:21:47] each of them. And let me just show you
[03:21:48] that again here. I'll come back to some
[03:21:50] slides and I'll show you again the
[03:21:53] riders table where we had Charlie,
[03:21:55] Alice, and Bob ID 1 2 3. Same for the
[03:21:59] stations. We had stations Harvard,
[03:22:02] Kendall, Park Street, ID 1, 2, 3. And to
[03:22:05] your question, isn't that a problem?
[03:22:08] Well, I would argue in this case it's
[03:22:11] not so long as we keep clear that these
[03:22:15] ids are for stations and these IDs are
[03:22:18] for riders. And we'll see how to do that
[03:22:20] using our SQL keywords later on. But
[03:22:23] again, so long as we have an ID just for
[03:22:26] our riders and an ID just for our
[03:22:28] stations, we can keep these separate
[03:22:31] even if they might have the same values.
[03:22:34] But a great question here. Let's take
[03:22:36] just one more.
[03:22:38] Uh regarding the entity relationship
[03:22:40] diagram, how is it possible for stations
[03:22:43] to have uh a possibility of zero
[03:22:45] writers, but writers must compulsorily
[03:22:48] have at least one station?
[03:22:49] >> Yeah, good question. So, this might be
[03:22:52] up to you and how you formulate it, but
[03:22:54] for me, let me show the diagram again.
[03:22:56] I'll go back to over here. Uh in my
[03:23:01] mind, to be a rider, you have to have
[03:23:04] visited a station. If you aren't
[03:23:05] visiting a station, you aren't really a
[03:23:06] rider right now. Presumably, there are
[03:23:09] stations that were built but aren't
[03:23:11] really being used right now or aren't
[03:23:13] really uh in service yet. That could be
[03:23:15] a station that has no visitors. So, you
[03:23:18] could argue let's make sure every
[03:23:20] station has at least one rider and every
[03:23:23] rider may or not have to visit a
[03:23:24] station. For that, I would say let's
[03:23:26] kind of we could probably reasonably
[03:23:28] disagree there and talk about how we
[03:23:29] could represent the diagram here too.
[03:23:31] But a great observation and a good um
[03:23:34] other critique of this this system here.
[03:23:38] All right. So let's now turn to
[03:23:41] representing this in our database. I'll
[03:23:44] go back to my computer and we'll learn
[03:23:47] about this new SQL uh keyword SQL
[03:23:51] statement. This one called create table.
[03:23:54] Create table allows us to as the name
[03:23:56] suggests create a brand new table. So,
[03:23:59] let's do just that in our new database
[03:24:02] to represent riders and stations. I'll
[03:24:06] go into my terminal and I want to make a
[03:24:09] brand new database. I'll call this one
[03:24:12] MBTA. DB because MBTA stands for the
[03:24:16] Massachusetts Bay Transportation
[03:24:18] Authority, the people who run the subway
[03:24:20] essentially. So, I'll do SQLite 3 MBTA.
[03:24:23] DB hit enter and I'll type Y to say yes
[03:24:27] I want to create this brand new
[03:24:30] database.
[03:24:31] Okay. Now if I type schema
[03:24:35] I see nothing but that's expected. I
[03:24:38] don't have any tables yet. I have
[03:24:40] nothing inside this database. It's up to
[03:24:42] me to create these tables myself. So
[03:24:46] what I'll do is clear my terminal and
[03:24:48] let's start first with riders. I might
[03:24:50] create a table for riders. So I'll say
[03:24:53] create table and now I have to give that
[03:24:56] table some name. I might call it riders
[03:24:59] here and then in parenthesis like this I
[03:25:03] can specify what columns should be part
[03:25:06] of this table. So let's start first.
[03:25:08] I'll hit enter here and continue this
[03:25:11] query. Now I'll by convention just
[03:25:14] indent four spaces. One, two, three,
[03:25:17] four. And I'll give an ID to each of
[03:25:20] these riders as we saw before. I'll say
[03:25:23] ID here is one of my columns.
[03:25:26] Now to create a new column, I'll follow
[03:25:29] this up with a comma and hit enter. I'll
[03:25:33] again by convention for style just
[03:25:35] indent four spaces. And what's my next
[03:25:37] column? Perhaps a name for these riders.
[03:25:40] I'll give this column the name name and
[03:25:43] I'll leave it at that. Once I'm done
[03:25:47] adding columns, I no longer need to have
[03:25:50] a comma. I could simply close out this
[03:25:53] query, this statement. I could hit enter
[03:25:55] here, say close parenthesis to close the
[03:25:58] top parenthesis here, semicolon, hit
[03:26:01] enter, and now nothing seems to happen.
[03:26:05] But that's actually a good sign. So let
[03:26:06] me type dots schema hit enter and I'll
[03:26:09] see the result of that statement before
[03:26:13] create table if it doesn't already exist
[03:26:15] riders and riders has inside of it two
[03:26:18] columns ID and name. Okay, let's keep
[03:26:22] going. Let's make one for stations too.
[03:26:25] I'll clear my terminal and I'll say
[03:26:27] create me a table called stations and
[03:26:30] include actually not station uh if you
[03:26:33] ever want to uh let's say fix this kind
[03:26:36] of table here let me try closing semi
[03:26:40] closing the parentheses hit semicolon
[03:26:42] enter I'll get a syntax error I can
[03:26:44] restart I'll do L now I'll do create
[03:26:47] table stations plural open parenthesis
[03:26:51] enter I'll indent by four spaces 1 2 3 4
[03:26:56] and now I'll similarly include an ID for
[03:26:58] each of these stations. I'll say ID,
[03:27:01] comma, and then what else should I have?
[03:27:04] Well, stations tend to have a name like
[03:27:07] the Kendall MIT station, the Harvard
[03:27:10] station, the Park Street station. So,
[03:27:12] I'll say I'll give each of these their
[03:27:14] very own name,
[03:27:17] what else do stations have? Well, they
[03:27:19] might also have a line that they're on.
[03:27:22] Let's say it's the red line or the blue
[03:27:24] line or the green line and so on. I'll
[03:27:27] have a space for them to write in their
[03:27:29] line that they're a part of. Okay. And
[03:27:33] maybe I'll leave it at that to keep it
[03:27:34] simple. I'll say stations have an ID, a
[03:27:36] name, and a line. Now I'll close this
[03:27:38] out. I'll say end parenthesis semicolon.
[03:27:41] Hit enter. And nothing seems to happen.
[03:27:43] But if I type dos schema, I'll now see
[03:27:46] my riders and my stations tables inside
[03:27:50] of my database.
[03:27:53] Now one more step here. We have riders.
[03:27:56] We have stations. But we have to relate
[03:27:59] them. We have to relate them using this
[03:28:02] many to many relationship as we saw last
[03:28:05] week. So let me try making a table to
[03:28:08] implement this many to many
[03:28:10] relationship. And if you remember we
[03:28:12] might call this kind of table a junction
[03:28:15] table, an associative entity, a join
[03:28:17] table. has a lot of names, but it looks
[03:28:20] a bit like this. I'll create this new
[03:28:24] table to represent, let's say, visits. A
[03:28:27] rider visits a station. So, I'll call
[03:28:30] this table visits. And inside, I'll make
[03:28:34] sure it has two columns. One for a rider
[03:28:38] ID to represent a rider and one let's
[03:28:42] say for a station ID to represent a
[03:28:46] station. Now, when I see a rider ID next
[03:28:50] to a station ID in this table, I'll know
[03:28:53] the rider with that certain ID visited
[03:28:56] the station with that certain ID. So,
[03:28:58] I'll close this out. I'll say end
[03:29:01] parenthesis here semicolon enter. And
[03:29:04] finally clear my terminal type dot
[03:29:06] schema and I can see I have riders
[03:29:09] stations and visits between riders and
[03:29:12] stations in this associative entity this
[03:29:15] junction table or a join table up to you
[03:29:17] what you might want to call it in this
[03:29:19] case. Now what questions do we have
[03:29:24] >> why we have not use the primary key and
[03:29:27] the secondary key in this table?
[03:29:29] >> Uh good question. So we're going to get
[03:29:30] there in just a minute. But if I look
[03:29:31] back at my uh terminal here, my schema,
[03:29:35] I'll see I really just have column
[03:29:37] names. And we saw before when we typed
[03:29:40] schema on our long list db, we had more
[03:29:43] than just column names. We had column
[03:29:45] names, we had perhaps data types, we had
[03:29:48] primary keys and foreign keys. So we'll
[03:29:50] get to that in just a minute, but
[03:29:51] suffice to say for now, we're going to
[03:29:53] keep improving this over time. Let's
[03:29:56] take one more.
[03:29:58] Is it required to put spaces the four
[03:30:02] spaces the indents or that's just for
[03:30:04] the visual look?
[03:30:06] >> Yeah, great question. Is it required to
[03:30:08] have these four spaces before each
[03:30:10] column name? And in fact, no, it's not.
[03:30:13] But it makes the code more readable. So
[03:30:15] if I I I could put this all on one line.
[03:30:17] I shouldn't, but I could. uh if I have
[03:30:20] um instead this new line followed by
[03:30:23] four spaces, I can make this more um
[03:30:25] readable for myself and for my
[03:30:27] colleagues too. Good question.
[03:30:30] Okay, so
[03:30:33] to our earlier point, there are things
[03:30:35] that are missing from this schema. Like
[03:30:38] we have column names, but as we saw
[03:30:41] before, we should ideally specify what
[03:30:44] kind of data should be able to go into
[03:30:47] each of these columns. And for that,
[03:30:49] we'll need some new ideas to talk about
[03:30:52] here. So let's focus now on this idea of
[03:30:56] data types and storage classes. Data
[03:30:59] types and storage classes are two very
[03:31:02] similar but distinct ideas and they're
[03:31:05] uh distinct in a way we'll talk about in
[03:31:07] just a minute. Now SQLite has five
[03:31:11] storage classes five kind of storage
[03:31:14] five kind of types so to speak of values
[03:31:16] that can values that can hold. So let's
[03:31:18] talk about the first one null for
[03:31:19] instance null in this case means
[03:31:22] nothing. There's nothing that actually
[03:31:24] is inside of this value. It's kind of a
[03:31:26] sentent value to mean nothing is here.
[03:31:28] Integer means a whole number like one
[03:31:31] two three four five. Real talks about
[03:31:34] decimals like floating points like 1.2
[03:31:37] or 2.4 and so on. Text is used for
[03:31:40] characters and blob kind of a funny one.
[03:31:44] Blob stands for binary large object and
[03:31:48] it represents the data exactly as I give
[03:31:51] it to this value. If I tell it to store
[03:31:54] 1 0 1 0 1 0, it'll store exactly 1 0 1 0
[03:31:57] 1 0 in binary. So useful for storing in
[03:32:00] this case like images and video files
[03:32:02] and audio files, things that have some
[03:32:04] structure we don't want to mess around
[03:32:07] with. Now let's focus on this idea of a
[03:32:11] storage class. These I'll say are
[03:32:14] storage classes and not data types in
[03:32:18] SQLite. Now a storage class like integer
[03:32:22] can comprise can hold several data
[03:32:26] types. Notice how there are seven
[03:32:29] different data types that could be
[03:32:30] stored under this integer storage class.
[03:32:33] We have a six byte integer two byte
[03:32:36] integer uh eight and zero and so on. It
[03:32:39] could be any of these particular types
[03:32:42] but each of these types is under the
[03:32:44] umbrella of this integer storage class
[03:32:47] and SQLite itself will take care of
[03:32:50] making sure uh it uses the appropriate
[03:32:53] data type. Like if I give a very large
[03:32:56] number like let's say 4 billion or 6
[03:32:58] billion or even bigger than that it'll
[03:33:01] probably use a longer that is a bigger
[03:33:04] bite integer to store that kind of
[03:33:06] value. If I give it a smaller one like 1
[03:33:09] 2 3 or four, it'll probably use a one
[03:33:12] bite or a two byte integer for that. But
[03:33:15] SQLite's idea is that I as a programmer
[03:33:19] shouldn't have to care if I use an 8 byt
[03:33:21] or a one bite or a two byte integer. I
[03:33:23] just care that I'm using integers, whole
[03:33:26] numbers. And they give me a storage
[03:33:28] class to use any of these up to their
[03:33:31] choice here as well.
[03:33:34] Now let's look at a few examples of
[03:33:36] values in SQLite that we could store.
[03:33:39] Well, we have perhaps the red line as
[03:33:42] some text. And because this is
[03:33:43] characters, it's quoted. We could use
[03:33:45] the text storage class to represent this
[03:33:48] particular value here. We could have
[03:33:51] maybe an image. To the earlier point, we
[03:33:54] could say, well, this image might be
[03:33:56] best represented using a blob, a binary
[03:33:59] large object to keep all of these pixels
[03:34:02] exactly as they are in this image. But
[03:34:05] we do get some choice, some interesting
[03:34:08] design challenges. We look at the idea
[03:34:11] of fairs. So let's say to our point
[03:34:14] earlier, fairs are 10 cents back in the
[03:34:17] 1950s or so. Well, 10 cents we could
[03:34:20] store as an integer, which seems just
[03:34:23] fine. But this could get confused. I'm
[03:34:27] talking about dollars here or cents.
[03:34:29] Maybe it would be better, let's say, if
[03:34:30] I did this. A dollar sign 0.10.
[03:34:36] And what might that be stored as? Well,
[03:34:38] probably text, right? I could say this
[03:34:41] dollar sign isn't really a number, but
[03:34:43] now I have to include it. So I'll say
[03:34:45] this will be quoted essentially as
[03:34:46] dollar sign0.
[03:34:50] Now there's some downsides here too.
[03:34:52] Like let's say I have uh I want to add
[03:34:54] these up. Well, I can't add up text.
[03:34:56] Like what does it mean to say dollar
[03:34:58] sign plus dollar sign.20.
[03:35:01] I can't do math with text. So maybe it
[03:35:04] would be better after all if I used a
[03:35:07] real or a decimal like this 0.1.
[03:35:12] But I mean even here you run into some
[03:35:14] problems. If you are familiar with um
[03:35:17] how these are represented in binary you
[03:35:19] might know that decimal values or
[03:35:21] floatingoint values can't be perfectly
[03:35:24] precisely represented. And if I talk
[03:35:26] talk about 010
[03:35:28] the computer might store 0.100000005679
[03:35:33] it could get very wonky out to the many
[03:35:35] many decimal digits down below here. So
[03:35:38] tradeoffs and challenges overall. Let's
[03:35:42] look at these three though. I have the
[03:35:43] first one to store as an integer. I'm
[03:35:46] trying to store fairs here. Second one
[03:35:48] as text and the third one as a floating
[03:35:53] point or a real in this case. Let me ask
[03:35:56] for some opinions here. Which one would
[03:35:59] you use and why? We're trying to
[03:36:02] represent fairs in this case.
[03:36:04] >> Thank you. I prefer using integers
[03:36:08] because
[03:36:09] of course I need to get the calculation
[03:36:11] very accurately. Uh that's my point of
[03:36:14] view. Well, sometimes I can use float
[03:36:16] but you know like you said before it can
[03:36:19] get very wonky if I get you know if I
[03:36:22] really need that kind of precision I
[03:36:25] don't really recommend using floats.
[03:36:28] >> Yeah, good point. So let me go back to
[03:36:30] some slides here. You might argue for
[03:36:32] the integer because you know you can
[03:36:34] precisely represent integers. And let's
[03:36:36] say I want to add up fairs over a lot a
[03:36:39] lot of riders. This might be useful for
[03:36:41] me because I know that each number will
[03:36:43] be perfectly precisely represented. I
[03:36:45] can do lots of big kind of math with
[03:36:47] this number here. To your point, this
[03:36:50] decimal might kind of as you should get
[03:36:52] wonky later on towards later decimal
[03:36:54] points. I might get some unexpected
[03:36:56] results if we add up these overall. Let
[03:36:59] me ask though are there any proponents
[03:37:02] of this floating point value or a real
[03:37:06] value?
[03:37:08] >> Okay. So I think the uh I think this
[03:37:11] float is uh in the the number of for
[03:37:16] example for each pair like the uh like
[03:37:20] the answer that like uh truncation
[03:37:24] probably suggest one of the comments
[03:37:27] there.
[03:37:27] >> Yeah good point. Right? So if we talk
[03:37:29] about using this float value, I mean one
[03:37:31] thing we could say for it is that this
[03:37:33] decimal could be, you know, it's it's
[03:37:35] more accurate to say like we're working
[03:37:36] with dollars now and we could have maybe
[03:37:38] 10 cents which is only 0.1 of a dollar.
[03:37:41] I totally hear that point as well. And
[03:37:44] the point we're making here is that
[03:37:45] they're really just tradeoffs among
[03:37:47] these data uh storage classes to use.
[03:37:49] Whether you're using integers or real
[03:37:51] values, it just depends on your use case
[03:37:54] and what you're designing for. So be
[03:37:56] sure to read up on trade-offs among
[03:37:58] these data types and determine for
[03:37:59] yourself which one should you best use.
[03:38:03] Okay. So we have now these storage
[03:38:07] classes to store values. And it turns
[03:38:10] out that columns can be made to store
[03:38:13] certain storage classes or prioritize
[03:38:16] certain classes. And the key distinction
[03:38:19] here is that columns in SQLite don't
[03:38:22] always store one particular type.
[03:38:26] Instead, they have type affinities,
[03:38:29] meaning that they'll try to convert some
[03:38:33] value you insert into a given cell or
[03:38:35] given row to the type they have the
[03:38:38] affinity for. Now, there are let's say
[03:38:41] five type affinities in SQLite. text
[03:38:45] columns can be of the type affinity text
[03:38:48] meaning they store just characters at
[03:38:49] the end of the day. There's also numeric
[03:38:52] which stores either integer values or
[03:38:55] real values depending on which one seems
[03:38:57] best to convert to. You have integer
[03:39:00] type affinity which means it'll store
[03:39:01] whole numbers real to store floating
[03:39:03] points or decimal values and we have
[03:39:05] blob here again our old friend to store
[03:39:08] binary exactly as we get it. So whereas
[03:39:11] before we were talking about storage
[03:39:12] classes, those are associated with
[03:39:14] individual values, type affinities are
[03:39:16] now associated with individual columns.
[03:39:19] So let's see some example of might how
[03:39:21] this might work in SQLite. Let's say I
[03:39:25] have this table of fairs and we've
[03:39:27] decided to store fairs as integers.
[03:39:31] Well, if I said that this column called
[03:39:34] amount has the affinity for the text
[03:39:38] storage class, what would happen is if I
[03:39:40] insert this integer 10, it would look a
[03:39:43] bit like this later on. It would be
[03:39:45] converted to text be quoted in a sense
[03:39:48] to represent is now been converted to
[03:39:50] some set of characters. Let's say I
[03:39:53] insert this value 25. Well, 25 has a
[03:39:57] storage class right now of an integer.
[03:39:59] It is a whole number. But if I insert
[03:40:03] this into a column that has the text
[03:40:06] affinity, it'll be converted into in
[03:40:09] this case text at the end of day. Let's
[03:40:12] do the opposite. Let's say I have my
[03:40:16] fair as a string, some text. In this
[03:40:19] case, I want to insert it into this
[03:40:21] column called amount. But now amount has
[03:40:24] the integer type affinity. Well, if I
[03:40:28] insert 10 quote unquote into the column
[03:40:31] amount, I'll get back not 10 the text,
[03:40:35] but 10 the integer because again amount
[03:40:39] this column here has an affinity for the
[03:40:42] integer storage class. Let's try this 25
[03:40:47] some text again. I'll insert it into
[03:40:49] this table. Now I'll have 25 as an
[03:40:53] integer. So this is how SQLite allows us
[03:40:57] to give certain columns an affinity for
[03:41:00] certain types that they'll try to store
[03:41:03] values of that type so long as we insert
[03:41:06] values that could be feasibly converted
[03:41:08] to that type here. So let's go back to
[03:41:11] our schema and try to improve it now to
[03:41:14] use not just column names but also type
[03:41:18] affinities to store certain data of a
[03:41:20] certain type. go back to my computer
[03:41:23] here and let's improve this once more.
[03:41:26] So I'll go over to my table. And now I
[03:41:31] probably want to improve the design
[03:41:33] here. And often if I want to improve
[03:41:36] this, I might just need to erase what
[03:41:38] I've already done. So let me introduce
[03:41:40] this new keyword, this new statement uh
[03:41:42] called drop table. To drop a table means
[03:41:45] to delete it, to remove it as
[03:41:47] effectively. So let me try doing this
[03:41:48] for riders stations and visits. I'll
[03:41:51] type drop table riders
[03:41:55] semicolon enter. Nothing seems to
[03:41:58] happen. But if I type dot schema or
[03:42:00] riders is gone. I'll try drop table
[03:42:04] stations. Then semicolon hit enter and
[03:42:08] type uh let's see dots schema again. No
[03:42:11] more stations. I'll try drop table
[03:42:14] visits semicolon. enter and then dots
[03:42:18] schema and our table our database is
[03:42:21] really gone. There are no more tables
[03:42:24] inside of it. So let me propose that
[03:42:28] instead of working inside of the SQLite
[03:42:30] prompt like typing out again and again
[03:42:32] and again create table riders, create
[03:42:34] table stations, create table visits, let
[03:42:36] me be a bit more efficient about this
[03:42:38] and create myself a schema file that I
[03:42:40] could reuse throughout this lesson and
[03:42:43] also wait it on while I'm working on
[03:42:45] this database on my own. To do that, let
[03:42:48] me quit my um SQLite prompt here and let
[03:42:52] me type something like code schema.sql.
[03:42:55] I'm just creating this file called
[03:42:58] schema.sql.
[03:43:00] Now, aSQL file allows me to type in SQL
[03:43:03] keywords and have them be syntax
[03:43:05] highlighted so I know what's going on
[03:43:08] inside of this file. So, let's just try
[03:43:11] this once more. I'll type create table
[03:43:15] riders and inside I'll say it has the ID
[03:43:19] column of what type ofity? IDs are whole
[03:43:24] numbers. So perhaps integer in this case
[03:43:26] I could say ID has the integer type
[03:43:29] affinity. Now let me say that writers
[03:43:32] also have a name. And how could names be
[03:43:34] best represented? Maybe text, right?
[03:43:37] Characters here. So I'll say name and
[03:43:40] text. Now I'll include a semicolon to
[03:43:43] say this is the end of my create table
[03:43:45] statement. And before remember how I had
[03:43:48] to kind of error out or I had to like
[03:43:51] backspace and so on to improve the
[03:43:53] design. Here I can literally just point
[03:43:55] and click and edit this file to improve
[03:43:58] my schema. And I'll later on apply this
[03:44:00] in my um database using a command that
[03:44:04] we'll see a bit later. So let's keep
[03:44:06] going here. I'll say create table
[03:44:09] stations and inside of this stations
[03:44:11] table I'll make sure it has an ID column
[03:44:14] of type integer a name column that
[03:44:18] probably stores some text and a line
[03:44:21] column that also stores some text where
[03:44:25] name is the name of the station like
[03:44:26] Kendall MIT Harvard and line is blue
[03:44:30] line or green line what line it's part
[03:44:32] of in our subway let me try now visits
[03:44:35] I'll say create table visits and then
[03:44:37] I'll do rider ID which has what type
[03:44:41] affinity probably integer and then I'll
[03:44:44] do station ID which has this same type
[03:44:47] ofinity it's we're talking about
[03:44:48] integers whole numbers here for ids
[03:44:51] semicolon to finish this statement now
[03:44:54] this is my schema as a whole I have
[03:44:58] riders stations and visits but now I
[03:45:01] want to apply this schema to my database
[03:45:05] so what could I I could reopen it. Let's
[03:45:07] say I'll do SQLite 3 mbta.db in my
[03:45:11] terminal. And now I want to read in this
[03:45:14] schema.sql file. That is run the
[03:45:17] commands that are inside of this file.
[03:45:19] So what could I do? I could say read
[03:45:23] schema.sql
[03:45:25] where readad is a command that says take
[03:45:28] whatever file you give me like
[03:45:29] schema.sql SQL and read it into this
[03:45:32] database running any SQL keywords you
[03:45:35] come across there. I'll hit enter and
[03:45:38] now nothing seems to happen. But if I
[03:45:41] type schema, I now see my schema
[03:45:45] improved. And this is helpful for me
[03:45:47] because I what I could do now is I could
[03:45:48] just edit my schema.sql file and rerun
[03:45:51] it and rerun it to make sure I now have
[03:45:54] these tables being improved over time.
[03:45:58] Okay, so this then is our new
[03:46:03] representation of our database. We have
[03:46:06] riders, of course, their own entity, and
[03:46:09] stations. They have an ID and a name,
[03:46:13] and stations have an ID, a name, and a
[03:46:15] line. We've also now included these type
[03:46:18] affinities integer text integer text to
[03:46:22] tell SQL what kinds of storage classes
[03:46:24] could be put inside of each of these
[03:46:27] columns.
[03:46:28] Now before we keep improving this, let
[03:46:31] me ask what questions we have on these
[03:46:34] storage classes and type affinities.
[03:46:39] Sir, you were using uh when you were
[03:46:41] creating the table, the table was not uh
[03:46:44] in the line. So when uh we search for
[03:46:48] the authors or books, so it comes with a
[03:46:51] perfect table. So how can we make a
[03:46:53] perfect table in the SQL?
[03:46:54] >> Yeah. Do you mind um clarifying what you
[03:46:56] mean by like the the perfect table?
[03:46:58] >> Uh sir, I mean that uh it was arranged
[03:47:01] in something like in boxes block boxes.
[03:47:05] >> Ah good question. So um before we're
[03:47:07] able to see the results of our queries
[03:47:10] inside some boxes in our terminal and
[03:47:13] that is actually a mode of SQL light. I
[03:47:15] think you type like do mode table to see
[03:47:17] results in that version. Um here though
[03:47:20] we have no data inside of our tables. So
[03:47:23] we can't really select anything from
[03:47:24] them. Like if I go to my terminal here
[03:47:27] and I try to select some data from this
[03:47:32] riders table. Let me say select star
[03:47:34] from riders semicolon. I won't get
[03:47:37] anything back. Next week though, we'll
[03:47:40] see how to insert and add and update and
[03:47:43] delete data inside of these tables. At
[03:47:45] which point you could write select star
[03:47:47] from riders and see some data you've
[03:47:50] inserted yourself. Great question. Let's
[03:47:53] take one more here.
[03:47:56] >> Yes. Uh I would like to know if you have
[03:47:59] a column data type uh boolean.
[03:48:01] >> Yeah. Do we have a a boolean type
[03:48:04] affinity? Let's say so here we don't at
[03:48:07] least in SQLite. Some other DBMS's
[03:48:10] database management systems might have
[03:48:12] bool or boolean true or false. Right?
[03:48:15] Let me show you this instead. If I go to
[03:48:17] my terminal, I can see if I type schema,
[03:48:21] I haven't used boolean. There's no need
[03:48:23] for me in this case, but I have used
[03:48:25] integer. And integer for SQL I can kind
[03:48:28] of for uh serve the same purpose. I
[03:48:30] could have the integer zero or the
[03:48:33] integer one to be true or to be false or
[03:48:35] true respectively. Zero being false and
[03:48:37] true being one I believe in this case.
[03:48:39] But good question.
[03:48:42] Okay. So to the earlier question like
[03:48:45] we've improved our tables. We now have
[03:48:48] type affinities for our columns but we
[03:48:51] don't yet have this idea we talked about
[03:48:54] last week which was primary keys and
[03:48:56] foreign keys. this idea of trying to
[03:48:59] uniquely represent each item in our own
[03:49:02] table using primary keys and trying to
[03:49:04] reference that primary key from some
[03:49:06] other table using foreign keys. So let's
[03:49:09] try to work on that now. And for this
[03:49:13] we'll need this new idea called a table
[03:49:16] constraint. In SQLite you can apply
[03:49:19] what's called a constraint to your
[03:49:21] entire table. A constraint means that
[03:49:24] some values have to be a certain way.
[03:49:27] Like let's say for a primary key,
[03:49:30] primary keys must be unique. They can't
[03:49:33] repeat and they must be at least in our
[03:49:35] cases going to be integers to be able to
[03:49:38] uh for quickly like add on to them over
[03:49:40] time. Similarly for foreign keys, well a
[03:49:44] constraint is that if you have a foreign
[03:49:46] key, you better find that value in some
[03:49:49] other table. Otherwise you violated this
[03:49:52] constraint of having a foreign key. So
[03:49:54] we have two kinds of table constraints
[03:49:57] among others but two of these are
[03:49:59] primary key and foreign key and we can
[03:50:02] apply these to our table by applying
[03:50:05] them underneath the columns we tend to
[03:50:07] say will be inside of our table. Let's
[03:50:10] try these two here now. So let me come
[03:50:12] back to my terminal here so we can
[03:50:14] implement our very own primary key and
[03:50:16] foreign key constraints. We'll go back
[03:50:18] to my SQLite terminal and clear my
[03:50:20] screen. And let's then pull up our
[03:50:22] schema.sql file. So we can keep
[03:50:24] modifying our schema. I can now see I
[03:50:27] have the writers table stations and
[03:50:29] visits. And I have some columns that
[03:50:31] could be primary keys or foreign keys,
[03:50:34] but I need to declare them as such. So
[03:50:37] here in the riders table, what was our
[03:50:39] primary key? Well, it was ID. Every
[03:50:42] rider should have their own unique ID
[03:50:44] that should not be duplicated across any
[03:50:46] two riders. So to ensure that constraint
[03:50:49] is applied, I could follow this up with
[03:50:52] a comma and then say primary key ID just
[03:50:56] like this. Now ID is the primary key of
[03:50:59] this rider's table. I can go down to
[03:51:01] stations and ask what was my primary
[03:51:04] key? Well, similarly, it was ID, this ID
[03:51:07] column on line 8. So I'll type a comma
[03:51:10] followed up with primary key ID. And now
[03:51:14] that ID column is a primary key. It has
[03:51:17] that constraint applied in stations. But
[03:51:21] now if I get down to visits, I have a
[03:51:23] few more options. Visits here actually
[03:51:26] doesn't have its own ID column that I
[03:51:29] created. I instead have a rider ID and a
[03:51:32] station ID column. So a few options
[03:51:35] here. One option is actually to make a
[03:51:37] joint primary key. I could have a
[03:51:40] primary key composed of two columns,
[03:51:43] both rider ID and station ID. If I
[03:51:47] applied that constraint, that would mean
[03:51:49] that if I were to ever insert a row that
[03:51:51] had the same rider ID and the same
[03:51:53] station ID as another row, I would
[03:51:55] trigger a constraint violation. Every
[03:51:59] row that has a rider ID and a station ID
[03:52:01] has to be unique in their combination of
[03:52:03] those two values. to write that kind of
[03:52:06] scenario. I could follow this up and I
[03:52:08] could say similarly the primary key of
[03:52:10] this table is not just rider ID like
[03:52:13] this but it's also station ID. Now this
[03:52:17] is a joint primary key constraint. But
[03:52:20] if we think about this logically I mean
[03:52:22] it kind of stands to reason that
[03:52:24] somebody would visit a station more than
[03:52:26] once and I don't want to make sure that
[03:52:28] every combination of rider and station
[03:52:30] ID should be unique. I want people to be
[03:52:32] able to visit a station more than once.
[03:52:34] So maybe not the best design for this
[03:52:36] table, but I could certainly use it in
[03:52:38] other cases or other contexts. One other
[03:52:41] option would be to uh do what you did
[03:52:43] before and to have maybe the ID column
[03:52:45] here of type integer and then down below
[03:52:49] make that our primary key a bit like
[03:52:51] this. And now visits has its own ID
[03:52:54] column. But actually SQLite by default
[03:52:58] will give me its very own primary key
[03:53:02] one called row ID. It's implicit. I
[03:53:05] can't see it. But I actually could query
[03:53:07] it. I could query for row ID all one
[03:53:09] word and get back a unique primary key
[03:53:12] for this table. SQLite is automatically
[03:53:14] created for me. Now we have seen the
[03:53:18] primary key options. What are our
[03:53:19] foreign key options? Well, it seems like
[03:53:21] rider ID and station ID are the foreign
[03:53:24] keys of this table where rider ID
[03:53:26] references the ID column in riders and
[03:53:29] station ID references the ID column in
[03:53:32] stations. So to codify that to make that
[03:53:35] a reality in our schema, I could follow
[03:53:37] this up with the foreign key. The
[03:53:39] foreign key of this table is rider ID
[03:53:42] and it references it references the
[03:53:45] riders table and the ID column inside of
[03:53:48] it using this syntax here.
[03:53:51] Now I could keep going. I could say I
[03:53:53] have more than one foreign key. I also
[03:53:56] have a foreign key foreign key called
[03:53:59] station ID and that references as we
[03:54:01] said before the stations table and the
[03:54:04] ID column inside of it. So now here I
[03:54:06] have my completed schema. I have a
[03:54:09] primary key for the tables I've declared
[03:54:11] an explicit column for a primary key and
[03:54:13] now I also have foreign key constraints
[03:54:16] for those columns that should be foreign
[03:54:18] keys. So now let me ask what questions
[03:54:22] do we have on the schema or on primary
[03:54:24] keys and foreign keys.
[03:54:27] >> Uh so yeah I just noticed that whenever
[03:54:30] before we hadn't added the affinities
[03:54:33] and the keys we were not applying commas
[03:54:35] after each column name. So what is the
[03:54:38] difference there?
[03:54:40] >> Yeah, a good catch. Let me um kind of
[03:54:41] show you what this looks like in my
[03:54:43] terminal so you can see it live. Um you
[03:54:46] I think had noticed that before we had
[03:54:48] let's say this primary key ID um
[03:54:52] constraint in writers we had done
[03:54:54] something like this. Let me just copy
[03:54:56] paste that. And we had removed this last
[03:54:58] column or comma from the name column. Is
[03:55:00] that right? And if that's the case well
[03:55:03] it's um just convention just style here.
[03:55:06] So if I want to keep adding some
[03:55:08] constraint or like a new line to my
[03:55:10] table, I should include a comma here.
[03:55:14] This name column was the last um portion
[03:55:18] of my table I had specified. I have a
[03:55:20] column called name that has type
[03:55:22] affinity text, right? But now if I add
[03:55:25] this new constraint, we'll have to
[03:55:27] follow it up with followed up after a
[03:55:29] comma from this new column here. Notice
[03:55:33] now this constraint primary key ID is
[03:55:36] the last um let's say attribute of my
[03:55:40] table I specified. I no longer need to
[03:55:42] include a comma at the end of it. So
[03:55:44] whatever is the last portion I should
[03:55:46] have a uh I should not have a comma
[03:55:48] after but everything else I should.
[03:55:51] Let's take one more question here too.
[03:55:54] >> Would it be okay for the visits table to
[03:55:56] have an ID column as well?
[03:55:58] >> Yeah, a good question. It would be okay
[03:56:00] for the visits table to have an ID
[03:56:02] column as well. It certainly would be.
[03:56:04] We could define our very own primary key
[03:56:07] for this table, too. So, let me go back
[03:56:08] and show you how that could work. I'll
[03:56:10] go to my visits table here, and I could
[03:56:14] try to add my own primary key to this
[03:56:17] table. I could say ID, make a new column
[03:56:20] here, make it of type affinity integer
[03:56:23] like this. Let me scroll up. And now,
[03:56:26] let me add some new constraint. I could
[03:56:28] say because I've made my very own
[03:56:30] primary key, I'll say primary key id.
[03:56:34] Now this table has a primary key that
[03:56:37] I've created called ID. And this will be
[03:56:41] in place of SQL lights that it would
[03:56:43] have made called row ID itself, but
[03:56:46] hidden from my own view.
[03:56:50] Okay,
[03:56:51] let's keep going then. We've seen table
[03:56:53] constraints. We've seen type affinities,
[03:56:55] but we could probably do more to improve
[03:56:58] the design of this table or this
[03:57:00] database. So let's introduce one more
[03:57:02] kind of constraint. This one called a
[03:57:05] column constraint. So whereas a table
[03:57:08] constraint applies to the table as a
[03:57:10] whole, a column constraint applies to a
[03:57:13] particular column. Let's say maybe I
[03:57:16] want a column to have certain uh data
[03:57:19] inside of it. I maybe I want to make
[03:57:20] sure it doesn't have null values and so
[03:57:22] on. I could do that with column
[03:57:25] constraints. There are four in SQLite.
[03:57:29] Check, default, not null, and unique.
[03:57:33] And each one does something different.
[03:57:36] Check allows me to make my very own
[03:57:37] check. Like check to be sure that this
[03:57:40] amount is greater than zero. Or I could
[03:57:43] use default. Default means if I don't
[03:57:46] supply a value, when I add a new row,
[03:57:48] it'll just use a default value instead.
[03:57:52] Not null means I can't insert null or
[03:57:55] empty values into this column. In fact,
[03:57:58] it's required. Unique means I want to
[03:58:02] make sure that every row in this column
[03:58:06] is a unique value. It doesn't appear
[03:58:08] twice in my data set. So, let's try
[03:58:11] applying a few of these to our schema
[03:58:13] here. Go back to my terminal. And now,
[03:58:17] let me check out this. Well, I could try
[03:58:20] applying the notnull constraint when I
[03:58:24] know I want a column to be required
[03:58:26] effectively. Now, where could I best
[03:58:28] apply that? Maybe I could apply that to
[03:58:32] the name column in stations. Like
[03:58:34] stations must have a name. So, I'll say
[03:58:37] the name column cannot be null. It
[03:58:39] cannot be empty in here. Line also
[03:58:44] should probably be not null. A station
[03:58:46] must be part of some line. I can't have
[03:58:48] an empty value for line. So I'll say too
[03:58:51] this should be not null.
[03:58:54] Now I could apply this up at name. I
[03:58:57] could say riders must have a name too.
[03:58:59] Let me try that. I'll say text not null.
[03:59:02] Or I could leave it optional. I could
[03:59:04] say maybe text just on its own and let
[03:59:07] writers choose to supply a name or not.
[03:59:11] Now the question here is should I apply
[03:59:14] not null to my primary key columns like
[03:59:17] ID not null or ID not null here you
[03:59:22] might think that you should for
[03:59:23] thoroughess sake. Well it turns out that
[03:59:26] when you apply the primary key table
[03:59:29] constraint down below here this already
[03:59:32] ensures that there are several
[03:59:33] constraints applied to this particular
[03:59:36] column called ID. among them being that
[03:59:39] ID cannot be null. So no need to
[03:59:42] duplicate this and say that this ID
[03:59:44] cannot be null when I already have it
[03:59:46] specified down below that ID is a
[03:59:49] primary key.
[03:59:51] Let me check others here. You might also
[03:59:54] think could I do it for rider ID and
[03:59:57] station ID? Should I include not null
[04:00:00] here? Rider ID not null. Station ID not
[04:00:04] null. Well, that would be a good
[04:00:06] thought, but again, we're taken care of
[04:00:08] by our table constraint using our
[04:00:10] foreign key here. Again, this constraint
[04:00:13] will say if rider ID doesn't already
[04:00:16] exist in the ID column of riders, I
[04:00:20] can't insert that value. And we could
[04:00:22] probably presume that if riders ID is a
[04:00:25] primary key, well, null will not be part
[04:00:28] of this column. And therefore I already
[04:00:30] can't insert null for rider ID or
[04:00:33] station ID. This would be in this case
[04:00:36] redundant. So not null is good when you
[04:00:39] have columns that are neither primary
[04:00:41] keys nor foreign keys and you want to
[04:00:44] make sure that they have all they always
[04:00:47] have a value that they are never uh null
[04:00:50] effectively.
[04:00:52] Okay. So that is not null and we could
[04:00:56] keep going here. We also had one called
[04:00:58] unique that makes sure every um every
[04:01:02] value every row in this column is
[04:01:04] unique. Where could we apply this? I
[04:01:07] could try to apply it let's say to the
[04:01:09] name of a station like station should
[04:01:11] have unique names. So I'll say not null
[04:01:14] and unique. Now this column has two
[04:01:17] constraints. The first not null. It
[04:01:20] should always have a value. The second
[04:01:22] unique the value shouldn't repeat
[04:01:24] throughout this column. line I might
[04:01:27] leave without this constraint. I could
[04:01:29] imagine two stations being on the same
[04:01:31] line like both on blue. I'll allow that
[04:01:33] in this case. Now again, we could try to
[04:01:37] apply unique to our primary keys or our
[04:01:40] foreign keys as I just did here, but
[04:01:43] it's already taken care of for us using
[04:01:46] this primary key constraint. A primary
[04:01:48] key again is always going to be unique
[04:01:51] and never null. So we'll take advantage
[04:01:53] of that already using our primary key
[04:01:57] and foreign key constraints here.
[04:02:00] Okay. So we've seen unique and not null.
[04:02:04] And I might argue we're at the point
[04:02:06] where this schema seems to be fairly
[04:02:08] optimized at least using our column
[04:02:11] constraints, our table constraints, our
[04:02:13] type affinities and so on. So let's ask
[04:02:17] then what questions do we have on not
[04:02:20] null and unique if any.
[04:02:23] >> So basically to recap if I understood
[04:02:26] correctly it's not precisely about not
[04:02:28] null and unique but about the concept of
[04:02:30] the key uh labeling a key immediately
[04:02:34] give us the attribute of not null unique
[04:02:36] and to be referenced. Right?
[04:02:38] >> That is true. So when you use a primary
[04:02:40] key or a foreign key constraint, there
[04:02:43] are other constraints that go along with
[04:02:45] that constraint. A primary key for
[04:02:47] instance must not be null. Um it must be
[04:02:50] unique and so on. So it would be
[04:02:52] redundant to apply that again to say
[04:02:54] that this primary key should be unique
[04:02:56] or not null. Good clarification there.
[04:02:59] Okay. So I think we're at the point
[04:03:01] where this schema is pretty well set for
[04:03:04] us. And we're going to need to think
[04:03:07] about though how we use this in the real
[04:03:10] world. Like if this is our schema here,
[04:03:14] we have riders and stations. Well, what
[04:03:17] could we do? I mean, riders tend to I
[04:03:20] mean, they could register for the
[04:03:22] subway. And riders, well, they do visit
[04:03:24] stations, but I think if we applied this
[04:03:26] to the real world, we'd see that this
[04:03:29] isn't quite how it's actually done. Like
[04:03:31] riders don't really register that often.
[04:03:34] if uh a rider who's new to the city
[04:03:35] comes in, they want to ride the subway,
[04:03:37] they should be able to ride, too. So, it
[04:03:39] turns out, at least here in Boston, the
[04:03:42] MBTA doesn't really track riders, per
[04:03:44] se, but they do track what we call
[04:03:47] Charlie Cards. If you want to ride the
[04:03:49] subway, you get a Charlie Card. Charlie
[04:03:53] card allows you access to the subway,
[04:03:54] keeps track of your fair, your balance,
[04:03:56] and so on. Allows you to swipe in to
[04:03:58] certain stations. So, and when we come
[04:04:01] back from a break here, we'll see how we
[04:04:03] can actually implement these Charlie
[04:04:04] cards instead of riders to make our
[04:04:06] system more efficient and more in line
[04:04:08] with what happens in the real world.
[04:04:10] We'll see you all in just a few.
[04:04:13] And we're back. So, we saw last time
[04:04:16] this challenge of designing a system for
[04:04:18] the Massachusetts Bay Transportation
[04:04:20] Authority to represent riders and
[04:04:23] stations, people who get on a subway to
[04:04:25] go around Boston. But as we also saw, we
[04:04:29] learned that the MBTA doesn't keep track
[04:04:32] of riders themselves. They keep track of
[04:04:36] Charlie cards, this card that a rider
[04:04:38] might carry in their pocket. And they
[04:04:40] can scan this card at a station to enter
[04:04:43] or even to exit in some cases to make
[04:04:46] sure that their fair is counted as they
[04:04:48] enter that station. So let's think now
[04:04:51] how to improve our schema to represent
[04:04:54] not just riders like me but Charlie cars
[04:04:57] themselves people might carry around
[04:04:59] when they enter the subway station. Well
[04:05:02] we saw before we had riders and cards.
[04:05:05] But our goal now is to remove riders
[04:05:08] from the picture. Focus only on cards.
[04:05:11] Well cards as we've seen might make us
[04:05:14] swipe at a station. If I enter Harvard
[04:05:17] station, I might swipe my Charlie card
[04:05:20] to enter that station. And we could see
[04:05:24] that a card would have maybe many swipes
[04:05:27] involved. Like if I swipe at Harvard, I
[04:05:29] might also swipe at MIT or swipe at Park
[04:05:32] Street and so on. We could see that a
[04:05:35] swipe can only happen at a single
[04:05:37] station at a time, though. Like if I
[04:05:39] swipe at Park Street, I'm only swiping
[04:05:42] at Park Street here. And similarly, a
[04:05:44] swipe might only involve one single
[04:05:47] card. So if we think about these
[04:05:49] entities and how they relate, we could
[04:05:52] also think about what kinds of columns
[04:05:53] we should have inside of each entity. In
[04:05:56] this case, I would argue we should have
[04:05:58] something a bit like this. We could say
[04:05:59] that a card has a ID for its primary key
[04:06:03] in this case. Similarly, this card makes
[04:06:06] a swipe and this swipe has itself an ID
[04:06:10] as well as a type, some time that that
[04:06:13] swipe happened and an amount or a
[04:06:16] transaction that is involved. So, for
[04:06:18] example, let's say I swipe in at the
[04:06:21] Harvard Square station. That type of
[04:06:23] swipe might be to enter the station at
[04:06:26] some certain time. Now, associated with
[04:06:29] that swipe is also some amount in
[04:06:32] dollars that happened to be subtracted
[04:06:34] from my card. Like, let's say the fair
[04:06:36] nowadays is $2.40. Well, that amount is
[04:06:39] subtracted from my card from this swipe.
[04:06:44] Now, of course, I do all of this at a
[04:06:46] station which has our same columns from
[04:06:48] before, ID, name, and line. So, a
[04:06:52] similar idea now, but we're replacing
[04:06:54] riders with cards and adding more
[04:06:57] information to these visits. They're
[04:06:59] instead swipes that could be maybe
[04:07:01] entering the station, exiting the
[04:07:03] station, or just adding funds to my
[04:07:05] balance, for instance. So, let's see how
[04:07:08] we could improve our schema now using
[04:07:10] some new SQL keywords to alter our
[04:07:13] tables and add some new ones, too. I'll
[04:07:16] go back to my computer and let's see how
[04:07:19] we could try to alter the tables that
[04:07:21] we've already created. Like we already
[04:07:23] have a riders table, a visits table, and
[04:07:26] a station's table, but we could learn
[04:07:28] some new statements, some new queries to
[04:07:30] actually update and alter these tables
[04:07:33] as well. The first one, as we saw a
[04:07:35] little bit before, is this one called
[04:07:37] drop table. Arguably the most dramatic
[04:07:39] thing you can do to a table is just drop
[04:07:40] it, delete it like this. So, let's try
[04:07:43] deleting the writers table from our
[04:07:45] database. I'll go back to my uh go back
[04:07:49] to my database here. I'll type SQLite3
[04:07:54] MBTA. DB to pull up this database again.
[04:07:57] And now, if I type schema, I'll see I
[04:08:00] have a riders, stations, and visits
[04:08:02] table. But no longer do I want to have
[04:08:05] the riders table. I want to remove that.
[04:08:08] So I'll say drop table riders semicolon.
[04:08:13] Now I'll hit enter. No more riders
[04:08:16] table. If I type dots schema, that's
[04:08:18] gone for my database.
[04:08:21] Well, what could I do now? I've dropped
[04:08:24] the table, but I'd still need to maybe
[04:08:26] update visits to instead be swipes. I
[04:08:29] could probably leave stations as is. But
[04:08:31] I want to update a table or alter its
[04:08:34] schema. I can use some new commands as
[04:08:37] well. I'll use this one called alter
[04:08:40] table. Alter table looks a bit like
[04:08:43] this. I can use the alter table um
[04:08:47] statement here and give it some table
[04:08:50] name like let's say alter table visits
[04:08:53] and then inside uh this visits table I
[04:08:56] get to ask what do I want to do? Do I
[04:08:59] want to let's say rename the table? I
[04:09:01] could do that. I could also decide to
[04:09:04] add a column, rename a column or drop a
[04:09:07] column algether. Let's try first looking
[04:09:09] at rename to. I want to rename this
[04:09:13] visits table to a swipes table
[04:09:16] representing not just a visit to the
[04:09:17] station, but a swipe of a card. So,
[04:09:20] let's try this one here. I'll go back to
[04:09:22] my computer and I'll go back to SQLite
[04:09:25] and I'll say I no longer want visits to
[04:09:28] be called visits. I ideally want visits
[04:09:32] to actually be called swipes. So let me
[04:09:35] try this. I'll say alter table. So we
[04:09:39] saw before visits rename to swipes like
[04:09:44] this semicolon. Now I'll hit enter. And
[04:09:48] now if I type dots schema again I see
[04:09:52] oops kind of strange. I'll type dots
[04:09:54] schema again. I'll see swipes. no longer
[04:09:57] called visits, but now called swipes.
[04:10:01] Well, we saw I'd ideally like to add a
[04:10:03] type of the swipe. Maybe I'm entering
[04:10:06] the station. Maybe I'm exiting. Maybe
[04:10:09] I'm just adding funds or depositing some
[04:10:11] funds. So, let me try adding let's say a
[04:10:14] new column to swipes. I'll say alter
[04:10:17] table add column alter table swipes.
[04:10:22] Going to name that table swipes like
[04:10:25] this. And then let's add a column. Add a
[04:10:29] column called type. And this will have
[04:10:32] the type affinity text. I'll hit
[04:10:35] semicolon. Enter. And now if I type
[04:10:38] schema, I'll see well I have a column
[04:10:42] called TTP.
[04:10:45] So clearly I made a typo here. I had
[04:10:47] rider ID, station ID, this new column
[04:10:49] down below called TTP.
[04:10:52] I kind of want to fix this, right? I
[04:10:54] don't want TTP. I want type. So probably
[04:10:57] a good chance to use my rename column.
[04:11:00] I'll come back here and I'll try that.
[04:11:02] I'll instead do alter table alter table
[04:11:07] swipes and I will rename a column. Now
[04:11:11] I'll say rename the column TTP
[04:11:16] to type spelled correctly. Now hit
[04:11:19] semicolon.
[04:11:21] Go my terminal type.s schema. And now I
[04:11:24] see over here that type has been added
[04:11:27] to my table of swipes. I see rider ID,
[04:11:30] station ID, and now a new column called
[04:11:34] type. So through alter table, can we go
[04:11:36] ahead and add new columns, rename them
[04:11:39] even, or if I wanted to just drop the
[04:11:42] column al together. Let's say I add this
[04:11:45] column type and I change my mind. I
[04:11:47] don't want it here anymore. I go back to
[04:11:49] my computer and I could try dropping a
[04:11:51] particular column. Let me try in this
[04:11:53] case alter table swipes. And now let me
[04:11:58] drop column type semicolon. Hit enter.
[04:12:03] And now if I type schema, I'm back to
[04:12:07] where I began. So these are the commands
[04:12:10] we can use to alter our tables to
[04:12:13] improve them if we make a mistake during
[04:12:14] our first create table command or if we
[04:12:17] want to add more functionality later
[04:12:19] down the line.
[04:12:21] So ideally I could keep using you know
[04:12:23] alter table, add table, create table,
[04:12:26] drop table and so on. But what I want to
[04:12:28] do here is just probably start from
[04:12:29] scratch. Like I have, you know, stations
[04:12:31] and swipes and so on. Why don't I just
[04:12:33] go back to my schema file and use that
[04:12:35] instead? So what I'll do is I'll drop
[04:12:37] table for stations and oop semicolon. I
[04:12:41] will drop table for uh swipes now.
[04:12:44] Semicolon. I'll type schema. And now
[04:12:48] I'll see nothing in here. I'll quit and
[04:12:52] I'll type code schema.sql.
[04:12:55] Let me just start from scratch using
[04:12:57] this schema.sql.
[04:12:59] So we no longer want to have riders. We
[04:13:02] only want to have cards. So I could just
[04:13:05] rename this table here. I'll call it
[04:13:07] cards. Crate table cards. Now cards
[04:13:10] don't have a name. They only have some
[04:13:12] unique ID in this case. Now I'll leave
[04:13:17] stations just as it is. This seems
[04:13:19] perfectly fine to me. Stations have an
[04:13:21] ID, a name, and a line with these
[04:13:23] constraints applied to the name and line
[04:13:26] columns. But now the visits table. Well,
[04:13:29] the visits table is no longer a visit to
[04:13:32] the station per se. It's more a swipe of
[04:13:34] the card at that station. So let's now
[04:13:36] say visits becomes swipes. And among
[04:13:40] these new columns to add are the
[04:13:42] following. I want to have not just an ID
[04:13:46] for each swipe, not just an ID for rider
[04:13:48] ID and station ID and so on, but also I
[04:13:52] want to have a type of swipe. Am I
[04:13:55] entering the station, exiting or
[04:13:57] depositing some funds? So I'll say the
[04:13:59] type of this uh is going to be a new
[04:14:02] column and the data type this holds will
[04:14:05] be text enter, exit or deposit for some
[04:14:10] funds. Now let me try another column
[04:14:13] too. I'll include a date time. A date
[04:14:16] time is like a time stamp. What time did
[04:14:18] this swipe actually happen? And I'll
[04:14:20] make this type numeric. Numeric can
[04:14:24] store all kinds of dates and times for
[04:14:26] me in this table. Now let me add one
[04:14:30] final column. This one will be an
[04:14:32] amount. I'll also use numeric for this
[04:14:36] kind of uh column here. And I'll say
[04:14:39] that this column uh called amount can
[04:14:41] store in this case integers or real
[04:14:45] numbers like floats and so on. I'll
[04:14:47] probably decide on that when I actually
[04:14:48] add some data to this table. Okay. So
[04:14:52] here we've updated our schema to
[04:14:55] represent that diagram we saw before. I
[04:14:57] have cards, I have stations, and I have
[04:14:59] swipes that have some type associated
[04:15:02] with them. enter, exit, deposit, some
[04:15:04] date, time, and some amount that was
[04:15:07] charged to me while I made this swipe.
[04:15:09] Either I added some funds, which case
[04:15:11] amount is positive, or I subtracted some
[04:15:13] fun entering or exiting, in this case,
[04:15:16] uh, from the station.
[04:15:18] All right, so I have these tables now,
[04:15:21] and now I want to probably apply some of
[04:15:24] those same column constraints we saw
[04:15:26] before. like here it's fine but I also
[04:15:29] want to make sure I'm not adding some
[04:15:30] data that I don't want to add to this
[04:15:33] table. So I could go back to my old
[04:15:35] friends these column constraints and we
[04:15:38] saw before we had uh default and not
[04:15:41] null unique and check we've used not
[04:15:44] null and unique but we haven't used
[04:15:47] check or default. So let's start using
[04:15:49] more than just not null and unique and
[04:15:51] also focus on check and default what
[04:15:53] they can do for us here. I'll go back to
[04:15:57] my schema and let me just make sure that
[04:15:59] I'm making all the columns that I want
[04:16:01] to be required actually required. I'll
[04:16:04] go into my swipes table and I'll say
[04:16:07] that type I mean this should be
[04:16:09] required. I should I I should know
[04:16:11] whether I entered, exited or deposited
[04:16:14] some funds. So I'll say text not null.
[04:16:17] Similarly for the timestamp the time
[04:16:19] this swipe happened I want that to be
[04:16:22] not null as well. So, I must know what
[04:16:24] time I swiped the card. And also, it
[04:16:26] makes sense for there to always be some
[04:16:28] amount associated with this swipe.
[04:16:31] Either I added some funds to my balance
[04:16:33] or I removed some funds overall. So,
[04:16:36] I'll make this not null as well.
[04:16:39] Well, let's see what we could do here
[04:16:41] with default. default gives me some
[04:16:45] default value, some initial value to add
[04:16:47] to this column if I don't specify what
[04:16:51] kind of value to add. Well, this could
[04:16:54] be good for date time. Date time here is
[04:16:57] again the timestamp, the time I swiped
[04:17:00] this card to enter, let's say, Harvard
[04:17:02] station. Well, if I want this to always
[04:17:06] have the current time, I could use
[04:17:09] default. I could say the default value
[04:17:12] for this column is this special value
[04:17:16] here. Current timestamp in all caps.
[04:17:20] Current timestamp will show me the year,
[04:17:23] the month, the day, the hour, the
[04:17:26] minute, and second all in one value and
[04:17:28] insert that into my table. So as soon as
[04:17:31] I add new row, if I don't supply a time
[04:17:35] for this datetime column, I'll instead
[04:17:37] get back the current time exactly as it
[04:17:41] is represented in SQLite.
[04:17:44] Now what could I do further than this? I
[04:17:46] could also try to add a my very own
[04:17:49] check. Maybe I want to make sure that
[04:17:51] the amounts here are never equal to
[04:17:54] zero. Like nobody should ever be able to
[04:17:56] make a Z transaction or Z swipe. they're
[04:17:59] always being charged some money or
[04:18:01] they're always depositing some money in
[04:18:03] this case. So I could say amount here
[04:18:06] has my very own check on this column and
[04:18:10] inside check I could actually write my
[04:18:12] very own expression to check for. I
[04:18:14] could say for example amount is not
[04:18:17] equal to zero using those same operators
[04:18:20] we saw back in week zero. This will
[04:18:23] ensure that any value inside amount will
[04:18:26] not be equal to zero.
[04:18:30] Let's try it also for type. I mean type
[04:18:33] can only have a few values. We saw enter
[04:18:37] exit deposit some funds. I could make
[04:18:40] sure that only those values are included
[04:18:42] inside my type column. I could say check
[04:18:45] that type is in some list of values.
[04:18:48] Going back to week one here we talked
[04:18:51] about in I could say maybe the type is
[04:18:54] in enter exit or is in deposit. So now
[04:19:00] when I have this table called swipes I'm
[04:19:03] representing what I'm actually doing
[04:19:05] when I go to Harvard station. I have
[04:19:07] here a visit for myself. My very own ID
[04:19:11] here which I'll update in just a second.
[04:19:12] I have a station ID where I'm actually
[04:19:14] going to visit. I have a type that I'm
[04:19:17] going to use to enter, exit, or deposit
[04:19:20] some funds at this station. I'm doing at
[04:19:23] a certain time, and I have an amount
[04:19:25] associated with this transaction.
[04:19:28] Now, there's one thing to fix here,
[04:19:30] which is that we're still talking about
[04:19:32] riders inside our swipes table. So,
[04:19:35] let's fix that here, too. I'll go back
[04:19:37] to my computer, and let's try fixing
[04:19:40] this. I have a rider ID inside of my
[04:19:43] swipes table, but no longer do I have
[04:19:46] riders, I have cards. So, let me say
[04:19:49] that this is now a card ID. And down
[04:19:52] below in my foreign key, I'll say that
[04:19:55] this card ID column references the ID
[04:19:58] column in cards. And I think this should
[04:20:02] represent everything I want to represent
[04:20:04] about swipes at the station.
[04:20:08] So let me ask now what questions we have
[04:20:10] about this new schema and the
[04:20:13] constraints we've applied.
[04:20:15] >> I wonder how how could you delete or
[04:20:18] drop table riders when you use uh ID as
[04:20:23] a foreign key. I tried to do that but I
[04:20:27] got an error.
[04:20:28] >> Ah yeah. So you're getting into some
[04:20:30] more advanced stuff here. And suffice to
[04:20:32] say for now, my foreign key constraints
[04:20:34] aren't actually being checked right now,
[04:20:36] but yours might be. If you try to drop a
[04:20:40] table that has actually has some data is
[04:20:42] referenced by a foreign key, SQLite will
[04:20:45] warn you, perhaps just tell you you
[04:20:46] can't do that because this ID is
[04:20:48] referenced from this table over there.
[04:20:50] So in that case, best to delete the
[04:20:53] value that has that foreign key and then
[04:20:55] proceed with dropping that table al
[04:20:57] together. Good question there. Yeah,
[04:21:00] let's take one more.
[04:21:03] >> How much this syntax uh same the other
[04:21:06] SQL languages same as SQ uh same as SQL
[04:21:10] like SQL languages.
[04:21:13] How much the syntax same?
[04:21:15] >> Yeah, good question. So here we're using
[04:21:17] the SQLite database management system.
[04:21:20] It is similar to but distinct in some
[04:21:23] ways from others like my SQL or
[04:21:25] Postgress SQL. I would say that most of
[04:21:27] what you're doing here could also be
[04:21:29] ported to MySQL and Postgress SQL with a
[04:21:33] few exceptions you might need to treat
[04:21:34] on a case- by case basis. In fact, the
[04:21:36] developers of SQLite built things so
[04:21:38] that it would be easy to port their
[04:21:40] database schemas to another schema like
[04:21:43] my SQL or Postgress SQL as well. But
[04:21:46] good question there.
[04:21:49] All right, let's take one more question
[04:21:51] here. Imagine
[04:21:53] if we put in the ID, we don't put any
[04:21:57] data type, it's going to give us in the
[04:22:01] schema, it's going to give us a text or
[04:22:06] Yeah, great question. So, you're asking
[04:22:07] if I didn't tell SQLite what kind of
[04:22:10] type affinity a column had, what type
[04:22:13] affinity would it actually have? A great
[04:22:15] question. In this case, by default, SQL
[04:22:18] light gives the numeric type affinity
[04:22:20] where numeric can store integers or real
[04:22:23] values. But if you give it like a string
[04:22:26] of text like let's say red line, it will
[04:22:28] store that for you too. Um kind of uh
[04:22:31] non-intuitively, but it will. But the
[04:22:33] default uh type is numeric in this case
[04:22:36] if you don't otherwise specify. Good
[04:22:38] question.
[04:22:40] Okay, let's come back then and let's
[04:22:42] focus on wrapping up on a final few
[04:22:45] pieces here. So, we've seen some table
[04:22:48] constraints which we applied primary
[04:22:50] keys and foreign keys. We saw column
[04:22:53] constraints where we could make sure
[04:22:54] that certain values were given to us
[04:22:56] through not null. We could also make
[04:22:58] sure that the uh uh let's say the value
[04:23:00] is in some list of values using check or
[04:23:03] making sure that it's not some value
[04:23:05] also using check as well. default allows
[04:23:08] us to specify a given value for every
[04:23:11] new insertion of rows here. And this is
[04:23:15] actually pretty important to have not
[04:23:18] just you know schemas that have column
[04:23:20] names and um let's say you know type
[04:23:23] affinities as well but also constraints
[04:23:25] to make sure the data we insert works
[04:23:27] well for us. And there actually a story
[04:23:29] behind this person who's on the Charlie
[04:23:33] card. Uh, this person who's on the
[04:23:35] subway, his name is Charlie, and he's
[04:23:38] perhaps the most famous subway rider in
[04:23:40] all of Boston. Back in the 19, let's say
[04:23:44] mid1 1900s, the uh band called the
[04:23:46] Kingston Trio wrote a song about this
[04:23:48] man named Charlie. Charlie supposedly
[04:23:50] got on at the Kendall Square station
[04:23:53] where MIT is, and he made for Jamaica
[04:23:55] plane. But once he got Jamaica plane,
[04:23:58] the guy asked him for one more nickel.
[04:24:00] And well, he didn't have that nickel. So
[04:24:02] he got stuck on the train for years and
[04:24:04] years and years and couldn't get off of
[04:24:06] the subway. So keep in mind Charlie when
[04:24:09] you're adding your own database
[04:24:10] constraints, making sure that if you get
[04:24:12] the train, you're able to get off of it
[04:24:14] at some point, right? Don't end up like
[04:24:15] Charlie in this case. So with this in
[04:24:18] mind, you're able to design your very
[04:24:20] own database schemas that keep not just
[04:24:24] certain columns involved, but also type
[04:24:26] affinities for those columns. Types that
[04:24:27] those data types types of columns can
[04:24:29] store. You're also able to apply
[04:24:31] constraints to those columns to make
[04:24:33] sure that the data you're inserting is
[04:24:34] data you actually want to have in that
[04:24:37] column. Next time we'll focus on
[04:24:39] actually adding data to our columns to
[04:24:41] actually write data to a database file
[04:24:43] to insert, update and delete that data
[04:24:46] all together. So with that in mind,
[04:24:48] we'll see you next time.
[04:24:52] [Music]
[04:25:08] Well, hello one and all and welcome back
[04:25:11] to CS50's introduction to databases with
[04:25:14] SQL. My name is Carter Zeni and last we
[04:25:17] left off we learned how to create our
[04:25:18] very own database schemas. It is a way
[04:25:21] to organize data in our database. Today
[04:25:24] we'll learn how to actually add data to
[04:25:26] our databases to insert to update and
[04:25:28] delete data. We'll do all of this in the
[04:25:31] context of Boston's very own Museum of
[04:25:34] Fine Arts or the MFA for short. So, the
[04:25:37] MFA here in Boston is a century, well
[04:25:40] maybe about a century old museum that
[04:25:41] has many artifacts and artwork inside of
[04:25:44] it, both historical and contemporary.
[04:25:46] And it's worth asking, I mean, how do
[04:25:48] they keep track of the thousands of
[04:25:50] items that are in their collections?
[04:25:52] What could they possibly use? Well,
[04:25:54] chances are they're likely using some
[04:25:57] kind of database. And on that database,
[04:26:00] they want to do four actions we learned
[04:26:03] about back in week zero. They could
[04:26:05] perhaps create data to add data or
[04:26:08] insert data to the database when they
[04:26:10] get some new piece of artwork for
[04:26:11] instance. They might want to query their
[04:26:13] database to read from it. They could
[04:26:15] also update data, change the artist,
[04:26:17] change the artwork in some way. And they
[04:26:19] could also just delete data to remove it
[04:26:22] all together. But if we think about
[04:26:24] these creating, reading, updating, and
[04:26:27] deleting, we'll notice that reading,
[04:26:30] updating, and deleting, we can't do
[04:26:31] those if we don't actually have data in
[04:26:34] our database. And so today, we'll see
[04:26:36] how to create data, how to insert data
[04:26:39] into our very own database.
[04:26:43] Now, let's think about the MFA's
[04:26:45] collections. They're collection of art
[04:26:47] and artifacts. And let me propose they
[04:26:49] have a database looks a bit like this.
[04:26:51] It's a single table and it has a title
[04:26:54] column, an accession number, which is a
[04:26:56] fancy way of saying a unique ID internal
[04:26:59] to the museum and also a date it was
[04:27:02] acquired. We have of course a primary
[04:27:04] key on this table called ID. And let's
[04:27:08] think, well, the museum might want to
[04:27:10] acquire this piece here, this one called
[04:27:12] profusion of flowers. Well, how could
[04:27:15] they log that this artwork is inside of
[04:27:18] their database? They could maybe just
[04:27:21] add a new row. They could say, "Let's
[04:27:23] put Profusion of Flowers as the first
[04:27:25] item in our collections here. We'll give
[04:27:27] it a title, an accession number, which
[04:27:29] again is just unique ID internal to the
[04:27:31] museum, and the date it was acquired.
[04:27:34] And that row then has its own primary
[04:27:37] key to identify this row uniquely in our
[04:27:39] database." Now, let's say they get
[04:27:42] another piece of artwork. They get this
[04:27:43] one called Farmers Working at Dawn. And
[04:27:46] they want to add this one to their
[04:27:47] table, too. Well, they could do the very
[04:27:49] same thing. They could just add a new
[04:27:51] row. They could say, "Let's make a
[04:27:52] title, an extension number, and a date
[04:27:54] it was acquired in this brand new row
[04:27:56] here for that piece of artwork." And
[04:27:59] maybe they get another one, too. Same
[04:28:01] thing. Maybe they'll get back spring
[04:28:03] outing and they want to add this to
[04:28:04] their collection. They could simply add
[04:28:07] another row like this.
[04:28:09] Now, it turns out that the database
[04:28:12] administrator behind the MFA might be
[04:28:14] running a SQL statement that looks a bit
[04:28:17] like this. Insert into. We can use
[04:28:21] insert into to add a new row to any
[04:28:25] given table. And notice how insert into
[04:28:28] needs to know a few pieces of
[04:28:30] information. The first is what table to
[04:28:33] insert into. What is the name of that
[04:28:36] table? Second, it needs to know what
[04:28:39] columns are we adding data to inside of
[04:28:42] this table. We give it a list of those
[04:28:44] columns here. Then, of course, it needs
[04:28:46] to know what new values should go into
[04:28:50] this new row. For each of these columns
[04:28:52] like we saw before, is it profusion of
[04:28:55] flowers? Is it spring outing? etc. Here
[04:28:58] we can see that we have this list of
[04:29:00] values. And notice how value zero, the
[04:29:03] first value in this list, corresponds to
[04:29:05] the new value that will be inserted to
[04:29:08] this first column. And we can keep
[04:29:10] having value one or column one, value
[04:29:12] two and column two, each one aligning
[04:29:14] with that particular column there. So
[04:29:18] let's see an example of this actually in
[04:29:20] code to understand it a bit more
[04:29:22] concretely. I'll go back to my computer
[04:29:25] here. Let's actually create our very own
[04:29:27] database that involves this schema of
[04:29:30] having our very own table which we can
[04:29:32] keep artists and artwork and um
[04:29:34] artifacts as well. So I'll type SQLite 3
[04:29:39] MFAD db to create a database for the
[04:29:43] Museum of Fine Arts abbreviated as MFA.
[04:29:47] I'll hit enter here and notice how I can
[04:29:50] now have access to my very own MFA. DB
[04:29:53] inside my SQLite environment. Well, now
[04:29:57] I can type schema to see the schema of
[04:30:00] this database. So, if I hit enter here,
[04:30:02] well, nothing's there because I just
[04:30:05] made this database. There's nothing in
[04:30:06] it yet. Well, it turns out I do actually
[04:30:09] have a schema file prepared for me
[04:30:12] already in schema.sql.
[04:30:14] Here, I propose we make a table called
[04:30:16] collections. And like our table
[04:30:18] visually, it has, let's say, four
[04:30:20] columns. one as an ID, the primary key
[04:30:24] of this table, one for a title, one for
[04:30:28] the accession number, the unique ID
[04:30:30] internal to the museum, and finally the
[04:30:32] date it was acquired. And notice here
[04:30:36] that title has to be actually added to
[04:30:39] our database. It can't be null. It can't
[04:30:41] have an empty value. Same thing for
[04:30:43] accession number. And further, accession
[04:30:46] number has to be unique. I can't have
[04:30:49] two items with a different accession
[04:30:51] number. Otherwise, I might get them
[04:30:52] confused in my database or inside my
[04:30:55] museum archives as well. So, let me then
[04:30:59] add this schema to my database. And I
[04:31:02] can do so with this command right here.
[04:31:04] This is a SQLite command called read
[04:31:07] that we saw a little bit last week as
[04:31:09] well. I could type read and then the
[04:31:12] name of this file I want to read. So
[04:31:13] I'll say read schema schema.SQL
[04:31:18] hit enter. And now if I type let's say
[04:31:22] dots schema I can see that same SQL
[04:31:25] schema same database schema now inside
[04:31:29] of my terminal.
[04:31:31] Okay. So now, as promised, let's try
[04:31:34] adding some rows to this table because
[04:31:36] right now, if I do select star from
[04:31:39] collections semicolon, I don't see
[04:31:42] anything because nothing is inside yet.
[04:31:45] But I could add something using insert
[04:31:47] into. So let's try that. I'll say insert
[04:31:50] into the collections table. And now I
[04:31:54] have to ask what columns inside of
[04:31:57] collections do I want to add data to?
[04:32:00] Well, I probably want to add to the
[04:32:02] first the ID column, that primary key
[04:32:04] column. Then maybe I want to add a title
[04:32:08] to this row and also an accession number
[04:32:11] and also of course the date this piece
[04:32:13] was acquired. So now I have the table
[04:32:16] I'm inserting into along with the
[04:32:18] columns I'm adding values for. So for
[04:32:21] style sake, I'll hit enter here. And now
[04:32:23] I could type a list of values to insert
[04:32:26] into this new row. I could say values
[04:32:29] and then inside parenthesis the values I
[04:32:32] want to insert. Maybe the first primary
[04:32:35] key that I give to this item is going to
[04:32:37] be just one. Start at one and add up as
[04:32:40] we add new items. For the title, I'll
[04:32:42] say let's call this one profusion of
[04:32:45] flowers. This is the piece we recently
[04:32:46] acquired into our collection. The
[04:32:49] accession number that we gave it was
[04:32:50] 56.257 257 and the date it was acquired
[04:32:54] was back in 1956 0412.
[04:32:58] Now I have all these values here. I'll
[04:33:00] type semicolon hit enter and nothing
[04:33:03] seems to happen. But if I type, let's
[04:33:05] say select star from collections
[04:33:09] semicolon, what do I see but this new
[04:33:12] row inside.
[04:33:14] Let's do it again to get a hang of this.
[04:33:16] I want to now add farmers working at
[04:33:18] dawn to my collection. So I'll do the
[04:33:20] same thing. I'll say let's insert into
[04:33:23] the collections table and let's add
[04:33:25] values for the ID column, the uh title
[04:33:29] column, the accession number, and also
[04:33:32] the acquired column like this. Again,
[04:33:35] for style sake, I'll hit enter. Now I
[04:33:37] give some list of values to add into
[04:33:39] this new row. I'll say values here. Then
[04:33:42] this list of values to add for each
[04:33:44] column. Well, the first column I have to
[04:33:47] give a value for is ID. If you remember,
[04:33:50] our last ID was one. So, what should
[04:33:52] this ID be? Maybe two. So, I'll type two
[04:33:56] here as the next uh increment of my
[04:33:59] primary key. Then I'll give it a title.
[04:34:01] And this title was farmers. Farmers
[04:34:03] working at dawn. We gave it an accession
[04:34:06] number to keep track of it in our own
[04:34:08] internal museum records, our own
[04:34:10] archives here. So, I'll say 11.615
[04:34:14] one 6.5 6.152 is the accession number
[04:34:17] for this particular item. Then I'll say
[04:34:19] we acquired it back in 1911
[04:34:21] on 0803.
[04:34:25] Now I'll hit a semicolon here. Hit
[04:34:27] enter. And now I should be able to see
[04:34:29] if I type select star from collections.
[04:34:32] Select star from collections semicolon.
[04:34:35] I now have these two items inside of my
[04:34:39] collection.
[04:34:40] Now let's do one more here, but let's
[04:34:44] focus in particular on this primary key.
[04:34:47] Like notice here how we've been actually
[04:34:49] inserting our very own primary key one
[04:34:52] and then two. But maybe that's not the
[04:34:55] best design. Like if I let me try this
[04:34:58] again. I'll say insert into uh let's go
[04:35:01] for collections is our table name. And
[04:35:04] maybe I'll try again to add to the ID
[04:35:07] column, the title column, the accession
[04:35:10] number, and the acquired
[04:35:14] column here. What could go wrong, do you
[04:35:18] think, if I try to specify the primary
[04:35:20] key myself? Let me ask this as an
[04:35:23] audience question here. Feel free to
[04:35:24] raise your hand. What might go wrong if
[04:35:27] I try to make the primary key myself and
[04:35:29] insert a value myself?
[04:35:34] Uh let's go to Sakiva.
[04:35:37] >> Yeah. what we could do when we had to uh
[04:35:40] you know load a lot of values like maybe
[04:35:43] uh like big data or something. Is there
[04:35:46] a way to add it through a CSV file or
[04:35:49] something rather than typing insert into
[04:35:51] tables?
[04:35:52] >> A good question. I think you're on to
[04:35:53] something here which is we're inserting
[04:35:54] one row at a time which could get easily
[04:35:57] repetitive. So let me hold that thought
[04:35:59] for just a minute here and focus on the
[04:36:00] primary keys before we see some more
[04:36:02] efficient ways to actually add data to
[04:36:04] our tables. So, I'm with you on this
[04:36:06] idea of maybe we don't want to duplicate
[04:36:08] this primary key, right? Maybe we could
[04:36:10] do a little better than that. So, I'll
[04:36:11] come back to my computer here. And if I
[04:36:14] specify the primary key, I might
[04:36:17] actually add a value that's already in
[04:36:19] there. So, I could thankfully leave it
[04:36:22] up to SQLite to actually increment this
[04:36:24] value for me. Let me try leaving off ID.
[04:36:27] In this case, I'll omit the ID
[04:36:30] altogether, which seems at first like a
[04:36:32] bit of a bad thought. Like shouldn't
[04:36:33] every row have its own ID? Well, let's
[04:36:36] just try and figure what happens. I'll
[04:36:38] hit enter here. And now I'll say let me
[04:36:40] give the values. Well, now the first
[04:36:42] column is the title column. So I'll go
[04:36:45] ahead and say that this one will be
[04:36:46] called spring outing. We're going to add
[04:36:48] this one to our collection here. The
[04:36:50] accession number in this case is 14.76.
[04:36:53] And we acquired this one all the way
[04:36:55] back in 1914 0108
[04:36:59] semicolon. So I'll hit enter here. And
[04:37:02] notice how there's no ID that I have
[04:37:04] specified. But now if I hit enter,
[04:37:07] seems to work. I'll type select star
[04:37:10] from collections. And what do I see? But
[04:37:14] the new primary key of three. So it
[04:37:17] seems like SQLite actually increments
[04:37:20] the primary key for me. If I add some
[04:37:23] new row, it looks what is the current
[04:37:25] highest primary key and adds one to that
[04:37:29] automatically for me. And I've gotten
[04:37:31] that by specifying in my schema this
[04:37:33] primary key constraint down on line six.
[04:37:37] So pretty handy for me here. I see a few
[04:37:41] other questions too. So let's take those
[04:37:42] before we move on as well.
[04:37:46] Let's go to Andre. I just want to ask if
[04:37:49] I delete uh the let's say the third uh
[04:37:52] record and type again will it uh number
[04:37:57] it of the fourth number or or the third
[04:37:59] one?
[04:37:59] >> Uh great question. We'll see this a
[04:38:01] little bit later on too. But if I delete
[04:38:03] some row, let's say I deleted the row
[04:38:05] with primary key of one. Well, what
[04:38:07] SQLite will do at least by default is
[04:38:10] actually take the highest value. Let's
[04:38:12] say the highest value is still three in
[04:38:14] my database. It'll add one to that. And
[04:38:17] when I insert that new row, it'll have
[04:38:18] the ID of four in this case. Okay. So
[04:38:22] let's explore a bit more some of these
[04:38:24] constraints on tables. Like here we're
[04:38:26] talking about the primary key
[04:38:28] constraint, but we also have as we saw
[04:38:30] before the notnull constraint and the
[04:38:32] unique constraint. So let's try
[04:38:34] inserting given those constraints here.
[04:38:37] I'll go back to my computer and again
[04:38:40] notice in my schema I specified that
[04:38:43] this title column should always be not
[04:38:47] null. It should never have a null value
[04:38:49] inside of it. And similarly accession
[04:38:50] number should also be not null. It
[04:38:53] should also be unique. I should have no
[04:38:56] two rows that have the same accession
[04:38:59] number. And maybe kind of uh playfully
[04:39:02] subversively here, let's try to run
[04:39:04] against this constraint. Let's actually
[04:39:06] try to add the same accession number and
[04:39:07] see what happens. So I'll come back to
[04:39:10] my terminal. Let me just reinsert let's
[04:39:13] say spring outing. Notice how if I
[04:39:15] select star from collections, it's
[04:39:18] already in here. But I'll try to add it
[04:39:20] yet again with the same accession
[04:39:22] number. So I'll say insert into
[04:39:24] collections. And by now this is what
[04:39:26] becoming a little more familiar. I now
[04:39:28] want to say the row the columns I want
[04:39:30] to add data to. So I'll say the title
[04:39:32] column, the uh accession number
[04:39:35] accession accession number column and
[04:39:38] also the acquired date. I'll hit enter
[04:39:41] and now I'll say the values again. Let's
[04:39:44] reinsert spring outing. I'll say spring
[04:39:46] outing as a title. The accession number
[04:39:48] is 14.76
[04:39:50] and the date it was acquired was again
[04:39:52] 191408
[04:39:55] semicolon. Now if I hit enter, what do
[04:39:59] we see?
[04:40:01] runtime error unique constraint failed.
[04:40:04] So it seems we ran against this
[04:40:06] constraint here that we specified on
[04:40:09] line four here. Excession number should
[04:40:11] always be unique. But by trying to add a
[04:40:14] new row that had that same accession
[04:40:16] number, we run into this runtime error
[04:40:19] and our operation was not completed. If
[04:40:22] I say in this case select star from
[04:40:24] collections. Notice how I guarded myself
[04:40:27] from adding spring outing more than once
[04:40:30] with the same accession number. So some
[04:40:32] usefulness here to these kinds of
[04:40:34] constraints.
[04:40:35] Let's try violating not null too. I'll
[04:40:38] try adding a title that is actually
[04:40:40] null, non-existent. Try to add a
[04:40:42] painting without a title itself. Let's
[04:40:43] try this. I might try insert into the
[04:40:46] collections table and I'll add to the
[04:40:49] title columns, the accession number and
[04:40:53] also the acquired column. Now I'll say
[04:40:56] the values here. But remember this null
[04:40:59] value. Null meaning nothing. This value
[04:41:01] doesn't exist. I could insert that into
[04:41:04] my table or at least try to. I'll say
[04:41:07] null is a title. And similarly null is
[04:41:10] the accession number. And let's say just
[04:41:12] playfully we got this painting uh back
[04:41:14] in 1900 on January 10th like this. Okay.
[04:41:19] Now semicolon. I'll hit enter. And we
[04:41:23] see the same runtime error. Constraint
[04:41:25] failed. In this case, the notnull
[04:41:27] constraint. So notice again how in my
[04:41:30] schema I specified title should be not
[04:41:33] null. But here when I try to insert a
[04:41:36] null value, I run into that constraint
[04:41:38] and I can't insert that value. If I try
[04:41:41] to select star from collections, I
[04:41:43] should see in this case that insert
[04:41:47] didn't work. So these constraints are
[04:41:50] really guard rails against me, against
[04:41:52] other users to adding values that we
[04:41:55] really shouldn't add to our table.
[04:41:58] Okay. So presumably here, you know,
[04:42:01] we're on to something by adding some
[04:42:03] rows. But if the museum acquires more
[04:42:06] than one item, maybe 100 at a time, I
[04:42:10] don't want to be the programmer who's
[04:42:11] sitting there writing 100 insert into.
[04:42:13] That's like not what I want to do.
[04:42:14] There's probably a better way to do
[04:42:16] this. And let me show you one way to do
[04:42:18] this. One way is to instead of inserting
[04:42:21] one row like this to instead insert
[04:42:24] multiple separated by commas. So here I
[04:42:28] might say this is my first row for each
[04:42:30] of these columns. This is my second row
[04:42:33] again for each of these columns and so
[04:42:35] on and so forth. And it's worth noting
[04:42:39] this is not just a matter of
[04:42:40] convenience. Like if I tried to insert a
[04:42:43] 100 rows, this is certainly convenient
[04:42:45] for me, but it's also most often in most
[04:42:48] cases going to be faster for me to
[04:42:51] insert 100 rows in one go than to insert
[04:42:54] one row 100 times. So this is both a
[04:42:57] convenience thing for programmers and
[04:42:59] also an efficiency thing to actually
[04:43:01] optimize your database as well. So let's
[04:43:04] try this syntax now to avoid me sitting
[04:43:07] there for hours and hours writing many
[04:43:09] insert into. I'll go back to my computer
[04:43:12] and this time let's say we got two
[04:43:14] paintings at once. We got two. So I'll
[04:43:17] try to add both of them. I'll say insert
[04:43:20] into the collections table. And again, I
[04:43:23] want to keep adding to my title column,
[04:43:26] my accession number column, and even my
[04:43:29] acquired column like this. Now, I want
[04:43:33] to add in some values. So, I'll type
[04:43:35] values here. And as a matter of style,
[04:43:38] let me just say I'll make a new line.
[04:43:40] I'll hit enter here. And now, I can type
[04:43:43] each of my new rows on their very own
[04:43:45] line. So, again, I'll type all of the
[04:43:48] values that I want in my first row. I
[04:43:51] might call this one imaginative
[04:43:53] landscape. We got this one back in.
[04:43:56] Actually, we don't quite know when we
[04:43:57] got this one. If I type 56.496 is the
[04:44:00] exception number like here. 56.496.
[04:44:04] The MFA actually doesn't know when they
[04:44:06] got this painting. So, if they don't
[04:44:08] know, let's just insert null. This is
[04:44:11] intentionally left blank. Okay, this is
[04:44:15] my first row. Now, I want to add a
[04:44:17] second one in one go. I'll follow this
[04:44:19] up with a comma. And now I'll type out
[04:44:21] my next set of values. This next one we
[04:44:25] required is called pianies and
[04:44:27] butterfly. Now I'll say the succession
[04:44:29] number is 0681899
[04:44:32] and the date we got this one was back in
[04:44:35] 1906 on January 1st. Now I'll hit
[04:44:39] semicolon here. And now if I hit enter,
[04:44:43] nothing happens. But if I type select
[04:44:46] star from collections semicolon, what do
[04:44:49] we see? But now two new rows being
[04:44:53] inserted. So a handy way to insert more
[04:44:56] than one value. And also if you have a
[04:44:58] lot of values, a more efficient way as
[04:45:01] well. So let me pause here and ask what
[04:45:04] questions we have on insert into
[04:45:08] whether adding one row or adding
[04:45:10] multiple. Let's go to teas. Sir, imagine
[04:45:14] you are writing a code or inserting a
[04:45:16] row. So by mistake you have entered the
[04:45:19] uh wrong spelling of the title. So how
[04:45:21] will we uh rename it?
[04:45:23] >> Uh a great question too and often is the
[04:45:26] case with me. I make typos all the time.
[04:45:28] I might add the uh artwork title and
[04:45:30] misspell it for instance. Well in that
[04:45:33] case I can't use insert into to correct
[04:45:36] it. But I can use a new statement we'll
[04:45:38] see a little later called update. And so
[04:45:41] with update can actually change the
[04:45:42] spellings of things and we'll see that a
[04:45:44] little later today. But great question
[04:45:46] to peek ahead as well.
[04:45:49] Okay, so let's keep going here. Let's
[04:45:52] think about how we can keep adding
[04:45:55] values to our data set. And so far we've
[04:45:57] seen insert into with one row and with
[04:46:00] multiple. But one more way to keep in
[04:46:04] mind is you might already have your data
[04:46:07] perhaps in some other format. And one
[04:46:10] common format looks a bit like this on
[04:46:13] our screen over here. This file is
[04:46:17] called a CSV for commaepparated
[04:46:21] values. Now why commaepparated values?
[04:46:24] Well, let's just look at it here. We see
[04:46:26] some presumably column or column names
[04:46:28] like ID, title, accession number and
[04:46:31] acquired. But what separates these
[04:46:34] column names? Well, looks like commas.
[04:46:36] ID, title, title, comma, accession
[04:46:39] number, and so on. Every row is still
[04:46:42] its own row. That makes sense here. But
[04:46:45] now those row values are also separated
[04:46:48] by commas. Notice here the first value
[04:46:51] before the first comma corresponds to
[04:46:54] the first column. This id is one.
[04:46:57] Similarly the next commaepparated value
[04:47:00] profusion of flowers belongs to that
[04:47:02] next column here title as well and so on
[04:47:05] and so forth. You could if you wanted to
[04:47:07] kind of draw a snaky line to see how
[04:47:10] these columns correspond down our file
[04:47:12] here. Now you might often have data
[04:47:16] already in this format and it's actually
[04:47:18] pretty convenient to try to import this
[04:47:20] data into SQLite into your very own
[04:47:23] table so you can use SQL on it. So let's
[04:47:26] try doing that here. Taking a CSV like
[04:47:29] this and adding it to our database. I'll
[04:47:32] come back to my computer and at this
[04:47:35] point I want to start over. Let's say I
[04:47:38] didn't use insert at all. I actually got
[04:47:41] a CSV from the MFA of all the items in
[04:47:43] our collection. So I'll typequit to
[04:47:46] leave this database. And now I'll type
[04:47:48] rm MFA. DB to remove this file al
[04:47:52] together. Now let me show you mfa.csv.
[04:47:56] This CSV file I have that looks exactly
[04:47:59] like what we just saw. I'll type code
[04:48:01] MFA. CSV. And now I can indeed see I
[04:48:05] have an ID column, a title column, an
[04:48:08] accession number, and the date these
[04:48:10] pieces were acquired, all separated by
[04:48:13] commas. So let's say I want to quickly
[04:48:16] import this data into its very own
[04:48:19] database to run SQL queries on it. As it
[04:48:22] stands, I can't use SQL queries on this
[04:48:24] table because it's not inside of a
[04:48:26] SQLite database. But let me add one.
[04:48:29] I'll type SQLite 3 MFA. DB to remake MFA
[04:48:34] down below. Let me now introduce this
[04:48:37] new command that is not a SQL keyword
[04:48:40] but is actually a SQL like command. And
[04:48:42] this command is called
[04:48:45] import.imp import lets you take a file
[04:48:48] like a CSV and automatically insert it
[04:48:51] row by row into a table of your own
[04:48:54] making or one that you can let SQLite
[04:48:57] create for you. Let's actually create
[04:48:59] the table ourselves and then insert this
[04:49:01] CSV using import. So I'll go back to
[04:49:05] SQLite. Let me recreate this schema.
[04:49:08] Right now there's no tables inside this
[04:49:10] database. But let me create one. I'll
[04:49:12] instead type read schema.sql to read in
[04:49:16] that old schema. SQL file. So I can have
[04:49:19] my own table here. I'll type that schema
[04:49:21] again. And now I see I have that table
[04:49:24] back. But if I type select star from
[04:49:27] collections
[04:49:29] semicolon, nothing is inside. Well, I
[04:49:32] could fix this. I could try to import
[04:49:34] this CSV into collections to insert all
[04:49:37] at once from this own from the CSV file
[04:49:40] we have right here. So to do this, let
[04:49:42] me type.imp import. Now before I finish
[04:49:46] this off, there are a few arguments or
[04:49:50] options I can give to.imp import to make
[04:49:52] sure it works properly. The ones for
[04:49:55] this look as follows. I should type.imp
[04:49:58] import and then dash d-csv
[04:50:02] to say I'm importing a CSV. If I don't
[04:50:05] type dash d- CSV, SQLite might assume
[04:50:09] something about this file that just
[04:50:10] isn't true. It should know that file
[04:50:12] that numbers are here separated by
[04:50:14] commas. Numbers or values, whatever's
[04:50:15] inside my table are separated by commas.
[04:50:19] And then d- skip one. Well, let's take a
[04:50:22] look. If I go back to this file here,
[04:50:25] let's see. I have the first row, the
[04:50:28] second row, the third row, the fourth
[04:50:30] row. Are there any rows I probably
[04:50:33] shouldn't insert into my table here? Let
[04:50:36] me ask the audience. You're free to
[04:50:37] raise your hand. Are there any rows I
[04:50:39] shouldn't insert into this table?
[04:50:45] Let's go to Sukana.
[04:50:46] >> Yes, I think we shouldn't include the
[04:50:48] first row because it doesn't give us any
[04:50:50] value that we need.
[04:50:52] >> Yeah, you're right. Right. So if I look
[04:50:52] at this header row as we call it, I see
[04:50:55] ID, title, accession number, and
[04:50:58] acquired the names for my columns. But
[04:51:00] notice in my schema, I already have
[04:51:03] those column names existing. So I
[04:51:05] shouldn't insert the value ID into my ID
[04:51:09] column. I want to just skip that row and
[04:51:11] only do the next one. So here by typing
[04:51:14] d- skip one, I'll skip that header row.
[04:51:18] So let's try this now. I'll say.imp
[04:51:19] import- CSV. I'm going to import a CSV
[04:51:23] now. D-s skip. How many rows should I
[04:51:26] skip? Well, just one, the header row
[04:51:28] there. Now, I say the file to import.
[04:51:31] So, I'll type mfa.csv,
[04:51:34] the CSV file to import into my database.
[04:51:37] Now, I type the name of the table I'm
[04:51:40] importing into, collections in this
[04:51:42] case. And notice how I no longer need to
[04:51:45] quote collections or quote MFA.CSV CSV
[04:51:49] because this is not a SQL statement.
[04:51:51] This is a SQL light statement. So I can
[04:51:53] get away with not quoting anything here.
[04:51:56] Now I'll hit enter. And again, nothing
[04:51:58] seems to happen, but it's probably a
[04:52:00] good sign. Let me try selecting star
[04:52:03] from collections. Semicolon enter. And
[04:52:07] now all my data is just magically in
[04:52:09] there. It's went from my CSV into my
[04:52:13] very own table.
[04:52:16] Okay, so that's a pretty nice step
[04:52:19] forward. Like no longer do we have to
[04:52:20] use just single line inserts or even
[04:52:23] bulk inserts, those multi-line inserts.
[04:52:25] We can now just import an entire table
[04:52:27] from a CSV. But I think I've been
[04:52:31] showing you a bit of a inaccuracy here,
[04:52:33] at least something that's not often
[04:52:35] going to happen to you. Like if I go
[04:52:37] back to this uh file here, the CSV, what
[04:52:41] you might notice is that I specified the
[04:52:44] primary key. I said ID of one, ID of
[04:52:47] two, ID of three. But if we heard
[04:52:50] before, this might not be the best
[04:52:52] design because what if I import this CSV
[04:52:55] and there's already an item that has the
[04:52:58] ID of one or the ID of two. Ideally, I
[04:53:00] could let SQLite create its very own
[04:53:03] primary keys for each of these rows. And
[04:53:06] more often than not, you'll likely have
[04:53:08] a database or a CSV that looks a bit
[04:53:09] more like this without the primary key,
[04:53:13] but you'll still want to have a primary
[04:53:14] key when you import into your database.
[04:53:17] So, let's try working with this kind of
[04:53:20] CSV now and having SQLite generate some
[04:53:22] of those primary keys for us. Come back
[04:53:25] to my computer and let's update our
[04:53:28] MFA.csv just to remove those primary key
[04:53:31] column here. So I will open up again
[04:53:34] MFA.CSV
[04:53:36] and let me try to just delete this
[04:53:38] column al together. I'll remove ID,
[04:53:41] remove one and two and three and four
[04:53:46] and five. Let me save it. And now that
[04:53:48] ID column is gone but now there's a
[04:53:52] problem. Like if I go to my schema and I
[04:53:55] type dot schema, notice how there are
[04:53:59] four columns in this table. ID, title,
[04:54:03] accession number, and acquired. Well,
[04:54:06] now my CSV only has three columns. So,
[04:54:09] if I try to import this CSV into this
[04:54:12] table, I'm going to run into trouble
[04:54:13] because I have different numbers of
[04:54:15] columns between my CSV and my table.
[04:54:19] What could I do instead? It turns out
[04:54:22] that I could actually import this data
[04:54:25] into a temporary table and then take
[04:54:27] that data and insert that data in that
[04:54:30] temporary table into my real one called
[04:54:32] collections. Here I can use both.imp
[04:54:35] import and insert into to accomplish
[04:54:38] that task for me. So let's try this.
[04:54:40] I'll say import I want to import a CSV
[04:54:44] now. D-csv.
[04:54:46] Which one? Well, MFA.csv
[04:54:48] in this case. Now though, I want to
[04:54:51] create a brand new table that doesn't
[04:54:53] yet exist. So I'll type the name of the
[04:54:55] table. I might just call it temp for now
[04:54:57] to temporarily import this data into a
[04:55:00] brand new table. And notice how here I'm
[04:55:02] not using dash skip one because now I
[04:55:06] want to take advantage of those header
[04:55:08] rows. SQLite if I import into a new
[04:55:11] table. Well, notice I have a header row
[04:55:14] and make my columns the very same names
[04:55:17] that are in my header row. title,
[04:55:20] accession number, and acquired. I don't
[04:55:22] want to skip them. I want SQLite to see
[04:55:24] them and create this table using those
[04:55:27] header rows. So now I'll hit enter.
[04:55:30] Nothing seems to happen. But but if I
[04:55:32] type schema, what do I see? But a brand
[04:55:35] new table called temp that SQLite has
[04:55:38] just made automatically. And notice how
[04:55:39] it used that header row. I have title,
[04:55:42] accession number, and acquired as my
[04:55:44] column names.
[04:55:46] Okay, let's now look inside the temp
[04:55:49] table. I'll say select star from temp
[04:55:53] semicolon. Oh, and now I see all the
[04:55:55] data in there, but I don't have primary
[04:55:57] keys yet. So, my goal is really to take
[04:56:00] all this data and insert it into my
[04:56:03] collections table to give it that
[04:56:05] primary key I've been wanting. Here,
[04:56:07] again, if I type select star from
[04:56:09] collections,
[04:56:11] uh, well, nothing. Oh, something is
[04:56:13] still there. Let me actually just delete
[04:56:15] this for demonstration. I'll say delete
[04:56:17] from collections to remove it all
[04:56:18] together. We'll get that done in just a
[04:56:19] minute. And now let me try select star
[04:56:23] from collections.
[04:56:25] And I should see nothing inside of
[04:56:27] collections.
[04:56:29] So what could I do? I could insert into
[04:56:31] collections using the data from my temp
[04:56:34] table. So I'll try that. I'll say insert
[04:56:37] into collections and choose those
[04:56:40] columns yet again. I'll say the title
[04:56:43] and the accession number.
[04:56:46] And now let's go for the acquired column
[04:56:49] as well. I'll hit enter. But instead of
[04:56:53] typing many new lines of values, I
[04:56:56] actually have a way to dynamically
[04:56:59] select all the values I want to insert.
[04:57:02] And it looks a bit like this. I could
[04:57:04] say insert into some table and some
[04:57:08] columns of that table. But I want to
[04:57:11] insert the results of this select down
[04:57:14] below. So I'll select some columns from
[04:57:17] some separate table. And so long as
[04:57:19] these columns align, I'll be able to
[04:57:22] actually take the results of that select
[04:57:24] and insert all of them into this new
[04:57:26] table using insert into. So let me
[04:57:29] finish my statement here and we can see
[04:57:31] the results. Come back to my computer
[04:57:34] and here I'll type a select to get back
[04:57:36] all the items from uh my temp table.
[04:57:39] I'll say select in this case select um
[04:57:43] let's go for the title column the
[04:57:46] accession number column and the acquired
[04:57:50] column from my temp table. Now if I hit
[04:57:54] semicolon I should see well nothing at
[04:57:58] first but if I type select star from
[04:58:01] collections
[04:58:03] I see all my data now in there selected
[04:58:06] from my temporary table and now if I
[04:58:09] type dots schema I still see temp but
[04:58:12] what can I do now I could just delete
[04:58:13] that table altogether I could say drop
[04:58:16] table temp as we saw last week semicolon
[04:58:19] hit enter dots schema again and Now
[04:58:22] we're back where we want to be with a
[04:58:24] single table. And now we've import our
[04:58:27] data from our CSV with primary keys. If
[04:58:31] I type collections here, we see it all
[04:58:34] in this table.
[04:58:36] Okay. So we've seen several versions of
[04:58:39] import. One to import into an existing
[04:58:41] table and one to import into a brand new
[04:58:43] table. Let me ask then what questions we
[04:58:46] have on how to use import or how to
[04:58:50] insert more data into our database.
[04:58:55] Let's go. Luis,
[04:58:56] >> can we ask the insert into command to uh
[04:59:00] place a column in a specific position?
[04:59:02] >> Ah, good question. Can we ask insert
[04:59:04] into to place a column in a certain
[04:59:06] position? Um, there's a few ways of
[04:59:09] getting at what I think you're asking
[04:59:10] here. So, let me show you a few of those
[04:59:12] here. I'll come back to my computer and
[04:59:15] let me pull up the syntax for insert
[04:59:18] into again. I will choose this and I'll
[04:59:22] show it on the screen over here. So I'll
[04:59:24] say insert into some table given some
[04:59:28] columns. And notice how down below I
[04:59:30] actually have values to insert into
[04:59:32] those columns. I could to your question
[04:59:35] rearrange these values. So I might have
[04:59:38] um this first value here is some value
[04:59:40] that goes into this column. This second
[04:59:42] column here is a value into that column
[04:59:44] and that would rearrange the values I
[04:59:46] insert into those columns. If you're
[04:59:48] asking though if I can reorder the
[04:59:50] columns that is up to create table and
[04:59:53] create table only. And in general I
[04:59:56] encourage you think not so much about an
[04:59:57] ordering of your columns because it
[04:59:58] could be in any order whatsoever. But
[05:00:00] you could just rearrange your selection
[05:00:02] of columns here to insert the data you
[05:00:04] want to insert.
[05:00:06] Okay, let's take one more question here.
[05:00:09] What happens if one of the rows you're
[05:00:11] trying to insert violates a constraint
[05:00:13] on the table?
[05:00:14] >> Yeah, so here we're inserting multiple
[05:00:16] rows and if one actually violates some
[05:00:19] constraint, then we won't actually
[05:00:21] insert any of those rows. This is
[05:00:24] because this insert is bundled inside of
[05:00:26] a transaction which we'll learn more
[05:00:28] about later on in the course. Let's take
[05:00:31] another one.
[05:00:32] >> I noticed that when you did select star
[05:00:34] from collections that one of the
[05:00:36] acquired dates was just blank. It didn't
[05:00:38] say no. Is that because the CSV itself
[05:00:40] just had an empty value next to the
[05:00:42] comma?
[05:00:43] >> Yeah, great observation. So, let me try
[05:00:45] this again so we can see the results of
[05:00:46] this select. I'll come back to my
[05:00:49] computer here and let me show you again.
[05:00:52] If I say select star from collections
[05:00:55] semicolon, notice how this acquired um
[05:00:58] col this acquired cell here, if I go
[05:01:00] back to my uh screen is just blank. But
[05:01:03] we saw before that if I selected star, I
[05:01:06] would have seen null there if this value
[05:01:09] was truly null. Well, it turns out one
[05:01:12] downside of importing from a CSV is that
[05:01:15] all of your data is imported initially
[05:01:18] as text. And if I have just a blank cell
[05:01:21] in my CSV, it won't be converted to null
[05:01:25] automatically. I need to do that myself,
[05:01:27] perhaps using an update statement that
[05:01:29] we'll see in just a bit. So be wary of
[05:01:31] this. If you do want to keep track of
[05:01:33] null values and so on, if you don't
[05:01:36] actually manually make this value a
[05:01:37] null, it'll appear as just a blank
[05:01:39] value, not a null, which is different in
[05:01:42] this respect.
[05:01:44] Okay, so here we've seen how to insert
[05:01:48] not just one row, but multiple and also
[05:01:50] how to import data from a CSV. When we
[05:01:54] come back, we'll see how to actually
[05:01:56] update our data altogether and even
[05:01:58] delete it too. So, we'll come back in
[05:02:00] just a few and talk about how to delete
[05:02:01] data from our tables. And we're back.
[05:02:04] So, we just saw how to insert some rows
[05:02:07] into our database and also to import
[05:02:09] some data. But presumably, we also want
[05:02:12] to be able to delete some data from our
[05:02:14] table as well. You can imagine the MFA,
[05:02:17] the Museum of Fine Arts, maybe they're
[05:02:19] selling a piece of artwork or maybe
[05:02:20] they've lost one or maybe it was stolen.
[05:02:23] But either way, they want to remove the
[05:02:25] row from their table. Well, let's see
[05:02:28] here. We could go back to our schema
[05:02:30] with a table of artifacts and artwork
[05:02:33] that is inside of the MFA. Now, if I
[05:02:36] want to delete a particular piece, you
[05:02:38] could visually think of it a bit like
[05:02:39] this. I could first identify that row I
[05:02:42] want to delete. Let's say it's spring
[05:02:44] outing here. We've sold this piece.
[05:02:47] Well, I could visually just remove this
[05:02:50] row so it's no longer there and shift
[05:02:52] the remaining ones up metaphorically.
[05:02:54] And it turns out that to do this in SQL,
[05:02:57] we have our very own statement we can
[05:02:59] use. This one reads delete from some
[05:03:03] table where a condition is true. So we
[05:03:07] see our old friend where back again and
[05:03:10] where is vitally important to this
[05:03:12] delete from. If I say delete from table
[05:03:14] with no where, what do you think is
[05:03:17] going to happen? We might drop
[05:03:20] everything from our table, right? But if
[05:03:22] I instead say where some condition is
[05:03:24] true, I can select the rows I want to
[05:03:27] delete and only delete those rows. So
[05:03:30] let's try this here. I'll try to delete
[05:03:33] some artwork from our collections table.
[05:03:35] For example, maybe we've sold it and we
[05:03:36] want to get rid of it. I'll come back to
[05:03:38] my computer over here and I will open up
[05:03:42] our SQLite database. I'll say SQLite 3
[05:03:45] mfa.db.
[05:03:46] And now I can type select star from
[05:03:49] collections. And I see a few more items
[05:03:52] than last time now all inside of our
[05:03:54] table. But per the visual, I want to
[05:03:58] delete spring outing to remove it from
[05:04:00] this table. So what could I do? I could
[05:04:03] try delete from and then the table I
[05:04:06] want to delete from. In this case, I'll
[05:04:08] use the let's say collections name
[05:04:12] delete from collections. But I don't
[05:04:14] want to do this. I don't want to say
[05:04:16] delete from collections semicolon end of
[05:04:19] statement because then all delete every
[05:04:22] row. What I should instead do is this
[05:04:25] delete from collections where some
[05:04:28] condition is true. Maybe the title in
[05:04:31] this case is a title I'm trying to
[05:04:33] remove. So I'll say title equals spring
[05:04:37] outing just like this. Semicolon enter.
[05:04:40] Now nothing seems to happen. But if I do
[05:04:43] select star from collections semicolon,
[05:04:47] we no longer see spring outing. And
[05:04:49] notice here how the ID column, the ID of
[05:04:52] three is now gone. If I were to insert
[05:04:55] some new row here, I would start over
[05:04:57] with the highest number, which is seven
[05:05:00] in this case, going from seven to eight.
[05:05:02] But three is no longer part of our
[05:05:04] database. Let me try this again. Notice
[05:05:07] how this one called imaginative
[05:05:09] landscape, the acquired date is null. We
[05:05:12] don't know when we got it. Well, let's
[05:05:14] say that we eventually sell it. It's no
[05:05:16] longer part of our database. We could
[05:05:17] use a condition based on null to remove
[05:05:20] this particular artwork. So, I'll say
[05:05:22] this. Let me try to delete from
[05:05:25] collections
[05:05:26] where title equals not spring outing,
[05:05:30] but uh where the acquired date, sorry,
[05:05:32] the acquired date is null semicolon. I
[05:05:36] could also use is not null where
[05:05:39] acquired is not null, but that would
[05:05:41] delete all the pieces of artwork that
[05:05:43] actually have an acquired date. Here I
[05:05:46] want to delete only those that do not
[05:05:48] have an acquired date. So I'll say where
[05:05:50] acquired is null. Now I'll hit enter.
[05:05:54] Nothing seems to happen, but I'll say
[05:05:55] select star from collections
[05:05:58] semicolon. And I'll see that that piece
[05:06:01] of artwork is now gone. I only have
[05:06:05] those that have an acquired date. Okay.
[05:06:09] So, similar to insert, we've been able
[05:06:12] to delete one row at a time, but it
[05:06:16] would probably be helpful for us to
[05:06:18] delete multiple rows at a time as well.
[05:06:21] Let's look again at our table. Here we
[05:06:24] have our artwork as it currently stands.
[05:06:27] And maybe let's say we want to delete
[05:06:30] those pieces that we acquired before
[05:06:32] 1909. Uh here in Boston, the MFA
[05:06:35] actually moved locations in 1909 to a
[05:06:38] new place still in Boston, but a brand
[05:06:40] new building altogether. So let's say
[05:06:42] that perhaps they left some items at
[05:06:44] their old location. They're no longer
[05:06:46] part of their collections. via what
[05:06:49] condition do you think could I select
[05:06:52] these three rows for my delete from?
[05:06:56] What could I put in my condition to
[05:06:59] delete these three rows? Let me ask the
[05:07:02] audience here. What might you propose
[05:07:04] for delete from here? Delete those three
[05:07:07] particular rows.
[05:07:13] Let's go to shiv
[05:07:14] >> greater than five.
[05:07:16] ID equals than five.
[05:07:18] >> That's a good observations. We could
[05:07:20] look at our table here. We see the ID
[05:07:22] could be greater than or equal to five.
[05:07:25] That would remove these three rows.
[05:07:27] Certainly, there's probably another way
[05:07:29] to do this, too. Any other ideas besides
[05:07:32] the ID? What else could we use?
[05:07:41] Let's go to Yoshvi. Uh
[05:07:43] >> so we could compare the dates and use
[05:07:46] greater than or less than sign with the
[05:07:48] acquired dates.
[05:07:50] >> Ah so you're proposing to use the date
[05:07:52] column too. That makes sense to me as
[05:07:54] well. We could see acquired here.
[05:07:56] Perhaps we could see is the acquired
[05:07:58] value less than 1909 that year that we
[05:08:02] move locations. We could also probably
[05:08:04] use the title, the accession number, and
[05:08:06] so on. And each has their own tradeoffs.
[05:08:09] Remember though, for this particular
[05:08:11] query, which is deleting those items
[05:08:14] that were part of the museum, acquired
[05:08:16] before 1909, probably best to use the
[05:08:20] acquired date to actually delete those
[05:08:24] rows. What if, for instance, our IDs are
[05:08:26] actually not like this, but they're kind
[05:08:28] of interspersed around. I couldn't
[05:08:30] really do a query like if the ID is
[05:08:33] greater than equal to five because I
[05:08:34] could also include those that were maybe
[05:08:36] acquired 1911 1956 and so on. Probably
[05:08:39] ideal for me to use this date if it's
[05:08:41] the date that I ultimately care about.
[05:08:44] So let's try this. I'll go back to my
[05:08:46] environment and I'll try to delete these
[05:08:49] three particular rows. I'll try delete
[05:08:53] from collections as we saw before. But
[05:08:56] now here comes my condition. I'll say
[05:08:58] where the acquired column is less than
[05:09:02] some date that I'll give. And here I'll
[05:09:05] give 1909 January 1st. It turns out that
[05:09:10] SQLite has a few ways to represent
[05:09:12] dates. One of which is this format that
[05:09:15] follows the YY or the year four digits
[05:09:19] and then dash and then MM or the month
[05:09:22] with two digits and then dash again dd
[05:09:25] in this case the day in two digits. So
[05:09:27] 1909-01-01
[05:09:30] means January 1st, 1909.
[05:09:34] And I can use these same operators with
[05:09:38] dates. I could say greater than or less
[05:09:40] than or equal to this particular date.
[05:09:43] And SQLite will be able to parse this
[05:09:45] for me to understand what I mean, which
[05:09:46] is earlier than 1909.
[05:09:50] So let's try this. Then I'll hit enter
[05:09:52] and nothing seems to happen. But if I do
[05:09:55] select star from collections, I now see
[05:09:59] I'm down to two paintings, two pieces of
[05:10:02] artwork that were required only after
[05:10:05] 1909.
[05:10:07] Okay. So given this uh part on delete,
[05:10:12] we're able to delete one row or even
[05:10:14] multiple rows at a time, but there are
[05:10:17] still instances where we might want to
[05:10:18] think about should we delete something
[05:10:21] or can we delete something. We'll talk
[05:10:23] about those in just a minute in terms of
[05:10:25] constraints.
[05:10:27] Be back in a few. And we're back. So, we
[05:10:30] just saw how to delete one row, even
[05:10:34] multiple rows. We haven't yet talked
[05:10:36] about whether we should delete some data
[05:10:38] or whether we should delete some data.
[05:10:40] And particularly in the context of these
[05:10:42] constraints where you might have maybe a
[05:10:44] piece of data you actually shouldn't
[05:10:46] delete to maintain the integrity of your
[05:10:48] table. Now, one example of this is a
[05:10:51] foreign key constraint, which means that
[05:10:54] you have some table with a primary key
[05:10:57] that is referenced by some other table.
[05:11:00] And we'll get concrete about this just a
[05:11:02] minute, but it might mean that if you
[05:11:03] were to delete that primary key, that
[05:11:05] other table would have nothing to
[05:11:07] reference. So, let's update our schema
[05:11:10] here for the MFA, the Museum of Fine
[05:11:12] Arts, and let's say that they have not
[05:11:14] just a collection now, but also artists
[05:11:17] involved. And there exists a many to
[05:11:20] many relationship among artists and
[05:11:22] items in the collection. We could say
[05:11:25] that an artist might make more than one
[05:11:27] piece of art in the collection. And a
[05:11:30] piece of art might be created by more
[05:11:32] than one artist. Now, concretely in our
[05:11:36] database, this might look as follows. I
[05:11:39] could have a table for artists and a
[05:11:42] table for collections. And notice how
[05:11:44] each has their own primary key. Artist
[05:11:47] has an ID column called our primary key
[05:11:49] column. Collections too has an ID called
[05:11:52] our primary key column. Here now in the
[05:11:55] middle is this table created that
[05:11:57] symbolizes that represents the
[05:11:59] relationship among artists and items in
[05:12:02] the collection. Here on the first row we
[05:12:05] see the artist ID of one created the
[05:12:07] piece of art with the collection ID of
[05:12:10] two. So who did what here? Well, we can
[05:12:13] see that the artist with the ID of one
[05:12:16] is Lee Yin. Lee Yin created this piece
[05:12:19] of art with the ID of two, which is
[05:12:22] imaginative landscape. So, we can kind
[05:12:24] of relate in this case artists with
[05:12:26] collections as we saw just a few weeks
[05:12:29] ago. But let's say we decide to delete a
[05:12:32] particular artist. Maybe we delete
[05:12:35] unidentified artists down here. Well, we
[05:12:38] could just delete from the artist table.
[05:12:40] Maybe we find a condition to select this
[05:12:43] row and we delete from artists. We'll do
[05:12:46] that here. Remove that row. But what
[05:12:49] have we done wrong? If we look at our
[05:12:52] created table in particular,
[05:12:55] what have we now done wrong? What kind
[05:12:58] of problem might we run into?
[05:13:04] Let's go to Kareem. The third row with
[05:13:07] ID three was only deleted from the
[05:13:10] artist table without the other table.
[05:13:13] >> Yeah, good point. We only deleted the uh
[05:13:16] artist with the ID of three from the
[05:13:18] artist's table. Now, if I look at the
[05:13:21] created table and I look for the artist
[05:13:23] with ID of three, well, do you see them?
[05:13:26] I don't exist anymore. So, I can't
[05:13:29] understand this relationship. I don't
[05:13:30] know the artist with the ID of three. So
[05:13:34] let's try this now with a new kind of
[05:13:38] schema now in our database. I'll go back
[05:13:40] to my computer and let me open up our
[05:13:44] new version of our database. I'll type
[05:13:46] SQLite 3 in this case uh MFA. DB same
[05:13:51] name but now different schema. If I type
[05:13:54] dot schema, notice a few things here. I
[05:13:58] have those same tables we saw visually.
[05:14:01] I have collections, artists and a
[05:14:04] created table. Let me focus in
[05:14:06] particular on this created table. If I
[05:14:09] say do schema in this case created
[05:14:12] enter, I'll see I have a foreign key
[05:14:16] constraint on my artist ID column and my
[05:14:20] collection ID column. So if I tried to
[05:14:23] delete an artist that is referenced in
[05:14:27] my created table, I would probably raise
[05:14:30] a constraint error, a foreign key
[05:14:33] constraint error. So let's just try this
[05:14:35] and see what happens. Let me try delete
[05:14:39] from the artist table. Delete from
[05:14:42] artists
[05:14:45] where let's say the name of that artist
[05:14:48] is literally unidentified
[05:14:51] artist. This is the name they have in
[05:14:53] the Museum of Fine Arts collections.
[05:14:55] Unidentified artist. So now I want to
[05:14:58] delete them from that table. Well, if I
[05:15:01] hit enter, I do get that foreign key
[05:15:04] constraint error. So, does this mean I
[05:15:07] just can't delete this artist? Or is
[05:15:10] there a workaround? Let's look at it
[05:15:12] visually again. I'll go back to what we
[05:15:14] had before as our table. And let me ask
[05:15:18] the audience here, what's the solution?
[05:15:21] Like, if I can't delete unidentified
[05:15:24] artist because they have an ID
[05:15:26] referenced by this table. What should I
[05:15:29] maybe do first? What should I do
[05:15:31] instead? Yeah, I want to say that first
[05:15:33] we can delete the ID that is being
[05:15:36] referenced by this ID that we want to
[05:15:38] delete. Then we can delete it. In fact,
[05:15:41] if we want to delete from the artist,
[05:15:43] first we have to delete from the created
[05:15:44] table or to other table which it is
[05:15:47] referencing, then we can delete from the
[05:15:49] artist table.
[05:15:50] >> Yeah, I like your I like your thinking
[05:15:51] here. So if we look at the created
[05:15:53] table, you notice that we can't delete
[05:15:55] unidentified artist because it's
[05:15:57] referenced in the created table. What we
[05:16:00] should maybe first do is delete this
[05:16:02] row, delete their affiliation with their
[05:16:05] work and then delete the artist so we
[05:16:08] don't run into this foreign key
[05:16:10] constraint. So let's try this in our
[05:16:12] SQLite environment. Come back to that
[05:16:16] computer and again our plan was to first
[05:16:19] delete the artist's affiliation with
[05:16:21] their work from the created table. So
[05:16:24] let me show you first the created table.
[05:16:26] I'll say select select star from created
[05:16:30] and see how it's exactly like the table
[05:16:32] we just visualized. Now let me try to
[05:16:35] delete this artist affiliation with
[05:16:38] their work. I'm not deleting the artist.
[05:16:40] I'm deleting their affiliation with
[05:16:43] their authorship, their artistship,
[05:16:45] whatever you want to call it for their
[05:16:47] work. Now I'll say delete delete from
[05:16:51] let's say delete from artists where the
[05:16:56] artist ID is equal to or equals three.
[05:17:02] Well I could do this but there's
[05:17:05] probably a better way. Like I know the
[05:17:07] ID and that's fine but we could also use
[05:17:10] what we saw a little bit ago which were
[05:17:12] sub queries. a way to write a query that
[05:17:14] returns me the result and that result
[05:17:16] gets included in another query
[05:17:18] altogether. So let's try that instead.
[05:17:20] Let's say I don't know the artist ID.
[05:17:23] What I could do is make a sub query. I
[05:17:25] could say inside of this let me select
[05:17:28] the ID from oh the artist's table where
[05:17:33] in this case the name equals
[05:17:37] unidentified
[05:17:38] artist. And then let me close out this
[05:17:41] query. hit a semicolon. And I already
[05:17:44] see a typo in this, but I'm just going
[05:17:45] to try it anyway. I will go ahead and
[05:17:48] hit enter. And let's see if I type
[05:17:51] select star from artists. Enter. I still
[05:17:56] see unidentified artists. And I think my
[05:17:59] typo here was as follows. If I look up
[05:18:01] my query using the up arrow on my
[05:18:02] keyboard, I see delete from artists
[05:18:05] where the artist ID equals some value
[05:18:07] here. But do I want delete from artists?
[05:18:11] I don't I actually can't delete from
[05:18:13] artists. What I should do instead is
[05:18:15] delete from the created table. So, let's
[05:18:17] try this. I'll say delete from created
[05:18:22] making sure I only have double quotes
[05:18:24] around created. Then I'll say where the
[05:18:26] artist ID equals let's say either three,
[05:18:30] but it could also be the result of this
[05:18:32] subquery. I'll say 1 2 3 4 and then
[05:18:36] select the ID from the artists from the
[05:18:40] artist table where the name equals
[05:18:43] unidentified
[05:18:46] artist
[05:18:48] then I'll close this sub query hitting
[05:18:50] semicolon hit enter and now if I say
[05:18:54] select star from created semicolon I
[05:18:58] should see that this artist's
[05:19:00] affiliation with their work no longer
[05:19:02] exists. artists. And because it no
[05:19:04] longer exists, I can now delete them
[05:19:06] from the artist table. I don't have this
[05:19:09] foreign key, artist ID, referencing the
[05:19:12] primary key of this artist. So, let's
[05:19:15] now try that. I could say select star
[05:19:17] from artists. I see that unidentified
[05:19:21] artist is still in here, but let's
[05:19:23] delete them now. I'll say delete from
[05:19:26] let's say artists where the name equals
[05:19:30] unidentified
[05:19:31] artist. Closing my quotes, semicolon,
[05:19:34] hit enter. And now if I select star from
[05:19:37] artists, semicolon, I should see they're
[05:19:41] no longer in this table to our earlier
[05:19:44] example. This becomes a two-step
[05:19:46] process. First, delete their
[05:19:47] affiliation, then delete their name.
[05:19:51] Okay, so let's try this yet again, but
[05:19:56] now using some additional uh tools that
[05:20:00] we have at our disposal. So let's look
[05:20:03] back at this foreign key constraint that
[05:20:06] existed in this table. If you remember,
[05:20:09] it looked a bit like this. In my created
[05:20:12] table, I had this line foreign key.
[05:20:15] Artist ID references the ID column in
[05:20:19] artists. Well, if that is the case, I
[05:20:23] can't delete the artist with the ID
[05:20:26] referenced by this foreign key. But it
[05:20:29] turns out that I could specify some
[05:20:32] alternative action that happens when I
[05:20:35] try to delete the ID that is referenced
[05:20:38] by this foreign key. I can specify that
[05:20:40] using a keyword called ondee.
[05:20:44] So after foreign key reference artist
[05:20:46] ID, I could say afterwards ondee and
[05:20:48] then specify some action I want to
[05:20:50] actually happen when I try to delete the
[05:20:53] primary key referenced by this foreign
[05:20:55] key. One thing I could use would be
[05:20:58] restrict, which is kind of like what we
[05:21:00] saw before. If I try to delete a primary
[05:21:04] key that is referenced by this foreign
[05:21:06] key, I will not be allowed to do it.
[05:21:09] That action is restricted.
[05:21:11] I could also decide to take no action.
[05:21:15] In this case, I could delete the primary
[05:21:18] key referenced by this foreign key and
[05:21:21] nothing would happen. I would actually
[05:21:22] be allowed to do that, which may be
[05:21:26] unwise in some cases, but I could give
[05:21:28] myself that power. I could also decide
[05:21:31] to set null. That is, if I delete the
[05:21:35] primary key that is referenced by this
[05:21:38] foreign key, what I'll do is set the
[05:21:40] foreign key to be null, meaning that
[05:21:42] value no longer exists. I could
[05:21:45] alternatively set it to a default value
[05:21:47] for that column. Or perhaps most
[05:21:50] compellingly, I could try to cascade the
[05:21:54] deletion. Where cascade means if I
[05:21:56] delete the artist, for instance, let's
[05:21:59] also delete their affiliation with their
[05:22:01] artwork all in one go. This converts our
[05:22:04] two-step process into a onestep process.
[05:22:08] So let's visualize this. Let's say we
[05:22:11] have now applied this constraint ondee
[05:22:15] cascade. So if I delete the artist, I'll
[05:22:18] also delete their affiliation with their
[05:22:20] work. We'll have the same two tables,
[05:22:22] artists, collections, and created. Now
[05:22:26] again, artist ID references this primary
[05:22:29] key in artists. Now I'm going to try I
[05:22:32] want to delete unidentified artist here.
[05:22:35] Well, I could do that. I could just
[05:22:36] delete their row. And now instead of a
[05:22:39] foreign key constrainted error, what I
[05:22:42] get is the following. I see and created
[05:22:45] that this row is also gone. The row that
[05:22:48] had the artist ID of three gets removed.
[05:22:52] We've cascaded the deletion onward to
[05:22:54] the created table.
[05:22:57] So let's try this now with a new
[05:22:59] database schema. I'll go back to my
[05:23:01] computer here.
[05:23:06] So I'm back at in my terminal here and I
[05:23:08] can type SQLite 3 MFA. DB to reopen this
[05:23:12] database. And notice how if I type dots
[05:23:15] schema, I've updated this schema to now
[05:23:17] have ondelete cascade. Let me show you
[05:23:20] over here on the screen here on the
[05:23:22] created table, I now have the very same
[05:23:25] kind of table schema, but now my only
[05:23:27] difference is I've applied this ondee
[05:23:30] action to my foreign key constraints. In
[05:23:32] particular, I'm going to cascade the
[05:23:34] delete from the artist's table to the
[05:23:37] created table. So let's try that out in
[05:23:40] SQLite. I'll come back over here and I
[05:23:43] will now try just delete from the
[05:23:46] artists table where the name equals
[05:23:50] unidentified
[05:23:51] artist. Unidentified artist semicolon.
[05:23:54] Now I'll hit enter and I don't get a
[05:23:58] foreign key constraint anymore. But if I
[05:24:01] say select star from created semicolon,
[05:24:05] notice how I've also deleted the
[05:24:07] artist's affiliation with their work. So
[05:24:10] that is wherever in the artist ID column
[05:24:14] I saw the ID for the artist I deleted, I
[05:24:17] would too delete that row. So I have no
[05:24:21] references to that primary key which is
[05:24:23] now gone from my table. So let me ask
[05:24:27] here we've seen how to delete single
[05:24:31] rows, how to delete multiple rows and
[05:24:34] now how to delete data among some
[05:24:36] constraints like our foreign key
[05:24:37] constraints. What questions do we have
[05:24:40] on those techniques?
[05:24:43] Let's go to Han.
[05:24:44] >> I have a question regarding deleting. Um
[05:24:47] since the uh the ID numbers have been um
[05:24:51] removed while we removing the record I
[05:24:53] was wondering if do we have to clean it
[05:24:55] up somehow later or will they be
[05:24:57] populated with the new data as it comes
[05:24:59] along?
[05:25:00] >> Yeah great question. So the question is
[05:25:02] what happens to our primary keys when we
[05:25:04] delete our data. So for this one let me
[05:25:07] show you the visual again that we had
[05:25:08] before of our tables nicely printed on
[05:25:11] the on the slide. So I'll come back here
[05:25:12] and I will go back to our idea of these
[05:25:17] um joint tables where we had an artists
[05:25:20] table, a collections table and a created
[05:25:23] table. And we saw before that we're
[05:25:24] going to delete this artist called
[05:25:26] unidentified artist. So I'll delete
[05:25:29] them. And to your point, well the ID of
[05:25:32] three no longer exists in this case. Now
[05:25:36] by default at least in SQL light if I
[05:25:39] insert a new row what I'll do is take
[05:25:42] the highest ID value and I will then
[05:25:46] make that the new primary key for the
[05:25:48] new row that I insert. That is the
[05:25:51] default situation. I could if I wanted
[05:25:54] to get more specific and if I had done
[05:25:57] in my um ID integer col my ID integer
[05:26:02] column here in my create table if I had
[05:26:05] also said this keyword called auto
[05:26:07] increment all one word what would happen
[05:26:10] instead is I would actually reinsert an
[05:26:14] ID that is not used so in this case
[05:26:16] three is not used I could insert that
[05:26:19] one here so up to you what you want to
[05:26:22] do in general General SQLite by default
[05:26:24] will take the highest ID, add one from
[05:26:27] there. If you specify this constraint
[05:26:29] called auto increment, you will instead
[05:26:32] take whatever ID is not being used and
[05:26:34] use that in your insert afterwards.
[05:26:38] Okay, so now we've seen how to insert
[05:26:41] and how to delete data. But of course,
[05:26:44] we make mistakes when we add data or
[05:26:46] even when we delete data. So, we'll see
[05:26:48] in just a minute how to update our
[05:26:50] values as well to correct typos and even
[05:26:52] to update associations between artists
[05:26:55] and artwork.
[05:26:57] And we're back. So, we've so far seen
[05:26:59] how to insert some data into our tables
[05:27:02] and how to delete it. But sometimes we
[05:27:05] don't want to fully delete something. We
[05:27:07] just want to change its value to correct
[05:27:09] some typo or correct some association.
[05:27:12] So let's think to our MFA example where
[05:27:15] the Museum of Fine Arts has some tables
[05:27:18] that look like this. They have artists
[05:27:20] in their collection and they also have
[05:27:22] artwork in their collection. They also
[05:27:24] have a created table to associate
[05:27:26] artists with their artwork. Now in this
[05:27:30] case we know that I have this
[05:27:33] unidentified artist and we can see that
[05:27:36] they authored this item in the
[05:27:38] collections farmers working at Dawn. But
[05:27:42] let's say that later on we find out it
[05:27:45] wasn't an unidentified artist. It was
[05:27:48] instead Lee Yin who created Farmers
[05:27:50] Working at Dawn. How could we update our
[05:27:55] tables to make sure it's Lee Yin who we
[05:27:58] have creating Farmers Working at Dawn?
[05:28:02] So uh what we could do is like uh we
[05:28:07] know that in created we have our artist
[05:28:10] ID and the collection ID. So we could
[05:28:14] update it there but somehow we need to
[05:28:17] cascade it over to the artists table
[05:28:19] because now this unidentified artist row
[05:28:23] I think we probably don't need it.
[05:28:25] >> Yeah. Yeah. So, a good point here where
[05:28:26] we could actually probably change the
[05:28:28] created table to reassociate an artist
[05:28:32] with some new artwork here. So, let's
[05:28:34] visualize this. I go to my created table
[05:28:36] and here the artist ID is currently
[05:28:39] three, but I want it really to be one. I
[05:28:43] want Lee Yin to be associated with this
[05:28:45] piece called Farmers Working at Dawn.
[05:28:48] So, I could update the created table to
[05:28:50] instead of having three here, have one.
[05:28:53] Now we see Lee Yin created Farmers
[05:28:56] Working at Dawn. And to your concern
[05:28:58] about this unidentified artist here, I
[05:29:01] think it's okay to have an artist in our
[05:29:03] table who may or may not have an item in
[05:29:05] collections. We'll say that's okay, at
[05:29:07] least for now. So if we can update our
[05:29:11] associations between artists and
[05:29:13] collections like this, let's actually
[05:29:16] try to do that in our very own database
[05:29:18] here. I'll go back to my SQLite
[05:29:21] environment. And now let me try to uh
[05:29:24] open it. First I'll do SQLite 3 MFA. DB.
[05:29:27] And now let me type dots schema to show
[05:29:29] you I have the very same schema from
[05:29:31] before. So I want to update the artist
[05:29:34] association between Lee Yin and farmers
[05:29:37] working at dawn. So let's say I'll
[05:29:40] select star from created like this.
[05:29:42] Semicolon. Here I have my artist ids and
[05:29:46] my collection IDs. I see that we have
[05:29:49] the unidentified artist ID of three
[05:29:52] creating uh farmers working at dawn with
[05:29:54] the ID of one our collection here. So
[05:29:58] now let's try to update the artist who
[05:30:01] created this particular painting here. I
[05:30:03] have three associated with one but I
[05:30:06] want one associated with one where one
[05:30:09] is the ID for Lee Yin and one my
[05:30:12] collection ID is the ID for this artwork
[05:30:14] here. So let me try this. I'll say
[05:30:16] update created and set let's say artist
[05:30:20] ID equal to some particular value. Well,
[05:30:25] what value should I set it to? I could
[05:30:28] try to set it to Lein's ID, which we
[05:30:30] know is just one. But let me try instead
[05:30:33] to use a sub query here. Let me try to
[05:30:36] say parenthesis and then write some
[05:30:38] query to update this value. I'll say
[05:30:41] select ID from artists like this. Enter
[05:30:46] again where the name equals Lee Yin. And
[05:30:52] then let me close this sub query. Well,
[05:30:56] if I try to run this query, what might
[05:31:00] happen? I'm updating the created table.
[05:31:02] I'm setting the artist ID equal to the
[05:31:05] ID for Lee Yin. But what I've forgotten
[05:31:08] is this where to only choose some rows
[05:31:12] to update. So let me not close it yet.
[05:31:15] I'll instead say where in this case the
[05:31:18] collection ID the piece of artwork in
[05:31:22] our collection is equal to well the ID
[05:31:26] for this painting. I'll say select ID
[05:31:29] from collections and then I'll say where
[05:31:32] the title equals farmers working at
[05:31:36] dawn. Now I'll close this subquery and
[05:31:40] hit semicolon. And here we've seen our
[05:31:43] first example of an update query. I'm
[05:31:46] trying to update the artist ID column in
[05:31:49] created to be the ID for Lee Yin. I only
[05:31:52] want to do that though on the row where
[05:31:55] collection ID is equal to the ID for
[05:31:58] this particular painting we want to
[05:32:00] change the attribution for. So now I'll
[05:32:02] hit enter and if I select star from
[05:32:05] created I should hopefully see in this
[05:32:08] case that the artist ID associated with
[05:32:13] this painting is two and also down below
[05:32:16] here is one as well. So I have Lein
[05:32:18] associated with now two paintings
[05:32:21] overall.
[05:32:23] So let's get a grasp on what this update
[05:32:25] uh syntax really looks like in general.
[05:32:28] And for that let's show this slide here.
[05:32:30] We have this update keyword update
[05:32:33] statement in SQL to take uh a table name
[05:32:37] and update the columns inside of it. I
[05:32:39] say update then the name of the table I
[05:32:42] want to update. Then I say set some
[05:32:46] column equal to some value. I could if I
[05:32:49] wanted to have more than one column
[05:32:51] here. I could say maybe title and even
[05:32:55] um maybe if we're talking about authors,
[05:32:56] authors over here or even acquired date.
[05:32:59] I could update more than one column in
[05:33:02] my set portion here. Then comes this
[05:33:05] where portion where some condition is
[05:33:07] true. I want to make sure I don't update
[05:33:10] all of my rows. I only update those
[05:33:13] where some condition is actually true.
[05:33:16] So this is your syntax for updating some
[05:33:19] columns. Let's say if you want to change
[05:33:21] an artist attribution or if you want to
[05:33:24] change a typo you've made. So let's see
[05:33:27] this now not just in terms of changing
[05:33:30] artists and their attributions. Let's
[05:33:33] see a use case for update. we've made
[05:33:35] some mistakes in our data and let's say
[05:33:38] the museum decides to host some kind of
[05:33:40] um event where people vote on their
[05:33:42] favorite piece of artwork. They kind of
[05:33:44] handwrite or type it into some online
[05:33:46] form. Well, we might get back a CSV of
[05:33:49] those responses, some commaepparated
[05:33:51] values, one line for each vote from our
[05:33:54] people who've attended this convention.
[05:33:56] Let's go back over here and I'll show
[05:33:58] you that CSV. Let me go to my
[05:34:02] environment and I'll type code MFA.csv
[05:34:05] to open this CSV that I already have.
[05:34:09] And here actually it's not called
[05:34:10] MFA.csv, it's called code votes.csv.
[05:34:14] And now here we can see I have a table
[05:34:18] of one column that has several votes
[05:34:21] inside of it. Let's see we have maybe 20
[05:34:23] votes to be exact. So the first row is
[05:34:26] the header row. I have in this CSV one
[05:34:30] column called title and each line here
[05:34:33] is one vote for a museum goer's favorite
[05:34:35] piece of artwork. We see farmers working
[05:34:38] at dawn. We see imaginative landscape
[05:34:40] profusion of flowers and our goal is to
[05:34:43] count up these votes to see which is the
[05:34:45] most popular. Well, let's try using
[05:34:49] import again to actually turn this CSV
[05:34:52] into our very own SQLite database. Let
[05:34:56] me go back to my terminal and I'll type
[05:34:58] SQLite 3 votes.db to create a votes
[05:35:01] database. I'll hit enter. And now I can
[05:35:05] use import. I could say import a CSV
[05:35:09] called votes.csv
[05:35:11] into a table also called votes. I'll hit
[05:35:14] enter now. And now if I select star from
[05:35:18] votes semicolon, I'll see all of my
[05:35:22] votes now in a single table. So, I want
[05:35:25] to tally these votes. We could do that
[05:35:28] using a technique we learned back in the
[05:35:29] week on querying and relating. What if I
[05:35:32] wanted to group by my titles and count
[05:35:35] up those groups? I could do that. I
[05:35:38] could say select, let's say, title and
[05:35:40] also the count of title. Let me count up
[05:35:43] the votes for each title from, in this
[05:35:47] case, my votes table like this.
[05:35:50] Now I want to count not just each vote
[05:35:53] individually but I want to group them. I
[05:35:55] want to count group votes by group where
[05:35:58] that group is in this case the title
[05:36:00] itself. So let me try running this query
[05:36:03] and hitting enter.
[05:36:05] Well I'll see I've started to count some
[05:36:09] votes like I have imaginative landscape
[05:36:11] here. Spring outing farmers working at
[05:36:14] dawn. Spring outing down below here too.
[05:36:17] But I seem to be missing something. Like
[05:36:19] I shouldn't have this many groups. I
[05:36:21] should only have four groups. Why do I
[05:36:23] have so many? Well, it seems like
[05:36:25] there's some typos here. What typos do
[05:36:28] you see? Feel free to raise your hand.
[05:36:32] >> So, uh I think that it is title is uh
[05:36:36] when you count it is uh case sensitive.
[05:36:38] So maybe it is counting one by one.
[05:36:41] >> Yeah, a good idea. So maybe it's case
[05:36:43] sensitive our group by is. And you'd be
[05:36:45] correct if you said that group by is in
[05:36:48] this case sensitive. So if we see here
[05:36:50] we see farmers working at dawn all
[05:36:53] capitalized at least the farmers working
[05:36:55] and dawn capitalized. Well that won't be
[05:36:57] part of the same group as uh let's say
[05:37:00] farmers working at dawn all cap properly
[05:37:04] capitalized in this case with lowercase
[05:37:06] working and lowercase dawn as it is in
[05:37:08] the MFA collections. So we could
[05:37:10] probably fix some capitalization here.
[05:37:13] What other things could we fix? Let's
[05:37:15] hear from one more person.
[05:37:17] Let's go to Laurens.
[05:37:18] >> The uh the count on each typo.
[05:37:22] >> There are some typos in here.
[05:37:23] Absolutely. So, if I look at some of
[05:37:25] these, I see uh not farmers but famers
[05:37:28] working at dawn. Um I might see instead
[05:37:31] of imaginative landscape, I just see
[05:37:32] imaginative landscape. So, definitely
[05:37:35] some typos in here to fix as well. So,
[05:37:38] let's start working on using our update
[05:37:40] tool, our update keyword to fix some of
[05:37:43] this data, to clean it up, so to speak,
[05:37:45] so we can count up our votes for these
[05:37:47] artworks. Come back to my terminal. And
[05:37:51] now, let's try updating to at least
[05:37:54] remove some of this white space here.
[05:37:56] Like, you might notice that imaginative
[05:37:58] landscape has a space before it. And so
[05:38:00] does spring outing here. That space
[05:38:02] counts as part of the title and I want
[05:38:04] to remove it. So, what could I do? I
[05:38:08] could try using a function in SQLite,
[05:38:11] one called trim. Trim takes a string and
[05:38:14] just removes leading and trailing whites
[05:38:17] space, giving back only the characters
[05:38:19] in the middle. So, let me try that. I'll
[05:38:22] say update votes my table here and set
[05:38:26] the title column equal to what? Well,
[05:38:31] the trimmed version of title. Trim looks
[05:38:34] like this. trim and then some
[05:38:36] parenthesis to say the input to this
[05:38:38] function. I'll give it the title column.
[05:38:42] Now I'll hit semicolon and this query
[05:38:44] will run as follows. It will update the
[05:38:47] votes table and inside the votes table
[05:38:50] set the title column equal to the
[05:38:53] trimmed version of whatever values are
[05:38:55] inside that column. Trimming here means
[05:38:58] remove trailing and leading whites
[05:39:00] space. I don't need to apply any
[05:39:03] condition. I don't need to say say where
[05:39:05] dot dot dot because I want to apply to
[05:39:08] all rows in my data set. Now I'll hit
[05:39:11] enter and let me try running this again.
[05:39:13] I'll say up arrow to get back my old
[05:39:16] query. Now I'll try counting again and I
[05:39:19] think we're making some progress. Like I
[05:39:21] can see that I've removed removed quote
[05:39:24] unquote those um titles that had leading
[05:39:26] or trailing whites space. They're now
[05:39:28] part of a group because their titles now
[05:39:31] match those groups. Let's keep going. We
[05:39:34] noticed before we had some
[05:39:35] capitalization issues. So, let's fix
[05:39:37] those as well. I can go back to my
[05:39:40] terminal and we could introduce this
[05:39:42] other function, one called upper. Upper
[05:39:45] converts a string like farmers working
[05:39:48] at dawn to be all in uppercase kind of
[05:39:50] shouted out. And that's useful for us
[05:39:53] here because we could kind of force
[05:39:54] everything to uppercase thereby removing
[05:39:56] any inconsistencies in capitalization.
[05:39:59] So, let me try that. I'll say update
[05:40:02] again the votes table and this time I'll
[05:40:05] set title equal to the uppercase version
[05:40:09] of title. So upper here is a function in
[05:40:13] SQLite that takes some values associated
[05:40:15] with a column and uppercases the entire
[05:40:18] thing to remove any consistencies and
[05:40:21] capitalization. Again no condition here
[05:40:24] because I want to apply this to all
[05:40:26] rows. I'll hit enter. And now if I
[05:40:28] select select star from collections
[05:40:32] semicolon oops select star from votes in
[05:40:35] this case no longer a collections table.
[05:40:36] I'll say select star from votes
[05:40:39] semicolon. I should see all of my titles
[05:40:42] capitalized. But now I want to group by.
[05:40:45] So let's try this. I'll go up arrow to
[05:40:47] get back to my old query that grouped by
[05:40:49] title. Hit enter. And now we're still
[05:40:53] making some more progress. I'm reducing
[05:40:55] my number of groups until I get to four.
[05:40:58] But there's still some typos like we see
[05:41:00] famers working at dawn or farmers
[05:41:03] working or farmser working at dawn. We
[05:41:06] want these to be included as part of
[05:41:08] this group. Farmers working at dawn. So
[05:41:11] we should fix some of these typos here.
[05:41:14] Let me go back to my terminal and let's
[05:41:16] try this out. I could in this case just
[05:41:19] manually correct these. Like you could
[05:41:21] imagine me doing something like this.
[05:41:23] update votes and set the title equal to
[05:41:28] all caps farmers working at dawn. Now
[05:41:32] including a condition where the title
[05:41:35] presently is is equal to far famers
[05:41:39] working like this semicolon or not
[05:41:42] famous work uh I think it's farmers
[05:41:44] working just all
[05:41:46] in two words that was one title we saw I
[05:41:49] could manually update it a bit like this
[05:41:51] let me hit enter and let me do the same
[05:41:54] query by hitting the up arrow on my
[05:41:55] keyboard
[05:41:57] me find this one hit enter and now we
[05:42:00] can see that that title Farmers working
[05:42:02] is now just part of the main group
[05:42:05] farmers working at dawn. I could keep
[05:42:08] going here. I could try to convert
[05:42:10] famers working at dawn to farmers
[05:42:12] working at dawn. Let me try it. I could
[05:42:15] say select let's say um not select let
[05:42:18] me update let me update in this case
[05:42:20] votes and set title equal to farmers
[05:42:24] working at dawn where the title equals
[05:42:29] in this case famers working at dawn
[05:42:33] semicolon enter let me hit up arrow to
[05:42:36] go back to my old query to group by and
[05:42:39] now we're getting somewhere I'm seeing
[05:42:41] now only two groups for farmers working
[05:42:43] at dawn on but one more to fix. Now,
[05:42:48] we'd be here for a while if I spend all
[05:42:50] this time like one by one fixing these
[05:42:52] typos. So, there's probably a better
[05:42:55] way. There is. This one's going to be
[05:42:58] using the like keyword. We don't have to
[05:43:01] say equal so much. We can just say like
[05:43:03] now I could try to match any title that
[05:43:06] looks like Farmers Working at Dawn and
[05:43:09] update it to be the correct title. So,
[05:43:12] let's try that here. I could now try
[05:43:14] update votes and set title equal to
[05:43:19] farmers working at dawn. Farmers working
[05:43:23] at dawn where the title
[05:43:27] is like
[05:43:30] where the title is like some pattern I
[05:43:33] could give. Now for this data set it
[05:43:36] turns out that the only artwork that
[05:43:38] begins with FA is farmers working at
[05:43:41] dawn. So to match any title with FA and
[05:43:45] then anything afterwards, I could use FA
[05:43:49] percent and then close out that pattern.
[05:43:53] Notice how I don't have to have
[05:43:55] consistent capitalization like is case
[05:43:58] insensitive. And notice how too the
[05:44:00] percent matches anything that comes
[05:44:02] after FA.
[05:44:04] Now in this data set, this is okay. But
[05:44:08] in a larger data set, you'd probably
[05:44:10] want to avoid this kind of query because
[05:44:12] you could match much more than farmers
[05:44:14] working at dawn. You'd match anything
[05:44:16] that begins with FA. So be careful with
[05:44:19] this and think through what pattern
[05:44:21] should you use to fix up your titles.
[05:44:24] Let me just hit enter here. And now let
[05:44:26] me try hitting up arrow again to show
[05:44:28] you the result. And now we're in a
[05:44:31] pretty good place. I see all of my
[05:44:33] titles like farmers working at dawn are
[05:44:36] correctly capitalized, consistently
[05:44:38] spelled, and all in one place.
[05:44:42] Okay, let's try the others here. I also
[05:44:44] have imaginative landscape which could
[05:44:46] be a little bit better designed here, a
[05:44:48] little bit better grouped as well by
[05:44:50] fixing some of these typos. Well, here I
[05:44:53] could try to match on to maybe
[05:44:56] imaginative. That seems like a long
[05:44:58] enough word that it could be useful for
[05:44:59] me here. So I'll say something like
[05:45:01] select not select I'll do update votes
[05:45:05] and set the title equal to imaginative
[05:45:09] landscape.
[05:45:11] Now I want to match any rows that have a
[05:45:14] title like imaginative space percent end
[05:45:20] quote semicolon. Now I'll match any
[05:45:23] title that has imaginative as a full
[05:45:26] word at the very beginning of this
[05:45:29] phrase. This is I would say a better
[05:45:31] query than FA because FA could match
[05:45:34] much more than this painting name here.
[05:45:36] If we have only one painting that begins
[05:45:39] with imaginative, this could work for us
[05:45:41] now. So I'll try this. I'll say enter.
[05:45:44] And now let me rerun the query
[05:45:47] group by. And we're so close. There's
[05:45:50] still one more imaginative landscape. So
[05:45:53] for this one, I might just need to
[05:45:55] manually update that piece. I could say
[05:45:58] let's do update votes and set title
[05:46:02] equal to in this case imaginative
[05:46:05] landscape where of course the title
[05:46:08] currently is imaginative landscape
[05:46:11] without the a in there. Now I'll hit
[05:46:13] semicolon to run this query. I'll show
[05:46:15] you the results. And now I think we're
[05:46:18] really almost there. There's only one
[05:46:20] more to do. Profusion of flowers. Let's
[05:46:22] fix that one. Now I could say select
[05:46:26] votes not not select update I'm always
[05:46:28] updating here update votes and then we
[05:46:31] want to set the title column to be equal
[05:46:35] to profusion
[05:46:37] profusion of flowers like this then
[05:46:42] where the title is like in this case
[05:46:45] profusion at the beginning notice how I
[05:46:48] can't use profusion space and then
[05:46:51] percent afterwards because we have one
[05:46:53] title that is literally just profusion
[05:46:56] plain and simple. No spaces afterwards,
[05:46:58] no spaces at the beginning. To match
[05:46:59] that, I should just say profusion at the
[05:47:02] beginning. Now I can hit enter. And if I
[05:47:05] do my usual query to show you the group,
[05:47:07] the votes group by title, I see I'm
[05:47:10] finally at my correctly formatted data
[05:47:13] set. Farmers working at dawn has six
[05:47:15] votes. Imaginative landscape has five
[05:47:18] and so on down the row. So here we've
[05:47:21] seen update being used not just to
[05:47:24] associate artists with new paintings but
[05:47:26] also to clean our data to make sure we
[05:47:28] can actually tally votes up in a way
[05:47:31] that's consistent and clean in this
[05:47:33] case. What questions do we have on
[05:47:36] update? Now
[05:47:40] let's go to Vixay.
[05:47:42] >> Yes. So uh what I wanted to ask is if
[05:47:44] there is a specific function for like
[05:47:46] lower case. So there's a there's a
[05:47:48] function for upper and there are the one
[05:47:50] for like all lowercase.
[05:47:52] >> Yeah, a good corresponding question
[05:47:54] here. We used upper, but is there lower?
[05:47:56] Turns out there is a lower function.
[05:47:57] It's spelled um L O W E R and is an all
[05:48:00] lower case like upper was. So I could
[05:48:02] use that as well. There is a whole list
[05:48:04] of what SQLite calls these scalar
[05:48:07] functions. Functions that take in some
[05:48:09] set of values and return to you some
[05:48:11] modified version of those values. So if
[05:48:13] you do some googling look for SQLite
[05:48:15] scalar functions you can find all those
[05:48:17] functions in one place in the SQLite
[05:48:20] documentation.
[05:48:22] Let's take one more question here. Let's
[05:48:24] go to Rupender.
[05:48:25] >> So yeah my question is so instead of
[05:48:28] updating all the titles is it possible
[05:48:31] to create a new column with the four
[05:48:33] categories that we want to have
[05:48:36] actually.
[05:48:37] >> Yeah I could see that working too. So
[05:48:39] there's a few ways to fix this data. You
[05:48:40] could for imagine adding a new column
[05:48:44] and maybe you assign values to the rows
[05:48:47] in that column based on what you see in
[05:48:50] the um title that they've given you. So
[05:48:52] if you can match something like
[05:48:54] imaginative and you'd know that all your
[05:48:56] paintings associated with imaginative
[05:48:58] have the same title, you could group
[05:49:00] them into the one category, the two
[05:49:02] category and so on. Um here you wouldn't
[05:49:04] be modifying those titles. you just be
[05:49:06] trying to strategically apply different
[05:49:09] categories which could also work as a
[05:49:11] solution here too. So good thinking.
[05:49:14] Okay, so we've seen now how to insert
[05:49:17] data, how to update data and previously
[05:49:20] how to delete data. What we can still do
[05:49:23] though are learn how to have other SQL
[05:49:27] uh command other SQL statements that can
[05:49:29] run after we make our very own SQL
[05:49:31] statements as well. We'll come back and
[05:49:33] talk about these things called triggers.
[05:49:36] And we're back. So, we've seen now a
[05:49:39] whole collection of ways to write data
[05:49:41] to a database. We've seen how to insert
[05:49:44] data, how to update data, and even
[05:49:47] delete data. What we'll see now, though,
[05:49:49] is this idea of a trigger, a way of
[05:49:51] writing a SQL statement to run in
[05:49:54] response to some other SQL statement
[05:49:56] like an insert, an update, or a delete.
[05:50:00] Let's consider our museum yet again. And
[05:50:04] let's say they have a schema a bit like
[05:50:07] this one. Now they have items in their
[05:50:09] collections, but they also have a
[05:50:12] transactions table. Now, wouldn't it be
[05:50:14] nice if whenever I deleted something
[05:50:17] from the collections table, it would
[05:50:19] show up in transactions as sold, having
[05:50:23] been sold from the museum's collections.
[05:50:25] Well, I could use a trigger to do just
[05:50:27] that. Let's see it visually first
[05:50:29] though. I'll say let's try to delete
[05:50:32] spring outing from our collections
[05:50:34] table. Well, if I do that, I could
[05:50:37] pretty easily do it with delete from.
[05:50:39] Right now, it's no longer part of my
[05:50:41] database. But if I have created a
[05:50:43] trigger to run and insert whenever I
[05:50:47] hear or have listened to a a delete on
[05:50:50] my collections table, I could then see
[05:50:52] that same title in my transactions table
[05:50:56] as sold all automatically.
[05:51:00] Let's think too maybe the museum
[05:51:02] acquires some piece of artwork. Maybe
[05:51:04] they actually add something new to their
[05:51:06] collection. We want that to show up in
[05:51:08] our transactions as well with the action
[05:51:11] of bought. Well, let's try it. I could
[05:51:13] probably add a new row here. I could say
[05:51:16] let's add pianies and butterfly to my
[05:51:19] collection here. Now, if I have the
[05:51:22] appropriate trigger, I could run an
[05:51:24] insert into on transactions
[05:51:27] automatically that would insert this
[05:51:29] same title with the action of bought,
[05:51:32] thereby keeping a log of all of our sold
[05:51:35] pieces of artwork and all of our bought
[05:51:37] pieces of artwork. Now, to create what
[05:51:40] we're calling a trigger here, we can use
[05:51:42] the following syntax. I could say first
[05:51:46] create trigger and then some name. So I
[05:51:50] tend to give triggers names to identify
[05:51:52] them among all of my database schemata
[05:51:54] like my tables and so on. Here after I
[05:51:58] say create trigger I have to specify
[05:52:01] should this trigger this statement run
[05:52:03] after or before some other SQL
[05:52:07] statement. Let's keep going with before
[05:52:09] here. Maybe it runs before an insert on
[05:52:13] some table. That's fine. It could also
[05:52:16] run before an update of a column on some
[05:52:20] table. It could even run before a delete
[05:52:24] on some table. And then keep in mind
[05:52:26] this could be before or after any of
[05:52:28] these kinds of SQL statements. In this
[05:52:30] case we have insert, update and delete.
[05:52:35] Now after we say this, we should say too
[05:52:37] is for each row. for each row means that
[05:52:41] if I were to maybe delete multiple rows,
[05:52:45] I should run my SQL statement for each
[05:52:48] row that I delete. If I delete two rows,
[05:52:51] I should run this statement coming soon
[05:52:54] two times. Okay, so now we've set up our
[05:52:58] trigger, at least kind of the data, the
[05:53:00] the the setup for it here. What we
[05:53:03] haven't done yet is specified what
[05:53:05] statement should run whenever we see a
[05:53:08] delete on particular table. Well, let's
[05:53:11] try this here. I could say begin. Begin
[05:53:14] means here comes my statement I want to
[05:53:16] run whenever I hear a delete on this
[05:53:19] table. Now I'll write that query down
[05:53:23] below that statement inside my begin.
[05:53:25] And I'll finish it off with an end to
[05:53:27] say this is the end of my statement. And
[05:53:30] my entire trigger looks like all of this
[05:53:32] lines of code here to say listen for a
[05:53:35] delete and run this statement in here
[05:53:38] for each row that I delete or update or
[05:53:41] insert.
[05:53:42] So let's try actually implementing in
[05:53:45] this case the museum's collections where
[05:53:47] they're trying to sell or buy pieces of
[05:53:50] artwork and automatically add them to
[05:53:52] their transaction table whenever they
[05:53:53] create or delete some piece of data from
[05:53:56] their collections. go back to my
[05:53:58] terminal here. Let me pull up a
[05:54:01] database. I'll do SQLite 3 MFA. DB. And
[05:54:05] you'll notice that this is the same
[05:54:07] schema that we've had before. We have
[05:54:09] collections, artists, and the created
[05:54:12] table. What's missing here though is our
[05:54:15] transactions table. So, let me make that
[05:54:17] for us here. I'll say let me go create
[05:54:20] table transactions. And now let me give
[05:54:24] it an ID column of type integer.
[05:54:28] Now I'll also give it a title column as
[05:54:31] we saw before called text. It's in this
[05:54:33] column I'll store the title of the piece
[05:54:35] we either bought or sold. Now let me
[05:54:39] also include the action column also of
[05:54:42] type text to say whether we bought or
[05:54:45] sold this piece. Okay. Finally, I'll
[05:54:48] make the ID column my primary key. And
[05:54:52] if I say semicolon here and hit enter, I
[05:54:56] now have created this table. So if I say
[05:54:59] dots schema, notice how I can now see my
[05:55:01] transactions table down below and I'm
[05:55:04] safe to run insert on this table to add
[05:55:08] some data to it. Well, let's try now
[05:55:11] creating our very first trigger. We're
[05:55:14] going to try to create a trigger that
[05:55:16] whenever an item is deleted from our
[05:55:17] collections table, we actually add it to
[05:55:20] our transactions table with the action
[05:55:22] of sold, meaning we sold this particular
[05:55:24] item. So let me say create trigger as we
[05:55:27] saw before and give it some name to
[05:55:30] identify it. I'll call this one sell.
[05:55:33] Now I'll say I want to run this trigger
[05:55:36] before I delete on the collections
[05:55:39] table. So before I run the delete query
[05:55:43] on my collections table, I want to run
[05:55:46] this statement instead. I'll say for
[05:55:50] each row begin, I want to now give you
[05:55:54] some statement to run for each row that
[05:55:56] I delete from collections. Let's make it
[05:55:59] this query here. I'll do one, two,
[05:56:01] three, four spaces to indent and make
[05:56:04] sure this is clearly the query I want to
[05:56:06] run after I uh run the delete on
[05:56:09] collections. I'll say I want to insert
[05:56:13] into transactions and I want to insert
[05:56:15] into the title and action columns. What
[05:56:20] value should I insert? Well, I should
[05:56:22] insert the old title. And actually in
[05:56:25] triggers, you get access to this keyword
[05:56:28] called old. This is the title that we've
[05:56:31] just deleted from our collection. So,
[05:56:34] old.title
[05:56:35] gives me access to the old row, the row
[05:56:38] we deleted, it's title column in
[05:56:40] particular. Now, let me add in the
[05:56:43] action which is just plain and simple
[05:56:45] sold. So, this is the query to run
[05:56:48] before I delete on collections. I will
[05:56:51] take the title of the row I'm about to
[05:56:53] delete and insert it into transactions
[05:56:56] along with the action sold. Let me type
[05:56:59] a semicolon here to say this is my
[05:57:00] entire query. Hit enter again. And now I
[05:57:03] can end that particular statement I want
[05:57:06] to run after I hear a delete on
[05:57:08] collections. So I'll hit enter now and
[05:57:11] let me type dot schema. I can actually
[05:57:14] see this trigger is part of my schema. I
[05:57:18] can see create trigger cell before
[05:57:20] delete on transactions underneath the
[05:57:23] transactions table.
[05:57:25] Okay, let's try putting this into action
[05:57:28] here. Let me try actually deleting
[05:57:29] something from our collections table.
[05:57:31] I'll say delete from collections where
[05:57:34] the title equals profusion of flowers. I
[05:57:38] want to sell this particular piece of
[05:57:39] artwork from our collection. I'll hit
[05:57:41] semicolon here. And now nothing seems to
[05:57:45] happen as usual. But if I select star
[05:57:48] from collections
[05:57:50] from collections,
[05:57:52] I see that piece is gone. It's no longer
[05:57:55] in here. And if I select star from
[05:57:58] transactions, select star from
[05:58:01] transactions,
[05:58:02] I actually see it's been sold. So
[05:58:05] automatically I added profusion of
[05:58:07] flowers with the action of sold to my
[05:58:09] transactions table. I did not type
[05:58:12] insert myself. I instead created a
[05:58:14] trigger to run this statement. Insert
[05:58:17] into whenever I deleted on collections.
[05:58:21] Let's try one more. We want to not to be
[05:58:23] able to sell artwork but also add it to
[05:58:26] our collection by buying it. So I could
[05:58:29] create a trigger called buy. Let me type
[05:58:32] create
[05:58:33] trigger buy. And now I want to run this
[05:58:38] statement forthcoming after an insert on
[05:58:43] collections. So I want to first insert a
[05:58:47] new item to collections. And when I do
[05:58:50] after I do I want to run this query
[05:58:52] coming next. Now I want to for each row
[05:58:57] begin the statement I want to run. So as
[05:59:00] we said before I want to insert into the
[05:59:03] transactions table. I want to insert
[05:59:05] into the title and action columns just
[05:59:08] like this. Now I want to insert some
[05:59:12] values. The values I want to insert well
[05:59:15] I want to insert the new title the new
[05:59:18] row I've just added. So in addition to
[05:59:20] old we also have new when I'm top when
[05:59:23] I'm using a trigger on an insert. So
[05:59:25] I'll say new.title title where again new
[05:59:29] is the new row or rows I'm inserting and
[05:59:32] thetitle is their column is a column
[05:59:35] called title. Now here I'll say the
[05:59:38] action was bought. We bought this
[05:59:40] artwork. I'll hit semicolon here and now
[05:59:43] I'll say end to say this is the end of
[05:59:45] my statement I want to run for every row
[05:59:48] I insert on collections. Let me hit
[05:59:51] enter here. I've created this trigger. I
[05:59:53] can type schema to see it in my actual
[05:59:56] schema.
[05:59:58] Now let's try inserting. I'll say insert
[06:00:01] into collections.
[06:00:03] I want to insert into the title and
[06:00:06] accession number as well as the acquired
[06:00:09] columns. Here I want to insert some new
[06:00:12] artwork. Maybe I sold profusion of
[06:00:14] flowers but now I want to just buy it
[06:00:16] back. So I'll say I'll insert profusion.
[06:00:19] Profusion of flowers is the title. The
[06:00:22] accession number was 56.257.
[06:00:27] And the date we acquired it, well, that
[06:00:29] was in 1956412.
[06:00:33] Let's hit semicolon here. Now I'll
[06:00:36] insert and I'll say select star from
[06:00:39] collections.
[06:00:40] I should see profusion of flowers back
[06:00:43] in my table. Now though, if I say select
[06:00:47] star from transactions, select star from
[06:00:49] transactions, I should see I previously
[06:00:53] sold provision of flowers and later
[06:00:55] bought it back. So again, I didn't run
[06:00:58] this insert myself. I instead triggered
[06:01:01] it by making my very own insert on the
[06:01:04] collections table. So this is the power
[06:01:07] of triggers to be able to run statements
[06:01:09] that I myself didn't create in response
[06:01:12] to statements that I actually did. So
[06:01:15] let me ask here what questions do we
[06:01:18] have on these triggers and what they can
[06:01:20] do for us?
[06:01:23] Let's go to Simon. I'd like to know um
[06:01:27] uh if uh there are only there is only
[06:01:31] one SQL query that uh that you can write
[06:01:34] in trigger
[06:01:36] or multiple queries.
[06:01:38] >> Yeah. So we saw begin and end in our
[06:01:41] triggers here where begin indicates the
[06:01:43] start of our statement and end indicates
[06:01:45] the end. You actually can have multiple
[06:01:48] statements inside of the begin and end
[06:01:50] separated by of course that usual
[06:01:52] semicolon that we have.
[06:01:55] Okay. So, one final idea here that we're
[06:01:58] getting at, we're kind of touching out
[06:01:59] with this transactions table is this
[06:02:01] idea of having a soft deletion. So, when
[06:02:05] I dropped something from my collections
[06:02:08] table, it actually ended up in my
[06:02:11] transactions table. So, it wasn't fully
[06:02:14] deleted in the sense that I'm keeping a
[06:02:16] record of it somewhere else. There's
[06:02:18] also one more way among many others to
[06:02:21] implement this idea of soft deletions.
[06:02:23] that is not quite fully deleting
[06:02:25] something from my database, but instead
[06:02:26] keeping it around with a log that we've
[06:02:28] removed it in some way. Let's look at
[06:02:30] this table here. I have collections, but
[06:02:33] I also have this column called deleted.
[06:02:37] And by default, the value here will be
[06:02:40] zero. That is, by default, I'll add some
[06:02:44] artwork to my collections table and
[06:02:46] deleted will be zero. If I want to
[06:02:50] delete a piece of artwork though, what
[06:02:52] could I do? Instead of deleting it fully
[06:02:55] from my table, removing the row, I could
[06:02:58] mark it as deleted. I could change the
[06:03:00] deleted column from a zero to a one.
[06:03:02] Let's say I want to delete farmers
[06:03:04] working at dawn. Instead of writing
[06:03:06] literally delete from collections where
[06:03:08] title equals farmers working at dawn, I
[06:03:10] could say update the deleted column of
[06:03:13] collections where the title is farmers
[06:03:15] working at dawn and make it not zero but
[06:03:18] one. Now I've marked this item as
[06:03:21] deleted. I could run a query that
[06:03:23] excludes deleted items, but this row is
[06:03:27] still around in my table. So let's try
[06:03:30] implementing this idea of a soft
[06:03:32] deletion inside of our collections
[06:03:34] table. so that we don't lose records of
[06:03:37] things we've actually had in our
[06:03:39] collection. I'll come back to my
[06:03:41] computer here and let's work on altering
[06:03:44] our table for collections here. If I
[06:03:47] type dots schema collections schema
[06:03:51] collections, you should see I have the
[06:03:54] table collections and also the triggers
[06:03:57] associated with it. What I don't have
[06:03:59] yet in collections. If I go over here
[06:04:01] and show you, I don't have a deleted
[06:04:04] column. I have ID, title, accession
[06:04:07] number, and acquired, but I don't have
[06:04:09] deleted. So, as we learned last week, we
[06:04:13] can use alter table to add a column to
[06:04:16] our collections table and by default
[06:04:18] make the value zero. So, let's try that.
[06:04:21] I'll go back to my environment and now
[06:04:24] I'll run alter table. I might say alter
[06:04:29] table and a table I want to alter which
[06:04:32] is collections. Now I want to add the
[06:04:35] column deleted deleted to collections
[06:04:39] and I want to make this type integer
[06:04:41] should store whole numbers whether
[06:04:42] positive or negative and the default
[06:04:45] value will be zero in this case. Now
[06:04:48] I'll hit enter. And if I type dots
[06:04:51] schema collections, I should see I have
[06:04:54] my very own deleted column inside of
[06:04:58] collections. If I type for instance
[06:05:00] select star from collections
[06:05:04] from collection semicolon, I'll see that
[06:05:07] by default all of these values are zero
[06:05:09] in my new deleted column.
[06:05:12] So instead of trying to delete,
[06:05:15] literally delete from collections, I
[06:05:18] could instead just update it. I could
[06:05:19] say take the updated column and flip it
[06:05:22] from a zero to a one. Let me try update
[06:05:25] collections and set the deleted the
[06:05:29] deleted column equal to one where let's
[06:05:33] say the title equals farmers working at
[06:05:37] dawn. And my query wraps here, but it
[06:05:39] should still work just fine. I'll hit
[06:05:41] semicolon enter. Now I didn't use delete
[06:05:45] from I used update. If I select star
[06:05:48] from collections semicolon here I'll see
[06:05:52] well farmers working at dawn is in this
[06:05:54] table but technically at least we marked
[06:05:57] it as deleted. So it seems now I don't
[06:06:02] want to use just select star from
[06:06:04] collections to see what's inside my
[06:06:06] collection. I want to apply a filter to
[06:06:08] remove those that have a deleted value
[06:06:11] that's not equal to zero. Let's try
[06:06:14] this. I'll say select star from
[06:06:17] collections
[06:06:18] where deleted does not equal one. If I
[06:06:22] hit semicolon here, what do I see? Only
[06:06:26] those values that are not deleted. I
[06:06:30] could go ahead and find them. I could
[06:06:31] say maybe select star from collections
[06:06:35] where deleted actually is one or deleted
[06:06:39] equals one like this. And now I see all
[06:06:42] those rows that I marked as deleted.
[06:06:45] Now this has some advantages. One of
[06:06:48] them is we keep data around. We don't
[06:06:50] actually formally delete it. We can
[06:06:52] still recover it later on. But it also
[06:06:54] has some tricky ethical questions too.
[06:06:57] Like it's okay if we're talking about
[06:06:58] artwork here, but if you're talking
[06:07:00] about user data, is it right to only
[06:07:03] soft delete it if they ask you to delete
[06:07:05] it? And particularly in conversation
[06:07:06] with um new frameworks like GDPR and the
[06:07:10] right to be forgotten and so on. It's up
[06:07:12] to you as a programmer to make the right
[06:07:14] decision here. When should you find data
[06:07:15] that's sensitive enough and actually
[06:07:16] delete it or when is it better to just
[06:07:19] soft delete it and keep it around in
[06:07:20] case you need it for later.
[06:07:23] So we'll end here on this note where if
[06:07:26] I say select star from collections and I
[06:07:29] want to find those only where deleted is
[06:07:32] not equal to zero like this or not equal
[06:07:36] to one. This gives me back all of the
[06:07:38] items that are not deleted. But wouldn't
[06:07:41] it be nice if I could actually run a
[06:07:44] query on some brand new temporary table
[06:07:47] that actually only will ever have those
[06:07:50] items that are not soft deleted. Turns
[06:07:52] out we can do that with an idea called
[06:07:54] views. And we'll see those in much more
[06:07:56] depth next week. We'll see you then.
[06:08:01] [Music]
[06:08:18] Well, hello one and all and welcome back
[06:08:21] to CS introduction to databases with
[06:08:23] SQL. My name is Carter Zeni and up until
[06:08:26] now you've been learning how to design
[06:08:29] databases and how to add data to them
[06:08:31] like how to insert, update, and delete
[06:08:34] some values all together. Now along the
[06:08:36] way we've added some complexity that is
[06:08:38] we went from one table to multiple and
[06:08:41] we had relationships too among all those
[06:08:43] tables as well. Now what we'll introduce
[06:08:46] today is a way to simplify some of that
[06:08:48] complexity and give you a way to see
[06:08:51] your data all the more clearly. This
[06:08:53] tool called a view. Now we'll begin with
[06:08:56] a familiar data set this data set of
[06:08:59] books. And we learned about this data
[06:09:00] set of books back in week zero. If you
[06:09:03] remember, we had a table of 78 books
[06:09:05] that had all been nominated for the
[06:09:07] International Booker Prize. It was a
[06:09:10] single table just of these books. Now,
[06:09:13] quickly in week one, we introduced more
[06:09:15] than just this single table. We actually
[06:09:17] had multiple tables. A table for books,
[06:09:20] a table for authors, for example, and
[06:09:22] also some relationship between those
[06:09:25] authors and those books. We said that an
[06:09:28] author could write not just one book but
[06:09:31] multiple books and similarly a book
[06:09:34] could be written by not just one author
[06:09:37] but multiple as well. This is what we
[06:09:39] called a many to many relationship. Now
[06:09:42] we also saw this not just visually but
[06:09:45] in our database in terms of tables as
[06:09:47] well. We had this kind of schema where
[06:09:51] we had a table for authors, a table for
[06:09:53] books, and then a table in the middle to
[06:09:56] talk about the relationship between
[06:09:58] authors and books. Which author wrote
[06:10:01] which book? We could see this in the
[06:10:03] authored table. Looking at these IDs
[06:10:06] here. And now to recap, if I wanted to
[06:10:09] find the book that Han here has written,
[06:10:12] let me ask how could I do that? How
[06:10:15] could I find the book that Han in the
[06:10:18] author's table has written over here in
[06:10:21] the books table? And feel free to raise
[06:10:24] your hand.
[06:10:25] >> By looking at the author ID, 31.
[06:10:28] >> Nice. So start by looking at the author
[06:10:30] ID. That's a great idea. So here we see
[06:10:32] that Han's author ID is 31. And we could
[06:10:35] make this link between the author's
[06:10:37] table and the authored table. So I'll
[06:10:39] highlight this here so we can see it
[06:10:41] visually. Han has the ID 31. And here in
[06:10:44] the author table we see the author ID of
[06:10:47] 31 next to actually some book ID. This
[06:10:51] book ID is 74. Well, what book has that
[06:10:54] ID 74? Turns out it's the white book all
[06:10:57] the way over here. Now this is adding
[06:11:02] some complexity to our queries. If I
[06:11:04] want to find who wrote what book, I have
[06:11:07] to go through the author's table, then
[06:11:09] the authored table, and then the books
[06:11:11] table. That's just a lot of steps to go
[06:11:13] through. And we could though try to
[06:11:16] simplify this to have a better view of
[06:11:19] this data to see it with just a single
[06:11:22] column for authors and a single column
[06:11:24] for titles. So let's try to visualize
[06:11:27] this together. What I might do first is
[06:11:30] try to flip around this primary key of
[06:11:32] authors, this ID column. Let's put it
[06:11:34] closer to the author table just
[06:11:36] visually, metaphorically here. Now I
[06:11:39] might see that these ids line up one to
[06:11:43] another. And we saw in a previous
[06:11:45] lecture that I could use a join in SQL
[06:11:48] to put these tables into a single table.
[06:11:52] And what a join does if you remember is
[06:11:54] take the primary key in one table and
[06:11:57] the foreign key in another and just find
[06:12:00] which ones match to put the rows of each
[06:12:02] table together. A bit like touching your
[06:12:03] fingertips together like this. So I'll
[06:12:06] then visually move these together, join
[06:12:08] these tables into a single table. And
[06:12:11] notice how if I now just get rid of
[06:12:13] these IDs metaphorically, just visually
[06:12:16] here, I now have a much more simple
[06:12:19] table, a simple view of this data. And
[06:12:22] if I want to find which book Han has
[06:12:25] written, well, I could do that. Look at
[06:12:26] a single row here. Look at the name
[06:12:29] column and then the title column here.
[06:12:33] Now what we're doing by creating this
[06:12:36] new view of our data set is actually
[06:12:39] creating well a view and a view is
[06:12:42] defined by this here a virtual table
[06:12:45] that is itself defined by a query. Now
[06:12:48] what does this mean? What is a virtual
[06:12:50] table? What is a query? Let's go back a
[06:12:52] few steps and see this in action. So we
[06:12:55] started with in this case three tables
[06:12:57] authors, books and authored. And
[06:13:00] presumably there's some query here that
[06:13:03] gets us from point A, these three
[06:13:05] tables, to point B, this single table.
[06:13:09] That query might involve some selects,
[06:13:11] some joins we talked about earlier. But
[06:13:13] there's some query we can write to get
[06:13:15] us from point A to point B. And notice
[06:13:19] here that the result of this query is
[06:13:22] itself a table. Like this has rows and
[06:13:26] columns. And what we can do is see all
[06:13:29] of those in terms of a table we could
[06:13:31] later on query. So a view is a way of
[06:13:35] writing some query to see our data in a
[06:13:38] new way and then saving this view of our
[06:13:42] data so we can query it later on.
[06:13:46] Now why might you want to build a view?
[06:13:48] Well, you might want to do it for a few
[06:13:50] reasons here. You could use it to
[06:13:52] simplify your data as we just saw here.
[06:13:54] You could use it to aggregate your data
[06:13:56] to try to sum up some values and store
[06:13:58] that in a single table. You could use it
[06:14:01] to partition your data or divide it into
[06:14:03] logical pieces. And you could even use
[06:14:05] it to secure your data to perhaps hide
[06:14:08] some columns you don't want somebody to
[06:14:10] see. There are more reasons too to use
[06:14:13] views, but we'll focus on these for
[06:14:15] today. And let's begin by focusing on
[06:14:18] simplifying. So we saw earlier a way to
[06:14:21] simplify these multiple tables down in
[06:14:24] to one. If I go back here, we'll see we
[06:14:27] got from this set of three tables to a
[06:14:30] single table that had both author names
[06:14:33] and author titles. So let's see here
[06:14:36] exactly how much we're reducing
[06:14:39] complexity by trying out different
[06:14:41] queries and then adding in a view to see
[06:14:44] all the benefits of this new view we
[06:14:46] have here. So we'll go back and we'll
[06:14:48] see in this case our three tables
[06:14:50] authors books and authored and let's say
[06:14:54] I want to find the books a particular
[06:14:56] author has written. I could write a
[06:14:58] query to do just that. Let's go back to
[06:15:00] SQLite here to run that query ourselves.
[06:15:04] I'll come back to my computer here in
[06:15:06] SQLite and my goal will be to find which
[06:15:09] author wrote which particular books. So
[06:15:11] if I go to my database here, I can go to
[06:15:14] my terminal and type SQLite 3 long list.
[06:15:17] DB to reopen this database. And now I
[06:15:21] should see if I type schema all the
[06:15:23] tables that are inside of it. I have a
[06:15:25] table for authors. If I scroll up a
[06:15:27] little bit, a table for books and a
[06:15:29] table for authored, that is
[06:15:31] relationships between authors and books.
[06:15:35] Now, let's say I want to write a query
[06:15:38] to find which books Fernanda Melor
[06:15:41] wrote. Well, I probably first need to
[06:15:43] find Fernandanda's ID as we just saw
[06:15:46] visually in our earlier example. So,
[06:15:49] let's find Fernandanda's ID. I could say
[06:15:51] select let's say ID from the author's
[06:15:54] table where the name equals Fernanda
[06:15:58] Melor. So, I'll say select ID from
[06:15:59] authors. Then where the name equals
[06:16:03] Fernanda Fernanda Melor semicolon. So it
[06:16:08] seems Fernanda's ID is 24. And I could
[06:16:12] use this ID in the rest of my query, but
[06:16:15] I could probably do better than this. I
[06:16:17] could use what we saw before something
[06:16:19] called a sub query to take this query I
[06:16:22] just wrote and put it inside some other
[06:16:25] one here. So let's take the next step
[06:16:28] and find the book ids that Fernando
[06:16:30] wrote. So let's try looking at the
[06:16:32] authored table for that which has author
[06:16:35] ids and book ids side by side. Okay,
[06:16:38] I'll say select in this case the book ID
[06:16:42] from the author table where in this case
[06:16:46] the author ID is equal to well I could
[06:16:48] say 24 but I want to do better. I could
[06:16:52] actually have a my very own subquery
[06:16:53] here to find Fran's ID dynamically. I
[06:16:56] could put uh parenthesis here, then hit
[06:16:58] 1 2 3 four spaces and say select ID,
[06:17:02] select ID from the author's table where
[06:17:07] the name equals Fernanda Melor, that
[06:17:10] same query from before. I'll close this
[06:17:12] out. Close out my sub query. And then if
[06:17:15] I hit enter, I should see now the book
[06:17:18] IDs that Fernanda has written. But
[06:17:21] there's still one more step here. What
[06:17:24] do I now need to do? I have book IDs
[06:17:27] that Fernando wrote. But how do you
[06:17:29] think I could find the titles from those
[06:17:33] book IDs?
[06:17:34] >> You could select the title from the
[06:17:36] books.
[06:17:37] >> Nice. We need to select title from that
[06:17:39] books table. So if you remember, we have
[06:17:41] titles inside of our books table, but we
[06:17:44] still need to link those titles through
[06:17:46] their ID to the book ids Fernanda has
[06:17:49] written. So let's do one last step here.
[06:17:52] I'll come back to my terminal and I'll
[06:17:54] write the query in full now. So I know I
[06:17:57] want to end up with titles. I'll say
[06:17:59] select in this case title from the books
[06:18:02] table. Now I want to find particular
[06:18:06] titles where the ID is in that list of
[06:18:09] books Fernanda has written. So I'll say
[06:18:12] where the ID is in some subquery, the
[06:18:17] query we actually just wrote. So let me
[06:18:19] write it again. I'll say 1 2 3 four
[06:18:21] spaces here to indent for style. Then
[06:18:24] I'll say select the book ID from the
[06:18:28] author table. in this case where the
[06:18:32] author ID is equal to some number in
[06:18:36] this case Fernand's ID. But what is
[06:18:38] Fernand's ID? Let's find out. I'll make
[06:18:41] another subquery here to find Fernand's
[06:18:44] ID indenting four times just for style
[06:18:47] here. Then I'll say select ID from the
[06:18:50] author's table and then again indent
[06:18:53] where the name equals Fernanda Melor.
[06:18:58] Then I'll close out all my queries to
[06:19:00] create this single long query to find
[06:19:03] all the books Fernanda has written. And
[06:19:06] again the order here is first find
[06:19:08] Fernandanda's ID, then find the book IDs
[06:19:11] associated with that ID, then find the
[06:19:14] titles associated with those book IDs
[06:19:17] themselves. Now I'll hit enter and I
[06:19:20] should see all those books that Fernanda
[06:19:23] has written. Now, as we talked about,
[06:19:26] this is a lot of complexity, a lot of
[06:19:28] tables to go through, and there's
[06:19:29] probably a better way to do this. Let me
[06:19:32] open up a new terminal and try out a
[06:19:34] different way of going about this. I'll
[06:19:36] make a new connection to my database.
[06:19:39] I'll make a new terminal and I'll say
[06:19:40] SQLite 3 long list. DB. Hit enter. Now,
[06:19:45] I should see that I have a brand new
[06:19:47] connection to my database. And I could
[06:19:50] try to find a better way to do this. Let
[06:19:54] me try to do what we did visually and
[06:19:56] like join these tables together. Well, I
[06:19:59] could try select name and title from the
[06:20:04] author's table. But notice how author's
[06:20:08] table doesn't have titles in it. It does
[06:20:11] have the name of the author, but it
[06:20:13] doesn't have book titles. So to get
[06:20:15] titles, I have to join in some new table
[06:20:18] here. I'll hit enter and I'll say join
[06:20:21] let's say the author table on author's
[06:20:26] dot id equals author do aauthor ID and
[06:20:32] all I'm doing here is saying I'll take
[06:20:35] first the author's table and then why
[06:20:38] don't I try to combine this table with
[06:20:40] the authored table linking it up by
[06:20:43] looking at the author's do ID column and
[06:20:46] the authorauthor ID column
[06:20:48] And visually, let's take a look at what
[06:20:50] we're doing here in this join. If I look
[06:20:52] at this in my slides here, I should see
[06:20:56] I started with my author's table here. I
[06:20:59] had names of those authors and I had an
[06:21:02] ID column in that author table. Now, I'm
[06:21:05] trying to join the author table by
[06:21:08] telling SQL that these two columns,
[06:21:11] author ID and ID, should align. They
[06:21:14] should line up like this. So, their rows
[06:21:16] are all together, but there's still one
[06:21:19] more step. I've joined the author table
[06:21:23] and the author table, but what's the
[06:21:26] next step to find book titles? I still
[06:21:30] have to join the books table. So, let's
[06:21:33] try that here. I'll come back over and
[06:21:36] instead of joining just the auth table,
[06:21:38] let me now try to also join let me hit
[06:21:42] enter to also join the books table. I'll
[06:21:46] join books on books.
[06:21:50] ID equals in this case authored dotbook
[06:21:56] ID. And to be clear, this line here
[06:22:00] means that what I'm trying to do is now
[06:22:03] join this books table which is over here
[06:22:07] with this author table aligning it so
[06:22:10] that their ids match up into a single
[06:22:12] row as we see here with 74 and 74 one
[06:22:16] and one and so on. I'll come back and
[06:22:19] now let me try this. come back over here
[06:22:23] and I'll just try hitting enter to see
[06:22:26] what I can see from this query.
[06:22:29] Okay, let me zoom out a little bit and
[06:22:31] you'll see I actually do have author
[06:22:35] names next to book titles all in one
[06:22:39] table just as we thought we would. So,
[06:22:43] this is useful to me. But what if I
[06:22:46] wanted to have this stored as a way to
[06:22:49] see my tables? I want to be able to
[06:22:52] query this kind of table I see right
[06:22:55] here. Well, for that I could try to
[06:22:58] introduce a view. Now, a view starts
[06:23:02] with a query as we just saw. I wrote a
[06:23:06] query to select names and titles from
[06:23:09] three different tables joining them
[06:23:11] together. But if I want to save the
[06:23:14] results of that query so I can query
[06:23:16] them later on, I could use this syntax
[06:23:19] here. create a view that has a name that
[06:23:23] I can give to it as this query down
[06:23:26] below here. So create view given some
[06:23:29] name as the result of this query gives
[06:23:32] me a view that is then saved and part of
[06:23:35] my schema. So let's try that here to
[06:23:38] create a view by which we can see both
[06:23:41] author and book titles side by side.
[06:23:44] I'll come back to SQL light here and I
[06:23:47] am already in this brand new terminal.
[06:23:50] So I could try to remake this view and
[06:23:54] save it now for later usage. I'll say
[06:23:57] create a view and call it long list. The
[06:24:00] same name we gave our single table back
[06:24:03] in week zero. Now I'll say this view is
[06:24:08] the result of this following query as
[06:24:12] let's say select name and title from the
[06:24:16] author's table but not just the author's
[06:24:19] table join let's say the author table
[06:24:23] join authorred on author's do ID equals
[06:24:28] author do aauthor ID and then join again
[06:24:34] our books table as we saw visually here.
[06:24:36] Join books join books on books dot id
[06:24:43] equals authored dotbook
[06:24:47] id. Now that is the query I used before
[06:24:50] to see author names and book titles side
[06:24:53] by side. If I create this as a view
[06:24:56] hitting semicolon and enter nothing
[06:24:59] quite happens. But now if I type dots
[06:25:03] schema and hit enter, I should see a
[06:25:06] view called long list that has two
[06:25:10] columns, name and title. And I actually
[06:25:12] see the query I used to create this
[06:25:15] view. So let me think now I want to see
[06:25:19] what's inside this view. And to query a
[06:25:22] view, I can use it exactly as I would a
[06:25:25] table. I could say select star from long
[06:25:29] list semicolon hit enter and now I
[06:25:32] should see author names and book titles
[06:25:35] side by side. So if I have this kind of
[06:25:40] table with authors and book titles side
[06:25:43] by side, what then does my query become
[06:25:46] to find the books written by Fernanda?
[06:25:49] Let me ask our audience here. What query
[06:25:52] could I use now on this view to find the
[06:25:56] books written by Fernanda?
[06:25:59] >> Thank you, Mr. Carter. We cannot query
[06:26:01] uh the book or the all of the books
[06:26:04] using her specific name.
[06:26:07] >> A good idea. I can use particular name
[06:26:09] in this case and perhaps just use a
[06:26:11] simple where. So let's try that here. I
[06:26:13] go back to my terminal and if I want to
[06:26:16] find the books written by Fernanda,
[06:26:18] well, I could just query for them in
[06:26:20] this single table that I created called
[06:26:22] long list or not really a table but now
[06:26:24] a view. I'll say in this case select the
[06:26:27] title from select title from long list
[06:26:32] where to Muhammad's point I could just
[06:26:34] say name equals Fernanda meernanda
[06:26:40] Melor semicolon. I'll hit enter here and
[06:26:43] I see those same books Fernanda has
[06:26:46] written. Paradus and Hurricane season.
[06:26:49] So let's see where we started here. We
[06:26:51] started with this kind of query long
[06:26:55] multiple lines many sub queries involved
[06:26:58] just to find the answer to which books
[06:27:01] Fernanda had written. Now though that we
[06:27:04] have a new view, I can simplify this
[06:27:07] query to just this here. select title
[06:27:10] from long list where the name equals
[06:27:13] Fernanda. And I can do all of this
[06:27:15] without using much if any more disk
[06:27:19] space. A view, remember, is a virtual
[06:27:21] table, not a real one. And I can then
[06:27:24] have the results organized like this,
[06:27:26] while still being in those underlying
[06:27:28] tables stored essentially elsewhere.
[06:27:32] So, let me ask what questions we have on
[06:27:35] how views can simplify
[06:27:37] our data. Um, can we then somehow
[06:27:40] manipulate the views to uh maybe order
[06:27:44] the results or display them just
[06:27:46] differently?
[06:27:48] >> A great idea. So, if I wanted to maybe
[06:27:50] order these books, I could absolutely do
[06:27:52] that in the same way I would do in a
[06:27:54] table. So, let me go back and show you
[06:27:56] how to do that. Let's say I want to
[06:27:58] organize these books alphabetically by
[06:28:01] title. So, if you remember using our
[06:28:04] regular old table, we could use order
[06:28:06] by. I could do the same thing here. I
[06:28:08] could say select both the name and title
[06:28:11] columns from my long list table. And now
[06:28:16] let me try to order by order by the
[06:28:19] title column in this case. And I'll hit
[06:28:21] semicolon. Now if I hit enter, I should
[06:28:25] see the book titles organized
[06:28:28] alphabetically. Now, the view itself
[06:28:31] does not have these titles automatically
[06:28:34] alphabetically sorted for me, but I
[06:28:36] could make it do that. If I had when I
[06:28:39] was making this view included order by
[06:28:41] let's say title at the end of that
[06:28:43] query, I would then have those titles
[06:28:46] saved in this view automatically as a
[06:28:50] toz. So very powerful if you want to not
[06:28:52] just find particular ways of seeing your
[06:28:54] data, but also organizing it or ordering
[06:28:56] it too.
[06:28:58] So with that note, we've seen how to
[06:29:01] simplify one example of having multiple
[06:29:04] tables down into one. We'll come back in
[06:29:06] just a few and see what we can aggregate
[06:29:08] data too, putting that data into a
[06:29:10] single table for us to see some
[06:29:12] statistics and such as well. Come back
[06:29:14] in a few.
[06:29:16] And we're back. So we just saw how to
[06:29:19] simplify some data, how to take multiple
[06:29:22] tables and see them as one. What we'll
[06:29:25] do now is think about how we can
[06:29:27] aggregate data. That is to take many
[06:29:29] individual data points and summarize
[06:29:31] them to find an average or a min or a
[06:29:34] max but see those results inside of a
[06:29:37] view. So if you remember in our long
[06:29:40] list database we had a table of ratings
[06:29:44] and in this case books had individual
[06:29:46] ratings from individual people. Like
[06:29:49] maybe I gave book ID one a four out of
[06:29:51] five stars, but David gave it only a
[06:29:54] three. Now we store these individual
[06:29:57] ratings in our database. But ultimately,
[06:30:00] I don't care so much what I rated it or
[06:30:02] maybe what David rated it. I care about
[06:30:04] the average rating, let's say, for each
[06:30:07] book. But if we care about those
[06:30:10] averages, why then would we store all
[06:30:13] the individual ratings? Let's think of
[06:30:15] this as a design question here. Can you
[06:30:17] think of a reason we might want to
[06:30:19] actually have these individual ratings
[06:30:21] stored in our database? What does that
[06:30:24] give us at the end of the day?
[06:30:26] >> Perhaps reliability to know uh how many
[06:30:29] persons rated a book.
[06:30:31] >> Nice. So, it's nice to have some more
[06:30:33] data. I could know how, let's say, I
[06:30:35] rated a book or how you rated a book.
[06:30:36] That's good here too. And I would argue
[06:30:38] that from having this additional data,
[06:30:41] we could compute more statistics. I
[06:30:44] could find not just the average rating
[06:30:46] but also the minimum rating or the
[06:30:48] maximum rating or the median rating and
[06:30:51] so on. So these individual results allow
[06:30:53] us to find and compute more statistics
[06:30:56] like averages, mins and maxes as opposed
[06:30:59] to just storing the average. Now if I
[06:31:03] wanted to find the average of these
[06:31:05] results, what could I do? Well, we saw
[06:31:07] before I could try to group ratings by
[06:31:11] individual book IDs. Let's say I want to
[06:31:13] find the ratings for book ID 1 and book
[06:31:16] ID 2. I could group by the book ID
[06:31:19] column, turning these into individual
[06:31:21] groups. And let's say I want to find the
[06:31:24] average here using a SQL query. I could
[06:31:27] say find me the average of the rating
[06:31:29] column when I have groups by book ID.
[06:31:33] that effectively takes my table like
[06:31:36] this and says, "Okay, I'll combine all
[06:31:39] the ratings for each individual book ID
[06:31:41] and find for you the average. I'll first
[06:31:45] kind of compress this data together,
[06:31:46] literally putting it maybe one on top of
[06:31:48] the other here. And then find the
[06:31:50] average of all those results. Let's say
[06:31:52] 3.67 for book one and 2.5 for book two."
[06:31:56] Kind of compressing all of our data into
[06:31:58] a single result. In this case, the
[06:32:00] average. So let's walk through then how
[06:32:03] we found the average using a SQL query
[06:32:06] and then we'll turn that into a view. So
[06:32:09] I'll come back over here to my computer
[06:32:12] and I'll open up long list db. I'm
[06:32:15] already here. So I can type dots schema
[06:32:18] ratings to see the schema for this
[06:32:21] ratings table. And you'll see it does
[06:32:23] have a book ID column and a rating
[06:32:26] column as well. So if I want to find the
[06:32:30] average rating for each individual book
[06:32:32] ID, what could I do? I could try to
[06:32:35] select the book ID column and the rating
[06:32:39] column like this. But I don't want to
[06:32:42] select just the rating column itself.
[06:32:45] That gives me individual values. I want
[06:32:48] to find the average rating instead. I
[06:32:52] could instead say find me the average
[06:32:54] rating from this table.
[06:32:57] Now let me give this a new name. I'll
[06:32:59] say as rating calling the average rating
[06:33:02] now newly in this case rating. And I'll
[06:33:05] select this from the ratings table. And
[06:33:08] finally I need to group by something. I
[06:33:11] need to group by book ID. That means
[06:33:15] I'll calculate the average rating for
[06:33:18] each book ID. I'll hit semicolon here
[06:33:21] and enter. And I should see all of these
[06:33:25] book IDs top to bottom with their own
[06:33:30] rating.
[06:33:31] But here it doesn't look so pretty. What
[06:33:35] could I do to try to make this not so
[06:33:37] long? Like 3.774019431.
[06:33:41] There's a better way to do this. And we
[06:33:43] saw it before. What could I do to
[06:33:45] enhance this view of my ratings table? I
[06:33:48] see some suggestions about rounding the
[06:33:51] ratings, but I was also going to suggest
[06:33:54] adding the book titles of course.
[06:33:57] >> Ah, good uh point here too. So, we first
[06:33:59] want to add the first want to probably
[06:34:01] add the book titles to see what titles
[06:34:03] we're talking about, not just in this
[06:34:04] case individual book IDs, but also a
[06:34:07] good point to say, let's try rounding
[06:34:09] these so we don't see 3.7740194.
[06:34:13] Let's try to round that maybe to two
[06:34:14] decimal places just to be safe. So let's
[06:34:17] first try rounding this and then we'll
[06:34:19] try adding in some book titles to your
[06:34:21] suggestion here. I'll come back over and
[06:34:24] let me just try rounding it first. So I
[06:34:26] will come back to my terminal and I'll
[06:34:29] say I want to find the average rating
[06:34:32] for each book ID and I want to select
[06:34:35] not just the average rating as we did
[06:34:37] before but the rounded average rating.
[06:34:40] So I can use round and say take the
[06:34:44] average rating and round it to two
[06:34:46] decimal places. And I'll call this
[06:34:48] column just rating in the final result.
[06:34:51] I'll select this from the ratings table.
[06:34:55] And now I can group by in this case book
[06:34:58] ID. Enter. I should see I have rounded
[06:35:03] ratings now. A little more pretty than
[06:35:05] before. Now to your point, let's try to
[06:35:08] add in not just book IDs but also book
[06:35:10] titles. Like what does it mean for a
[06:35:12] book ID to have some rating? I want to
[06:35:14] see titles here in the end. So let's do
[06:35:17] that. I'll say select book ID and also
[06:35:22] select title and maybe even select the
[06:35:25] year that book was nominated for the
[06:35:27] Booker Prize. I'll then select the
[06:35:30] rounded average rating to two decimal
[06:35:33] places as rating. And I want to select
[06:35:37] this from the ratings table from
[06:35:40] ratings. But what do you notice? If I
[06:35:43] were to select just from ratings, what
[06:35:46] data am I missing? And where could I
[06:35:49] find it?
[06:35:51] >> Hey, you're missing the titles from the
[06:35:53] books uh table. Yeah, I have to have
[06:35:57] titles and those are stored in the books
[06:35:59] table. So, what should we do? Probably
[06:36:00] just join in the books table matching up
[06:36:03] that primary key with some foreign keys.
[06:36:06] So, I'll come back over here and we'll
[06:36:07] do that. I want to select from ratings
[06:36:10] of course, but I also want to join in in
[06:36:12] this case the books table. So, I'll hit
[06:36:14] enter. And now I'll say join as well the
[06:36:18] books table. Now, how can I match up the
[06:36:21] books table with the rating table? Well,
[06:36:23] I know that the rating table has a
[06:36:26] foreign key called book ID and the book
[06:36:29] table has a primary key called ID. So,
[06:36:32] I'll tell SQL I want to match these two
[06:36:34] up a bit like this. I'll say join books
[06:36:37] on ratings.book
[06:36:40] ID, that foreign key that's inside of
[06:36:43] ratings equals in this case books.
[06:36:47] ID.
[06:36:49] Now, there's one more step which is to
[06:36:51] group by book ID. still. So, I'll hit
[06:36:54] enter and group by book ID, but now I
[06:36:58] should be able to hit semicolon and
[06:37:00] enter. And I should see not just book
[06:37:04] IDs, but now titles and the years those
[06:37:07] books were nominated as well. So, this
[06:37:10] view is getting better and better. And I
[06:37:13] might say we actually go ahead and just
[06:37:14] add this to our schema. We could create
[06:37:16] a view that returns to us the results of
[06:37:19] this query. So, let's try that. I'll say
[06:37:23] create a view called maybe average book
[06:37:26] ratings. Average book ratings for people
[06:37:29] to come in and do analysis on if they'd
[06:37:31] like. Then I could say um I want to
[06:37:34] create this view as that query we wrote
[06:37:37] before. So I'll say again select the
[06:37:40] book ID the um title and the uh let's
[06:37:45] say the year column the rounded average
[06:37:49] rating to two decimal places and then I
[06:37:54] want to select it as rating. I'll select
[06:37:56] this from the ratings table
[06:37:59] from ratings and then I'll join as we
[06:38:02] did before the book table from ratings
[06:38:04] and then join books on that primary key
[06:38:08] and that foreign key. So I'll say on
[06:38:11] ratings dotbook id that foreign key in
[06:38:15] ratings and set that equal to books ID
[06:38:19] that primary key we're going to use to
[06:38:20] join these tables together. Then I'll
[06:38:23] say group by book ID. And I should have
[06:38:26] if I hit enter my very own view called
[06:38:29] average book ratings that I can use to
[06:38:32] then see the averages for each of these
[06:38:34] books. I'll say select let's say star
[06:38:37] from average book ratings semicolon. And
[06:38:43] now I should see all of those results
[06:38:46] just as we had before. Now, notably,
[06:38:49] because this is in a view, I'm not using
[06:38:52] much if any additional space in my
[06:38:55] database. I still have underlying this
[06:38:58] view individual ratings. But because I
[06:39:01] saved this query and the results it
[06:39:03] created in a view, I can actually have
[06:39:06] access to the a rounded average ratings
[06:39:08] for each of these and I can query that
[06:39:10] view as well. So let me ask then what
[06:39:15] questions we have on how we've used
[06:39:17] views to aggregate some data so far.
[06:39:21] >> Actually I have a question can we use
[06:39:24] both uh uh same name like we before use
[06:39:29] long list and here we using for average
[06:39:32] something can we use long list for this
[06:39:35] both of them.
[06:39:37] >> Yeah. So if you remember before we had
[06:39:38] this view called long list and long list
[06:39:41] had book titles and authors inside of
[06:39:44] it. And I think you're asking could we
[06:39:47] try to join let's say the long list
[06:39:49] table with our ratings to get book
[06:39:50] titles and so on. We couldn't do that
[06:39:53] because we don't have the ID column in
[06:39:55] that long list view. Um we could though
[06:39:58] perhaps write some queries that involve
[06:40:00] that long list view as well.
[06:40:04] Okay, let's keep going here and seeing
[06:40:07] what advantages this view might give us.
[06:40:09] So, I'll come back over here. And one
[06:40:12] more advantage is that if I were to add
[06:40:14] in some new rating to my ratings column,
[06:40:18] I could just requery this view to find
[06:40:21] the updated average. So, let's say we
[06:40:23] use some insert into statement here and
[06:40:26] I update some books ratings. Well, if
[06:40:28] I'm a data analyst and I come back in a
[06:40:31] little later and I want to find the
[06:40:33] updated rating, I can do it just again
[06:40:35] by selecting from selecting star from
[06:40:38] average book ratings like this. Average
[06:40:42] book ratings. Hit enter. And now I see
[06:40:47] perhaps some updated averages as well.
[06:40:49] Every time I query this view, I'll rerun
[06:40:52] essentially that query from before. And
[06:40:54] now I'll see the updated averages for
[06:40:57] each book.
[06:40:59] Now sometimes as a data analyst I might
[06:41:02] want to create a view but not store it
[06:41:06] longterm as part of my schema. Like here
[06:41:09] if I type schema I see both our prior
[06:41:12] view called long list right here and I
[06:41:16] also see our average book ratings view.
[06:41:19] But if I am somebody who comes in and I
[06:41:22] maybe want to find the average book
[06:41:24] ratings not by each book but by each
[06:41:27] year I could do that but then not store
[06:41:30] that view long term. Maybe I don't want
[06:41:33] others to see this view or maybe it's
[06:41:35] just for my own u analysis on this given
[06:41:37] day. Well, to do that, I could move
[06:41:40] beyond just create view and I could also
[06:41:44] enhance this to be create temporary view
[06:41:47] where a temporary view exists only for
[06:41:50] the duration of my connection with
[06:41:53] database. So to be clear, that means if
[06:41:55] I type SQLite 3 long list db, I'm
[06:41:58] opening a connection to the database. If
[06:42:01] I then typequit,
[06:42:03] I would then lose that connection, quit
[06:42:05] that connection, and that view would no
[06:42:07] longer be there. So, let's try this.
[06:42:10] I'll come back to my terminal, and we'll
[06:42:12] create a temporary view that shows us
[06:42:14] the average ratings for the books by the
[06:42:16] year they were nominated, not by every
[06:42:19] individual book here. So I could try
[06:42:24] doing the same query from before like
[06:42:25] select um let's say the rating average
[06:42:28] rating select it from the ratings table
[06:42:30] join books and titles and so on but what
[06:42:33] do I have already to build on top of if
[06:42:36] I wanted to find a view that has a title
[06:42:41] a rating and even let's say the year
[06:42:44] that book was published what do I
[06:42:46] already have in my schema for that? Uh,
[06:42:50] so we could use the view that we just
[06:42:53] created.
[06:42:54] >> Yeah, nice idea. So we could actually
[06:42:56] use the same view we just created to
[06:42:59] create ourselves a brand new view. So
[06:43:01] just because something is a view doesn't
[06:43:03] mean we can't use it to then create
[06:43:04] another view as well. So we'll do
[06:43:07] exactly that. We'll come back over here
[06:43:10] and I can type uh dots schema to see I
[06:43:13] still have this view called average book
[06:43:16] ratings and in it I have book ids their
[06:43:20] title the year they were nominated and
[06:43:22] their average rating but now I want to
[06:43:24] find let's say the average rating for
[06:43:27] each individual year not for each
[06:43:29] individual book so what could I do I
[06:43:31] could say select the year column and the
[06:43:35] rounded average rating
[06:43:38] in this case from the rating column in
[06:43:43] average
[06:43:45] average book ratings and I'll wrap this
[06:43:48] query here. Let me zoom out so you can
[06:43:50] see it all online. Now I'll say I want
[06:43:53] to group by the year column. So here I'm
[06:43:57] now saying find me the average rating of
[06:44:00] each book of each book's average rating
[06:44:03] for each individual year. I'll hit enter
[06:44:06] and we should see if I zoom back in for
[06:44:09] 2018 we have 3.75 for 2019 we have 3.64.
[06:44:13] So this means that apparently in 2023
[06:44:16] the average rating for books that were
[06:44:18] long listed for the international booker
[06:44:20] prize was 3.78 and same for 2022 3.87
[06:44:24] 2021 was 3.69.
[06:44:26] So I have this new view here. I could
[06:44:29] store this temporarily inside of a view
[06:44:31] that I could use while I'm doing some
[06:44:33] analysis on this given day. So I'll say
[06:44:37] create a temporary view and I'll call
[06:44:40] this one average ratings by year. How
[06:44:44] were the books rated each individual
[06:44:46] year on average? And I'll say this is
[06:44:49] the query that I just did before. Select
[06:44:51] in this case the year and the rounded
[06:44:54] average rating to two decimal places as
[06:44:58] the rating column from average book
[06:45:02] ratings. That same view from before. Now
[06:45:06] I'm creating a view from my view. I'll
[06:45:10] group by here. Group by year. And then
[06:45:13] I'll hit enter. And I should see nothing
[06:45:16] popping up. But now if I wanted to query
[06:45:19] this view, I could say select star from
[06:45:22] average ratings by year and I'll see the
[06:45:26] results of that view.
[06:45:30] Now though, here's the catch and why
[06:45:32] it's temporary. If I were to typequit
[06:45:35] now.quit
[06:45:38] and try it again, SQLite 3 long list db.
[06:45:42] Oops, let me retype that. SQLite 3 long
[06:45:45] list.db.
[06:45:47] If I now try to select star from average
[06:45:52] ratings by year semicolon,
[06:45:55] I'll get no such table and really no
[06:45:58] such view. I don't have a view called
[06:46:00] average ratings by year anymore because
[06:46:02] this was temporary.
[06:46:05] So let me ask what questions do we have
[06:46:07] on temporary tables if any
[06:46:11] temporary views rather? Right. So thank
[06:46:15] you. So the the first thing that I notic
[06:46:17] is that it just you know helps us to do
[06:46:20] some kind of testing when we use you
[06:46:23] know temporary views. Basically you know
[06:46:26] uh the views will not be saved in the
[06:46:29] database. Uh but again it's just you
[06:46:32] know a good way to you know just to test
[06:46:34] the query whether it is usable or not.
[06:46:38] >> That's a great use case for them. And in
[06:46:40] general, if you are working on a
[06:46:42] database and you want to organize the
[06:46:44] data in some way, but you don't want to
[06:46:46] store that organization long term, a
[06:46:48] temporary view is great for that. If
[06:46:51] though you are a developer and you want
[06:46:54] to ingrain this view as part of your
[06:46:56] database, you might just use create
[06:46:58] view, plain and simple, to have it
[06:46:59] always be in your database for you
[06:47:01] wherever you connect to it and whenever
[06:47:03] you connect to it. Great question.
[06:47:06] Okay, let's keep going and let's
[06:47:08] introduce now something called a common
[06:47:10] table expression or a CT.
[06:47:14] And a common table expression is simply
[06:47:17] a view that exists for the duration of a
[06:47:19] single query. So a regular view, as we
[06:47:23] saw before, exists forever in my schema.
[06:47:26] A temporary view exists for a single
[06:47:29] connection, but a CTE exists for a
[06:47:32] single query. And the syntax looks just
[06:47:35] a bit different. With a CTE, I can write
[06:47:38] a single query, but at the beginning of
[06:47:40] that query, define the CTE, the common
[06:47:43] table expression. To do so, I would say
[06:47:46] with and give it some name as and then
[06:47:50] inside these parenthesis say the query I
[06:47:52] want to be this CTE here. I could then
[06:47:57] optionally follow it up with more CTE
[06:47:59] for this same query or I could omit the
[06:48:02] comma and then use just select from the
[06:48:05] name of my CTE up above. This is useful
[06:48:09] if you want to have some very temporary
[06:48:11] view that you don't want to store in
[06:48:13] your schema but you do want to use for
[06:48:16] this particular query. So let's see an
[06:48:19] example now recreating our average
[06:48:22] ratings by year but now using a CTE. So
[06:48:26] I'll come back to my computer and I'm
[06:48:29] already in my SQLite terminal. What I
[06:48:32] should do though is try to drop the
[06:48:34] prior view. I want to remove that view
[06:48:37] called average book ratings to create
[06:48:39] room to have now a CTE with that very
[06:48:42] same name. So I'll say drop view and the
[06:48:46] name of the view I want to drop average
[06:48:48] book ratings average book ratings
[06:48:53] semicolon and now I should see that that
[06:48:56] view is no longer in my schema. So I
[06:49:00] want to recreate though what we did
[06:49:02] before which was finding the average
[06:49:05] ratings of books year overyear. So let
[06:49:09] me try to write this query. But it would
[06:49:11] be handy if in that query I had access
[06:49:14] to a view that gave me the average
[06:49:16] rating for each book. So I'll write the
[06:49:18] query like this. I'll use a CTE and I'll
[06:49:21] say with average book ratings average
[06:49:26] book ratings as now this query I'll
[06:49:30] write now inside. And this query should
[06:49:33] be familiar. It's the same query we use
[06:49:36] to find the average rating for each
[06:49:38] book. I'll say here I want to select I
[06:49:42] want to select the book ID column, the
[06:49:46] title column, the year column, and the
[06:49:50] rounded average rating to two decimal
[06:49:54] places. Calling it rating calling it
[06:49:57] rating in this case from my ratings
[06:50:02] table like this.
[06:50:04] Now what do I need to do? I also need to
[06:50:07] you saw before join in my books table
[06:50:10] join books on the primary and foreign
[06:50:13] keys aligning. So I'll say the book ID
[06:50:18] column that foreign key in the ratings
[06:50:20] table should equal books. ID that
[06:50:24] primary key column in books. Then I will
[06:50:28] group by the book ID to find the average
[06:50:31] rating for each book. And now let me
[06:50:34] close out this CTE. I'll close my
[06:50:38] parenthesis. And because I'm only using
[06:50:41] one CTE, I don't need a comma. I can
[06:50:44] then just write the rest of my query.
[06:50:47] I'll hit enter for style sake. And now
[06:50:50] with this CTE called average book
[06:50:53] ratings, I want to find the average
[06:50:55] rating yearover-year grouping not by
[06:50:58] book but by year. So I'll say select in
[06:51:01] this case year and then select the
[06:51:04] rounded average rating still to two
[06:51:08] decimal places as a new rating column.
[06:51:12] Then I'll select this from in this case
[06:51:16] my CTE. So I'll hit enter here as well
[06:51:20] from average book ratings that same CTE
[06:51:25] I defined earlier in my query. Now
[06:51:28] finally to find the average rating
[06:51:30] across individual years I'll say group
[06:51:32] by year semicolon and now hopefully if I
[06:51:36] hit enter I should see the average
[06:51:40] rating for each year in my database.
[06:51:44] Okay, so the CTE is useful when you have
[06:51:48] sub queries you don't want to repeat or
[06:51:51] when you want to make a view that only
[06:51:53] exists for the duration of a query. And
[06:51:55] it's with all of these tools like views,
[06:51:58] temporary views, and CTE that we can get
[06:52:01] away with storing statistics about some
[06:52:03] data in our data set and not storing
[06:52:06] them uh in the actual um database, but
[06:52:09] only inside this view we might have
[06:52:11] here. we'll do next is see how we can
[06:52:14] use views to create not just these
[06:52:16] aggregations but also partitions of our
[06:52:19] data. A way to split our data up into
[06:52:21] logical pieces for use for our own sake
[06:52:24] or even for application sake as well.
[06:52:26] We'll come back in just a few. And we're
[06:52:29] back. So we've seen so far how to use
[06:52:32] views to simplify and also aggregate our
[06:52:35] data. What we'll see now though is how
[06:52:37] to use views to partition our data. that
[06:52:40] is to break it into smaller pieces that
[06:52:42] be useful to us or to some application.
[06:52:45] Now on the international booker prize
[06:52:48] website they have a page for each year
[06:52:51] of long listed books. But in our table
[06:52:54] we have all the books together
[06:52:56] regardless of their year. Well maybe it
[06:52:59] will be useful in the application even
[06:53:01] for me personally to have a table one
[06:53:04] for each year of books that have been
[06:53:06] nominated for this prize. But before I
[06:53:09] create that view, I should ask how do I
[06:53:11] try to find the books nominated in 2023?
[06:53:16] If my table looks like this, I have a
[06:53:18] table of books with ID, title, and year
[06:53:22] columns. What query could I use to find
[06:53:25] only those books nominated in 2023?
[06:53:29] >> Use the wear clause with the year.
[06:53:33] >> Yeah, I could use the wear clause and
[06:53:35] try to search for a given year. Like I
[06:53:36] could try to say where in this case the
[06:53:39] year is 2023 or equal to 2023 and that
[06:53:42] would give me back these two rows. If
[06:53:45] only two books were nominated in 2023.
[06:53:47] In reality it's 13. If I wanted to find
[06:53:50] the next ones from 2022, what could I
[06:53:52] do? I could just change the wear clause
[06:53:54] to say where year equals 2022.
[06:53:58] And then same thing for 2021. I could
[06:54:01] say where year equals 2021.
[06:54:04] Now each of these segments of my data is
[06:54:08] what we'll call a partition a certain uh
[06:54:11] breaking down of my data into smaller
[06:54:13] pieces in this case organized by year.
[06:54:17] So let's now create smaller tables one
[06:54:20] for each year that might be in our data
[06:54:23] set here. Come back to my terminal and
[06:54:27] let's think about writing this query
[06:54:29] from before. So, if I wanted to find the
[06:54:32] books that were nominated in 2022,
[06:54:35] I could say select the ID column and the
[06:54:39] title column from my books table. And
[06:54:42] then I want to find only those books
[06:54:46] where the year equals 2022.
[06:54:49] Then semicolon and then enter. And I
[06:54:52] should see only those books that were
[06:54:54] nominated in 2022.
[06:54:58] But now I want to create a view that
[06:55:00] might actually store the results of this
[06:55:02] query more long-term. I could say create
[06:55:06] view and call this let's say 2022
[06:55:10] as now same query from before select ID
[06:55:14] and title from my books table from my
[06:55:18] books table in this case where the year
[06:55:22] equals 2022
[06:55:25] semicolon.
[06:55:26] Now, if I ever want to find only those
[06:55:29] books nominated in 2022, I could now use
[06:55:32] my view. I could say select star from
[06:55:36] 2022 semicolon or uh quote and then
[06:55:38] semicolon. Hit enter. And now I should
[06:55:41] see those very same books. So, what
[06:55:45] could I do now? Maybe I want those books
[06:55:47] from 2021 as well. Let me ask the
[06:55:50] audience, what could you do to create
[06:55:52] the view for the books in 2021 based on
[06:55:56] what we've just seen now?
[06:55:58] >> We could just change the year from 2022
[06:56:02] to 2021.
[06:56:04] >> Yeah, just change the year. And what
[06:56:06] would you propose we call this new view?
[06:56:08] If you had to take the the reigns on
[06:56:10] naming this view, what would you name
[06:56:11] it?
[06:56:12] >> Books that were written in 2021. Yeah,
[06:56:15] we could we could call it books that
[06:56:17] were nominated in 2021, but I would
[06:56:19] argue that might be a bit of a long view
[06:56:21] title. So, let's shorten it just a
[06:56:23] little bit and maybe keep in keeping
[06:56:24] with our current naming, we'll say 2021
[06:56:26] instead. So, I'll come back over here
[06:56:28] and let's try this. I'll say create a
[06:56:31] view. Create a view. And we could by all
[06:56:35] accounts and purposes, we could say um
[06:56:37] books nominated books nominated in 2021.
[06:56:43] And that's totally okay. But if I were
[06:56:45] to pass this view on to a new
[06:56:48] programmer, a new database analyst,
[06:56:50] well, I kind of want to shorten it for
[06:56:51] them, make it more simple for them to
[06:56:52] read. So, I could just call this 2021.
[06:56:56] Of course, this title is kind of
[06:56:58] ambiguous. Like, if I pass you a view
[06:57:01] called 2021, are you automatically going
[06:57:03] to know what's inside that view?
[06:57:06] Probably not. So, it's actually a
[06:57:07] balance between how descriptive you want
[06:57:09] to be with your names here. We'll stick
[06:57:12] though with 2021 to our earlier example
[06:57:15] here. Now I'll say create view 2021 as
[06:57:19] select ID title from books and to
[06:57:24] Vavian's point I'll say where the year
[06:57:26] equals 2021 semicolon enter and now I
[06:57:30] could say select star from
[06:57:34] sect star from 2021 semicolon.
[06:57:38] So this is a good way to break apart a
[06:57:40] large table into logical pieces. It's
[06:57:44] useful both for both you as a programmer
[06:57:46] and also for applications that might
[06:57:48] only need to access some subset of your
[06:57:51] data where some condition is true. So
[06:57:55] based on what we've seen so far, what
[06:57:57] questions do we have on partitioning
[06:57:59] data with views?
[06:58:02] >> We have created few views for 2021 and
[06:58:05] 2022. uh rather than creating two views,
[06:58:08] is it possible to uh you know uh
[06:58:11] simplify it as one and then use it
[06:58:14] rather like uh where is simply change
[06:58:17] that alone?
[06:58:19] >> Yeah, I mean it's a trade-off here. So
[06:58:21] you could imagine trying to do let's say
[06:58:24] a single view that maybe has just titles
[06:58:27] and just years in it, but then you have
[06:58:29] to rewrite the query later on to find
[06:58:31] only those books for a certain year.
[06:58:33] Here, what we're trying to do is just
[06:58:35] like break up this big table into
[06:58:37] smaller pieces. And you can imagine this
[06:58:38] being particularly useful if you had not
[06:58:40] just 78 books, but even like thousands
[06:58:43] or tens of thousands or millions of
[06:58:45] books. Could be useful to have a view
[06:58:47] for each logical segment of those 10,000
[06:58:50] or more books.
[06:58:52] Let's take one more question here.
[06:58:54] >> I uh would like to ask about uh updating
[06:58:57] the view itself. If I update the single
[06:59:02] table, any element in each table, the
[06:59:05] view can be updated automatically or
[06:59:09] maybe it needs some involvement.
[06:59:12] >> Okay, a good forward thinking question
[06:59:13] here. Uh, you can, you're right, update
[06:59:16] a table. You can say update the table
[06:59:19] and set some column to some value. What
[06:59:22] you can't do actually is update a view.
[06:59:25] And that's because a view doesn't have
[06:59:27] any underlying actually doesn't have any
[06:59:28] data inside of it exactly. It only pulls
[06:59:31] data from underlying tables. So let me
[06:59:34] show you how I could update this view or
[06:59:37] at least try to update this view. I'll
[06:59:39] come back to my computer and let's say
[06:59:42] we wanted to change a book in the 2021
[06:59:45] view. I could say select star from 2021
[06:59:49] semicolon. And maybe it turns out that
[06:59:51] there's a typo in here. So instead of uh
[06:59:54] minor detail, it's called something like
[06:59:56] the minor detail. This um book on ID34
[07:00:01] here, I could try to update this view. I
[07:00:04] could say update 2021 and set the title
[07:00:09] equal to the minor detail. The minor
[07:00:13] detail where the title currently is the
[07:00:16] title currently is minor detail like
[07:00:19] this minor detail. Then I'll hit
[07:00:22] semicolon. And if I do this, I get this
[07:00:25] error. Cannot modify 2021 because it is
[07:00:29] a view. Now, why can't we modify a view?
[07:00:33] Well, recall that a view is simply the
[07:00:36] um combination of data from underlying
[07:00:39] tables. I've assembled data from
[07:00:41] different pieces of my database and put
[07:00:43] them into a single view. But I can't
[07:00:46] then update that data because that data
[07:00:48] is located in multiple individual tables
[07:00:50] around my database. What I should
[07:00:52] instead do is try to update the
[07:00:54] underlying table which I can do as we
[07:00:56] saw before with just update and set to.
[07:01:00] Okay. So more on how we can update or at
[07:01:03] least uh try to update views a little
[07:01:06] bit later. We'll take a break and come
[07:01:08] back to talk about how we can secure
[07:01:09] data using views as well. And we're
[07:01:12] back. So, one more use case for views is
[07:01:16] being able to secure the data that's in
[07:01:17] your database. You might imagine having
[07:01:20] a table, but some columns in that table
[07:01:23] you don't want to share with somebody
[07:01:25] else. Well, a common practice in
[07:01:27] security is to only give someone the
[07:01:30] information they need to know. With
[07:01:33] views, you could do that very principle.
[07:01:35] You could accomplish that by taking a
[07:01:37] table and reducing the number of columns
[07:01:39] somebody else might see. So let's
[07:01:42] consider here some ride share company.
[07:01:45] And ride share companies keep track of a
[07:01:46] lot of information about us. They keep
[07:01:48] track of where we're going, where we're
[07:01:50] coming from, who's in the car with us
[07:01:53] and who drove us there. Even sometimes.
[07:01:55] Let's say that a ride share company has
[07:01:58] a table called rides. And inside this
[07:02:01] table is the origin of several rides and
[07:02:04] the destination along with the rider who
[07:02:07] took that ride. Now, if I were to ask
[07:02:10] you here, let's say I want to give this
[07:02:14] data to an analyst to figure out which
[07:02:16] rides are most popular or which rides
[07:02:18] are highly rated. What data should I
[07:02:20] probably omit if I wanted to share this
[07:02:23] data with somebody else? What should I
[07:02:26] remove from this table?
[07:02:28] >> The data you could remove would be the
[07:02:33] rider.
[07:02:34] >> Yeah, good point. So if I look at this
[07:02:36] table and I think of what information is
[07:02:39] personally identifiable P II personally
[07:02:43] identifiable information it seems like
[07:02:45] this rider column could identify
[07:02:47] somebody who took a ride from let's say
[07:02:49] goodday good galaxy to Honeyhive Galaxy
[07:02:51] and we don't want to leak that
[07:02:53] information if I gave this to some
[07:02:55] analyst. Well, with a view, I could keep
[07:02:58] this underlying table, but I could
[07:03:01] create a view that only has the origin
[07:03:04] and the destination that omits the rider
[07:03:07] column. And I could more confidently
[07:03:10] share this view with an analyst, not the
[07:03:13] underlying table. So, let me try to
[07:03:16] implement this view so we can see it in
[07:03:17] action inside this database here. I'll
[07:03:20] come back to my computer. And in this
[07:03:23] case, I have a new database. I have one
[07:03:25] called rid share. DB. I'll type SQLite 3
[07:03:29] ridshare. DB to open up this database.
[07:03:33] And if I type dots schema to see the
[07:03:35] schema of this database, I should see I
[07:03:38] have one table called rides where each
[07:03:40] ride has an ID, an origin, a
[07:03:43] destination, and a rider. Now I'll
[07:03:47] select star from the rides table. Select
[07:03:51] star from rides. Hit semicolon. And I
[07:03:54] should see the very same data we just
[07:03:57] saw in our slides where Peach is going
[07:03:59] from good galaxy to Honeyhive Galaxy,
[07:04:01] Mario going from Castle Courtyard to
[07:04:03] Cascade Kingdom and so on. So now I know
[07:04:07] I don't want to share this data with
[07:04:10] somebody else. What could I do? Instead
[07:04:13] of selecting everything, I could try to
[07:04:15] omit this rider column to the point
[07:04:17] before. So let's try that. I'll select
[07:04:20] just ID and just origin and just
[07:04:23] destination from rides. I'll
[07:04:26] deliberately omit that rider column. Now
[07:04:30] I'll hit enter and I should see the
[07:04:33] origin and destination, but I actually
[07:04:36] don't see the rider column. So this is a
[07:04:39] decent view, but I could probably
[07:04:41] improve this even more. It turns out
[07:04:44] that in SQLite, if I want to fill a
[07:04:47] column with some arbitrary value, I can
[07:04:49] do that a bit like this. Why don't I try
[07:04:52] to select ID and select origin and
[07:04:56] destination, but I also want to let
[07:04:59] somebody know that this data has been
[07:05:02] anonymized. There is rider information
[07:05:04] in the underlying table, but you don't
[07:05:06] have access to it. What I'll do instead
[07:05:08] is say, let me make this new column
[07:05:11] that's filled with this value anonymous
[07:05:13] as a string. I'll say quote unquote
[07:05:16] anonymous as this column name called
[07:05:20] rider. I'll select all of this from the
[07:05:23] rides table semicolon.
[07:05:26] Now I've more helpfully indicated that
[07:05:29] there is a rider column, but you
[07:05:31] deliberately don't have access to see
[07:05:33] who those riders are.
[07:05:36] So my last step here is probably to turn
[07:05:38] this into a view. I have a good query,
[07:05:41] but I want to save it so I could query
[07:05:43] it later on. Well, I could type select
[07:05:46] or not select. I could type create view
[07:05:48] first. I'll create a view. This one just
[07:05:50] called analysis. I'll give this to my
[07:05:52] data analysts here. Create view
[07:05:54] analysis. And then I'll say as let's go
[07:05:58] for select ID origin and destination as
[07:06:03] well as the anonymous the anonymous
[07:06:06] column as in this case the rider and
[07:06:10] I'll select all of this from my rides
[07:06:14] table semicolon hit enter now if I type
[07:06:19] schema I see my new view analysis and if
[07:06:22] I say select star from analysis is
[07:06:26] from analysis semicolon. I should see
[07:06:30] that I've anonymized quote unquote this
[07:06:32] data.
[07:06:34] But to the extent this is helpful, I'd
[07:06:37] argue it's not very secure, at least in
[07:06:40] SQL light. And if you're thinking
[07:06:43] adversarially here,
[07:06:46] what might you be able to do still if I
[07:06:48] gave you access to this database?
[07:06:51] What could you do to deanonymize this
[07:06:53] data and to see the data I didn't want
[07:06:55] you to see?
[07:06:57] >> You can just uh query the writers table
[07:07:00] and find what are the riders values in
[07:07:03] the writers column.
[07:07:04] >> Okay, so you're correct that we could
[07:07:06] still see the rides table. Maybe I look
[07:07:08] at the ID column in the analysis view
[07:07:11] and I see those IDs. I might be able to
[07:07:13] link those IDs with the IDs in the rides
[07:07:16] table. And nothing's stopping me, at
[07:07:18] least in SQLite, from saying select star
[07:07:20] from the rides table. So I'll come back
[07:07:22] over here and I'll try that. I'll say in
[07:07:25] this case, select star from rides. Hit
[07:07:29] semicolon. And now I see all that ride
[07:07:32] information although I hid it in this
[07:07:34] view called analysis. And this is a
[07:07:36] downside of SQLite. In SQLite, we can't
[07:07:40] set access controls. Meaning I either
[07:07:43] give you the entire database or nothing
[07:07:45] at all. In other DBMS's though, I could
[07:07:48] set access controls. I could give David
[07:07:51] access only to the analysis view. I can
[07:07:54] give myself access to both the rides
[07:07:57] table and the analysis view. So keep
[07:07:59] that in mind when you're working with
[07:08:01] SQLite.
[07:08:03] Okay, so we've seen here how to secure
[07:08:05] some data using SQLite and using views
[07:08:08] in this as well. Let's come back in just
[07:08:11] a minute and see how we could actually
[07:08:12] use SQLite and views to not just secure
[07:08:16] our data but also to work on soft
[07:08:18] deletions which you saw just a bit ago.
[07:08:20] And we're back for one final application
[07:08:23] of views. We saw just a little week a
[07:08:26] few weeks ago how we could implement
[07:08:27] soft deletions. That is not fully
[07:08:30] deleting something in our database but
[07:08:31] only marking it as deleted. And we saw
[07:08:34] this in the context of Boston's own
[07:08:36] Museum of Fine Arts, keeping track of
[07:08:38] items inside their collection. So let's
[07:08:41] say we had this table called collections
[07:08:43] full of items in the MFA, the Museum of
[07:08:46] Fine Arts in Boston. Here I have four
[07:08:49] items currently in our collections. ID
[07:08:52] 1, ID2, 3, and four. But I also have
[07:08:56] this deleted column which is either zero
[07:08:58] or one depending on whether an item has
[07:09:00] been deleted or not. So, I want to
[07:09:04] delete, let's say, farmers working at
[07:09:06] dawn. This first piece here, instead of
[07:09:08] deleting it from the table fully, I
[07:09:10] could set this deleted column from a
[07:09:12] zero to a one, just like this. And now
[07:09:15] it's only soft deleted. I still have the
[07:09:18] data here. I still have the title, but
[07:09:20] now instead of being a zero, it's marked
[07:09:23] as a one. Now, this is useful, but what
[07:09:27] could I do to only see now the items
[07:09:31] that have not been deleted? Like, if I
[07:09:33] show you this database collections here,
[07:09:36] the table here, I have titles and the
[07:09:39] deleted column. But if I only want to
[07:09:41] see those items that are not deleted,
[07:09:44] what query could I use for that?
[07:09:48] >> Would you use the wear statement?
[07:09:50] >> I could use a select statement and I
[07:09:52] could use probably a wear clause as
[07:09:53] well. I could say select star where
[07:09:56] perhaps deleted equals zero because in
[07:09:59] this case when deleted is zero we know
[07:10:02] this item is still supposed to be in our
[07:10:05] table. So here's that query here select
[07:10:08] star from collections where deleted
[07:10:10] equals zero. Now we could try to convert
[07:10:13] this query into a view. So we could
[07:10:16] always only see the items in our current
[07:10:19] collection not those we have marked as
[07:10:22] deleted. So, I'll come back over here
[07:10:23] and we'll see we have our collections
[07:10:25] table, but we also have now perhaps a
[07:10:28] new view of this table called current
[07:10:31] collections. Well, if I set current
[07:10:34] collections to be the result of this
[07:10:36] query, I should see when I update
[07:10:39] deleted to be one for some of these
[07:10:41] items here, it should be removed from
[07:10:44] this current collections table. So,
[07:10:46] let's try that. I could take farmers
[07:10:48] working at dawn and delete it. I could
[07:10:51] see this correspondence between this row
[07:10:54] here and this row here. It's in both our
[07:10:57] collections table and current
[07:10:59] collections. But if I set deleted from
[07:11:01] zero to one, I should see that item
[07:11:05] removed from current collections, thus
[07:11:08] updating my view and keeping track of my
[07:11:11] items that are not currently in my
[07:11:13] collection. So let's come back here and
[07:11:16] implement this in terms of our own
[07:11:18] database. come back over here and I will
[07:11:21] open up MFA. DB, that old database from
[07:11:24] a few weeks ago. I'll say SQLite 3 MFA.
[07:11:29] DB. And now if I type dots schema, I
[07:11:32] should see the tables inside of this
[07:11:35] database. Collections, artists, and
[07:11:37] created. We'll focus in particular on
[07:11:39] the collections table. So if I say
[07:11:41] select star from collections, I should
[07:11:45] see that I have the title, the accession
[07:11:48] number, and the date this piece was
[07:11:49] acquired by the MFA. Now though, if I
[07:11:53] want to add a deleted column, I could do
[07:11:56] so by using alter table, I could say,
[07:12:00] let's alter table collections, alter
[07:12:03] table collections, and add a column
[07:12:06] called deleted. I'll say this column has
[07:12:10] the type integer. It stores whole
[07:12:13] numbers and the default number is zero
[07:12:16] semicolon.
[07:12:18] Now if I say select star from
[07:12:21] collections select star from collections
[07:12:24] semicolon I should see there's this new
[07:12:27] deleted column where all the values are
[07:12:30] zero at first. So if I want to delete
[07:12:34] something, I could instead of typing
[07:12:36] delete from as we saw before, I could
[07:12:39] just update this deleted value. I could
[07:12:41] say maybe update update collections and
[07:12:45] set deleted equal to one where a certain
[07:12:51] title is present. I'll say this that the
[07:12:54] title is equal to farmers
[07:12:59] title equals farmers working at dawn
[07:13:03] semicolon. So now I've soft deleted this
[07:13:07] item. It's still in my table at least
[07:13:09] the title is but now I've marked it as
[07:13:12] being deleted. It should not long be in
[07:13:14] my ultimate view. Hit enter here and
[07:13:17] I'll say select star from collections.
[07:13:20] I'll see that in this case I still see
[07:13:23] farmers working at dawn. But what do I
[07:13:26] want? I want a view that only removes
[07:13:28] that only shows me those items that have
[07:13:30] not been deleted. So I'll try this. I'll
[07:13:34] say select star from collections and
[07:13:36] apply a condition to it to our earlier
[07:13:39] um point before. So I'll say where in
[07:13:41] this case deleted equals zero semicolon
[07:13:44] hit enter. And now I should see only
[07:13:47] those items that are not marked as
[07:13:49] deleted.
[07:13:51] But I want to turn this into a view
[07:13:53] which I could. I could say maybe create
[07:13:56] a view called current collections. And
[07:14:00] then I'll make this the following query
[07:14:03] as select ID select title accession
[07:14:08] number and acquired. But now I'll
[07:14:11] actually omit that deleted column. I
[07:14:14] don't want this column to show up in my
[07:14:16] current collections. I only want it to
[07:14:18] be in the underlying table. So I'll
[07:14:22] select all these columns from the
[07:14:24] collections table and then I'll say
[07:14:26] where deleted equals zero to apply this
[07:14:30] condition and only get those items that
[07:14:32] are not marked as deleted.
[07:14:34] Now I'll hit enter and I should be able
[07:14:37] to do this. Select star from current
[07:14:40] collections
[07:14:41] semicolon. And now I'll see only those
[07:14:44] items that have not been deleted.
[07:14:48] So this seems worthwhile. I'm now able
[07:14:51] to view the items that are currently in
[07:14:54] my collection. But a problem remains.
[07:14:57] Like if I tried to update this table and
[07:15:02] insert something into it, what might
[07:15:05] happen? Let me ask our audience here.
[07:15:08] Based on what we saw before, what would
[07:15:10] happen if tried to insert into this
[07:15:12] table here, this view perhaps?
[07:15:15] >> I think we cannot uh update the view
[07:15:19] itself as we saw before.
[07:15:22] >> Yeah, we can't update the view itself.
[07:15:24] We can't insert new data. We can't even
[07:15:26] delete data. So, let me try first to
[07:15:28] delete data and then we'll see how to
[07:15:30] insert some data a little bit later.
[07:15:32] I'll come back over to my terminal and
[07:15:35] what if I wanted to delete imaginative
[07:15:37] landscape I could say delete from delete
[07:15:41] from current collections where the title
[07:15:45] equals let me make a new line here where
[07:15:48] the title equals imaginative landscape
[07:15:52] imaginative landscape semicolon
[07:15:56] now I'll see that same error we got
[07:15:58] before we tried to update some view I
[07:16:00] can't modify this because it is a view.
[07:16:04] Well, it turns out there is a way to
[07:16:06] work around this. We can't modify the
[07:16:09] view, but we can modify the underlying
[07:16:12] table. So to do this, we need rank from
[07:16:15] old friends. In this case, those called
[07:16:18] triggers. So if you remember, a trigger
[07:16:21] is a way to specify some SQL statement I
[07:16:24] want to run when some other SQL
[07:16:26] statement is run. we saw before. We
[07:16:29] could use before or after to say run
[07:16:32] this SQL statement either before or
[07:16:34] after some other SQL statement here.
[07:16:36] What we didn't see until now is this
[07:16:40] instead of trigger. I can create a
[07:16:42] trigger that has a name and I can run it
[07:16:45] instead of some other SQL statement. So
[07:16:48] I could say instead of deleting on this
[07:16:51] view, let me give you the other the
[07:16:53] proper query to run in this case. So
[07:16:56] instead of deleting on this view, I will
[07:16:58] for each row run this other statement.
[07:17:02] I'll say begin. This is the same I want
[07:17:04] you to run instead. And in this
[07:17:06] statement, we could have something that
[07:17:08] actually updates not the view but the
[07:17:11] underlying table. And we then end that
[07:17:14] query here.
[07:17:16] So based on what we know about our view
[07:17:19] and the underlying table called
[07:17:22] collections,
[07:17:23] what query should we put in here to
[07:17:26] actually delete something from our
[07:17:28] table? Let me ask our audience
[07:17:32] instead of deleting from our view, what
[07:17:34] should we instead do to our table?
[07:17:38] >> Yeah, you should update the deleted
[07:17:39] column in the collections table.
[07:17:42] >> Yeah. Uh, so instead of deleting from
[07:17:44] our view, what I really want to do is
[07:17:46] update that table. So let's write a
[07:17:49] trigger to do just that. Come back to my
[07:17:51] computer here and I'll start on this
[07:17:55] trigger. To our point, I want to create
[07:17:58] a trigger that runs instead of deleting
[07:18:00] on this view. And what I want to instead
[07:18:02] happen is an update on the underlying
[07:18:05] table. So I'll say create a trigger.
[07:18:08] This one called delete. And then I'll
[07:18:12] say instead of delete on current
[07:18:16] collections that is whenever SQL hears
[07:18:19] or listens and hears a delete on the
[07:18:22] current collections view I don't want
[07:18:24] that to happen. I instead want this
[07:18:26] other statement to happen. I'll say for
[07:18:28] each row affected by that delete. For
[07:18:31] each row I asked delete on current
[07:18:33] collections run instead this other
[07:18:35] statement. I'll say begin. Here is that
[07:18:37] statement 1 2 3 4 indents for style
[07:18:40] sake. And now I'll say I want to update
[07:18:43] collections. Update collections and set
[07:18:47] deleted
[07:18:48] set deleted equal to one.
[07:18:52] But I don't want to leave this just as
[07:18:55] is. If I say update collections set
[07:18:58] deleted equal to one. What's the problem
[07:19:02] with that statement if I end it there?
[07:19:04] Uh so yeah it will update all the
[07:19:06] columns whether it is we want it to be
[07:19:09] deleted or not.
[07:19:11] >> Yeah with no condition it'll update all
[07:19:13] the columns here. So I want to apply a
[07:19:15] condition to make sure it only affects
[07:19:17] the particular row I'm working with.
[07:19:20] Well what unique identifies each row?
[07:19:22] The ID does. So let's try using the ID
[07:19:24] here. I'll come back and I'll say I want
[07:19:27] to update collections set deleted equal
[07:19:29] to one but only when some condition is
[07:19:32] true. I'll indent again four times and
[07:19:35] say where in this case the ID the ID
[07:19:40] column is equal to the old ID. Now old
[07:19:46] here is a special keyword that means the
[07:19:49] row we just deleted or that we would
[07:19:50] have deleted from current collections. I
[07:19:53] want to update that same row with that
[07:19:56] same ID in the underlying collections
[07:19:59] table. So I'll put a semicolon here to
[07:20:03] end and then I'll say end this
[07:20:06] statement. This is the entire statement
[07:20:07] I want to run after I try to delete on
[07:20:10] my current collections table. Now I'll
[07:20:13] hit enter and I'll see nothing changes.
[07:20:15] But if I say dots schema, I should then
[07:20:18] see down below here I have a trigger
[07:20:20] called delete that will instead run an
[07:20:22] update when I try to delete from this
[07:20:24] view. So let's try that. What I can do
[07:20:28] now is try again to delete from current
[07:20:31] collections. I'll say delete from
[07:20:34] current collections. Current collections
[07:20:36] where in this case the title equals
[07:20:41] imaginative landscape. Let's say we sold
[07:20:43] this painting. It's no longer part of
[07:20:44] our collection. Imaginative landscape
[07:20:47] semicolon. And now it actually seemed to
[07:20:51] work. I get no error here. So it seems
[07:20:54] like it went okay. Okay. Well, if I
[07:20:56] select star from current collections,
[07:21:01] I actually see that it's gone. But is it
[07:21:04] really gone? If I try select star from
[07:21:07] collections, not current collections.
[07:21:09] The underlying table for current
[07:21:11] collections semicolon, what do I see?
[07:21:14] That the ID column has been updated from
[07:21:16] a zero now to a one.
[07:21:20] So a good way of trying to use triggers
[07:21:22] here to update our views by instead
[07:21:25] modifying the underlying table. Now
[07:21:29] there might be one more issue we
[07:21:31] encounter here which is the following.
[07:21:34] Let's say I'm at this current state in
[07:21:37] my tables. I have collections where
[07:21:39] farmers working at dawn is deleted. It
[07:21:41] has a one right here and we thus can't
[07:21:44] see it inside of current collections.
[07:21:46] Well, let's say I want to not delete
[07:21:49] from current collections, but also add
[07:21:51] to current collections. I could try to
[07:21:54] insert into this view, but I probably
[07:21:57] actually won't be able to do that
[07:21:58] because it is a view. Let's think then.
[07:22:01] If I wanted to insert into this view,
[07:22:04] what should I really do instead?
[07:22:08] >> You should add it to the collections
[07:22:10] table instead of the view.
[07:22:13] >> I like that idea. So, I should add this
[07:22:15] row to the collections table instead of
[07:22:18] the view. But now, here's a bit of a
[07:22:22] trick. Let's say I add farmers working
[07:22:25] at dawn. We reacquired it. What should I
[07:22:29] do in that case? When I'm adding a
[07:22:33] painting I previously deleted. So uh
[07:22:38] what we could do is we know that the
[07:22:40] deleted we we can check if the deleted
[07:22:43] column is one and then uh based on that
[07:22:47] we could like uh update that particular
[07:22:50] column or if the if uh the there is no
[07:22:56] uh title in the connections table you
[07:22:59] can just add it inside there. Yeah, I
[07:23:02] like your thinking there of first trying
[07:23:03] to check, do we have this item already
[07:23:06] in our table or do we not? If we do
[07:23:09] already have it in our table, we should
[07:23:11] just flip this bit from a zero from a
[07:23:13] one to a zero. If we don't though, let's
[07:23:16] add a brand new row as we heard before.
[07:23:19] So, let's think. What could we use to
[07:23:21] conditionally run some code on this
[07:23:24] collections table? Well, it turns out
[07:23:26] that you can use some other aspects of
[07:23:28] triggers. In this case, triggers have
[07:23:30] not just um unconditional uh use cases,
[07:23:34] but also conditional ones too. So, let's
[07:23:37] try this. I could try to insert to on
[07:23:41] this view and then run some code down
[07:23:44] below. But to our discussion a little
[07:23:46] bit earlier, I don't want to
[07:23:48] unconditionally do this. I want to check
[07:23:50] is this item in my table or is it not
[07:23:53] already? So, for that, I could use this
[07:23:55] keyword called when. I could say for
[07:23:58] each row when some condition is true,
[07:24:01] run this trigger. And you can imagine
[07:24:04] having two triggers to insert into our
[07:24:07] view. One that runs when the item is
[07:24:09] already in our table. We could then flip
[07:24:12] that bit from a one to a zero. We could
[07:24:15] also have a different trigger to
[07:24:17] actually insert a new item. In that
[07:24:20] case, actually inserting a brand new row
[07:24:22] to our underlying collections table. So
[07:24:25] let's work on this now to finish off and
[07:24:28] polish our collections view. Come back
[07:24:31] to our terminal here. And what we'll try
[07:24:33] to do is now insert into this table.
[07:24:37] I'll create a new trigger this case
[07:24:40] called insert when exists. I'll say
[07:24:43] create trigger. Create trigger. Insert
[07:24:46] when exists. So this trigger will run
[07:24:49] when an item we're trying to insert is
[07:24:51] already in our collections table. I'll
[07:24:54] say instead of insert on the current
[07:24:57] collections table I want this to happen
[07:25:00] instead I'll say for each row now I'll
[07:25:06] hit enter again and say when just for
[07:25:09] style sake when new
[07:25:12] accession number new accession number is
[07:25:16] in my table already well I want to find
[07:25:20] which accession numbers I already have
[07:25:22] and if you Excession number is a unique
[07:25:24] ID for the museum. It's not the ID
[07:25:27] column in my table, but a unique ID to
[07:25:29] keep track of items in the museum. So if
[07:25:31] I've already given this item an
[07:25:32] exception number, I should already see
[07:25:34] it in my table already. So I'll say then
[07:25:37] enter enter for style sake. Select
[07:25:40] accession number.
[07:25:42] Select accession
[07:25:45] number
[07:25:47] from collections.
[07:25:49] So this sub query tells me what
[07:25:52] accession numbers do I already have and
[07:25:54] this condition tells me is the new row
[07:25:57] I'm inserting does that have the same
[07:25:59] accession number or not. Now I'll close
[07:26:02] this sub query and I'll continue my
[07:26:05] trigger. I'll say begin. Well in the
[07:26:09] case that this item already exists in my
[07:26:12] collections table I just want to update.
[07:26:14] I want to flip that integer from a one
[07:26:17] back down to a zero. So I'll say update
[07:26:20] collections update collections and set
[07:26:23] deleted deleted equal to zero.
[07:26:28] Now I want to do this not on my entire
[07:26:30] table but only where the accession
[07:26:33] number is equal to the new accession
[07:26:38] number. That is the accession number I'm
[07:26:40] inserting here as well. I'll then end
[07:26:44] like this. And now I have my entire
[07:26:46] trigger. I'll say instead of inserting
[07:26:49] into my view, I want to run this
[07:26:51] instead. Check if I've already added
[07:26:54] this item and if I have changed that
[07:26:56] deleted column from a one to a zero. Now
[07:27:00] I'll hit enter and let me hit enter
[07:27:03] again and let me check.
[07:27:07] I needed to have a semicolon after my
[07:27:10] where. So let me try to run this again.
[07:27:13] I'll do control D to restart and I'll
[07:27:16] say SQLite 3. Um let's do MFA. DB and
[07:27:20] I'll restart this trigger. So here I'll
[07:27:23] say create trigger create trigger insert
[07:27:26] when exists we gave the name before.
[07:27:29] Then I'll say instead of
[07:27:32] insert on current collections what I
[07:27:35] want to do is run this. I'll say for
[07:27:37] each row I insert check some condition
[07:27:41] when the new accession number that is
[07:27:43] the unique ID the museum has for this
[07:27:45] item is in my already available
[07:27:49] accession numbers. I'll say select in
[07:27:51] this case select accession number
[07:27:55] from
[07:27:58] from collections
[07:28:01] and then I'll close the subquery.
[07:28:04] Now I'll say I want to begin the same
[07:28:07] thing I want to run begin. Now update in
[07:28:11] this case my collections table and set
[07:28:13] the deleted column from a one back down
[07:28:15] to a zero. Update collections
[07:28:18] and set deleted equals zero
[07:28:24] where in this case the accession number
[07:28:28] is equal to the new accession number
[07:28:31] only modifying that particular row. Now
[07:28:34] I'll hit semicolon to close this
[07:28:36] statement. And then I'll say end below a
[07:28:38] second semicolon enter. And now if I
[07:28:41] type dot schema, I should see my new
[07:28:44] trigger to insert into my collections
[07:28:46] table when I try to insert into my view.
[07:28:49] So let's try this. I'll say maybe I want
[07:28:51] to insert into my collections my current
[07:28:54] collections. Insert into well let me try
[07:28:56] this. I'll say select star from select
[07:29:00] star from collections. And let's say I
[07:29:03] want to reinsert in this case profusion
[07:29:06] of flowers. So I'll say insert into um
[07:29:10] my current collections. Actually
[07:29:11] reinsert into
[07:29:13] current collections.
[07:29:16] I want to insert imaginative landscape.
[07:29:18] So I'll say insert into current
[07:29:20] collections some set of values along
[07:29:22] with some columns. I'll say the title is
[07:29:25] profusion of flowers. There's
[07:29:26] imaginative landscape later on. then
[07:29:28] accession number
[07:29:31] then the date it was acquired like this
[07:29:34] now hit enter and provide the values
[07:29:37] I'll say the title is imaginative
[07:29:39] landscape like this number is 56.496 496
[07:29:45] and the acquired date is going to be
[07:29:47] null in this case. We don't know when we
[07:29:49] got it. I'll hit semicolon here and
[07:29:52] enter. So if I select star from
[07:29:54] collections now, select star from
[07:29:56] collections. Semicolon. I should see
[07:29:59] that I didn't actually insert a new row.
[07:30:01] I only flipped that deleted value from a
[07:30:04] one back down to a zero. Now, there's
[07:30:07] certainly more to do here. I could write
[07:30:09] a trigger to actually add a brand new
[07:30:12] row to this table here. I could also try
[07:30:14] to update this data, change, for
[07:30:16] example, the acquired date from null to
[07:30:19] date we actually do know. For now,
[07:30:21] though, we'll leave all that up to you
[07:30:23] and we'll see you next time.
[07:30:27] [Music]
[07:30:44] Well, hello one and all and welcome back
[07:30:46] to CSF's introduction to databases with
[07:30:49] SQL. My name is Carter Zeni and today
[07:30:51] we'll focus on optimizing trying to
[07:30:54] reduce the time our queries take as well
[07:30:56] as the storage space our database might
[07:30:59] use. We'll also see how to handle
[07:31:01] concurrency that is many queries all at
[07:31:04] once. Now, we'll do all of this in the
[07:31:06] context of a new database. This one, the
[07:31:09] Internet Movies Database, or IMDb for
[07:31:12] short. If you've been to imdb.com,
[07:31:15] you may have seen this whole big
[07:31:17] database of movies and we've compiled
[07:31:19] that into our very own SQLite database
[07:31:21] for us today. Now, this database is big.
[07:31:26] It is much bigger than anything we've
[07:31:27] seen so far. In fact, it has over
[07:31:29] 200,000 movie ratings, over 400,000
[07:31:33] movies, and 1.4 million stars or people
[07:31:37] who have acted in some movie. And the
[07:31:40] goal of this database is to represent
[07:31:42] movies, the people in them, and the
[07:31:45] average ratings for each of those
[07:31:47] movies. Now, we have ourselves an entity
[07:31:50] relationship diagram to describe this
[07:31:52] database. And it looks a bit like this.
[07:31:54] We have people in one table, movies in
[07:31:58] another, and ratings in a separate table
[07:32:01] down here. Notice that people have a
[07:32:03] name and a birthday along with an ID,
[07:32:06] the primary key for that table. Movies
[07:32:09] too have a title and the year they were
[07:32:11] released as well as their own primary
[07:32:13] key ID here. rating down here has the
[07:32:17] average rating for a given movie as well
[07:32:19] as the number of votes that went into
[07:32:22] calculating that average rating here.
[07:32:24] And notice too that the movie and people
[07:32:27] table has a many to many relationship.
[07:32:30] That is a person can star in more than
[07:32:33] one movie in the same way a movie can
[07:32:36] have multiple stars. So if we want to
[07:32:39] implement this many to many
[07:32:41] relationship, we've seen one way to do
[07:32:44] that. Let me actually ask the audience
[07:32:45] here. How have we implemented a many to
[07:32:48] many relationship historically? What
[07:32:50] kind of tables do we need for this do
[07:32:53] you think? All right. So, not to worry
[07:32:55] if you don't have an idea of what we're
[07:32:56] going to use here. Let's take a peek at
[07:32:58] what tables we can actually use. So,
[07:33:00] here as we've seen historically, we
[07:33:01] might have two tables. One for people
[07:33:04] and one for movies. And notice here in
[07:33:07] the people table, we have names along
[07:33:09] with a primary key called ID. And
[07:33:12] similarly in our movies table we also
[07:33:15] have a title column along with movies's
[07:33:18] own primary key and ID column over
[07:33:21] there. Now to implement the relationship
[07:33:24] between people and movies we have to
[07:33:27] have some table in the middle of these
[07:33:29] two. One that relates people ids or
[07:33:32] person IDs with movie ids. And if we
[07:33:36] look at this table, I could see that if
[07:33:37] I see person ID next to some given movie
[07:33:40] ID, well, it means that the person with
[07:33:42] this ID has starred in played a role in
[07:33:45] this movie here. We see person 158.
[07:33:48] Let's see, Tom Hanks was in the movie ID
[07:33:51] with 11479
[07:33:53] or Toy Story as we see in the movies
[07:33:55] table. And now knowing this, how could
[07:33:58] we figure out which movies Kristen Bell
[07:34:02] has starred in? If we know Christian
[07:34:04] Bell's ID, what should we then do to
[07:34:06] find the movies Christian Bell has
[07:34:08] starred in?
[07:34:10] >> Uh, you could select the ID of the
[07:34:12] people, then look it into the stars
[07:34:15] table, then look it into the movies
[07:34:17] table.
[07:34:19] >> Yeah, I like your thinking. So, there's
[07:34:20] multiple steps here. We have to go
[07:34:22] through each table to find ultimately
[07:34:25] the movie that Kristen Bell has starred
[07:34:26] in. The first step might be to ask, what
[07:34:29] is Kristen Bell's ID? Well, it seems to
[07:34:31] be 68338.
[07:34:33] Then, to your point, we could look at
[07:34:35] the stars table and find out what movie
[07:34:37] IDs correspond to that ID here. So, it
[07:34:40] seems like 2294629
[07:34:42] corresponds with Kristen Bell's ID here.
[07:34:45] Then, finally, we look up in the movies
[07:34:46] table. Well, what title corresponds with
[07:34:49] 2294629?
[07:34:51] It seems to be the movie Frozen. So,
[07:34:53] visually, we have this relationship
[07:34:54] among these tables here. So, let's now
[07:34:58] dive into our movies database to
[07:35:01] actually get a sense of what data is
[07:35:02] inside of this. And for that, I'll go
[07:35:04] back to my computer so we can open this
[07:35:05] database up in SQLite. Come back over
[07:35:08] here and I'll open up my own environment
[07:35:11] where I can type SQLite 3 movies. DB
[07:35:15] movies. DB. And now, if I zoom in just a
[07:35:19] bit, I can then type schema to show you
[07:35:24] all the tables that exist in this
[07:35:26] database. I see up top I do have a
[07:35:29] movies table that has a primary key
[07:35:32] called ID, a column called title, and a
[07:35:35] column called year. I have that same
[07:35:37] people table with names and birthdays.
[07:35:39] And I also have this stars table that
[07:35:42] corresponds with person IDs and movie
[07:35:44] IDs relating in this case people and
[07:35:47] movies. Okay, so let's try selecting
[07:35:51] then from our movies table to see what
[07:35:53] movies we have. Take a peek at our data.
[07:35:56] what we saw just a little bit ago. We
[07:35:57] could try to take a peek at our data
[07:35:59] using a certain SQL keyword. I could
[07:36:01] select star from movies to see all
[07:36:04] columns from movies. But if I have,
[07:36:07] let's say, 400,000 rows, I don't want to
[07:36:10] print all those to the screen. So, what
[07:36:12] could I use instead? Certain SQL
[07:36:15] keyword. I'm hearing limit. So, let's
[07:36:18] try that. I'll say limit five. I only
[07:36:20] want the first five results here. I'll
[07:36:22] hit enter. And here I'll see those first
[07:36:25] five movies in my movies table. They
[07:36:28] each have their own unique ID, a primary
[07:36:30] key. They have a title and the year that
[07:36:32] they were published. But if you've been
[07:36:36] to imdb.com,
[07:36:38] you may have wanted to search for a
[07:36:40] particular movie. Maybe you wanted to
[07:36:41] find your favorite movie among all the
[07:36:44] possible movies in their database. And
[07:36:46] we can simulate that kind of query by
[07:36:48] querying the database here. Whenever you
[07:36:50] type in IMDb's browser, let's like the
[07:36:52] search for a movie called um Frozen, for
[07:36:54] example, it odds are that behind the
[07:36:57] scenes, a database is actually running
[07:36:58] that same query to return to you what
[07:37:00] movies have that title called Frozen.
[07:37:03] Now, for me, uh my favorite movie since
[07:37:05] I was a kid is one called cars. So, let
[07:37:07] me try to search for cars here. I'll try
[07:37:09] to find select star from movies where
[07:37:13] the title equals cars. And you could
[07:37:16] imagine me going to IMDb, typing in cars
[07:37:19] in the search bar, and behind the
[07:37:20] scenes, this cql query gets run to find
[07:37:24] what movies have the title cars. So, let
[07:37:27] me hit enter here. And now I'll see that
[07:37:30] one movie has that title. Cars came out
[07:37:32] in 2006 and the ID is 317219.
[07:37:38] But this is a lecture on optimizing. So,
[07:37:40] it's worth asking how much time did it
[07:37:43] take for this query to run? Let's find
[07:37:46] out. Well, I can use a SQL light command
[07:37:49] here called timer. I'll say dot timer on
[07:37:52] to make sure that I time my future
[07:37:55] queries. I'll hit enter now. And now if
[07:37:58] I try selecting again, I'll hit the up
[07:38:00] arrow twice to get back my old query. I
[07:38:02] can type enter and I'll see not just the
[07:38:06] results, but the time it took to run
[07:38:09] that query.
[07:38:11] Now notice we have several different
[07:38:13] measures of time here. I have the quote
[07:38:15] unquote real time, which is essentially
[07:38:17] the stopwatch time, meaning from the
[07:38:19] time I pressed enter to the time I saw
[07:38:21] these results. How long did that take?
[07:38:24] But of course, if you're familiar with
[07:38:25] computers, you know that there's more
[07:38:27] involved than just this query running. I
[07:38:29] also have to wait for the operating
[07:38:30] system, other processes as well. That's
[07:38:32] where user and system time come in. User
[07:38:35] time is how much time this query
[07:38:37] particularly took on the CPU. System
[07:38:39] time is how long I spent waiting around
[07:38:41] for other processes to finish before I
[07:38:42] could run this query. For us, we'll
[07:38:45] focus on real time. What was the wall
[07:38:47] clock time, the stopwatch time, so to
[07:38:49] speak, between the time I pressed enter
[07:38:50] and the time I saw these results.
[07:38:53] Okay, so here we have a query taking
[07:38:57] 0.084
[07:39:00] seconds. I mean, that is pretty good. If
[07:39:02] I only wait around for less than a tenth
[07:39:05] of a second, like I'm not complaining.
[07:39:08] But if I'm the engineer at IMDb,
[07:39:11] why might I be concerned about a query
[07:39:14] that takes 0.084
[07:39:16] seconds? Particular if I have lots and
[07:39:18] lots of users. What's the problem there?
[07:39:22] Users, the database might be overwhelmed
[07:39:26] by the queries. And you should also
[07:39:28] consider like how much time the
[07:39:31] application takes to form the query to
[07:39:34] the database too.
[07:39:36] >> Yeah. Yeah. So the basic idea here is
[07:39:38] that when I have a single query that
[07:39:39] takes maybe less than ten of a second,
[07:39:41] that's fine. But if I have many many
[07:39:43] users running those queries all at once,
[07:39:46] like that time is going to add up. And
[07:39:48] so if I'm an engineer or even somebody
[07:39:50] in finance, I want to reduce that time
[07:39:53] because I'm paying per second that I run
[07:39:55] this database on some other server. So
[07:39:58] we can optimize these queries. But let's
[07:40:00] first get a sense of how they're
[07:40:02] presently running. Like what is SQLite
[07:40:04] doing underneath the hood? defined this
[07:40:07] movie called Cars. Well, for that I'll
[07:40:09] bring up a certain visual here of our
[07:40:11] titles column. So imagine here that we
[07:40:15] have a uh sort of smaller database
[07:40:17] called movies that just has titles in
[07:40:19] this case. And now I want to search
[07:40:21] these titles. But I'm a computer. I'm
[07:40:24] not a human. Meaning I can only look at
[07:40:27] one item at a time. I can only look at
[07:40:30] one row and check its title. Now, if I
[07:40:34] want to find the row or the rows that
[07:40:37] have cars in them, what's the best I
[07:40:40] could do? If my titles are not sorted,
[07:40:44] what's the best approach I could take
[07:40:45] here? If I can only look at one row at a
[07:40:48] time, how might I search this column?
[07:40:52] >> You should use a linear search then,
[07:40:54] right?
[07:40:55] >> So, I like your intuition. There is an
[07:40:57] algorithm, a step-by-step process called
[07:40:59] linear search where we look at one
[07:41:01] element at a time or in this case one
[07:41:04] row at a time. That's exactly what we
[07:41:06] can do for this table. I can look at one
[07:41:09] row at a time to find is this title in
[07:41:11] this column or is it not. So here to
[07:41:14] visualize I could take this title
[07:41:16] column. I can only look at one at a
[07:41:19] time. But if this data is not sorted, I
[07:41:23] can do no better than looking at every
[07:41:25] row exactly once. So here we start with
[07:41:28] Toy Story. We ask, is Toy Story equal to
[07:41:31] Cars? It's not. So we'll keep going.
[07:41:34] Here I'll check Cars 3. Is Cars 3
[07:41:37] strictly equal to Cars? I mean, it has
[07:41:39] Cars in it, but it's not Cars exactly.
[07:41:42] So I'll keep going. I'll look at Frozen.
[07:41:44] And Frozen is not cars either. So I'll
[07:41:47] keep going again. And here I see cars.
[07:41:50] So maybe I could stop here.
[07:41:53] But why couldn't I? Well, if I need to
[07:41:57] find not just the one row that has cars,
[07:42:00] but all the rows that have cars, I have
[07:42:03] to keep going to see is cars elsewhere
[07:42:06] in this column. Is it not just here, but
[07:42:08] also in other rows, too? So, I'll keep
[07:42:10] going. I'll look at Wall-E, Ratatouille,
[07:42:13] Soul turning red until I get to the end
[07:42:16] of this column. And this process is
[07:42:18] called a scan of the table. We're
[07:42:21] scanning our column top to bottom
[07:42:24] looking for the result that we need to
[07:42:26] find. But it turns out we can actually
[07:42:29] optimize this search. We can do a bit
[07:42:31] better than going one by one by one by
[07:42:34] one. And for this we need a bit of a a
[07:42:36] metaphor to think about how we can
[07:42:38] search our table. So if you have ever
[07:42:40] seen a kind of textbook, you might have
[07:42:42] seen something a bit like this here.
[07:42:44] This is a handbook of education
[07:42:46] research. And maybe I want to find which
[07:42:49] pages correspond to how students learn
[07:42:52] computer science. So one thing I could
[07:42:54] do is open to the start of the book. I
[07:42:56] could go kind of page by page looking
[07:42:58] for which pages have how students learn
[07:43:02] computer science. I keep going here. And
[07:43:05] if I want to find all the pages that
[07:43:07] have how students learn computer science
[07:43:09] on them, I can do no better than going
[07:43:11] through everyone one by one by one until
[07:43:14] I'm at the end of this textbook. But
[07:43:17] chances are you yourself don't do this.
[07:43:20] You do something better. And there's
[07:43:24] some built-in structure in this book
[07:43:26] that could help you find what you're
[07:43:28] looking for. What might you use to find
[07:43:30] something in a textbook or some other
[07:43:32] book, too? We can use the index of the
[07:43:37] book.
[07:43:38] >> You can use the index. So often a book
[07:43:40] like a textbook has something at the
[07:43:42] very back of the book that tells me all
[07:43:45] the subjects that are inside this book
[07:43:47] but in alphabetical order. So I can see
[07:43:49] here there's a subject index in the back
[07:43:51] of the book here that lists the subjects
[07:43:53] in alphabetical order A to Z. And if I
[07:43:56] want to find how students learn computer
[07:43:57] science, I could perhaps search for
[07:43:59] computer science in this index. I could
[07:44:01] find A B C. Oh, there's C. And here I
[07:44:04] see computer science. Now I know all the
[07:44:06] pages I need to look at inside this book
[07:44:09] without going through each of them one
[07:44:12] by one by one. So in the same way that
[07:44:15] books have an index, so too can
[07:44:17] databases and tables have an index as
[07:44:20] well. So let's see a definition here for
[07:44:22] what an index is. Well, an index is a
[07:44:26] structure that we can use. It's built
[07:44:28] into our database to help us speed up
[07:44:30] the retrieval of rows from that table. I
[07:44:34] first search my index, find out what
[07:44:37] rows my given search term is in, and
[07:44:40] then look those rows up in my table.
[07:44:44] Now, if I want to create an index on a
[07:44:46] table, I can use some SQL syntax. I can
[07:44:50] say create index and give it some name.
[07:44:55] But I need to also specify a few other
[07:44:57] things like similar to my books index.
[07:45:00] That index has some content. It's an
[07:45:03] index by subject or an index by author.
[07:45:06] So I need to have tell this index what
[07:45:08] to include. So I should also say create
[07:45:11] index give it a name on some table and
[07:45:15] some columns in that table telling my
[07:45:17] index what data from my table it should
[07:45:21] include. So let's create our very own
[07:45:24] index in the movies table to identify
[07:45:27] how we can make this query just a bit
[07:45:28] faster overall. So I'll come back to my
[07:45:31] computer here and let's now try to
[07:45:34] create this index. I will open up a new
[07:45:37] tab here, a new tab and then I'll log
[07:45:40] back into my database. I'll say SQLite 3
[07:45:43] movies. DB. And now I want to first
[07:45:47] create some index here. So, I'll turn my
[07:45:50] timer back on. And now I'll type the
[07:45:53] syntax we just learned. I want to create
[07:45:55] an index. And if I'm searching my title
[07:45:59] column in movies, I should probably
[07:46:02] include the title column in this index.
[07:46:05] So, I'll say call this the title index
[07:46:08] here. It'll be on the movies table and
[07:46:11] it'll contain the data in the title
[07:46:13] column of movies. A bit like this. Now
[07:46:17] I'll hit enter and I'll see this index
[07:46:20] took some time to be created. There's
[07:46:22] some stuff going on underneath the hood
[07:46:24] where I'm putting this data in a new
[07:46:26] structure. We're calling the index here.
[07:46:28] But now if I rerun this query, if I say
[07:46:31] select star from movies, select star
[07:46:35] from movies where the title equals cars
[07:46:39] semicolon.
[07:46:42] It's a lot faster. Here I see 0.01. 01
[07:46:47] seconds real time compared to 0.084
[07:46:52] seconds. That's a savings of almost
[07:46:54] eight times like almost eight times
[07:46:56] faster now that we have this index. Now,
[07:46:59] it took some time to create the index.
[07:47:01] If I run just a few queries, I much
[07:47:04] easily make that time up in terms of the
[07:47:07] time I'm using on my server to look up
[07:47:10] these kinds of pieces of information.
[07:47:13] Okay, so let's actually take a look at
[07:47:16] how we can ensure a query is using some
[07:47:19] index. Here I just kind of taking it on
[07:47:22] my word like here it was faster so it
[07:47:24] used the index but there is a way for
[07:47:26] you to know whether an index was used. I
[07:47:29] could use a SQL statement called explain
[07:47:32] query plan. Other DBMS's might call this
[07:47:36] just simply explain but in SQL write
[07:47:38] it's explain query plan and then after
[07:47:42] explain query plan I can type the query
[07:47:45] that I want to learn the plan for that
[07:47:48] is how does SQLite plan to find me this
[07:47:51] information how does it plan to execute
[07:47:53] this query so now I'll type select star
[07:47:57] from movies where title equals cars like
[07:48:01] this semicolon I'll hit Enter. And now I
[07:48:04] don't get the results, but I do get the
[07:48:07] plan SQLite intends to use to find me
[07:48:11] this result. And take a look here. I see
[07:48:14] query plan. And underneath I see what
[07:48:17] SQLite intends to do. It will search the
[07:48:20] movies table, but it will do so using
[07:48:23] the index that we called title index.
[07:48:25] And it will do so given some value for
[07:48:28] title here. So we can actually see
[07:48:31] SQLite does plan to use the index to
[07:48:33] speed up this query. We can confirm that
[07:48:36] this is exactly what's happening. But
[07:48:39] let me try now to remove this index and
[07:48:42] see what SQLite would have done when we
[07:48:45] didn't have this index. I'll come back
[07:48:47] over here and I'll go back to my other
[07:48:49] connection to my database. This one over
[07:48:52] here. And now I'll remove the index we
[07:48:55] just created. To remove an index I can
[07:48:57] drop it. I can say drop index title
[07:49:01] index semicolon. And now that took it
[07:49:04] just a small amount of time, but now I
[07:49:05] don't have that index anymore. I can
[07:49:07] type dos schema and I'll see that that
[07:49:09] index is not part of my schema. But now
[07:49:13] if I try explain query plan select star
[07:49:18] from movies where title equals cars
[07:49:23] semicolon.
[07:49:25] I'll see that the plan is not to use the
[07:49:27] index. The plan is to scan movies where
[07:49:30] scan we saw before means to go top to
[07:49:33] bottom through that title column and
[07:49:35] find me all the rows that have cars in
[07:49:38] them. So we can see here the
[07:49:40] optimization we're already making by
[07:49:42] using this index here.
[07:49:46] Okay, so let's take a moment here and
[07:49:48] pause. What questions do we have about
[07:49:51] indexes and how they're used in this
[07:49:53] case? Doesn't uh databases have implicit
[07:49:58] algorithms to optimize search?
[07:50:01] Yeah, good question. Do databases have
[07:50:03] implicit algorithms to optimize search?
[07:50:06] They do for some columns. So if we saw
[07:50:09] in our table earlier, we had a primary
[07:50:12] key column like ID in SQLite and most
[07:50:15] other DBMS's. If I specify that a column
[07:50:18] is a primary key, then that database
[07:50:20] management system will automatically
[07:50:22] create an index v which I can search for
[07:50:24] a primary key. If though I have a
[07:50:27] regular old column like title or like
[07:50:30] year or so on, it doesn't go through the
[07:50:32] process of automatically optimizing that
[07:50:34] search for me. I have to do that myself
[07:50:37] as we're doing here.
[07:50:39] >> Let's take one more.
[07:50:40] >> Would it be advisable to create a
[07:50:42] different index for every column in case
[07:50:44] we need it? Yeah, I mean it seems like
[07:50:46] indexes are so good. They speed up
[07:50:48] queries for us. Why not create an index
[07:50:50] on every column we have? Well, as we'll
[07:50:52] see in just a moment, there are some
[07:50:54] tradeoffs involving space and also the
[07:50:57] time it later takes us to insert or add
[07:50:59] new data. So, good questions. I'll come
[07:51:01] back to my laptop where we can continue
[07:51:03] on. So, we've seen how uh indexes can
[07:51:06] speed up queries and we've we're
[07:51:08] searching for one column here, but they
[07:51:10] could also speed up queries across
[07:51:12] multiple tables. So, let's try a
[07:51:14] different kind of query here. What I
[07:51:16] might do now is try to find all of those
[07:51:19] movies that Tom Hanks starred in. And we
[07:51:23] did a bit of a um example of this a
[07:51:25] little earlier visually, but my goal is
[07:51:27] to find all of those titles that Tom
[07:51:29] Hanks played a role in. Well, if my goal
[07:51:32] is to end up with titles of movies, I
[07:51:35] could try selecting title from the
[07:51:38] movies column like this. But if I look
[07:51:41] at that movies table, I'll know I only
[07:51:44] have titles, year, and the ID of those
[07:51:47] movies. I don't have anything related to
[07:51:49] Tom Hanks. Well, Tom Hanks, though, is
[07:51:52] probably showing up in the stars table
[07:51:54] where I could correspond Tom Hanks's ID
[07:51:57] with the movie IDs that Tom Hanks played
[07:51:59] a role in. So, let me try filtering
[07:52:01] these movies by an ID. I'll say where
[07:52:03] the ID of that movie is in some list of
[07:52:06] movie IDs that also correspond with Tom
[07:52:09] Hanks's person ID. So I'll make a
[07:52:11] subquery here to find exactly those
[07:52:14] films. Now I'll say select movie ID from
[07:52:18] stars where the person ID is equal to
[07:52:23] well I don't know Tom Hanks's person ID.
[07:52:25] I could try to hardcode it here, but I
[07:52:27] could do better by having another
[07:52:29] subquery to find what is Tom Hanks's ID.
[07:52:33] Now I'll indent not just four times, but
[07:52:35] eight to show this is my next level of a
[07:52:38] subquery. Here I'll now select ID from
[07:52:42] people where the name equals Tom Hanks.
[07:52:46] Tom Hanks like this. And now I can close
[07:52:49] out my sub queries. I've found the ID of
[07:52:52] Tom Hanks. I've found those movie IDs
[07:52:55] that correspond with the person ID of
[07:52:57] Tom Hanks. And then I found the titles
[07:53:00] that correspond to those movie IDs. Now
[07:53:02] I'll hit a semicolon here, press enter,
[07:53:05] and I should see I get back all of Tom
[07:53:07] Hanks's movies, all of those that he
[07:53:09] played a role in, and I'll also see the
[07:53:12] time that it took. The real time for
[07:53:14] this query was about 0.197
[07:53:17] seconds. So getting a little bit slower
[07:53:19] now that we're looking across multiple
[07:53:21] tables and having multiple sub queries.
[07:53:24] Well, an index could speed this up as
[07:53:27] well. I can make a um new terminal here.
[07:53:31] And let me open up the connection in my
[07:53:32] database. Again, I'll say SQLite 3
[07:53:34] movies. DB. And now I should figure out
[07:53:38] what columns do I need to index to speed
[07:53:41] up this query. Well, one thing I could
[07:53:44] do is try explain query plan. Again, I
[07:53:47] want to understand what SQLite plans to
[07:53:50] do to execute this query. So, I'll
[07:53:52] explain query plan and I'll type in the
[07:53:55] same query from before. I'll say select
[07:53:57] the title from movies where the ID is in
[07:54:02] those movies that Tom Hanks played a
[07:54:04] role in. So I'll select in this case
[07:54:07] movie ID movie ID from the stars table
[07:54:12] where the person ID equals Tom Hanks's
[07:54:15] ID. Now I'll find that I'll indent eight
[07:54:18] times to show this is my next level
[07:54:20] subquery. I'll select ID from people
[07:54:24] where name equals Tom Hanks. And I'll
[07:54:28] wrap the line just a little bit. Let me
[07:54:30] zoom out so you can see it all in one
[07:54:31] go. And now I'll close out these sub
[07:54:33] queries just like this.
[07:54:36] Hit enter. And I should see if I zoom
[07:54:39] back in the plan SQLite intends to use
[07:54:42] to find me the results of this query.
[07:54:44] Now let's take a look here. I'm planning
[07:54:47] to first scan people. To understand the
[07:54:50] structure of this, I need to first go
[07:54:51] all the way in to this bottom part here.
[07:54:53] I'm going to scan people to find
[07:54:56] presumably Tom Hanks's ID. Then after I
[07:55:00] do that, I'm going to scan stars
[07:55:03] presumably to find all the movie IDs
[07:55:06] that have Tom Hanks's ID. But then up
[07:55:09] here, I'm finally going to search movies
[07:55:12] using integer primary key. Some index is
[07:55:15] automatically created for me as we saw
[07:55:17] before for my primary keys. So it seems
[07:55:20] like the optimization here could be in
[07:55:23] the people table and the stars table.
[07:55:27] Now let me ask if I wanted to create an
[07:55:30] index on either the people table or the
[07:55:34] stars table. What do you think I should
[07:55:36] include? Which column should I include
[07:55:38] in this index given my query here?
[07:55:43] What column should I include in this
[07:55:44] index given this previous query?
[07:55:48] >> We could index the uh ID and the name of
[07:55:52] the person.
[07:55:54] >> Yeah, a good idea. index the ID and the
[07:55:56] name of the person. So if we look at
[07:55:57] this query again, we'll see that our
[07:56:00] wear clause here is um searching by the
[07:56:03] name in the people table. And up here,
[07:56:06] this wear clause is searching by the
[07:56:07] person ID column in our stars table. So
[07:56:11] it would stand a reason that I should
[07:56:13] actually create an index that includes
[07:56:15] the name column in people and the person
[07:56:18] ID column in stars. Perhaps two separate
[07:56:20] indexes, one for each here. So let's go
[07:56:23] ahead and create those. Now I'll come
[07:56:25] back to my computer and here I will try
[07:56:29] to create this index. I'll say first
[07:56:32] create an index. Create index called
[07:56:35] person index. And I'll create it on
[07:56:38] stars and the person ID column in stars
[07:56:43] as we just discussed. Now if I hit
[07:56:46] enter, I should let it take some time to
[07:56:49] build up this index. But now I can also
[07:56:52] create my next one. I'll say create
[07:56:55] index and then I'll choose name index on
[07:57:00] the people uh on people table and I'll
[07:57:02] include the name column here. So now
[07:57:05] I'll hit enter. That too will take some
[07:57:08] time to run. But now if I try to explain
[07:57:11] the query plan again I'll clear my
[07:57:13] screen try explain query plan
[07:57:16] and then I'll type in this query again.
[07:57:18] I'll say select title from movies where
[07:57:20] the ID is in those movies that Tom Hanks
[07:57:24] played a role in that have the person ID
[07:57:25] next to it. Then I'll say um which is
[07:57:29] Tom Hanks's ID. And I'll close out this
[07:57:31] subquery here just like this.
[07:57:35] And now if I explain the plan yet again
[07:57:39] I should see I'm now optimizing this
[07:57:42] query even further. I can see down below
[07:57:44] here, my plan is to search the people
[07:57:46] table. Not to scan it, but to search it
[07:57:49] using what we call a covering index
[07:57:51] called name index, the one we just
[07:57:53] created. We'll explain covering index in
[07:57:55] just a little bit. Next though, I'm
[07:57:58] going to search stars using the index we
[07:58:00] just created called person index given
[07:58:03] some person ID. And then finally, I'll
[07:58:06] search movies using an integer primary
[07:58:08] key index, the one that's automatically
[07:58:10] created for me here. So here we see some
[07:58:14] new vocabulary, not just using index,
[07:58:17] but using a covering index. What is a
[07:58:21] covering index? A covering index, it
[07:58:24] turns out, is is still an index. It's
[07:58:26] the same kind of idea, but it is one in
[07:58:28] which we have all the data we need
[07:58:31] inside the index itself. It's one in
[07:58:34] which the query data can be found only
[07:58:36] by searching the index. There's no need
[07:58:39] for me to go from the index to the
[07:58:41] table. I can just look it up in the
[07:58:43] index. It's similar to me searching this
[07:58:46] textbook and getting to the index and
[07:58:48] not then needing to actually go back in
[07:58:50] the book's pages, I can find everything
[07:58:53] I'm looking for in the index itself. And
[07:58:56] this is good because if I need to not
[07:58:59] just find the items in my index, but
[07:59:01] then look them up in my table, like that
[07:59:03] look up in the table takes some time. So
[07:59:06] if I instead have a covering index, one
[07:59:08] that includes all data I want to find
[07:59:11] exactly right there in it, that's going
[07:59:12] to be faster for me than a regular old
[07:59:15] index. So let's try then turning one
[07:59:19] more index into a covering index. I'll
[07:59:22] come back over here and we saw before
[07:59:24] that we had the um index on the stars
[07:59:28] table using just a regular old index
[07:59:30] using index person index. But what are
[07:59:34] we trying to find from this index? We're
[07:59:37] trying to find the movie ID column. So I
[07:59:40] could create an index that includes the
[07:59:43] movie ID column as well. I can have
[07:59:46] indexes that span multiple columns. So
[07:59:49] let's try that here. I'll come back over
[07:59:52] and I'll create this new index that
[07:59:54] intends to cover our search here. I want
[07:59:57] to include not just the person ID column
[08:00:01] but also the movie ID column so I can
[08:00:03] quickly find that data inside the index
[08:00:06] itself. Let me drop our current
[08:00:09] implementation of the of the person
[08:00:11] index like this. I'll hit semicolon
[08:00:13] here. And now that index is gone. But if
[08:00:16] I type now create index I'll also call
[08:00:20] this person index on stars. and I'll say
[08:00:24] let's include not just the person ID
[08:00:26] column, let's also include in this case
[08:00:29] the movie ID column like this. Now I'll
[08:00:33] hit semicolon enter and that'll take a
[08:00:36] bit of time to run but once it's done I
[08:00:39] can probably try to explain the query
[08:00:41] plan again and see if we have our
[08:00:43] covering index. I'll go back up top
[08:00:45] here. I'll explain query plan and I'll
[08:00:48] choose to recreate this query from
[08:00:49] before just like this. going to select
[08:00:52] the uh movie ID from stars and then find
[08:00:56] Tom Hanks's ID and then close out these
[08:00:58] subqueries here
[08:01:01] just like this.
[08:01:03] And now once I explain query plan, we've
[08:01:07] optimized even further. Now I have two
[08:01:10] covering indexes. I can find all the
[08:01:12] information I need just by looking in
[08:01:15] these indexes, not by doing a table
[08:01:17] lookup. So let's now run this query and
[08:01:21] see just how much faster it might be.
[08:01:24] Come back to my laptop here and let's
[08:01:25] get rid of explain query plan. Let's now
[08:01:28] turn our timer on. I'll turn timer on
[08:01:30] like this and I'll rerun this query.
[08:01:33] I'll say we select title for movies
[08:01:35] where the ID is in the stars table. So
[08:01:38] long as the movie ID aligns with the
[08:01:40] person ID. Then I'll find Tom Hanks's
[08:01:42] person ID here. I'll close out my sub
[08:01:44] queries and I should be able to find
[08:01:47] that this query is just a little bit
[08:01:51] there's an understatement here a lot
[08:01:53] faster. So if I go back to my old query
[08:01:55] here I'll see this one took 0.197
[08:01:58] seconds. This one with two covering
[08:02:01] indexes takes 0.004
[08:02:04] seconds. This is an order of magnitude
[08:02:06] faster than my prior query because I've
[08:02:09] used indexes now. So let's see if we
[08:02:15] have all these benefits of indexes, we
[08:02:18] must be paying something like if I have
[08:02:21] this book here and I'm trying to find
[08:02:23] some data inside of it. What might the
[08:02:27] tradeoffs be? If I want to create an
[08:02:30] index, maybe think first about this
[08:02:32] database on my computer. What am I
[08:02:35] giving up? I'm making sure my query is
[08:02:37] faster. What am I losing? Do you think
[08:02:41] >> space we required for indexing also the
[08:02:43] more index we would have the more space
[08:02:46] and more memory we would have to consume
[08:02:47] for that?
[08:02:49] >> Yeah. Uh so it's a general theme that
[08:02:50] when I try to speed up something in
[08:02:52] computer science I have to pay some cost
[08:02:55] which is often in terms of space that
[08:02:57] when I create an index I'm using more
[08:02:59] space in my database and this similarly
[08:03:02] applies to a oldfashioned textbook like
[08:03:04] if I have an index in here I'm literally
[08:03:06] paying in pages to print so people can
[08:03:09] find content better. This is some extra
[08:03:12] money I have to spend, extra pages I
[08:03:14] have to print in order to make my
[08:03:15] queries faster either on this book or in
[08:03:19] my database. So let's understand why
[08:03:22] indexes take up so much space by looking
[08:03:25] at the underlying data structure they
[08:03:27] use to store information. Well, it turns
[08:03:30] out that the part of the reason indexes
[08:03:33] take up so much space is because they
[08:03:35] use a certain data structure, a way of
[08:03:37] organizing data called a B tree or a
[08:03:41] balanced tree structure. So, not to
[08:03:44] worry if you don't know what a tree
[08:03:45] structure is. Here's a visual to keep in
[08:03:47] mind as you think about using trees in
[08:03:50] computer science and in indexes in
[08:03:51] particular. A tree might look a bit like
[08:03:54] this. And notice how it's similar to a
[08:03:56] family tree with grandparents and
[08:03:59] parents and children and so on. You
[08:04:02] could, if you wanted to, kind of do a
[08:04:04] 180 on this diagram, flip it right side
[08:04:06] up. And now you might see more of a tree
[08:04:08] structure going from top to bottom. You
[08:04:11] could see down here, what we might call
[08:04:12] the trunk of the tree, followed by some
[08:04:15] branches, these over here, and then the
[08:04:17] leaves, these up top, kind of the edge
[08:04:19] of this tree diagram. And there's a few
[08:04:22] vocabulary words you might want to know
[08:04:24] when you talk about trees. One of them
[08:04:27] is this idea of a node. So this right
[08:04:30] here is a single node in our tree. A
[08:04:33] tree is made up of a collection of
[08:04:36] nodes. And each of these nodes stores
[08:04:39] some value. Maybe it's a value in the
[08:04:42] column we're trying to index, for
[08:04:44] example. But in addition to that value,
[08:04:47] this node also stores pointers, kind of
[08:04:51] arrows metaphorically, to other nodes to
[08:04:54] tell us where in memory these nodes are.
[08:04:58] And by stringing these nodes together,
[08:04:59] we can build up this treel like
[08:05:02] structure. Now, this node here points to
[08:05:06] three other nodes. And some new
[08:05:08] vocabulary here is that this node has
[08:05:11] three children. Going back to that
[08:05:13] family tree example, we see that this
[08:05:15] node here has three children, which are
[08:05:17] these right here. But these nodes
[08:05:20] themselves also have three children of
[08:05:22] their own. So if I were to go down to
[08:05:24] the next level of our tree, well, if I'm
[08:05:26] referring to this node here, these nodes
[08:05:28] down below are that node's
[08:05:30] grandchildren, the children of its
[08:05:33] children. Now, these nodes here also
[08:05:36] have another name. We saw it before.
[08:05:39] They're often called leaf nodes. or the
[08:05:41] edge of our tree. And we know a node is
[08:05:43] a leaf node when there are no other
[08:05:45] nodes it points to. So this is the
[08:05:49] general idea of what an index looks
[08:05:52] like. But let's get a little more
[08:05:53] concrete and try to build an index from
[08:05:56] our title column in our movies table
[08:05:58] here. So let's assume we have a table of
[08:06:02] ids and titles here. And I want to
[08:06:05] create an index on this title column to
[08:06:08] search it more efficiently. Well, we saw
[08:06:11] before that the best I can do when this
[08:06:13] data is unsorted is to go top to bottom.
[08:06:16] First look at Toy Story, then look at
[08:06:18] Cars 3, then look at Frozen, all the way
[08:06:20] down to the bottom. I can only scan this
[08:06:23] column, so to speak. But I know I could
[08:06:26] probably do a little better if the data
[08:06:28] is sorted. If the data is sorted, I
[08:06:30] could look roughly in the middle and if
[08:06:32] I've gone too far, go back a little bit.
[08:06:34] or if I haven't gone far enough, go
[08:06:36] forward a little bit and do a fewer
[08:06:37] number of lookups to find the I'm
[08:06:40] looking for. So, let me sort this title
[08:06:42] column. I'll put it like this.
[08:06:46] What have I done wrong?
[08:06:49] First, I had this.
[08:06:51] Then, I wanted to sort my title column
[08:06:54] to make it faster to search.
[08:06:57] But what did I what rule did I break
[08:07:00] here by sorting this title column like
[08:07:02] that?
[08:07:03] >> Yes, Carter. The thing is that by
[08:07:04] sorting only the movie's name and not
[08:07:06] the ID, you will break uh the entire
[08:07:09] other databases that relates to that
[08:07:12] one. So for example, let's look for a
[08:07:15] movie in which I don't know Johnny Depp
[08:07:18] is working or has work done and the
[08:07:20] result may be I don't know Titanic.
[08:07:23] >> Yeah, I love that example that really
[08:07:25] drives it home here. And in more general
[08:07:27] terms like I had this primary key called
[08:07:30] ID and in the prior state I had Toy
[08:07:33] Story with the ID of 114709.
[08:07:37] A primary key means that Toy Story
[08:07:40] should be consistently identified with
[08:07:42] this number 114709.
[08:07:46] But to your point Matteo, if I sort only
[08:07:48] the title column, well now cars has that
[08:07:52] ID 11479,
[08:07:54] I've broken that relationship.
[08:07:56] particularly if other tables are relying
[08:07:58] on uh Toy Story being identified by 1
[08:08:02] 14709.
[08:08:04] So I can't do this. This is bad. I need
[08:08:07] some other way to sort my title column.
[08:08:10] So let's bring this back to what it was
[08:08:12] here. Let me focus just on the title
[08:08:15] column. Well, I can't sort this title
[08:08:18] column because it's part of my table and
[08:08:21] the ordering of that table does matter.
[08:08:24] What I could do though is create a copy
[08:08:26] of this column and maybe sort that copy.
[08:08:29] So I'll literally create a copy of this
[08:08:31] title column elsewhere in memory. And
[08:08:33] let me just remove this title column
[08:08:35] identifier here. So I have just the
[08:08:37] data, just the data in this column
[08:08:39] somewhere else in memory. And now I
[08:08:42] could sort this data like this. So let's
[08:08:45] say I now want to find cars. Well, now
[08:08:49] that my data is sorted, what could I do?
[08:08:51] I could look first in the middle at
[08:08:53] Ratatouille, for instance, and then
[08:08:55] realize, well, cars comes before
[08:08:57] Ratatouille. Maybe I'll go a little
[08:08:59] higher in my index here. I'll search in
[08:09:02] the middle of this first half. I'll look
[08:09:04] at, in this case, Frozen. And cars,
[08:09:06] well, it still comes before Frozen. So,
[08:09:08] let me look up at the first half of this
[08:09:11] first half. I'll then go up here and
[08:09:13] I'll have spotted cars. So, a much
[08:09:15] faster way to search for information now
[08:09:18] once I have it sorted.
[08:09:21] But I don't think we're quite there yet.
[08:09:23] Like if I wanted to find the year that
[08:09:26] cars was released. I found that it's in
[08:09:29] my title column. But what am I not able
[08:09:32] to do at this point? I've copied the
[08:09:36] data somewhere else. But now I want to
[08:09:38] find some other data in my table. What
[08:09:40] can't I do?
[08:09:43] >> We need to point to index. Yeah, I need
[08:09:46] to be able to find some way to relate
[08:09:48] this index with the rows in my table. So
[08:09:52] here, this is elsewhere in memory. It's
[08:09:54] good that I can find that cars is in my
[08:09:57] title column. But if I want to find the
[08:10:00] other data in this row, like the year
[08:10:02] that cars was released, well, I have to
[08:10:04] have some way of linking this uh this
[08:10:07] data here, cars, to my table. So often
[08:10:11] in an index, we not just copy the data
[08:10:13] to some new location and sort it. will
[08:10:15] also have some link between these index
[08:10:18] pieces of data over here and our rows in
[08:10:20] our table back here. So for instance,
[08:10:23] here is cars and cars appears to be in
[08:10:27] row four. Similarly, cars three looks to
[08:10:30] be in row two in my table and I could
[08:10:33] metaphorically visually draw some lines
[08:10:36] between cars over here in my index and
[08:10:40] cars in my table. I could draw one that
[08:10:42] looks a bit like this. Going from cars,
[08:10:44] my index to actually cars in my table. I
[08:10:47] could draw one for cars three going from
[08:10:50] this index place here to row two in my
[08:10:53] title column. So that is the way I can
[08:10:56] link my index with my table data. I
[08:10:59] could do the rest of these two for all
[08:11:01] of my other pieces of data in my index.
[08:11:06] So let's focus on this now like just to
[08:11:08] check for understanding. I have this
[08:11:10] index. That index has my sorted title
[08:11:13] data and also the row number in which I
[08:11:17] found that piece of data. So let's say
[08:11:19] here I want to find the movie soul. I
[08:11:23] want to find the movie soul. How could I
[08:11:26] find soul in my index?
[08:11:31] >> Yeah, since it is already sorted, I
[08:11:34] believe you could use binary search.
[08:11:36] >> Yeah, I could use algorithm called
[08:11:37] binary search. which if you're not
[08:11:38] familiar simply means start in the
[08:11:40] middle and if I've gone too far look in
[08:11:43] either the left half or the right half
[08:11:44] and repeat that process over and over.
[08:11:47] So here is my index again. I'll go
[08:11:49] roughly to the middle and I'll look at
[08:11:51] Ratatouille here. Well, soul I know
[08:11:54] comes after Ratatouille alphabetically.
[08:11:56] So what should I do? I should now look
[08:11:59] in this second half here. I might go to
[08:12:01] Toy Story. Well, once I see Toy Story, I
[08:12:04] know I've gone a little bit too far.
[08:12:05] like soul comes before Toy Story
[08:12:08] alphabetically. So I'll look in the
[08:12:10] first half of this second half and what
[08:12:12] do I see? I see soul right there. Okay,
[08:12:17] so our index seems to be working. It
[08:12:20] allows me to more efficiently find data.
[08:12:22] I no longer have to look through every
[08:12:24] single row. I can simply use a more
[08:12:26] efficient algorithm like binary search.
[08:12:30] But now there's one more catch, which is
[08:12:33] if I had many, many, many rows, not just
[08:12:36] nine, but literally thousands or
[08:12:38] hundreds of thousands or millions of
[08:12:40] rows in this index, like that's a lot of
[08:12:43] data to store in one location in memory
[08:12:46] or even to load into my computer's RAM,
[08:12:49] so to speak. It's random access memory,
[08:12:51] so it can do all this jumping around.
[08:12:54] Ideally, what I would do is break this
[08:12:56] index up into smaller pieces. So, I
[08:12:59] don't have to load all of this at once.
[08:13:01] And in reality, our index is not a
[08:13:03] single column like this, but often
[08:13:06] individual nodes where each of these 1 2
[08:13:10] 3 might be some node scattered about the
[08:13:14] computer's memory. But what problem have
[08:13:17] I introduced now? If these are around
[08:13:19] the computer's memory, I can't actually
[08:13:21] jump between them anymore. I can't go
[08:13:24] maybe one space above Toy Story and find
[08:13:26] Soul. This node might be elsewhere in
[08:13:29] memory. And so, we'll need some other
[08:13:32] nodes to actually help us find what
[08:13:35] we're looking for in this index. I might
[08:13:37] have one more over here that tells me
[08:13:41] what kind of data is in each of these
[08:13:43] nodes. Maybe I have one here that has
[08:13:46] both frozen and soul. Notice how here
[08:13:49] frozen is the furthest down
[08:13:52] alphabetically in this node up here. And
[08:13:54] notice down below here, soul is the
[08:13:56] furthest down alphabetically in this
[08:13:59] node here. That is, if what I'm looking
[08:14:02] for comes before frozen, I should look
[08:14:05] at this node. If what I'm looking for
[08:14:07] comes after frozen but before soul, I
[08:14:10] should look in this node. Or if what I'm
[08:14:13] looking for comes before none of these,
[08:14:15] it comes after soul, I should look at
[08:14:18] this node down here. So let's find an
[08:14:21] example. Let's say I want to find cars
[08:14:23] now. Well, I'd start in this root node,
[08:14:26] the face of this tree we're building
[08:14:28] here that I've turned kind of right side
[08:14:30] this way. Let's say frozen. I'll go
[08:14:33] here. And does cars come before Frozen?
[08:14:36] Well, it does. So I'll look in this node
[08:14:39] now. I'll come up here and I'll find
[08:14:41] cars in that node. Let's see here. Maybe
[08:14:45] I want to find Ratatouille. I'll go back
[08:14:47] to the beginning and I'll look through
[08:14:49] this par this root node. I'll say, does
[08:14:51] Ratatouille come before Frozen?
[08:14:54] It doesn't. It comes after Frozen. So,
[08:14:56] I'll look and check soul. Does
[08:14:58] Ratatouille come before Soul? Well, it
[08:15:01] does. So, I'll look in this node now.
[08:15:03] I'll go find Luca. And not quite there
[08:15:05] yet, but I will see Ratatouille. So I
[08:15:08] know that I've now found Ratatouille in
[08:15:10] my index. And now for one more, let me
[08:15:13] check for understanding here. How could
[08:15:15] I find turning red? What steps would I
[08:15:19] follow to find turning red? I might
[08:15:24] start at that root node, but then what
[08:15:27] questions should I ask
[08:15:29] >> from um frozen or so? We can see uh
[08:15:33] rather two to the right. So that we move
[08:15:36] in the direction of so and once we get
[08:15:39] there we find the middle elements and we
[08:15:41] can see two ways to the right of um the
[08:15:45] middle element. So that's how we find
[08:15:47] it. Divide the list into two halves and
[08:15:51] look into the half that the element is
[08:15:54] found.
[08:15:55] >> Yeah, I like what you're thinking here.
[08:15:56] So you're talking about traversing this
[08:15:59] tree we've built and turned on its side
[08:16:00] here. And let's visualize that search
[08:16:02] here. So, first we'll start at Frozen
[08:16:05] and ask, does Turning Red come before
[08:16:07] Frozen? It doesn't. It comes after. So,
[08:16:10] I'll keep looking. I'll look at Soul.
[08:16:12] Does Turning Red come before Soul? Well,
[08:16:14] it doesn't. It comes after Soul. So, I
[08:16:17] know I need to look at this node down
[08:16:20] here. I'll go find Toy Story. Not quite
[08:16:22] there yet. But now I'll see Turning Red.
[08:16:25] I'm able to find what I'm looking for.
[08:16:27] And not just that, I can find what row
[08:16:30] number Turning Red is actually in. in my
[08:16:33] table. So when you use an index, SQL or
[08:16:36] SQLite is using some algorithm a bit
[08:16:39] like this. It creates some tree
[08:16:41] structure a bit like this here with
[08:16:43] individual nodes that has your column
[08:16:45] data. It then uses this kind of
[08:16:47] algorithm to search that index and find
[08:16:50] whether or not that piece of data is in
[08:16:53] your index. And if it is, it will go
[08:16:55] ahead and look up that piece of data in
[08:16:57] your table. So see here, although this
[08:17:00] is turned on its side, the relationship
[08:17:03] between a kind of tree, we had a root
[08:17:06] node or a a trunk node here pointing to
[08:17:09] some of these leaf nodes, the edges of
[08:17:11] our graph right here. And you can see
[08:17:13] some relationship between these nodes
[08:17:15] here and our tree as well right here
[08:17:18] with arrows pointing across these
[08:17:20] individual nodes.
[08:17:23] So let me pause here and ask what
[08:17:25] questions do we have on this structure
[08:17:28] and how we've searched it.
[08:17:30] >> Uh is that related to linked lists or
[08:17:34] arrays?
[08:17:35] >> Uh good question. Is this related to
[08:17:37] linked lists or arrays? So if you're
[08:17:39] familiar, a linked list is some set of
[08:17:42] nodes that have been linked together in
[08:17:43] memory using these arrows like we saw on
[08:17:46] our diagram here. It is the case that
[08:17:48] sometimes an index will include a linked
[08:17:51] list.
[08:17:54] Let's take one more here. I want to know
[08:17:57] uh covering index what how is the create
[08:18:01] covering index and uh what I mean if we
[08:18:06] just first we saw example index and then
[08:18:09] we saw covering index how SQL
[08:18:12] automatically get that covering index
[08:18:16] that's
[08:18:17] >> yeah we're asking how is the index
[08:18:19] created like what is the process for
[08:18:21] doing that well it turns out that just
[08:18:23] as we saw here in the slides SQLite or
[08:18:25] whatever DBMS you're using will take a
[08:18:28] copy of the data that should be in that
[08:18:29] index and organize it into a tree
[08:18:32] structure like we saw here. It may or
[08:18:34] may not be similar to the structure we
[08:18:36] saw just a little earlier with nodes
[08:18:37] that have different pieces of um row
[08:18:40] data in them. But good question there.
[08:18:44] Okay, so we've seen now the tradeoff
[08:18:47] that we get with index which is they're
[08:18:49] very fast to look up some data but they
[08:18:52] take up a lot more space. There's a lot
[08:18:54] of redundancy to them here. There's also
[08:18:57] one more trade-off, which is if I want
[08:18:59] to insert something into this structure,
[08:19:02] it'll take me more time. I have to
[08:19:05] navigate this structure here. I have to
[08:19:06] figure out should it come before this v
[08:19:08] this this value or after this value and
[08:19:11] I'll have to traverse this tree every
[08:19:13] time. Versus without an index, I could
[08:19:16] just add something to the end of this
[08:19:18] list. But with a B tree with an index I
[08:19:20] need to traverse all these nodes to
[08:19:22] figure out where should that piece of
[08:19:23] data go. So these trade something you
[08:19:26] should keep in mind as you build indexes
[08:19:28] and optimize your queries.
[08:19:30] Okay. There are ways though to actually
[08:19:33] optimize the space that we use using a
[08:19:37] tree like this. We can use a structure
[08:19:39] called not an index but a partial index.
[08:19:42] And if you're concerned about space, a
[08:19:44] partial index might be good for you. A
[08:19:47] partial index only includes a subset of
[08:19:50] the data from a given column, thus
[08:19:52] making your index smaller overall. You
[08:19:56] can think of a partial index being
[08:19:57] useful when you know that your users
[08:20:00] will only query a subset, only a small
[08:20:03] number of rows from that table. And for
[08:20:06] example, in IMDb, maybe we know people
[08:20:09] are more likely to search for a movie
[08:20:12] that came out this year versus someone
[08:20:14] that came out in like 15 years ago or
[08:20:16] so. So, we could create an index that
[08:20:18] focuses on those movies that came out
[08:20:21] this year versus 15 years ago or so. And
[08:20:25] we'll do just that. If I want to create
[08:20:27] a partial index, I can use this syntax
[08:20:30] here. I could say create an index and
[08:20:32] give it some name. Then include some
[08:20:36] data from this table and this column
[08:20:38] here or list of columns I can provide.
[08:20:41] But then what I need to do is add a
[08:20:43] condition where some condition is true.
[08:20:46] These are the rows I want to include in
[08:20:49] this index. Before we had just create
[08:20:52] index name on table, some list of
[08:20:54] columns. Now we can add in this wear
[08:20:57] clause that says only include those rows
[08:21:00] where this condition is true. So let's
[08:21:03] try that now. I'll come back to my
[08:21:05] computer and why don't we try creating a
[08:21:08] partial index to help speed up the um
[08:21:10] lookup of movies that came out this
[08:21:13] year. I could come back to my terminal
[08:21:15] and I could remove let's say this one
[08:21:18] over here. Now I'll try to create this
[08:21:21] partial index. I'll say uh create an
[08:21:23] index called recents to indicate this
[08:21:27] will help us search for recent movies.
[08:21:30] Now I'll make this movie uh recents on
[08:21:33] movies and the title column. I want to
[08:21:36] look up titles ultimately. But now I
[08:21:39] only want to create an index for those
[08:21:42] rows where the year equals 2023.
[08:21:47] I only want to include those titles in
[08:21:50] my index that were released in 2023.
[08:21:54] So I'll hit enter now and I'll see I
[08:21:56] created this index for myself here. Now
[08:21:59] let me try searching for those. I'll
[08:22:01] select title from movies where the year
[08:22:05] equals 2023. Enter. And I'll see a lot
[08:22:09] of movies came out in 2023. Almost one
[08:22:12] uh almost taking 1.3 seconds here. But
[08:22:16] now I could prove to you that we are
[08:22:17] using some index. I could say explain
[08:22:21] explain query plan. And now type select
[08:22:25] title from movies where the year equals
[08:22:29] 2023. Hit enter. And now we'll see what
[08:22:33] are we doing. We're going to we'll st
[08:22:36] scan movies, but we're still going to
[08:22:37] use the index we just created called
[08:22:40] recents. So it's helping speed us up
[08:22:42] just a little bit overall. Now, let me
[08:22:45] try dropping this index and showing you
[08:22:48] the opposite. I'll come back over here.
[08:22:50] And I could try dropping it. Actually,
[08:22:52] before I do that, let me show you what
[08:22:54] would happen if I didn't search for
[08:22:55] movie in 2023. I would try explain query
[08:22:58] plan. And let me try select title from
[08:23:04] movies
[08:23:05] where the year equals 1998
[08:23:09] like this. And see now I'm only back to
[08:23:13] scanning movies. So before in my prior
[08:23:15] query I was able to use the index
[08:23:18] because my wear clause included 2023.
[08:23:22] Now though I'm using 1998 which were
[08:23:25] rows that were not included in this
[08:23:27] partial index.
[08:23:29] Okay. So let me ask now what questions
[08:23:32] we have on these partial index which we
[08:23:35] can use to optimize some of the space
[08:23:37] these indexes take up.
[08:23:40] >> Why index is not saved in schema?
[08:23:43] >> A good question. Are indexes saved in
[08:23:45] the schema in SQLite. If I type schema I
[08:23:49] can actually see them in my schema. So
[08:23:50] let me go back here and show you. If I
[08:23:53] now type something like let me turn
[08:23:55] timer off here. Dot schema. You can see
[08:23:59] down below here that I actually have
[08:24:01] these indexes as part of my schema. I'll
[08:24:04] see the create index statements I used
[08:24:07] down below here. Create an index called
[08:24:09] name index called person index called
[08:24:11] recents. And all that I use to create
[08:24:13] these indexes now inside my schema. If I
[08:24:17] drop some index, it'll then be just
[08:24:18] removed from my schema altogether.
[08:24:22] Good question.
[08:24:24] Okay, so speaking of dropping indexes,
[08:24:27] one other way we can more efficiently
[08:24:28] use space is to a bit of vacuuming, so
[08:24:31] to speak. So let's introduce this idea
[08:24:32] of vacuuming up our database. Let me
[08:24:35] show you a slide here. And um this one
[08:24:39] involves this idea of trying to clean up
[08:24:41] unused space in our database. Often when
[08:24:45] we delete something, either a rows or an
[08:24:49] index, we don't actually delete those
[08:24:52] bits that were being used by those rows
[08:24:55] or that index. We just mark them as
[08:24:57] being available for whatever we next
[08:25:00] insert. They can be overwritten, so to
[08:25:02] speak. But if I want to actually reduce
[08:25:05] the size of my database after I delete
[08:25:08] something, I should use something like
[08:25:10] vacuum in SQLite or optimize in some
[08:25:13] other DBMS. Vacuuming is a bit like
[08:25:16] taking those unused bits and just like
[08:25:17] sucking them up, taking them back in so
[08:25:19] we can give them back to the operating
[08:25:22] system. And the keyword we can use for
[08:25:24] vacuum is just simply vacuum. So let's
[08:25:27] try this. So, I'll come back to my
[08:25:28] computer over here and let me open up a
[08:25:31] new terminal, one that I can use to find
[08:25:33] the current size of movies. DB. So, I'll
[08:25:36] hit this plus button here. And now I
[08:25:38] could type a command, not a SQL command
[08:25:41] or SQLite command, but actually a Unix
[08:25:44] command. I could type du-b
[08:25:47] for the disk usage in bytes. How many
[08:25:50] bytes is a particular file? I could then
[08:25:52] say movies. DB here. And if I hit enter,
[08:25:56] I should see movies. DB is something
[08:25:59] like 158 million bytes or 158 megabytes.
[08:26:04] So let's see what happens if I were to
[08:26:06] delete an index, which you know takes up
[08:26:08] some amount of space in our database.
[08:26:10] I'll go back to my terminal here and let
[08:26:13] me try to drop an index that we had
[08:26:14] recently created. I'll say drop index
[08:26:18] person index to remove the person index.
[08:26:21] In this case, I'll hit enter. And now I
[08:26:24] see that person index is dropped. If I
[08:26:26] type dot schema here, I no longer see it
[08:26:30] in my schema down below. So now let me
[08:26:33] check the disk usage in bytes and see if
[08:26:35] it's any smaller. I'll hit the up arrow
[08:26:37] to get access to that same command. Hit
[08:26:39] enter. And it seems like it's the same
[08:26:41] size. It's still 158 megabytes. So let
[08:26:45] me try dropping something more here.
[08:26:47] I'll go back to my terminal here. And
[08:26:49] now I'll try what other do I have? So I
[08:26:51] have um I have name index. So I'll say
[08:26:54] let's drop index name index like this.
[08:26:57] I'll hit enter and I'll see that that
[08:27:00] index is now gone. Well now I'll also
[08:27:03] try dropping recent. I'll drop index
[08:27:06] drop index recents. And now I believe
[08:27:09] all of my indexes should be gone. If I
[08:27:11] type dos schema, I don't see any more
[08:27:14] indexes.
[08:27:16] So now let's check on the disk usage in
[08:27:18] bytes. I'll go back to my other
[08:27:19] terminal. Hit du-b again and it's still
[08:27:23] 158 megabytes.
[08:27:25] Well, what could we do to clean this up?
[08:27:28] We could run vacuum. If you remember
[08:27:31] here, when we delete an index, we drop
[08:27:33] the index. We don't actually shrink our
[08:27:36] database file. We just mark those bits
[08:27:38] that were part of the index as being
[08:27:40] available for reuse. So, let's now
[08:27:43] vacuum and compress our file to give
[08:27:45] back those bites, those bits to the
[08:27:47] operating system. I'll come back to my
[08:27:49] terminal here and type vacuum semicolon.
[08:27:53] Hit enter and I'll wait for it to find
[08:27:56] those bits and bytes. Wait for it to
[08:27:58] give them back to deallocate them to go
[08:28:00] back to the operating system. And now if
[08:28:03] I come back and I type du-b again, hit
[08:28:06] enter, I should see a much smaller file.
[08:28:10] So before we had about 158 million
[08:28:12] bytes. We're down to in this case 100
[08:28:15] million after dropping our indexes and
[08:28:18] using vacuum.
[08:28:20] So let me ask now what questions do we
[08:28:23] have on vacuuming?
[08:28:25] >> Can we do vacuuming in a faster way?
[08:28:27] >> Can you vacuum in a faster way? Uh so I
[08:28:30] think it depends on the size of the
[08:28:31] vacuum that you're trying to implement
[08:28:33] here. If you have a lot of bits and
[08:28:35] bites you're trying to deallocate that
[08:28:37] could take more time. I mean the process
[08:28:39] here is the computer has to find those
[08:28:41] bits and byes you're no longer using and
[08:28:44] then give each of those back to the
[08:28:45] operating system. So it could depend on
[08:28:48] the size and how long they take to find.
[08:28:51] Let's take another question here.
[08:28:53] >> Initially you said once we drop a
[08:28:55] database we don't lose the the data is
[08:28:58] not deleted. It's just uh the space is
[08:29:01] just uh reallocated right if if I got
[08:29:04] you right. So, does that mean um the
[08:29:07] queries we run today, are they locked
[08:29:10] somewhere that let's say you mistakenly
[08:29:12] did a a query, you can go back and pull
[08:29:15] that data back? Is it is that possible?
[08:29:19] Kind of like a reversal of a a query.
[08:29:22] >> Yeah. So, you're talking about some
[08:29:24] forensics here, like could we mark
[08:29:26] something as deleted but still find it
[08:29:28] later? Um there actually are uh people
[08:29:30] who are trained in this in forensics to
[08:29:32] find pieces of data that you thought
[08:29:34] were deleted but are actually still on
[08:29:36] your computer just kind of um forgotten
[08:29:38] if you will. In this case in SQLite it
[08:29:41] would take a lot of work to go ahead and
[08:29:42] find all of those bits and bites we've
[08:29:44] removed. Um but once we vacuum once we
[08:29:47] actually give them back to the operating
[08:29:48] system we can no longer find those in
[08:29:50] the database because they're not just
[08:29:52] marked as being deallocated they
[08:29:54] actually have been given back and
[08:29:55] they're no longer part of our database.
[08:29:58] Good question there. Okay, so we've seen
[08:30:01] here how we can optimize our queries by
[08:30:04] reducing the time that they take,
[08:30:05] although at the cost of some space. When
[08:30:08] we come back, we'll see how we can
[08:30:10] handle not just one query at a time, but
[08:30:12] many all at once. See you in a bit. And
[08:30:16] we're back. So we've seen so far how to
[08:30:19] optimize individual queries, ensuring
[08:30:21] they take less time and also to ensure
[08:30:24] our databases use as little space as
[08:30:27] possible. What we'll focus on now is
[08:30:29] trying to ensure we can handle not just
[08:30:31] one query at a time but multiple all at
[08:30:35] once. And this is this idea of
[08:30:36] concurrency. Concurrency is when I get
[08:30:40] multiple queries, multiple interactions
[08:30:43] all at roughly the same time and my
[08:30:46] computer system, my database needs to
[08:30:47] figure out how to handle all of those at
[08:30:50] once. This is particularly important for
[08:30:52] websites get a lot of traffic or even
[08:30:54] for the financial sector. People are
[08:30:56] constantly making trades, placing
[08:30:58] orders, exchanging money and so on. So
[08:31:02] let's see one example here of a bank.
[08:31:05] Let's say here I have a table of
[08:31:07] accounts and each account has a name and
[08:31:10] some balance to it. Well, we decide here
[08:31:13] that uh maybe Alice wants to pay Bob
[08:31:17] $10. So, what should I do to update the
[08:31:20] balances here? Maybe the first thing I
[08:31:22] should do is make sure that Bob receives
[08:31:24] that money. I could update Bob's account
[08:31:27] to have a balance not of 20, but of 30.
[08:31:30] Now, from 20 to 30. But here's the
[08:31:34] thing. If at this moment somebody looks
[08:31:37] at this table, what will they see that's
[08:31:40] wrong?
[08:31:42] What will they see that they might not
[08:31:45] get the right picture of? At this point,
[08:31:51] I'm hearing they might not see the
[08:31:53] correct balance for Alice. Like Bob has
[08:31:55] gotten some money. He's gotten he's gone
[08:31:57] from 20 here to 30. But now I have not
[08:32:00] just let's see $60 in the bank. I now
[08:32:03] have 70 it looks like. So somebody looks
[08:32:06] at this transaction in this moment,
[08:32:08] they'll see some incorrect information.
[08:32:10] What I should then do is update Alice's
[08:32:12] balance subtracting 10. So we're at the
[08:32:15] right amount of dollars across our bank
[08:32:18] accounts here. So this is an issue. When
[08:32:21] I have one ongoing transaction like this
[08:32:24] and somebody else wants to look at that
[08:32:26] data, they really shouldn't be able to
[08:32:29] until this transaction is complete in
[08:32:31] its entirety. So ideally, let's go back
[08:32:34] to what we had before with Alice at 10,
[08:32:36] Bob at 20. Ideally, if Alice wants to
[08:32:39] pay Bob, this should happen to an
[08:32:41] outside observer all at once. Bob should
[08:32:44] get those $10 and Alice should lose
[08:32:46] those $10 at the same exact moment. So
[08:32:50] nobody can look and see that Bob has
[08:32:53] more money while Alice doesn't have less
[08:32:55] money. Now we can implement this idea of
[08:32:59] this transaction using a very similarly
[08:33:02] named idea in databases called a
[08:33:05] transaction. Now a transaction in the
[08:33:08] world of databases is an individual unit
[08:33:11] of work. That means a transaction can't
[08:33:14] be broken down into smaller pieces. It
[08:33:16] happens all at once or not at all. And
[08:33:20] in fact, a transaction has several
[08:33:22] properties and helps implement several
[08:33:24] properties of a database. Among these
[08:33:26] are ACID, AC, CI, D. You may have heard
[08:33:30] of these if you've looked up some about
[08:33:32] databases. But each one stands for some
[08:33:34] principle of ensuring a consistent and
[08:33:37] reliable database. In fact, A stands for
[08:33:41] atomicity, which means I can't break a
[08:33:43] transaction down into smaller pieces. I
[08:33:46] can't break a transaction between Alice
[08:33:48] and Bob into Bob's update and then
[08:33:50] Alice's update. It's just update both
[08:33:53] accounts at the same time. Consistency
[08:33:56] means a transaction help me ensure that
[08:33:59] I don't violate some database
[08:34:01] constraint. Let's say I try to pay Bob
[08:34:05] from Alice's account, but Alice doesn't
[08:34:07] have the money. If that is the case, a
[08:34:09] transaction will revert, undo. So I go
[08:34:12] back to being in this consistent state
[08:34:14] for my database. Isolation means if I
[08:34:18] have more than one person trying to
[08:34:20] access this database, their queries,
[08:34:22] their transactions won't interfere with
[08:34:25] each other. And then finally, durability
[08:34:28] means if I were to unplug this database
[08:34:30] were to encounter a power failure or the
[08:34:32] server were to crash, all that data
[08:34:34] would still be there from the time we
[08:34:36] committed our transaction or saved the
[08:34:39] results there. So transactions do a lot
[08:34:43] for us, but they have some very simple
[08:34:45] syntax. I can simply use begin
[08:34:47] transaction and then follow it up with
[08:34:50] some statements I want to include in
[08:34:52] that transaction. And once I'm sure I
[08:34:55] want to save the results of these
[08:34:57] statements, I can then say commit,
[08:35:00] meaning save these changes thus far. And
[08:35:03] it's using this kind of syntax we can
[08:35:06] ensure that nobody sees incorrect
[08:35:08] balances. Let's say for this bank
[08:35:10] account um table here. So let's try this
[08:35:14] out and implement a payment between
[08:35:16] Alice and Bob, but now using a
[08:35:18] transaction. Come back to my computer
[08:35:21] here and let me show you a new database.
[08:35:24] I'll type SQLite 3 bank. DB. I'll hit
[08:35:28] enter and I'll SQLite 3, sorry, bank.db.
[08:35:32] I'll hit enter. And now let me type dot
[08:35:34] schema to see the schema of this
[08:35:36] database. I'll see here a few different
[08:35:39] columns that I have an ID column, my
[08:35:42] primary key, a name column like we saw
[08:35:44] in our slides that is text and can't be
[08:35:46] null. And then a balance column. There's
[08:35:49] an integer, a whole number of dollars
[08:35:52] that also must have a value can't be
[08:35:54] null. And I have a check constraint here
[08:35:57] saying the balance must be at all times
[08:36:00] greater than or equal to zero. So this
[08:36:03] is our implementation of a table of bank
[08:36:06] accounts. Let me try querying here to
[08:36:09] see what our account balances look like.
[08:36:12] I'll say select star from accounts
[08:36:16] semicolon. And now I'll see that very
[08:36:19] same arrangement we saw in our slides.
[08:36:21] Alice has $10, Bob has $20, and Charlie
[08:36:24] has $30. So let me try then processing
[08:36:28] this transaction between Alice and Bob.
[08:36:31] Well, at this moment, I might try to
[08:36:34] update Bob's account. At the first bat,
[08:36:36] I'll say, uh, let's try update and
[08:36:40] update the accounts table. Set the
[08:36:42] balance equal to balance + 10, where the
[08:36:47] ID equals 2. Remember, Bob's accounts ID
[08:36:51] is two. So now, if I hit enter here, Bob
[08:36:55] should have gotten just 10 more dollars.
[08:36:57] But there's a problem. If I also connect
[08:37:00] to this database to another connection
[08:37:01] here, SQLite 3 bankdb.
[08:37:04] Maybe I'm somebody who's checking on the
[08:37:06] balances of the bank. I say select star
[08:37:09] from accounts.
[08:37:11] What do I see? But an incorrect total
[08:37:15] balance. We should have $60, but here I
[08:37:18] see 70. So I need to complete this
[08:37:20] transaction to ensure that I actually
[08:37:23] have the right amount of balances across
[08:37:24] the board. Let me go back here and let
[08:37:27] me try to run the next part here. I'll
[08:37:29] change let me update this. I'll say
[08:37:31] update accounts and I'll set balance
[08:37:35] equal to balance minus 10 minus 10 where
[08:37:40] the ID equals in this case 1 where
[08:37:43] Alice's bank account ID is one. Now if I
[08:37:47] hit enter, I should be able to go back
[08:37:49] to my other terminal and check on the
[08:37:51] balances again. And now I'll see the
[08:37:54] right balances all together. But there
[08:37:57] is a way to avoid me looking at this
[08:38:00] table and seeing an incorrect state. And
[08:38:03] that's the way to do that is called a
[08:38:05] transaction. So let's go back here and I
[08:38:07] will reset my terminals. I'll now also
[08:38:10] give back Alice's money. I'll say um let
[08:38:12] me give back Bob the $10. Let me go back
[08:38:15] give Alice back $10. I say where ID
[08:38:17] equals one here. Now Alice will have 10
[08:38:20] more dollars. And I'll go back and I'll
[08:38:22] update accounts. I'll set um the balance
[08:38:26] equal to balance um minus 10 where the
[08:38:30] ID equals 2. So I'm giving Bob back the
[08:38:34] $10 that they just gave to Alice. Now if
[08:38:37] I select star from accounts,
[08:38:39] we're back to where we began. So ideally
[08:38:43] I should be able to complete this
[08:38:44] transaction between Alice and Bob
[08:38:47] without somebody seeing the intermediate
[08:38:49] process of Bob having more money than
[08:38:51] Alice. So let's try this. I'll say begin
[08:38:55] transaction semicolon. Enter. And now I
[08:39:00] can include what I want to have happen
[08:39:02] in this transaction. First I want to
[08:39:04] update Bob's account. I'll say update
[08:39:07] accounts and set balance equal to
[08:39:10] balance + 10 where the ID in this case
[08:39:15] equals let's see two because Bob's
[08:39:18] account ID is two. Now I'll hit enter.
[08:39:22] And now I'm in the middle of this
[08:39:23] transaction. But if I go to my other
[08:39:25] terminal, let's say I'm somebody new and
[08:39:28] I check on the balances of the bank. I
[08:39:30] say select star from accounts.
[08:39:33] What do I see? I don't see any change
[08:39:36] from before. Alice still has $10, Bob
[08:39:39] has $20, and Charlie has 30. And even
[08:39:42] though in this terminal, I've been able
[08:39:44] to update the account balance, I haven't
[08:39:47] committed those changes. I haven't saved
[08:39:49] them to the database just yet. So, let
[08:39:51] me try now removing money from Alice's
[08:39:53] account. I'll say update accounts and
[08:39:56] set balance equal to balance minus 10
[08:40:00] where the ID equals 1. Now I'll remove
[08:40:05] $10 from Alice's account. Hit enter. And
[08:40:08] still if I go back to this other
[08:40:09] perspective here from somebody else
[08:40:11] checking on the bank balances, I see
[08:40:14] well everything is still the same. But
[08:40:17] the moment I then go to this transaction
[08:40:19] and finish it by typing commit, meaning
[08:40:21] save these changes, I'll commit here. I
[08:40:24] can go back and I'll see all in one
[08:40:27] moment that it appears Alice has paid
[08:40:30] Bob $10.
[08:40:33] So this is the atomicity part of
[08:40:36] transactions. I don't see the
[08:40:38] intermediate steps in the transaction. I
[08:40:41] only see that it happened all at once or
[08:40:44] not at all. Okay. So this is one example
[08:40:48] here of a transaction. Let me ask what
[08:40:51] questions we have so far on the
[08:40:53] transactions we've made and how they can
[08:40:55] be used.
[08:40:58] uh I mean you are searching based on ID
[08:41:00] like ID is equal to question mark but uh
[08:41:03] in a real world scenario how they will
[08:41:05] search maybe like using the transaction
[08:41:09] ID or basing the account number like
[08:41:11] >> uh good question so here I'm searching
[08:41:13] by ID I'm saying that I want to update
[08:41:16] the balance of account with ID 1 or ID2
[08:41:19] for instance and this is similar in
[08:41:20] spirit to how your bank account likely
[08:41:22] has some unique number an account number
[08:41:25] so to speak so here In this table, I'm
[08:41:27] updating balances by referring to the
[08:41:30] account number. You could imagine me
[08:41:32] using names, but there might be in some
[08:41:34] world multiple Alice, multiple Bobs. So,
[08:41:37] I should uniquely identify each account
[08:41:39] using its ID in this case.
[08:41:43] Okay. So, let's come back and think
[08:41:45] through more kinds of transactions here.
[08:41:47] And let's think through a transaction we
[08:41:49] actually don't want to complete. So,
[08:41:52] let's go back to our balance sheet where
[08:41:54] we have Alice at $0 and Bob at 30. And
[08:41:58] let's say Alice wants to pay Bob $10
[08:42:01] more. Well, if I go through this
[08:42:04] transaction, what's going to happen?
[08:42:07] Alice will have $10 and Bob will have
[08:42:11] 40. That violates our check constraint
[08:42:13] that we saw in our schema. The balance
[08:42:15] of Alice's account must always be at
[08:42:18] least $0.
[08:42:20] So if I were to complete this
[08:42:22] transaction that would bring our
[08:42:24] database to an inconsistent state. It
[08:42:27] violates some uh constraint that we
[08:42:30] have. But what I can do is undo these
[08:42:33] changes, revert them so that we go back
[08:42:36] to the original state if we ever violate
[08:42:39] some constraint like we just did.
[08:42:41] There's a technical name for this which
[08:42:43] is rolling back. So if I ever want to
[08:42:46] not save the changes in this
[08:42:48] transaction, I can say roll back. Go
[08:42:51] back to the beginning. Think about it as
[08:42:53] if this transaction never even happened
[08:42:55] at all. So let's try this. I'll come
[08:42:58] back to my computer and what I'll do is
[08:43:01] try to implement this idea first without
[08:43:04] a transaction. I'll go back to let's say
[08:43:07] this first terminal here and I'll select
[08:43:09] star from accounts like this. Notice how
[08:43:13] Alice has zero dollars and Bob has 30.
[08:43:17] Well, I want to pay Bob 10 more dollars
[08:43:19] from Alice. So, I'll update Bob's
[08:43:21] account. I'll find here my prior um my
[08:43:24] prior statement. Update accounts set
[08:43:27] balance equal to balance plus 10 where
[08:43:29] the ID equals 2. And recall that Bob's
[08:43:32] account ID is two. I'll hit enter. And
[08:43:36] now if I select star from accounts,
[08:43:37] we're looking somewhere else. Select
[08:43:39] star from accounts.
[08:43:42] I'll see Bob has 10 more dollars. But
[08:43:45] now I need to subtract money from
[08:43:47] Alice's account. So I'll use the same
[08:43:49] thing, but now I'll say minus 10 where
[08:43:53] the ID equals 1. Alice's account ID is
[08:43:56] one. Now I'll try to subtract $10 from
[08:43:59] Alice. But I get a constraint failure
[08:44:02] here. My check constraint failed on the
[08:44:05] balance column. Well, why did it do
[08:44:07] that? because I now have less than $0 in
[08:44:12] that balance column. So, I need to undo
[08:44:16] this. But I don't have a transaction
[08:44:18] here. What could I do instead to undo
[08:44:22] what I've just done?
[08:44:25] >> So, we can roll back.
[08:44:26] >> We could roll back. But here's the
[08:44:28] thing. A roll back only works while
[08:44:30] we're inside of a transaction. And a
[08:44:33] transaction begins when we say begin
[08:44:35] transaction. So here I actually didn't
[08:44:38] say begin transaction. What I have to do
[08:44:41] instead is run another update statement.
[08:44:43] I have to update um let's see uh Bob's
[08:44:46] account to remove the $10 that Alice
[08:44:49] paid Bob. So let's try that. I'll come
[08:44:51] back to my computer and I will then
[08:44:54] revert back. I'll say let's undo this.
[08:44:56] Let's subtract $10 now from Bob's
[08:44:59] account where the ID is two. Now we're
[08:45:02] back to where we began. If I check in
[08:45:04] from some other detection here, I'll see
[08:45:07] we're back to Alice having zero and Bob
[08:45:10] having 30. But we ideally want to use
[08:45:13] roll back to undo some changes that we
[08:45:16] had made in a transaction. So for that,
[08:45:19] let me now use a transaction. I'll say
[08:45:22] begin begin transaction like this. Hit
[08:45:25] enter. Now I want to update Bob's
[08:45:28] balance. I'll say update accounts set
[08:45:30] balance equal to balance plus 10 where
[08:45:33] the ID where the ID equals 2. Bob's
[08:45:37] account ID is two. Now let me subtract
[08:45:40] $10 from Alice like this minus 10. I'll
[08:45:43] go back here and say where the ID equals
[08:45:46] 1 for Alice's account. Hit enter. But
[08:45:49] now I get that same constraint failure.
[08:45:51] Alice has less than $0 which can't be
[08:45:54] possible. So what do we do? Instead of
[08:45:57] having another update, we could just
[08:45:59] roll back. We could undo all of these
[08:46:02] previous statements here. Roll back like
[08:46:04] this. Hit enter. And now I should see
[08:46:06] from another perspective here my table
[08:46:09] exactly as it was before with no
[08:46:12] intermediate step of Bob having money
[08:46:14] but Alice having -10.
[08:46:17] So let me ask now we've seen commit and
[08:46:20] roll back. What questions do we have on
[08:46:23] transactions? now.
[08:46:30] Okay, seeing none so far. So, let's keep
[08:46:33] going. Um, transactions are helpful for
[08:46:36] ensuring that our data is consistent
[08:46:38] like we just saw and that they're also
[08:46:40] we have atomic transactions. We can't
[08:46:42] break things down into smaller pieces.
[08:46:46] But there is a case that transactions
[08:46:47] can help guard against some adversarial
[08:46:50] kind of attack where we run into what we
[08:46:53] call race condition. A race condition is
[08:46:56] when we have multiple people, multiple
[08:46:58] processes trying to access some value
[08:47:01] and also making a decision based on that
[08:47:04] value. If unressed, it can lead to a
[08:47:07] scenario that's inconsistent in our
[08:47:10] database. And actually hackers can
[08:47:12] exploit race conditions to bring our
[08:47:14] database to an inconsistent state in a
[08:47:16] way that benefits them. So let's say our
[08:47:18] friends uh Charlie and Alice here, they
[08:47:21] decide to rob our bank. They decide to
[08:47:23] take money from it by exploiting race
[08:47:25] conditions. And here are the logs of
[08:47:28] what Charlie and Alice actually did. We
[08:47:31] see here that Charlie and Alice executed
[08:47:35] three concurrent transactions with our
[08:47:37] bank. On the one hand, Charlie opened up
[08:47:40] his bank account on two different
[08:47:42] computers. He logged in and he said,
[08:47:45] "Let me transfer $30 to Alice." He at
[08:47:48] the same time clicked transfer on both
[08:47:50] computers. Knowing just well he had only
[08:47:53] $30 to give to Alice, but he was going
[08:47:55] to send her 60. In this case, he was
[08:47:58] hoping that we weren't guarding against
[08:48:00] race conditions that he could send $30
[08:48:03] on both accounts to Alice. Now, at the
[08:48:06] same time, Alice is at the ATM, and
[08:48:08] they're hoping that at the same time
[08:48:10] Charlie Price's transfer, Alice hits
[08:48:13] confirm on their transaction to withdraw
[08:48:15] $60 from the ATM. And when all of these
[08:48:19] happen at once, we might run into some
[08:48:21] inconsistent states in our database.
[08:48:24] Let's say first we run this transaction
[08:48:26] here. Let's focus on this one. The first
[08:48:28] step is to check Charlie's balance. Does
[08:48:30] Charlie have $30? It seems like Charlie
[08:48:34] does. We continue. We might say, "Okay,
[08:48:35] let me add $30 to Alice's account like
[08:48:37] this. Then let me subtract $30 from Al
[08:48:40] from Charlie's account down below here."
[08:48:42] And finally, that's the end of our
[08:48:44] transaction. We checked Charlie's
[08:48:46] balance. We added $30 to Alice and
[08:48:49] subtracted $30 from Charlie.
[08:48:52] But now, at the same time, we're also
[08:48:55] processing the other transfer of $30 to
[08:48:58] Alice. So here, we check in terms of our
[08:49:01] time top to bottom here. We check
[08:49:03] Charlie's balance at this point. It's
[08:49:05] still $30. Knowing this, this process
[08:49:09] goes ahead and says, "Let's add $30 to
[08:49:11] Alice's account." And now, only later,
[08:49:14] let's subtract $30 like this. Now,
[08:49:18] Charlie will appears to have no money in
[08:49:21] his account. But at this time up above,
[08:49:24] we've already sent $30 to Alice's
[08:49:26] account two times. And if Alice is
[08:49:29] waiting at the ATM over here and they
[08:49:31] press confirm on that withdrawal, what
[08:49:33] might happen is something like this. At
[08:49:35] that moment that Alice has $60 in their
[08:49:37] account, they check and they see it.
[08:49:39] They could then withdraw that $60 and
[08:49:42] now that money is gone from our bank,
[08:49:44] even if we realize Charlie shouldn't
[08:49:46] have been able to make that transaction
[08:49:48] happen.
[08:49:50] So what logically is a solution here? It
[08:49:54] seems these transactions happened all at
[08:49:57] the same time. But what would you do to
[08:50:00] reorder these statements to make it
[08:50:02] clear that we can only do
[08:50:05] one at a time? What would you do in this
[08:50:07] case to update this table to fix this
[08:50:11] problem?
[08:50:12] >> I would group um the withdrawal and the
[08:50:17] debit as um one transaction. So the
[08:50:20] subtraction is done and the addition is
[08:50:23] done as one unit of work in order for
[08:50:25] the double transfer not to happen.
[08:50:29] >> Yeah. So ideally we should treat each of
[08:50:31] these as a separate transaction
[08:50:33] literally a transaction in the database
[08:50:35] sense where if I go back to this table
[08:50:37] if Charlie transfers $30 to Alice at
[08:50:40] roughly the same time I should handle
[08:50:43] these sequentially. I should first do
[08:50:45] this one, then I should do this one, and
[08:50:48] only after that should Alice be able to
[08:50:50] withdraw their $60, or at least try to
[08:50:53] in this case. So, we need to make these
[08:50:55] transactions sequential. And the word
[08:50:57] for this is isolating our transactions.
[08:50:59] Here, they are not isolated. They're
[08:51:02] working at the same time, but in
[08:51:04] reality, I want them to be isolated,
[08:51:06] happen one after another after another.
[08:51:08] So, ideally, our table looks more like
[08:51:11] this. Charlie hits transfer at the exact
[08:51:14] same time on two laptops, but because
[08:51:17] we're working in transactions, we only
[08:51:19] process one first. We start with this
[08:51:22] one here. We check the balance. We say,
[08:51:25] let's add 30 to Charlie to Alice's
[08:51:26] account and subtract 30 from Charlie's.
[08:51:29] Once we're sure that is okay, we'll
[08:51:31] commit the transaction. And that is a
[08:51:34] done deal. Now though, we'll go down
[08:51:36] below. We'll say begin transaction.
[08:51:39] We'll then say Charlie's balance is $0
[08:51:41] because we're doing this after we did
[08:51:43] our first transaction. Charlie has no
[08:51:45] more money to give Alice. At that point,
[08:51:47] what we'll do is try to add 30 to Alice,
[08:51:50] but subtract 30 from Charlie. And we'll
[08:51:52] realize, well, we made a mistake. We
[08:51:54] should roll back and undo what we just
[08:51:57] did here. So, these now are separate
[08:52:00] transactions happening sequentially. And
[08:52:02] we avoid our error of giving Alice $60
[08:52:05] when she shouldn't have that money at
[08:52:07] all. And then only after this is done do
[08:52:11] we let Alice try to withdraw $60. We'll
[08:52:13] go over here and see. Alice tries to
[08:52:16] have a balance of $60. Withdraw 60 and
[08:52:18] commit it. But at this point she
[08:52:20] wouldn't actually have that money there.
[08:52:23] So let's see now what questions do we
[08:52:26] have on the way transactions are
[08:52:29] sequential. In this case
[08:52:32] >> in practically I want to ask that there
[08:52:35] millions of transactions are going on
[08:52:37] the practically also is it like that
[08:52:39] that sequentially this is these
[08:52:41] transactions are being handled for
[08:52:42] example financial transaction or any
[08:52:44] other because you know there are a
[08:52:46] number of banks in a single country or
[08:52:48] international transactions are they
[08:52:49] handled sequentially or there is some
[08:52:51] parallel handling mechanism also exist
[08:52:53] if you may please clarify.
[08:52:55] >> Yeah good question. And so here visually
[08:52:56] we see these transactions are actually
[08:52:58] sequential in the operation here. And I
[08:53:01] think your question is are they
[08:53:02] literally sequential like one after
[08:53:04] another after another. In reality they
[08:53:07] are very much just sequential like this.
[08:53:09] A database can get creative with the use
[08:53:10] of locks we'll see in just a minute. But
[08:53:12] by and large they are sequential one
[08:53:14] after the other. And it's the job of a
[08:53:16] database module to ensure that these
[08:53:19] transactions are executed sequentially
[08:53:21] in an isolated way. Good question.
[08:53:25] Okay, so let's see now how if a database
[08:53:29] is able to make these sequential, it
[08:53:31] must be using something underneath the
[08:53:33] hood to ensure that these transactions
[08:53:36] don't interfere. And in SQL light and
[08:53:38] other DBMS's we use this idea of a lock
[08:53:42] on database to ensure people can't
[08:53:44] access data when they really shouldn't
[08:53:46] be able to. So here let's take an idea
[08:53:49] of what SQLite has as different kinds of
[08:53:52] locks on this database. We have a few
[08:53:54] different kinds, unlocked, shared, and
[08:53:57] exclusive among some others here. Each
[08:53:59] one has a different meaning for
[08:54:02] different processes. Let's take a look
[08:54:04] here at our bank account table. Let's
[08:54:05] say two computers want to access this
[08:54:08] accounts table. Well, at this time,
[08:54:11] because nobody is accessing our
[08:54:12] database, it is unlocked. Anyone could
[08:54:15] read from the database that is see
[08:54:17] what's inside or write to it, add some
[08:54:19] data, or update some data. But let's say
[08:54:22] we have one computer here who wants to
[08:54:25] read from this database. They want to
[08:54:27] see what data is inside. Well, that
[08:54:30] database in SQLite would acquire what's
[08:54:33] called a shared lock like this. They're
[08:54:36] able to read the database, but also
[08:54:39] still allow others to read as well. A
[08:54:42] shared lock means I'm only reading. You
[08:54:44] too could read as well. So, let's say
[08:54:48] this computer comes in. they decide to
[08:54:50] read from this table, they could acquire
[08:54:53] the same shared lock. And because we're
[08:54:56] only reading, not updating, multiple
[08:54:59] transactions can read all at once. We
[08:55:02] don't have to make these sequential.
[08:55:05] But if we have a transaction that's
[08:55:07] hoping to write to the base to update
[08:55:10] some value, well, that's when things get
[08:55:12] a little weird. I can't let somebody
[08:55:14] else read my data while I'm updating it.
[08:55:18] So what I need is for this process here
[08:55:20] if it's writing to acquire an exclusive
[08:55:24] lock meaning this is the only computer
[08:55:26] only transaction that can read and write
[08:55:29] to this database. All others must hold
[08:55:33] off in order to be sequential.
[08:55:37] So we've seen transactions then are
[08:55:39] sequential and they use this idea of a
[08:55:42] lock to ensure other folks can't read
[08:55:45] when they make something sensitive like
[08:55:46] writing the database.
[08:55:49] Let me ask now what questions we have on
[08:55:52] locks and how they work for us here.
[08:55:55] Okay. My question is that uh suppose uh
[08:55:58] uh one computer means for what amount we
[08:56:01] will should we should allow to do the
[08:56:04] exclusive log. Maybe uh if the time if
[08:56:07] the time stamp is larger then some other
[08:56:10] computers will get time out exception
[08:56:12] and all the things right because it's
[08:56:14] not allowed to do but exclusively it's a
[08:56:17] locked how we going to decide those
[08:56:19] things for what time one instance is
[08:56:21] going to be put the exclusive lock on
[08:56:24] the resource
[08:56:25] >> so the question is at what point does a
[08:56:27] transaction actually get an exclusive
[08:56:29] lock and how do we decide how to
[08:56:32] prioritize different transactions here
[08:56:34] well there are a two algorithms you
[08:56:36] could use. One of which is simply taking
[08:56:38] the transaction that just came first. If
[08:56:41] at this point I receive a request for an
[08:56:43] exclusive lock, I might just wait for
[08:56:46] others to finish reading and allow that
[08:56:47] one to proceed. I could also use a
[08:56:50] process called timestamping which is
[08:56:52] similar to this where I look at the
[08:56:54] timestamp the time a database tried to
[08:56:56] write to the log and use the one that is
[08:56:58] earliest in that case. Now it's
[08:57:01] important to note that an exclusive lock
[08:57:04] does block others from running their own
[08:57:06] transactions. If I have an exclusive
[08:57:08] lock, no one else can run their
[08:57:10] transaction. That is kind of a necessary
[08:57:13] necessary downside in this case to
[08:57:15] ensure that I don't make mistakes in
[08:57:18] updating my table.
[08:57:21] Let's take one more here. What's the
[08:57:23] granularity on locking? I mean, you seem
[08:57:25] to say you lock the table uh database,
[08:57:27] but that's craziness. Do you lock a
[08:57:30] table or would you lock a record on a
[08:57:31] table?
[08:57:32] >> Yeah, it might depend on the DBMS
[08:57:34] itself. So, um, at the very at the very
[08:57:37] coursest, a lock might just lock the
[08:57:39] entire database. I can't actually see
[08:57:42] anything inside of it. And I might be
[08:57:43] able to demonstrate that for you in a
[08:57:45] minute here. Let me go back to my
[08:57:46] computer. Let me try to deliberately
[08:57:48] lock this database. If I go to my
[08:57:50] terminal, I can begin a transaction that
[08:57:53] automatically has an exclusive lock. In
[08:57:56] SQLite, the statement is begin exclusive
[08:58:00] again exclusive transaction. I'll hit
[08:58:02] enter like this. And now I'm in the
[08:58:05] middle of this transaction is exclusive
[08:58:07] has an exclusive lock. Nobody else can
[08:58:09] read. If I go back to my um other
[08:58:12] terminal here, connect to my database. I
[08:58:14] could try select star from accounts just
[08:58:17] to read from this table. And now I see
[08:58:20] runtime error. Database is locked. the
[08:58:23] entire database cannot be read from at
[08:58:26] the very coarsest level of an exclusive
[08:58:28] lock. Now, because these locks are so
[08:58:31] coarse, I have to lock the entire
[08:58:33] database. SQLite has its own module, a
[08:58:36] way of prioritizing transactions and
[08:58:39] ensuring that a transaction only has an
[08:58:41] exclusive lock for the duration
[08:58:43] absolutely needs to because otherwise
[08:58:45] you would slow down substantially if I
[08:58:47] had to wait and wait and wait for
[08:58:48] somebody to finish with their
[08:58:50] transaction.
[08:58:52] Okay,
[08:58:54] so this then is how we can handle not
[08:58:56] just one query at a time, but multiple.
[08:58:59] And today we've seen how to optimize our
[08:59:01] databases from making sure queries are
[08:59:03] faster to also making sure our databases
[08:59:05] use as little space as possible. We'll
[08:59:08] see next time how to actually scale up
[08:59:10] our databases using other DBMS's like my
[08:59:13] SQL besides SQLite. We'll see you next
[08:59:16] time.
[08:59:19] [Music]
[08:59:36] Okay. Well, hello one and all and
[08:59:38] welcome back to CS50's introduction to
[08:59:40] databases with SQL. My name is Carter
[08:59:43] Zeni and this week is the culmination of
[08:59:46] all you've learned over the past several
[08:59:48] weeks in the course. Today we'll give
[08:59:50] you the tools to do all that you've done
[08:59:51] in the past, but now just at a bigger
[08:59:54] scale. Now, while we're talking about
[08:59:56] scale, it's worth defining what scale is
[09:00:00] and what it means for some application
[09:00:02] to have scalability. For an application
[09:00:05] to be scalable or to have scalability,
[09:00:08] it means it can take some number of
[09:00:10] requests and handle those. whether that
[09:00:12] request is small or large. And so to
[09:00:15] kick things off here, let me ask a
[09:00:16] question. What are some famous tech
[09:00:19] companies you've seen that have needed
[09:00:21] to scale over time? Let's brainstorm
[09:00:24] here. Which ones are you familiar with
[09:00:27] that have needed to scale over time to
[09:00:28] handle more users, more data? What have
[09:00:32] you seen?
[09:00:33] >> Any social media sites such as Facebook?
[09:00:35] >> Yeah, any social media sites. You could
[09:00:37] think of things like Facebook, now Meta,
[09:00:40] uh Instagram, and similar. And these
[09:00:42] kinds of sites might have some really
[09:00:45] large number of users that are always
[09:00:47] accessing their data. But even though
[09:00:50] they have a constantly large number of
[09:00:52] users, there might even be spikes in the
[09:00:55] number of requests that they get. Maybe
[09:00:57] during the World Cup, for example,
[09:00:59] everyone is on Facebook, everyone's on
[09:01:00] Instagram. That would be a spike our
[09:01:03] application should be able to handle if
[09:01:05] it is truly scalable. Let's take one
[09:01:09] more idea here. What other kinds of
[09:01:11] companies tech prominently have needed
[09:01:15] to scale? So I think uh for banking
[09:01:18] systems who they might start locally but
[09:01:21] if you consider national and
[09:01:22] international level banking
[09:01:24] >> so you're right a banking system might
[09:01:26] need to scale as they gain more users or
[09:01:29] more accounts or they want to process
[09:01:31] more transactions. Now today we'll
[09:01:34] introduce you to a few new DBMS's or
[09:01:37] database management systems like MySQL
[09:01:40] and PostgresQL or just Postgress for
[09:01:43] short and developers often reach to
[09:01:45] these when they want to scale some
[09:01:47] application or some database because
[09:01:50] whereas SQLite was a embedded database
[09:01:54] MySQL and Postgress these are database
[09:01:57] servers that means they often run on
[09:02:00] their own dedicated hardware that you
[09:02:02] connect to over the internet to run your
[09:02:05] SQL queries. And now being a database
[09:02:08] server, they have a few advantages. They
[09:02:10] can store data not just on disk, like on
[09:02:13] an SSD or a hard drive, but in RAM or
[09:02:16] random access memory, which often allows
[09:02:19] for faster querying. They also have a
[09:02:22] full feature set to take advantage of
[09:02:24] ways you could scale like replication
[09:02:26] and sharding that we'll talk about later
[09:02:28] on today. Now before then we'll actually
[09:02:32] compare MySQL and Postgress with SQLite
[09:02:36] paying attention in particular to types
[09:02:38] but later on we'll focus on their
[09:02:40] features for scaling as well. Now we'll
[09:02:43] do all of this in the context of the
[09:02:45] MBTA or the Massachusetts Bay
[09:02:47] Transportation Authority. This is the
[09:02:50] subway system here in Boston. And if
[09:02:52] you're ever in town and you want to get
[09:02:54] around, you might use one of these
[09:02:56] subway lines. You could enter under the
[09:02:59] ground, get on a train and go across
[09:03:02] town on either, let's say, the red line
[09:03:04] on which Harvard and MIT are apart, the
[09:03:06] green line, the orange line, or the blue
[09:03:09] line. And if you recall in our week on
[09:03:11] designing, we talked about how to
[09:03:12] represent all of the riders and stations
[09:03:16] on MBTA here. Now, one thing we
[09:03:19] discussed was that the MBTA doesn't keep
[09:03:22] track of individual people. You often
[09:03:24] don't register your name with them. you
[09:03:27] instead get your very own Charlie card
[09:03:30] that you might swipe when you enter some
[09:03:32] station. Uh often if I'm getting on the
[09:03:35] Harvard Square stop, I'll take out my
[09:03:36] Charlie card and to enter that station,
[09:03:39] I'll swipe it against some counter and
[09:03:41] that will log my fair. I could also
[09:03:44] swipe my card to deposit some funds to
[09:03:47] pay my fair in the future. And in some
[09:03:50] stops, I might actually swipe to leave
[09:03:52] the station and pay some extra fair
[09:03:54] there. Now we decided then to represent
[09:03:57] in this case cards, swipes and stations
[09:04:01] own table for each of them. Cards just
[09:04:04] had their own unique ID and those cards
[09:04:07] made some swipe and like we just
[09:04:09] mentioned this swipe has a certain type.
[09:04:11] Did I swipe it to let's say enter the
[09:04:14] station? Did I swipe it to exit the
[09:04:16] station? Or did I swipe my card to
[09:04:19] deposit some funds into my account? And
[09:04:22] each swipe has as well its own date and
[09:04:25] time it occurred as well as some amount
[09:04:27] associated with it. Did I pay some money
[09:04:29] to enter or did I deposit some money to
[09:04:32] actually uh add to the funds in my
[09:04:34] account? And then finally, this all
[09:04:36] happens at individual stations with
[09:04:39] their own IDs, their own names like the
[09:04:41] Harvard Square stop or the Kendall MIT
[09:04:43] stop and their own line like the red,
[09:04:45] green, blue or orange lines. So our goal
[09:04:49] will be to first compare MySQL with
[09:04:52] SQLite, seeing how we can translate a
[09:04:55] schema like this from SQLite to MySQL.
[09:04:59] Okay, let me come back to my computer
[09:05:00] here and open up our very first instance
[09:05:02] of a MySQL server. So to connect to this
[09:05:06] server here, I can run some command that
[09:05:08] begins with MySQL. This is a command
[09:05:11] line program I can run to connect to the
[09:05:13] server over the internet. Now unlike
[09:05:16] SQLite, MySQL actually has individual
[09:05:19] user accounts to log into the database.
[09:05:22] And here I want to log in as the root
[09:05:25] user or the admin for this database. Now
[09:05:28] to say the user I want to log in as I
[09:05:31] can type dash u where u is in lowercase
[09:05:34] here followed by the name of the user
[09:05:36] I'm logging in as in this case root. And
[09:05:39] again, root is just some synonym uh for
[09:05:42] the admin of some database. Now I
[09:05:45] connect to this database over the
[09:05:46] internet and I might often include the
[09:05:49] IP address of the computer, the unique
[09:05:51] identifier of that computer on the
[09:05:53] internet. For my sake though, I mean
[09:05:55] this database is on my very own computer
[09:05:57] here. So for the host where I type H or
[09:06:01] H is in lowercase, I can say 127.0.0.1
[09:06:05] 0.1 which if you're familiar is the IP
[09:06:08] address for my own home computer also
[09:06:11] known as localhost.
[09:06:13] Now I can keep going and I should tell
[09:06:15] my SQL what the uh port I'm connecting
[09:06:18] to is. In this case I'll type dashp
[09:06:21] where p is an uppercase and then the
[09:06:23] port number 336
[09:06:26] by default. And then I want to be
[09:06:28] prompted for the root password. So I'll
[09:06:31] type -ashp where p is lowercase. And
[09:06:34] finally, I'll hit enter to connect. I'll
[09:06:36] type in my password and I should see
[09:06:39] that I'm connected to my MySQL server.
[09:06:43] Now, this is a full database server and
[09:06:46] as such, it could have multiple
[09:06:48] databases inside of it. In fact, there
[09:06:51] are a few here already. If I type show
[09:06:54] databases just like this, you should see
[09:06:57] by default on your own MySQL
[09:07:00] installation on your own server a few
[09:07:02] default databases like information
[09:07:04] schema or MySQL or performance schema or
[09:07:07] CIS. And these are tables or databases
[09:07:09] that have some um meta information on
[09:07:12] the server like the user accounts, how
[09:07:15] performance is configured, and other
[09:07:16] details that you might care about if
[09:07:18] you're a system administrator.
[09:07:21] So, we've seen here how to log in to a
[09:07:23] MySQL server and some of these default
[09:07:26] databases. Now, let me ask what
[09:07:29] questions do we have on MySQL so far.
[09:07:32] >> Uh, what's hyphen new room?
[09:07:34] >> Yeah, let me go back to my computer. I
[09:07:36] can show you what that looked like so we
[09:07:37] can refresh our memories on that. So, if
[09:07:39] you recall, let me open up a new
[09:07:40] terminal here. To connect to this
[09:07:43] server, I typed MySQL u root or u root.
[09:07:49] And what this means is when I want to
[09:07:51] connect to my server, I have to connect
[09:07:53] to it using some user account. Unlike
[09:07:56] SQLite where I could just kind of log in
[09:07:58] without any users, MySQL has users. So
[09:08:01] the dash u says here comes the user I
[09:08:04] want to log in as and root in this case
[09:08:07] is a name for the admin. Just some uh
[09:08:10] geek historical term for the admin of
[09:08:13] some a system. I could also very well
[09:08:16] use dash u carter if my username was
[09:08:19] just carter but here we're using root to
[09:08:22] get access to some administrative
[09:08:24] privileges.
[09:08:26] Okay, good question and good to clarify
[09:08:28] that. So let's keep going. And right now
[09:08:32] we have access to our database server
[09:08:35] with the databases inside of it. But our
[09:08:37] goal is to design the MBTA system and
[09:08:40] create our very own database now in
[09:08:42] MySQL.
[09:08:44] So let me try creating some new
[09:08:46] database. I'll say create database like
[09:08:49] this. And now I'll give it some name.
[09:08:52] And in MySQL I don't use double quotes
[09:08:54] like I did in SQLite. I use back ticks
[09:08:57] like this. Create database back tick.
[09:09:00] MBTA for the title. Back tick again to
[09:09:02] close that all out. Now I'll hit enter
[09:09:06] and I'll see the query was okay. One row
[09:09:09] affected. If I now type show databases.
[09:09:12] show databases.
[09:09:15] I should see that MBTA is now part of
[09:09:18] this server. And if I want to run my
[09:09:21] future queries on this database, I could
[09:09:24] use another command, another statement
[09:09:26] here, use. I'll say use MBTA semicolon,
[09:09:30] hit enter, and I see database changed.
[09:09:33] So now all my future queries will be run
[09:09:36] on this MBTA database that I just made.
[09:09:41] So presently our database is empty and
[09:09:43] it's up to us to add in some tables. So
[09:09:47] let's think through how we could add
[09:09:49] tables to our very own database we've
[09:09:51] just made here. Well, one thing we
[09:09:54] should focus on is this idea of the
[09:09:56] types for our columns. Like I think we
[09:09:58] know already what tables we'll have,
[09:10:00] what names we'll give them, but it
[09:10:02] remains to be seen what kind of columns
[09:10:04] should we add? And actually in MySQL, we
[09:10:08] get a lot more control over types. We no
[09:10:11] longer have just text and numeric and
[09:10:14] integer. We have a lot more control and
[09:10:16] a lot more variety. So let's look here
[09:10:20] at our cards table. We want to recreate
[09:10:23] this now in MySQL. And this is from SQL
[09:10:26] light here. Recall how we had a table
[09:10:28] called cards that had an ID column with
[09:10:31] the type affinity of integer. And that
[09:10:33] was our primary key down here. So our
[09:10:36] goal is now to think about how do we
[09:10:38] translate this from SQLite to MySQL.
[09:10:42] So we should think what kind of types
[09:10:44] might MySQL have for integers. Well, it
[09:10:48] turns out there's more than just one.
[09:10:50] There actually several here. We have
[09:10:52] tiny int, small int, medium int, in int,
[09:10:56] and then big int. So lots of choices
[09:10:59] over our integers. And these vary just
[09:11:02] based on their size. I mean they all
[09:11:04] store whole numbers but they do vary
[09:11:07] based on their size. So a tiny int is
[09:11:10] only a single bite. It's about eight
[09:11:12] bits. But a big int that's eight bytes
[09:11:15] or 64 bits. Now why do we have so many
[09:11:20] of these? Like why can't we just have
[09:11:22] one? Well, let me ask you all to use
[09:11:25] your own intuition. I mean what does
[09:11:28] using more bytes and more bits get me
[09:11:32] when I'm trying to represent an integer?
[09:11:34] >> So basically it depends on the need of
[09:11:37] the DB or you know the organization. If
[09:11:40] the data requires much more storage then
[09:11:43] it means we need to have you know a
[09:11:46] bigger data type but if you know uh
[09:11:50] currently if we need smaller sizes then
[09:11:53] it means we need to use smaller data
[09:11:56] types.
[09:11:57] >> Yeah. So, I like your thinking and I
[09:11:59] think um kind of behind that is this
[09:12:00] idea that if we used more bits, we'd be
[09:12:03] able to count higher like just as I have
[09:12:06] on my hands like 10 fingers. If I had
[09:12:08] more fingers, I could count higher in
[09:12:10] unary notation, right? Or if I had more
[09:12:12] digits, I could count higher using
[09:12:14] decimal. So, it's the same thing in
[09:12:16] binary here where I could count higher
[09:12:19] the more bits that I have. So if I take
[09:12:21] a look at this table here, each data
[09:12:24] type has a range of values that it could
[09:12:27] possibly store. If I'm talking about
[09:12:29] both negative and positive values,
[09:12:32] here's the range for each of these data
[09:12:34] types. You could see for a tiny int, we
[09:12:37] can only count up to 127. And that is
[09:12:41] it. We cannot count higher using a
[09:12:43] single bite. But if I used a big int,
[09:12:47] well, I could count all the way up to 2
[09:12:49] to the 63rd power minus one. That is
[09:12:52] almost unpronouncably big. It's
[09:12:54] something like a quintilion uh, you
[09:12:56] know, number of options that you might
[09:12:58] have between these two minimum values
[09:13:01] and the maximum values here. So all
[09:13:04] trade-offs what you want to represent.
[09:13:07] But our goal here is to translate a
[09:13:09] primary key. Like a primary key doesn't
[09:13:12] be it isn't negative. So, we could
[09:13:14] perhaps use something called an unsigned
[09:13:17] integer. An unsigned integer has no
[09:13:20] negative values, starts at zero, but can
[09:13:23] then go to a higher positive value
[09:13:27] because we're now using some of those
[09:13:28] combinations of ones and zeros that
[09:13:30] represented negative numbers now for
[09:13:33] positive numbers, too. So, here an int
[09:13:36] can go up to almost 4.2 2 billion values
[09:13:41] between 0ero and 4.2 billion. So an int
[09:13:44] is already pretty darn big. So with
[09:13:48] these in mind, tiny int, small int,
[09:13:51] medium int, in int and big int, let's go
[09:13:53] back to our SQLite create table
[09:13:56] statement. And let me actually ask you
[09:13:58] all like what would you substitute in
[09:14:01] place here? We no longer have integer
[09:14:03] for our primary key. But which of these
[09:14:07] do you think seems the best substitute
[09:14:09] for our primary key on cards? Tiny,
[09:14:14] small, medium, int, or big int.
[09:14:18] >> So, uh, in case we know that it's not
[09:14:21] going to be really huge, we can just use
[09:14:24] a int. But if it's going to be very
[09:14:27] large, like say a timestamp, we could
[09:14:30] use a big int.
[09:14:32] >> Yeah, I like your thinking. So if it's
[09:14:34] if it's big but not too big, maybe an
[09:14:36] int would be good. If we know for sure
[09:14:39] though that it's going to be huge, well,
[09:14:41] a big int is probably best. And let me
[09:14:44] um offer some intuition here. So, if
[09:14:46] there are fewer than 4 billion people on
[09:14:49] this earth, which I believe is a true
[09:14:51] fact, and we're using one of these IDs
[09:14:54] to represent one card, well, if everyone
[09:14:56] on Earth visited Boston and got their
[09:14:58] own Charlie card, we wouldn't run out of
[09:15:01] values using an int here. So, it seems
[09:15:04] like that's a pretty safe bet. Unless
[09:15:07] unless we knew that everyone in Boston
[09:15:09] was going to have like 10 Charlie cards
[09:15:11] or 20 or more, then we could use a big
[09:15:13] int. But in this case, an int seems
[09:15:16] pretty safe. So let's update this. Let's
[09:15:19] go from SQLite now to MySQL. So here I
[09:15:23] had the ID column with type affinity
[09:15:25] integer. And my first step in converting
[09:15:28] should probably be to get rid of these
[09:15:31] double quotes. I no longer need to use
[09:15:33] double quotes. I should use back ticks
[09:15:35] as a matter of style in MySQL. But now I
[09:15:39] should update this type from integer
[09:15:41] perhaps to a plain old int. As we
[09:15:44] discussed before, some intuition for
[09:15:45] that is we'll probably never have more
[09:15:47] than 4 billion Charlie cards in our
[09:15:50] table. Now there's one more thing to add
[09:15:53] to which is this auto increment. So
[09:15:58] SQLite for free gave us a primary key
[09:16:01] that if I inserted some value and didn't
[09:16:04] provide a value for the primary key,
[09:16:06] SQLite would generate that for me. But
[09:16:08] in MySQL, I have to actually say auto
[09:16:11] increment. If I add some new row, make
[09:16:14] sure you take the highest primary key
[09:16:17] right now, increase it by one and assign
[09:16:19] it to that new value. So you'll often
[09:16:22] see primary keys being defined with the
[09:16:25] name ID and the type int and the auto
[09:16:28] increment property of that column there.
[09:16:32] So let me ask now what questions do we
[09:16:35] have on these integers and types so far
[09:16:39] >> for for ID we have using integer type
[09:16:42] why we know that ID cannot be negative
[09:16:44] it will always start from one or and go
[09:16:47] onward so we should use here unsigned
[09:16:50] >> nice so here we didn't include it um
[09:16:52] partly for slide's sake but you could if
[09:16:54] you wanted to make sure that the ID is
[09:16:56] unsigned so unsigned means going from
[09:16:59] zero all the way up to some larger
[09:17:01] number whereas not unsigned or just
[09:17:03] assigned integer goes from negative to
[09:17:05] some positive value. Absolutely right.
[09:17:09] Okay, let's keep going then and let's
[09:17:11] think through our next table here. So
[09:17:13] our next table is not just the cards
[09:17:16] table, it's also the stations table.
[09:17:19] Actually before we do that, let's
[09:17:20] actually try to add in our cards table
[09:17:23] to our server. So I'll go to MySQL here
[09:17:27] and now let me try to create this table
[09:17:29] to store it inside of our server before
[09:17:31] we move on to stations. So I'll say
[09:17:34] create table cards and then I'll follow
[09:17:38] some very similar syntax what you've
[09:17:40] seen before. Create table cards. Now let
[09:17:43] me add an ID column int and auto
[09:17:47] increment like this. And now I'll make
[09:17:50] the primary key ID like this. Now I'll
[09:17:55] close out my create table with a
[09:17:56] semicolon. Hit enter. And I should see
[09:17:59] the query is okay.
[09:18:03] Now if I use the MBTA database as I did
[09:18:06] before, I typed use MBTA. I could show
[09:18:10] tables like this. Semicolon. Hit enter.
[09:18:14] And now I'll see I have a cards table
[09:18:17] inside the MBTA database. So kind of
[09:18:21] like for example typing schema or tables
[09:18:24] in this instance in my in SQLite to see
[09:18:27] what tables I had. Now though let me try
[09:18:30] this. Let me try describe
[09:18:33] cards. Describe is a bit more like
[09:18:36] schema to show me the schema of this
[09:18:39] table. I'll describe cards and I'll see
[09:18:42] a few different columns here. Let me
[09:18:44] come over to this this uh board here and
[09:18:47] we'll see that this table cards has one
[09:18:51] column, one field called ID. The type of
[09:18:55] this column is an integer as we said it
[09:18:58] was before in our create table
[09:18:59] statement. Now this null here, this is
[09:19:03] whether this column can accept a null
[09:19:05] value, yes or no. Yes means it can
[09:19:08] accept a null value. can hold null. No
[09:19:11] means it should never hold a null value.
[09:19:14] So this ID should always should never
[09:19:16] include a null value.
[09:19:19] Now the key the key column tells us what
[09:19:23] role this column plays in terms of the
[09:19:25] keys of this table. Pry here PRI stands
[09:19:28] for primary key. This is the primary key
[09:19:32] of our table. Default means the initial
[09:19:35] value given to any um value. If we
[09:19:38] inserted some, if we inserted some row
[09:19:40] with no value, we'd get back this
[09:19:41] default value here, null. And the extra
[09:19:44] is what we included auto increment. It
[09:19:46] should increase by one every time we add
[09:19:48] some new row. So using describe and show
[09:19:52] tables, can you actually see what you're
[09:19:55] creating along the way?
[09:19:58] So now let's keep going. Let's actually
[09:20:00] focus on creating our stations table.
[09:20:02] And for that we'll pull up our SQL
[09:20:04] lights syntax we used to create that
[09:20:07] table. So here here was what we used to
[09:20:12] create the stations table in SQLite. We
[09:20:15] gave each station an ID that was an
[09:20:18] integer. The primary key of this table.
[09:20:21] We then gave them each a name and a
[09:20:24] line. Like the name could be uh the
[09:20:26] Harvard Square station or the Kendall
[09:20:27] MIT station. And the line could be red,
[09:20:30] green, blue, whatever line this station
[09:20:32] is a part of. And of course the uh
[09:20:35] primary key is our ID column as we just
[09:20:38] said. Now here we've seen how to handle
[09:20:40] this integer type, but we haven't yet
[09:20:42] seen how to handle text. Like could we
[09:20:45] do better than this in MySQL compared to
[09:20:48] SQLite? Turns out that we can. We have a
[09:20:52] variety of options for representing
[09:20:54] strings. Basically this collection of
[09:20:56] text here. And two of the more popular
[09:20:58] ones are going to be char and var.
[09:21:02] So char is a fixed width string, a
[09:21:06] string that only has and will ever have
[09:21:09] the same number of characters. You could
[09:21:12] think of, for example, in the US we
[09:21:15] abbreviate state names using two letters
[09:21:19] like ma for Massachusetts or VA for
[09:21:22] Virginia. You might do the same thing
[09:21:23] with countries as well. Now, that would
[09:21:26] be useful for a char because this char
[09:21:29] will always hold only two characters,
[09:21:33] but often you're not sure how long the
[09:21:37] string is. You're going to add to your
[09:21:38] column. Like, let's say you're trying to
[09:21:40] store names of people. Well, my name is
[09:21:43] Carter, but yours could be longer or
[09:21:46] shorter. So a varchchar works well for
[09:21:48] that scenario where a varchchar can
[09:21:51] accept a variable length string up to
[09:21:55] some number of characters. And when you
[09:21:58] use these, my SQL will ask you to
[09:22:00] provide how much space this type should
[09:22:04] take up using m here. So I could say
[09:22:06] char parenthesis 2 to get back a fixed
[09:22:10] width string of two characters. For
[09:22:14] varchar I could say varchchar and then
[09:22:16] put in the middle here like let's say 16
[09:22:18] or 32 or 64 and that would be the
[09:22:21] maximum size of the string that I could
[09:22:24] represent using varchchar.
[09:22:27] So good here for strings that are going
[09:22:29] to be a bit shorter in length. What if
[09:22:32] though you want to store the text of a
[09:22:34] book or something a bit longer than
[09:22:36] that? Well, you could use another type.
[09:22:39] this one called text. And this is
[09:22:41] different than SQL lights text. In SQL
[09:22:44] lights text, I could store short
[09:22:46] strings, long strings, etc. In MySQL,
[09:22:49] text is good for longer chunks of text,
[09:22:53] paragraphs, pages of books, and so on.
[09:22:56] And you actually have some options for
[09:22:59] the length or the size of this text. You
[09:23:02] could use tiny text, medium text, or
[09:23:05] long text. Each just uses some variable
[09:23:08] amount of space on your computer to
[09:23:10] store in this case characters that are
[09:23:13] going to be longer than any particular
[09:23:15] string like a name and more like some
[09:23:17] page in a book.
[09:23:20] Now besides text we do have our old
[09:23:22] friend blob and blob still stores binary
[09:23:26] exactly as you give it. And more
[09:23:29] interestingly though we also have enum
[09:23:32] and set and these are brand new. These
[09:23:34] are not in SQL light, but they're very
[09:23:37] useful for us. If you remember back in
[09:23:40] our week on designing, we introduced
[09:23:43] constraints. Maybe a constraint is that
[09:23:45] this column should only have a certain
[09:23:48] uh certain values. Like let's say for
[09:23:50] calculating t-shirt sizes, I should only
[09:23:53] have xs for extra small, s for small, m
[09:23:57] for medium. There's some fixed range of
[09:24:00] values this column could hold. Well, I
[09:24:04] could use enum for that where enum lets
[09:24:07] me enumerate the possible options I
[09:24:10] could put into this column like xsm
[09:24:15] if I'm doing t-shirt sizes or something
[09:24:17] else altogether.
[09:24:19] Now set complements enum. Enum means I
[09:24:24] can only have one of these options. If I
[09:24:27] had XS, XX Sm and so on for t-shirt
[09:24:30] sizes, I can only choose one. But a set
[09:24:34] would allow me to choose more than one
[09:24:36] to store in that same cell. You could
[09:24:39] think of, for example, um movie genres.
[09:24:42] A movie isn't just uh horror or fiction
[09:24:45] or it isn't just comedy. It could be all
[09:24:47] of those together. And so set would
[09:24:49] allow you to choose not just one option
[09:24:52] from your list, but multiple and put it
[09:24:55] inside of that single cell there.
[09:24:59] So let's go back to our SQLite create
[09:25:01] table statement and let's update this
[09:25:04] for MySQL. Well, the first thing to do
[09:25:06] is what? Change these double quotes to
[09:25:09] back tick. So I'll do that here. And now
[09:25:12] let's update this ID. We saw before we
[09:25:15] could use just regular old int and auto
[09:25:18] increment like this. But now we have
[09:25:21] some more choice like for this name
[09:25:23] field that should store the name of a
[09:25:27] station. Let me actually ask you all
[09:25:29] what do you think is the best type to
[09:25:31] use when we're storing the name of some
[09:25:34] station?
[09:25:35] >> Um it would be a varchar simply because
[09:25:38] you don't know how long the station name
[09:25:40] actually is.
[09:25:41] >> Yeah, good point. So, um, we're always
[09:25:43] creating new stations and maybe some
[09:25:46] station name is pretty long or maybe
[09:25:48] it's short. We can't really tell, right?
[09:25:50] So, a var is good if we have some
[09:25:53] variable amount of characters inside the
[09:25:56] text we're trying to store. And notice
[09:25:58] how a station name isn't paragraphs of
[09:26:02] text. It's just, you know, maybe a few
[09:26:04] words. So, that's good for a varchchar.
[09:26:06] And in general here, I could say, well,
[09:26:08] let's try to use a varchchar and say we
[09:26:10] could use up to 32 characters including
[09:26:14] spaces. I think that'll cover us pretty
[09:26:15] well for names of stations.
[09:26:19] Now, let's talk about the line. Now, in
[09:26:22] Boston, there are a few lines. There's
[09:26:24] the blue line, the green line, the red
[09:26:27] line, um even the silver line. But what
[09:26:31] what type should we use for storing
[09:26:34] lines then that these stations are a
[09:26:37] part of?
[09:26:38] >> In this case, I could believe that there
[09:26:41] can be two options where it would be a a
[09:26:44] small integer number uh and pointed to
[09:26:46] another table uh storing the colors.
[09:26:49] Another one will be a limited chart
[09:26:52] taking into account that perhaps the
[09:26:54] longest uh color name will be like
[09:26:57] aquamarine or something like that and
[09:26:59] truncated it just to that size will be
[09:27:01] another option as well.
[09:27:03] >> Yeah, I love you're thinking through
[09:27:04] multiple options here and indeed there's
[09:27:06] usually more than one option for any
[09:27:08] given type of a table here. So for this
[09:27:11] one, I mean, you could actually have
[09:27:13] line be a foreign key and reference some
[09:27:16] other table to your point of those
[09:27:19] colors. So line might then be an
[09:27:21] integer. We could also make line another
[09:27:24] varchchar. Maybe this one's a little
[09:27:26] shorter, like it's always going to be
[09:27:28] just blue, green, red, or so on. So a
[09:27:30] pretty short string, but still variable
[09:27:33] length nonetheless. So we could say
[09:27:35] varchchar maybe nine, for instance, to
[09:27:37] represent a color here. One other option
[09:27:40] though exists, one that kind of
[09:27:44] constrains us, but that might still be a
[09:27:47] good fit.
[09:27:49] >> Um, maybe it would be good to use a set
[09:27:52] >> to use set. Yeah, you could use set as
[09:27:53] well. So, you could say that a station
[09:27:55] might be on the blue line and the green
[09:27:58] line as exists in the real world. You
[09:28:00] could certainly use set for that. For
[09:28:02] our purposes, I might just go ahead and
[09:28:04] simplify things and just say enum. A
[09:28:06] station will only be on one line at a
[09:28:09] time for simplicity. But if you wanted a
[09:28:11] station on more than one line, you could
[09:28:13] use set as well. And in this enum or in
[09:28:16] this set, we could include the possible
[09:28:18] lines that currently exist in the MBTA.
[09:28:22] So great reasoning through some
[09:28:25] different data types here. Let's now
[09:28:27] build this into our MySQL server here.
[09:28:30] I'll come back and I will create this
[09:28:33] table. So we saw before I could simply
[09:28:36] use create table. I could say create
[09:28:39] table and then I could say give it a
[09:28:41] name called stations and inside I'll
[09:28:44] make sure to include let me indent four
[09:28:47] spaces here 1 2 3 4 give it an ID which
[09:28:52] has the type integer and auto increment.
[09:28:56] Then afterwards we also want to include
[09:28:58] the name of our station which could be a
[09:29:01] varchchar up to size 32. It could
[09:29:04] include up to 32 characters. And this
[09:29:07] should also be not null and unique.
[09:29:10] Those same kind of column constraints.
[09:29:12] So they're still here in MySQL.
[09:29:15] Now I could also include the line
[09:29:18] column. And for simplicity, I could just
[09:29:20] assume every station is part of only one
[09:29:23] line. So I'll say enum here. And I'll
[09:29:27] choose blue and green and orange and
[09:29:31] red. These are four lines for the subway
[09:29:34] that exist here in Boston. And I'll make
[09:29:37] sure this has to be uh have a value. It
[09:29:39] can't be null that not null constraint
[09:29:41] here. Then I'll say my primary key is
[09:29:45] the ID column. And I will go ahead and
[09:29:48] close this out. Hit semicolon and enter.
[09:29:51] And I'll see query. Okay. So now if I
[09:29:54] show tables enter, I'll see both cards
[09:29:58] and stations. And if I were to describe
[09:30:02] describe stations, what do I see here?
[09:30:05] Let's take a look. I'll come back over
[09:30:07] here and I'll see I have three columns,
[09:30:10] ID, name, and line. And each of these
[09:30:14] has their very own type as I see in this
[09:30:16] column of my describes output. I see
[09:30:19] here that the type of ID is an integer.
[09:30:22] The type of name is a var 32. And the
[09:30:25] type of line is an enum. Blue, green,
[09:30:28] orange, or red are the possible values
[09:30:30] for that column. Now, none of these
[09:30:33] columns can have a null value inside of
[09:30:36] them. But here's the interesting part. I
[09:30:38] see ID has a key prior. That means ID is
[09:30:43] my primary key. But I also see uni where
[09:30:47] uni stands for unique. Now we saw before
[09:30:51] this name column I applied a unique
[09:30:54] constraint meaning there can only be a
[09:30:57] given station with a unique name. I
[09:31:00] can't duplicate station names and then
[09:31:02] of course over here we also saw the
[09:31:04] extra column auto increment that I
[09:31:07] applied to the ID column here. So let me
[09:31:11] ask we've seen now uh some new types for
[09:31:14] text some new types for enum and set and
[09:31:18] so on. What questions do we have on
[09:31:21] these new types and how we've used them?
[09:31:24] >> I was wondering if if it would be
[09:31:26] perhaps possible to include a table as
[09:31:28] the argument to enum.
[09:31:30] >> Oh, a good question. I actually am not
[09:31:33] sure. I could imagine the possibility of
[09:31:37] using a um nested select for that. But I
[09:31:41] mean, let's reason through this here. If
[09:31:44] I had a table that was growing, would I
[09:31:47] want to use those table results in my
[09:31:51] create table statement? I would argue
[09:31:54] probably not because then things are
[09:31:55] going to change over time. So, probably
[09:31:58] worth just enumerating one at a time
[09:32:01] explicitly what might go into that enum.
[09:32:04] But I encourage you to just try that out
[09:32:05] too and see what happens.
[09:32:08] Let's take one more. Is it a problem for
[09:32:10] the database if I for example I have no
[09:32:13] idea how long uh could be the name of
[09:32:15] the station and if I write a v chart for
[09:32:18] example 100 or 300.
[09:32:21] >> Yeah. So maybe you're think of a
[09:32:23] scenario where you don't know how long
[09:32:25] it's going to be. So you'd be kind of
[09:32:27] extra safe. You say like varchchar 300
[09:32:29] for instance just accommodate anything
[09:32:31] you could put in there. that is okay,
[09:32:34] but the trade-off is you're then using
[09:32:36] up to 300 bytes every time you store a
[09:32:40] smaller string. Like if I use varchchar
[09:32:42] 300 and I only ever use let's say like
[09:32:45] 10 characters on my longest string,
[09:32:47] well, I'm wasting some space. So, it's
[09:32:49] worthwhile to think through beforehand
[09:32:52] what should I actually use here. And um
[09:32:55] something to keep in mind is you can
[09:32:56] always expand a varchar using MySQL's
[09:33:00] alter table statements. So, we'll see
[09:33:02] that in just a bit. How to use alter
[09:33:03] table, but you could always expand if
[09:33:06] you need to.
[09:33:08] Okay, good questions here. Let's keep
[09:33:09] going then. And our next table is going
[09:33:12] to be the table that represents swipes.
[09:33:15] We have cards and stations, but now we
[09:33:19] have to represent swipes at those
[09:33:22] stations. Well, let's come back to our
[09:33:25] schema for swipes in SQLite. Here I had
[09:33:30] this table called swipes that had some
[09:33:32] columns up top and some primary foreign
[09:33:35] keys down below. But the important part
[09:33:37] for us now is going to be these three
[09:33:40] columns. Type, date, time, and amount.
[09:33:43] And remember that on the MBTA, I can
[09:33:46] take my Charlie card. I can make a swipe
[09:33:49] when I enter, exit, or deposit some
[09:33:53] money at a station. That's that type
[09:33:55] column here. It could be either enter,
[09:33:58] exit or deposit. Now, date time is the
[09:34:02] time and date. I swipe that card to
[09:34:05] enter, exit, or deposit some funds. And
[09:34:08] amount is the amount in dollars
[09:34:11] associated with that transaction. Now,
[09:34:15] the fair nowadays is like $2.40. Back in
[09:34:18] the 50s, it was maybe like a dime or so.
[09:34:20] It changes over time, so it's worth
[09:34:22] keeping track of in our table here. So
[09:34:25] let's think through some options that
[09:34:27] MySQL gives us. Among them are options
[09:34:30] for dates and times. So whereas in SQL
[09:34:33] light we had numeric for dates and times
[09:34:36] in MySQL we actually have explicit date
[09:34:39] and time types. For instance we have all
[09:34:42] these here date which is just a date
[09:34:45] like the year the month the day. Time
[09:34:48] which is the uh actual time like hours,
[09:34:51] minutes and seconds. We then have date
[09:34:53] time which combines those timestamp
[09:34:56] which is similar but used with a bit
[09:34:58] more precision often for logging events
[09:35:00] on your own software and then year which
[09:35:03] is just 2023 or 2020 for instance in a
[09:35:07] single column. Now you can get more
[09:35:11] particular about how precise you want to
[09:35:13] be with these times. For time, date,
[09:35:17] time, and time stamp, I can specify how
[09:35:21] many decimal digits I want to keep track
[09:35:24] of after the decimal point. Do I want to
[09:35:28] keep track of tenths of seconds,
[09:35:30] hundreds, or thousands? I could specify
[09:35:32] that using this uh parenthesis FSP. In
[09:35:36] this case, I could say 1, two, three,
[09:35:39] four up to, I believe, six to figure out
[09:35:42] how precisely do I want to keep track of
[09:35:45] time where more digits means more
[09:35:47] precision.
[09:35:49] So, I could use these for dates and
[09:35:51] times that could get us through part of
[09:35:54] our table migration here. But I should
[09:35:57] also think about how to represent real
[09:35:59] numbers. That is numbers with a decimal
[09:36:02] point in them.
[09:36:04] Now you might think back to SQLite and
[09:36:08] remember the real data type affinity and
[09:36:11] we have some similar options here. We
[09:36:14] have float and double precision where
[09:36:17] the only difference is float stores um a
[09:36:21] number in size four bytes whereas double
[09:36:24] precision stores that number in eight
[09:36:28] bytes. And you might be thinking, well,
[09:36:31] if they both store a decimal number, a
[09:36:34] real number, why would I choose one over
[09:36:38] the other? Or why would I use more space
[09:36:41] when float does the same thing for me in
[09:36:43] fewer bytes? Well, it turns out that in
[09:36:47] computer science, we run into this
[09:36:49] problem of floating point imprecision
[09:36:53] where there are an infinite number of
[09:36:55] real numbers. Like if I asked you to
[09:36:57] find me all of the decimal numbers
[09:37:00] between one and two, you would be here
[09:37:03] for literally an eternity. And if we
[09:37:06] have so many numbers to represent but so
[09:37:08] few bits, it goes to say that we can
[09:37:12] only represent some of them and not all
[09:37:14] of them. So at the end of the day,
[09:37:16] floatingoint numbers, decimals, uh real
[09:37:20] numbers will be imprecisely
[09:37:22] represented. Now, a double precision
[09:37:25] could get us more could get us um more
[09:37:28] of the way there. We could use more bits
[09:37:30] to more precisely represent some number,
[09:37:33] which you might use if you're a
[09:37:34] scientist, someone who wants to keep
[09:37:36] track of things very precisely. If you
[09:37:39] don't care as much though, you could use
[09:37:41] a float and just use a little bit less
[09:37:43] space.
[09:37:45] Now, thankfully, this trade-off isn't um
[09:37:50] isn't quite so salient in MySQL because
[09:37:53] you also get access to fixed precision
[09:37:56] types where fixed precision means I can
[09:37:59] specify I want to always have two places
[09:38:04] after decimal precisely represented. And
[09:38:07] one type for this will be the decimal
[09:38:10] type where I can use a decimal and then
[09:38:12] say I want to store a certain number of
[09:38:16] digits with some number coming after the
[09:38:19] decimal point. Now for example I could
[09:38:22] say decimal 5,2
[09:38:25] and I could store any number
[09:38:27] between99.99
[09:38:31] up to 999.99
[09:38:34] so long as there are only two places
[09:38:38] after the decimal here. Now I could
[09:38:41] increase this. I could say I want to go
[09:38:43] beyond this range. I want to have more
[09:38:45] digits. I could increase this first
[09:38:48] parameter here from five, let's say, to
[09:38:51] six. And now I have a wider range. I
[09:38:54] have 9,999
[09:38:57] all the way down to 9,999
[09:39:00] in both cases.99.
[09:39:03] Two decimal digits after this decimal
[09:39:06] point.
[09:39:08] Now I keep going. I could say seven and
[09:39:10] get an even bigger range. But if I want
[09:39:12] to represent something precisely after
[09:39:14] this decimal point, what could I do? I
[09:39:17] could change this one too from two,
[09:39:20] let's say, to three or even to four. I
[09:39:23] could keep going, but notice how my
[09:39:26] range shrinks. What I get in return is
[09:39:29] just more digits after that decimal
[09:39:31] point precisely represented. I don't
[09:39:34] have to worry about floating point
[09:39:35] imprecision so long as I'm using decimal
[09:39:38] and telling my SQL how many I want and
[09:39:41] how many come after the decimal point.
[09:39:45] Okay, so let's try this here. I want to
[09:39:48] migrate this table from SQLite to MySQL.
[09:39:52] The first thing to do change these
[09:39:54] quotes from double quotes to back ticks.
[09:39:57] I could then update uh my primary key
[09:39:59] and so on. Let's focus now on this type.
[09:40:03] This type column should only have some
[09:40:06] set of values like enter, exit or
[09:40:10] deposit. And when you see that, you
[09:40:11] could think I should probably use an
[09:40:14] enum to only store some piece some data
[09:40:17] types that are some uh values that are
[09:40:19] inside of this list. So I'll make this
[09:40:21] now an enum. But the question then
[09:40:24] becomes, what should I use for datetime?
[09:40:27] What type have we seen so far that could
[09:40:30] be useful for storing the date and time?
[09:40:33] I swiped my Charlie card.
[09:40:35] >> Yes, I believe we can use the date time
[09:40:38] uh data type.
[09:40:39] >> I could use date time. So, kind of
[09:40:41] self-explanatory here. I mean, the
[09:40:42] column is called date time. And
[09:40:44] coincidentally, MySQL also has a type
[09:40:47] called date time that stores both a date
[09:40:50] year year year mm dd and then the hour
[09:40:53] along with that. I could say date time
[09:40:56] here to get both day and time.
[09:40:59] Now the next one amount. Now it's worth
[09:41:03] noting I want to be precise with this
[09:41:06] amount. Like if I'm going to sum up many
[09:41:09] many amounts, many fairs. I want it to
[09:41:12] be accurate. So I don't want to deal
[09:41:14] with let's say float or double
[09:41:16] precision. I want to specify how precise
[09:41:19] I should be. Let me ask what data type
[09:41:23] might be good for storing the amount of
[09:41:26] some given fair.
[09:41:28] >> Uh I believe we can use the decimal data
[09:41:30] type.
[09:41:31] >> Yeah, you could absolutely use decimal
[09:41:32] data type here. So decimal was part of
[09:41:35] MySQL's fixed um precision kinds of
[09:41:38] types. So we could use that here to
[09:41:39] precisely represent the amount column
[09:41:42] here. I could change this from numeric
[09:41:45] in SQLite to decimal now where decimal I
[09:41:48] could say takes five possible digits
[09:41:51] like um five total and two now could
[09:41:55] come after the decimal point. So I could
[09:41:57] have um amounts or fairs that go up to
[09:42:00] hundreds of dollars which often isn't
[09:42:02] going to happen but I could be safe here
[09:42:04] if I need to be.
[09:42:06] Okay, let's go ahead and combine this
[09:42:08] and put this inside of our MySQL server
[09:42:11] here. I'll come back to my computer here
[09:42:14] and my goal is to run this create table
[09:42:16] statement to create this table on our
[09:42:19] server. I'll say create a table called
[09:42:22] swipes like this. And I'll include a few
[09:42:25] columns we didn't show on the slides
[09:42:27] just for simplicity. I'll first include
[09:42:30] the ID column with type int. And I also
[09:42:34] want to make sure this auto increments
[09:42:36] as I add to it. I'll then go on and I
[09:42:40] will also include a card ID column that
[09:42:43] has a type int. And then I'll include a
[09:42:46] station ID column which also has type
[09:42:49] int. So now I can see which card ID is
[09:42:53] swiped at which station. Now when they
[09:42:56] swipe here at the MBTA, a swipe can mean
[09:43:00] a few different things. It can have a
[09:43:02] different type. One type we might care
[09:43:04] about is the enter type. When I swipe to
[09:43:08] enter some station, I could also swipe
[09:43:11] to exit some station or to deposit to
[09:43:14] deposit some funds into my account. And
[09:43:19] a type should never be null. It has the
[09:43:21] not null constraint here.
[09:43:24] Now, a type a a swipe happens at some
[09:43:27] particular date and time. So, I'll
[09:43:29] include the date time column and say
[09:43:33] that this is of type date time. I want
[09:43:36] to make sure that this uh column always
[09:43:39] has some value. So it's not null. And
[09:43:41] the default when I insert some new row
[09:43:44] will be this special value here. Current
[09:43:47] timestamp, the current date and time.
[09:43:51] Now I'll go on and I'll include the
[09:43:53] amount of some swipe. I'll hit enter
[09:43:56] space and then I'll say amount here.
[09:43:58] This is the amount associated with that
[09:44:01] swipe. Was I charged money? Was I adding
[09:44:04] money? Here I'll say I want this to be a
[09:44:06] decimal type because you said we want
[09:44:08] this to be precise and decimal is a
[09:44:11] fixed precision type. I'll say I want
[09:44:13] five decimal digits with two after the
[09:44:17] decimal point. Now this similar should
[09:44:19] be not null and I'll include our same
[09:44:22] check constraint. I'll check that amount
[09:44:25] with back ticks here does not equal
[09:44:28] zero. And if that's the case, I'll be
[09:44:30] able to insert some new swipe. Now I'll
[09:44:34] assign my table constraints like primary
[09:44:36] keys and foreign keys. I'll say my
[09:44:40] primary key my primary key is the ID
[09:44:43] column like this. And then if I hit
[09:44:47] enter again my foreign key my foreign
[09:44:50] key in this case card ID should
[09:44:54] reference it references cards table and
[09:44:58] the ID column in cards bit like this. So
[09:45:02] that card ID column references the ID
[09:45:05] column in the cards table. Now I'll
[09:45:08] include my last foreign key. The foreign
[09:45:10] key station ID. Station ID references
[09:45:15] the stations table and the ID column in
[09:45:20] stations. And now to quickly review to
[09:45:22] make sure I've typed everything in
[09:45:23] correctly here. So we have the ID
[09:45:25] column, the card ID column, station ID,
[09:45:28] type of enum, date time, amount. I think
[09:45:31] we'll be good here. So if I hit enter
[09:45:34] and then use parenthesis semicolon, I
[09:45:37] should see query. Okay, zero rows
[09:45:40] affected. Now if I type in this case
[09:45:43] show tables enter, I'll see I have a new
[09:45:46] swipes table. And if I type describe
[09:45:50] describe swipes like this, I should see
[09:45:54] some familiar output. If I go back to um
[09:45:58] my screen over here, we can take a look.
[09:46:00] We have again our fields ID, card ID and
[09:46:04] so on. Types int, enum, date, time,
[09:46:07] decimal. Some can have null values, some
[09:46:10] should not. We have a primary key here.
[09:46:13] But now the interesting thing is this
[09:46:16] mul.
[09:46:17] Well, if I look at card ID and station
[09:46:20] ID, what do we call those two columns?
[09:46:26] What kind of constraints did I apply to
[09:46:28] card ID and station ID?
[09:46:31] >> So, we use the foreign key constraints.
[09:46:34] The foreign key, so it's referencing the
[09:46:37] stations and the card key.
[09:46:38] >> You're exactly right. We applied the
[09:46:40] foreign key constraint to the card ID
[09:46:43] and station ID columns. So, this mul
[09:46:46] here is referring to the fact that these
[09:46:48] are foreign keys. And mul stands for
[09:46:51] something like multiple or multi. It
[09:46:53] means I could have um in this case
[09:46:56] multiple um of the same value because it
[09:46:59] is a foreign key in this table. Now the
[09:47:03] default here we now see current
[09:47:05] timestamp when I insert some value into
[09:47:08] this table and I insert some row sorry
[09:47:10] into this table and don't supply a value
[09:47:12] for the date time column I'll instead
[09:47:15] make that default value the current date
[09:47:17] and the current time. And here we see
[09:47:20] some extras like auto increment that we
[09:47:22] saw before and now default generated
[09:47:25] meaning this is a generated column that
[09:47:27] will automatically create some value for
[09:47:29] me when I insert some new row.
[09:47:33] Okay. So let me ask what questions do we
[09:47:36] have then on these new types dates and
[09:47:39] times and more.
[09:47:41] >> Yes. Um I wanted to know the precedence
[09:47:44] in which the um the attributes the
[09:47:49] specific constraints to attributes are
[09:47:51] added. So is it in the format of the
[09:47:55] describe table you know in the describe
[09:47:58] table there's a certain format in which
[09:47:59] the data is is that the priority in
[09:48:03] which you do it let's say an integer
[09:48:05] before let's say a unique constraint
[09:48:08] before um a not what's the precedent and
[09:48:12] secondly is there any type affinity in
[09:48:15] MySQL
[09:48:16] >> yeah both good questions I'll answer the
[09:48:19] first one first so the first one is
[09:48:21] what's the prec precedence I believe of
[09:48:23] these constraints we're applying. If I
[09:48:25] look at this um output of describe
[09:48:27] swipes here, I see that I applied some
[09:48:30] constraints. Among them are the foreign
[09:48:32] key constraint, the primary key
[09:48:34] constraint. Some I made sure that I
[09:48:36] couldn't have some null value in here.
[09:48:39] Uh in effect, they all combine to um
[09:48:42] work for me here. So when I made that
[09:48:44] create table statement, I applied
[09:48:47] multiple constraints like not null and
[09:48:50] unique and I could put those in any
[09:48:53] order. MySQL is designed so I can do it
[09:48:55] in any order and get the same result
[09:48:57] forwards or backwards. When I read this
[09:49:00] table, I might just read it right or
[09:49:02] left to right here and kind of get a
[09:49:04] feel for which constraints are being
[09:49:06] applied in no particular order in this
[09:49:09] case.
[09:49:10] >> Okay. Yeah. The second question has to
[09:49:11] do with type affinity and you know with
[09:49:15] SQL like we had something like a type
[09:49:18] affinity where a particular value is
[09:49:20] appropriate for a particular row. So is
[09:49:23] there anything like that in MySQL?
[09:49:26] >> Yes there is. So in SQLite you're right
[09:49:28] we had type affinities where we defined
[09:49:31] a table and said that this column should
[09:49:34] store values of this type. We're doing
[09:49:37] the very same thing in MySQL when we say
[09:49:41] ID of type int or the the name of a
[09:49:44] station of type varchchar 16 for
[09:49:46] instance. Um, one difference though is
[09:49:49] that SQLite will allow you to add in
[09:49:53] some value that doesn't actually have
[09:49:56] the type of that given column. So if I
[09:49:59] had a SQL like column of type text or of
[09:50:02] type let's say um let's say type numeric
[09:50:05] and I added some text it would try to
[09:50:08] convert but if it couldn't it would
[09:50:10] actually just store text. MySQL is more
[09:50:13] strict than that. It will make sure you
[09:50:14] have the proper type when you insert
[09:50:17] some new rows at least by default.
[09:50:21] Okay, great questions here. Let's keep
[09:50:25] going and show some more features of
[09:50:27] MySQL. So, one of them is the ability to
[09:50:31] uh alter tables in a more fundamental
[09:50:34] way. So, let me zoom back in here. In
[09:50:37] SQLite, we had some options to alter
[09:50:40] tables, but at the end of the day, they
[09:50:42] just weren't all that powerful. With my
[09:50:44] SQL though, we're actually able to alter
[09:50:46] tables a little bit more um a little bit
[09:50:50] more fundamentally. So, let's say that
[09:50:52] the MBTA adds in a new line, a new
[09:50:56] subway line. And actually, the silver
[09:50:58] line, if you can see it here, is
[09:51:00] currently a bus line, but it was planned
[09:51:03] to be a subway line. So, if I wanted to
[09:51:07] add in a subway line called the silver
[09:51:10] line, well, I can't currently do that
[09:51:13] because my type for the um lines is an
[09:51:17] enum. It only has red, green, blue, and
[09:51:21] orange, not silver. So I should actually
[09:51:24] edit this create table to now be able to
[09:51:27] include the silver line as a possible
[09:51:30] value among that enum. So I'll come back
[09:51:33] over here and I'll introduce you to
[09:51:36] MySQL's alter table syntax. So in MySQL,
[09:51:40] we have still alter table similar to
[09:51:42] SQLite. They're all based on the SQL
[09:51:45] standard, but now we have modify where
[09:51:48] modify can take some column definition
[09:51:51] and change it on the fly. So I'll go to
[09:51:54] MySQL here and let me just uh let me
[09:51:57] describe again the stations table. I'll
[09:52:00] hit enter now and we'll see that the
[09:52:04] line is an enum and it has a few
[09:52:06] options, blue, green, orange, and red.
[09:52:09] But now I want to add silver here. So
[09:52:12] what could I do? I could do this. I
[09:52:15] could use alter table and I could say I
[09:52:18] want to alter table. I want to alter the
[09:52:21] stations table and I want to modify I
[09:52:25] want to modify the line column to be
[09:52:29] this. I want it to be an enum with these
[09:52:32] options. Blue,
[09:52:35] blue, green,
[09:52:37] orange, red, and silver like this. Now I
[09:52:43] have more options in my enum. I could
[09:52:46] also include not null too. Hit enter and
[09:52:49] I should see Oops. I think I might have
[09:52:52] forgotten a quote somewhere. I believe I
[09:52:55] did. Let me fix this. I will finish the
[09:52:57] quote. hit semicolon. And let me show
[09:53:00] you how I noticed that. If I go back to
[09:53:02] my screen here, see in MySQL, it's kind
[09:53:04] of helpful. If I finish a line and I
[09:53:07] haven't closed this quote here, like I
[09:53:09] did in red, it will alert me on this
[09:53:11] next line with this single quote here
[09:53:14] saying, "Hey, you didn't close that
[09:53:16] thing that you probably thought you were
[09:53:17] going to." So, let me restart. I'll come
[09:53:20] back over here and I will try this
[09:53:23] again. I will alter table stations and
[09:53:26] then I will modify the line column as we
[09:53:29] said before to be an enum with a few
[09:53:31] different values. Blue, green, orange,
[09:53:36] red, closing both quotes now. And then
[09:53:39] silver again closing both quotes. And
[09:53:41] let me double check. Believe we're all
[09:53:43] set. I'll then say not null semicolon.
[09:53:46] Enter. And I'll see the query is okay.
[09:53:50] Now, if I do describe describe
[09:53:54] stations like this semicolon and zoom
[09:53:58] out just a bit, I see I've added to my
[09:54:00] possible values for this enum. I have
[09:54:02] blue, green, orange, red, and silver.
[09:54:06] So, this is one example of using alter
[09:54:09] table to adjust a column definition. To
[09:54:12] an earlier question, you could also use
[09:54:14] this to expand the size of varchars or
[09:54:17] to change your table altogether. you can
[09:54:19] do so a little bit more powerfully than
[09:54:21] you can with SQLite just because MySQL
[09:54:23] decided to focus on this particular
[09:54:25] feature. So let me ask now what
[09:54:29] questions we have on altering tables in
[09:54:32] MySQL.
[09:54:33] >> This is uh regarding to generally
[09:54:35] regarding to MySQL and Postgress. Can
[09:54:38] you use those applications instead of VS
[09:54:40] code? I mean that uh user interface.
[09:54:43] >> Yeah, good question. So I think you're
[09:54:45] asking what would be the difference or
[09:54:47] how could I use like MySQL and Postgress
[09:54:49] compared with VS code. Um in fact there
[09:54:53] are kind of different use cases. So VS
[09:54:55] code as you might know is an IDE an
[09:54:58] integrated development environment
[09:54:59] allows you to write code in a file to
[09:55:01] run that code and to edit it and see it
[09:55:04] all in one place. Whereas MySQL and
[09:55:06] PostgreSQL those allow you to write SQL
[09:55:09] statements on a command line talking to
[09:55:12] some underlying server. So a bit
[09:55:14] different. You could for example use VS
[09:55:18] code and connect to a MySQL or
[09:55:21] PostgresQL server to run your SQL
[09:55:23] queries you're creating in VS Code. A
[09:55:26] good question there for workflows.
[09:55:30] Okay. So what we'll do is take a quick
[09:55:32] break here and we'll come back and talk
[09:55:34] about stored procedures. Some functions
[09:55:37] we can define to run over and over and
[09:55:40] over again. We'll see you in a few.
[09:55:43] Okay, and we're back. Now, we'll next
[09:55:46] talk about stored procedures, which are
[09:55:48] a way to automate the running of SQL
[09:55:51] statements over and over and over again.
[09:55:54] This is useful as you're scaling because
[09:55:57] if you have some process you often call,
[09:56:00] you can put it inside of a stored
[09:56:02] procedure and run it all the more
[09:56:04] simply. So to demonstrate stored
[09:56:07] procedures, what we'll do is go back to
[09:56:09] our example of the Museum of Fine Art,
[09:56:12] one of Boston's oldest museums, also
[09:56:14] called the MFA. And if you remember in
[09:56:18] the MFA, we had a certain number of
[09:56:21] tables where one of these tables was a
[09:56:24] collections table. It is the items the
[09:56:26] MFA has in their collection, the items
[09:56:29] they put on display. For instance, here
[09:56:31] we had a few pieces. Farmers working at
[09:56:34] dawn. imaginative landscape and so on.
[09:56:37] Each had their own ID and they also had
[09:56:39] a deleted column to implement what we
[09:56:42] called a soft delete where to delete
[09:56:45] something we wouldn't remove the row. We
[09:56:47] would instead just mark this deleted
[09:56:50] column from a zero to a one sort of
[09:56:53] hiding it or marking it as having been
[09:56:56] deleted to keep data around without
[09:56:59] removing it all together. Now to find
[09:57:02] all of the items that weren't marked as
[09:57:05] deleted, we could use this query select
[09:57:08] star from collections where deleted
[09:57:11] equals zero, at least in SQLite.
[09:57:16] Now we then created a view. We said
[09:57:19] maybe I want to just always be able to
[09:57:22] view those items that have not been
[09:57:24] marked as deleted. one table called
[09:57:27] current collections or one virtual table
[09:57:29] of view called current collections. If I
[09:57:32] were to update farmers working at dawn
[09:57:35] to be marked as deleted, what would
[09:57:37] happen? This deleted column would become
[09:57:39] a one and I would not see it in current
[09:57:42] collection. So our goal then is to
[09:57:45] reimplement something like this. But now
[09:57:49] not using a view in this case using a
[09:57:52] stored procedure we could simply call to
[09:57:55] find all the items that have not been
[09:57:58] marked as deleted. So to create a stored
[09:58:02] procedure we have some syntax we can use
[09:58:05] that syntax looks a bit like this. We
[09:58:08] could say create procedure and give it
[09:58:12] some name. Well, this procedure we could
[09:58:14] call maybe current collections being
[09:58:17] able to view what is inside our
[09:58:19] collection and not marked as deleted. We
[09:58:22] could then similar to a trigger say
[09:58:26] begin after which we say the SQL
[09:58:30] statements we want to run as part of
[09:58:32] this procedure. So begin we then type
[09:58:35] the SQL statements we want to run and
[09:58:38] finally say end. This is the end of our
[09:58:42] procedure. And then later on, we could
[09:58:44] use a statement called call to call this
[09:58:47] procedure over and over again. So let's
[09:58:51] work on creating our very first stored
[09:58:54] procedure to find all the items in our
[09:58:57] collection that have not been deleted.
[09:59:00] Well, I'll go back to my MySQL server
[09:59:03] and I'll show you a new database I've
[09:59:05] made. Here I can type show databases
[09:59:09] semicolon. And now I should see I have
[09:59:13] not just the default MySQL databases, I
[09:59:16] also have the MFA database. So if I type
[09:59:20] use use MFA semicolon, I should see
[09:59:25] database changed. Now all my future
[09:59:27] queries will run on this MFA database.
[09:59:31] And so I could type show tables to see
[09:59:33] all the tables inside of this database.
[09:59:36] Hit enter and I'll see I have artists,
[09:59:39] collections, and created. I could even
[09:59:42] if I wanted to describe the collections
[09:59:45] table. Describe collections semicolon.
[09:59:48] And now I'll see the description for
[09:59:50] this collections table here. I have an
[09:59:53] ID, title, accession number column, and
[09:59:56] an acquired column too. But what am I
[09:59:59] missing? I want to be able to implement
[10:00:02] soft deletes. If you were to look at
[10:00:05] this describe output, what am I missing?
[10:00:09] If I want to implement soft deletes,
[10:00:13] >> you're missing the deleted column.
[10:00:15] >> Yeah, the deleted column is not yet in
[10:00:17] this table. I know because I used
[10:00:19] describe here. So, I don't have deleted
[10:00:21] yet. But I can add it using alter table.
[10:00:23] So, I'll come back to my computer and
[10:00:25] let me use alter table to add in this
[10:00:28] particular column. I could say alter
[10:00:31] table collections like this. And then I
[10:00:34] could use add column. Modify was good
[10:00:38] for modifying a column that already
[10:00:39] existed. Add column is good for adding a
[10:00:42] brand new column. I'll call this one
[10:00:44] deleted. And its type will actually be a
[10:00:47] tiny int. A tiny int. Why? Well, it's
[10:00:50] only ever going to be one or zero. I
[10:00:53] should use as few bits as possible, and
[10:00:55] tiny int gives that to me. Now I'll say
[10:00:58] the default value is zero for not
[10:01:01] deleted. And I'll hit enter. And now if
[10:01:03] I describe collections again, describe
[10:01:06] collections. I should see that I'm back
[10:01:09] to having a deleted column of type tiny
[10:01:12] int with a default value of zero. Okay.
[10:01:16] So now we saw I could select everything
[10:01:19] from collections that's not deleted by
[10:01:22] saying something like select star from
[10:01:24] collections where deleted equals zero. I
[10:01:27] could implement the same thing here, but
[10:01:29] now using a stored procedure, something
[10:01:32] I could call again and again and again
[10:01:34] to speed up this process just a little
[10:01:36] bit. So I'll say I want to create this
[10:01:39] procedure current collections. But
[10:01:42] there's something a little interesting
[10:01:44] about the MySQL syntax here. If you
[10:01:47] remember, if I go back to some slides
[10:01:48] here, in the middle of begin and end,
[10:01:51] we're going to put our very own SQL
[10:01:54] statements to run as part of this
[10:01:56] procedure. Well, to end a SQL statement,
[10:01:59] we have to have a semicolon. But MySQL
[10:02:04] might actually prematurely end this
[10:02:07] statement. If I type create procedure
[10:02:10] name begin some statement, then a
[10:02:12] semicolon, it'll say, "Okay, you're
[10:02:14] done." But I'm actually not. I might
[10:02:16] want to add more statements. I might
[10:02:18] want to conclude with this end down
[10:02:19] here. So a workaround is to temporarily
[10:02:23] declare a different delimiter. Instead
[10:02:26] of ending my queries with semicolon
[10:02:28] here, I'll end them with let's say slash
[10:02:32] slash. And we'll see that in just a
[10:02:33] moment here. I'll come back to my
[10:02:35] computer and for the sake of writing
[10:02:38] this procedure, I'll change my
[10:02:41] delimiter. that is what icon represents
[10:02:44] the end of my query to slash slash like
[10:02:47] this. Then I'll hit enter. Now I can
[10:02:51] start creating my procedure. I'll say
[10:02:53] create procedure and I'll call this one
[10:02:57] current current collections with a open
[10:03:01] and close parenthesis after this. This
[10:03:03] is common for names here. Then I'll say
[10:03:06] begin this procedure. And in this
[10:03:08] procedure I want to select the title
[10:03:12] accession
[10:03:14] accession number and acquired columns. I
[10:03:19] want to do it from the collections table
[10:03:23] where deleted equals zero. And now I can
[10:03:27] safely include a semicolon because my
[10:03:30] delimiter for this entire query is a
[10:03:33] slash slash. So this is the end of this
[10:03:36] particular query inside my procedure.
[10:03:38] It's also the end of my procedure in
[10:03:41] general. And now to declare the end of
[10:03:44] this procedure, the end of this
[10:03:45] overarching statement, I could say slash
[10:03:48] slash instead of semicolon. Now if I hit
[10:03:51] enter, I'll see query. Okay. And now I
[10:03:55] should change back to in this case
[10:03:57] semicolon. So I can get back to what I'm
[10:03:59] used to using to end my queries. I'll
[10:04:02] hit enter. And now let's see what we can
[10:04:05] do. Well, I could say call current
[10:04:09] collection. I think we called it
[10:04:10] collection singular. And I'll say this
[10:04:14] semicolon there. Now I should see all of
[10:04:18] the items that are marked as not
[10:04:21] deleted. So using call, can I then call
[10:04:24] this procedure I've made and stored?
[10:04:27] Let's try deleting something. I'll try
[10:04:29] maybe deleting farmers working at dawn.
[10:04:31] I could say update in this case
[10:04:34] collections and set deleted set deleted
[10:04:38] equal to one where the title equals
[10:04:42] farmers working at dawn. Farmers working
[10:04:46] at dawn semicolon. I'll hit enter again.
[10:04:49] I'll see one row has changed. If I call
[10:04:52] current collection again like this
[10:04:55] semicolon enter I'll see that that
[10:04:59] particular artwork is now gone is not
[10:05:01] returned to me by the query that was
[10:05:04] part of my procedure.
[10:05:07] So this then is one example of a stored
[10:05:10] procedure. One way of saving a query and
[10:05:12] calling it again and again if I might
[10:05:14] use it very often. But what questions do
[10:05:17] we have so far on stored procedures and
[10:05:20] how we can use them?
[10:05:22] >> I have a question that just like in
[10:05:23] other languages do we have the
[10:05:24] provisioning that we can pass some
[10:05:26] parameters and arguments in the function
[10:05:27] in the procedure as well in MySQL. And
[10:05:30] secondly, can we call other procedures
[10:05:32] also in one procedure like in other
[10:05:34] languages we have one function call from
[10:05:36] other?
[10:05:37] >> Yeah,
[10:05:37] >> a great question about the power of
[10:05:38] stored procedures. So the first
[10:05:40] question, could I add parameters or
[10:05:42] arguments to this procedure and could I
[10:05:44] change what I do based on that input?
[10:05:46] The answer is absolutely yes, you can in
[10:05:49] MySQL and I'll show you that in just a
[10:05:50] minute here. The next one, which is can
[10:05:53] I call other procedures inside my
[10:05:56] procedure? Yes to that as well. Any
[10:05:58] statement you might write, you could
[10:06:00] probably put in a procedure too.
[10:06:04] Okay, let's take one more.
[10:06:06] >> Yes, I have a question. uh there is any
[10:06:08] way that I can add any note or comment
[10:06:12] to the table.
[10:06:13] >> Ah could you add any note or comment to
[10:06:15] your table? Um a good intuition like
[10:06:18] it's good to include notes to yourself
[10:06:20] or to include notes to others. To my
[10:06:22] knowledge you would best do that in
[10:06:25] something like a schema.sql file. If you
[10:06:28] have a um a text editor you could make a
[10:06:31] SQL file and store your schema inside of
[10:06:34] that. at which point you could leave
[10:06:36] comments to other developers to make
[10:06:37] them know what you were thinking as you
[10:06:39] were building this. There might be a way
[10:06:41] to leave comments in MySQL, but I don't
[10:06:43] personally know what that is. You could
[10:06:45] do some research to look that up, too.
[10:06:48] Okay, great question. Let's keep going
[10:06:50] then into our question about procedures
[10:06:52] and trying to make sure they could have
[10:06:54] inputs. Let's see that as well. Well, we
[10:06:58] saw too that I might want to mark some
[10:07:01] particular item as sold as soon as I
[10:07:04] mark it as being deleted. So, for that,
[10:07:07] I'll need a new table here. If I type um
[10:07:10] show tables semicolon, I'll see artists,
[10:07:15] collections, and created. But back in
[10:07:17] our week on um the MFA, we also had a
[10:07:21] table to keep track of transactions when
[10:07:24] we might buy and sell some piece of
[10:07:26] artwork. So let's recreate that table
[10:07:30] here. I'll create a table called
[10:07:31] transactions. Create table transactions
[10:07:35] like this. And then I'll give it an ID
[10:07:38] column with the type int and auto
[10:07:42] increment. Then I'll give it a title to
[10:07:46] mark as being sold or bought. Let's say
[10:07:49] the title is a var of size up to 64 and
[10:07:54] it can't be null. Then I'll say the
[10:07:57] action which can be either bought or
[10:08:00] sold. Do we buy or sell this piece of
[10:08:03] artwork with this particular title? So
[10:08:06] I'll say this is an enum with the
[10:08:08] possibility of bought or sold. Then I'll
[10:08:12] say this is not null. And I'll then say
[10:08:14] the primary key, primary key of this
[10:08:17] table is ID. And I'll close out this
[10:08:20] create table statement here. Hitting
[10:08:22] enter. Now I can see I have a
[10:08:24] transactions table to log the buying and
[10:08:27] selling of pieces of artwork.
[10:08:31] Well, it stands to reason that when I
[10:08:33] update my uh my collections table and I
[10:08:37] set some item to be deleted from a zero
[10:08:39] to a one that deleted column I want to
[10:08:42] add it to the transactions table and
[10:08:45] also mark it as sold. So normally that
[10:08:48] is two steps updating the table and also
[10:08:52] adding it to transactions. With a
[10:08:54] procedure though I could give that
[10:08:56] entire sequence one name. So let's try
[10:09:00] that here. I'll say I want to make a my
[10:09:04] delimiter slash. I'm going to create
[10:09:06] some procedure here. I'm going to end it
[10:09:08] with slash.
[10:09:10] So I'll say create procedure and I'll
[10:09:14] call this one cell like this. But now
[10:09:17] instead of open parenthesis and close
[10:09:20] parenthesis, I actually want to give
[10:09:22] some input to this function. And let me
[10:09:26] actually ask you all here like what kind
[10:09:29] of input should I give to this cell
[10:09:31] function so I can identify the painting
[10:09:34] I want to sell.
[10:09:36] >> Uh should we like uh do a primary key
[10:09:39] and refer to the name of the painting
[10:09:41] probably.
[10:09:42] >> Yeah, I like your thinking. We could
[10:09:43] think about what identifies this
[10:09:45] artwork. Maybe it's the ID or the title.
[10:09:48] In this case, I like your intuition for
[10:09:50] the ID which is unique, will never
[10:09:52] change. So let's actually use the ID
[10:09:54] here of an item in the collections table
[10:09:56] to mark it as sold. So I'll come back to
[10:09:59] my computer and I'll say that cell
[10:10:03] actually takes an input and I can say in
[10:10:06] here to note a um value as an input.
[10:10:09] I'll say the input is something called
[10:10:11] sold sold ID the item we're selling and
[10:10:15] the type of this is an int like this. So
[10:10:19] now I have a procedure that takes in
[10:10:21] some value, an integer called sold ID.
[10:10:25] Now I'll say let's begin this procedure.
[10:10:28] Let's begin down below. And the first
[10:10:30] thing I should do is update update
[10:10:33] collections like this and set deleted
[10:10:37] equal to one under what condition or
[10:10:41] perhaps under the condition where the ID
[10:10:45] is equal to our input which is called
[10:10:48] sold ID. So I'm using the input of sold
[10:10:52] ID to find in collections which artwork
[10:10:55] I'm marking now as deleted. But the next
[10:10:58] step I'll say semicolon here to end that
[10:11:01] step is to then insert into the
[10:11:03] transactions table. I've marked it as
[10:11:05] being deleted but now I need to insert
[10:11:07] into transactions. I'll say then I want
[10:11:10] to insert into insert into transactions
[10:11:14] in the title in the title and action
[10:11:19] columns some values here. Well, what
[10:11:22] values? The first value is actually the
[10:11:25] title of this artwork and I only have
[10:11:29] the ID right now. But I could use the ID
[10:11:33] to get back the title. I could say write
[10:11:35] a subquery that is select in this case
[10:11:38] title from collections where the ID
[10:11:43] equals sold sold ID like this. That is a
[10:11:48] subquery that gives me back the title of
[10:11:50] this artwork. Now I'll also log sold
[10:11:54] here like this and then I think that's
[10:11:57] the end for that particular query there.
[10:12:00] I'll hit let me just double check this.
[10:12:02] Insert in transactions title action
[10:12:04] value select title from collections
[10:12:06] where id equals sold ID sold. Okay, I
[10:12:09] think we're good. I'll hit enter on
[10:12:11] that. And then I think I can safely end
[10:12:14] my procedure. I'll say end here. Slash
[10:12:18] enter again. I see everything was okay.
[10:12:21] So now if I change my delimiter, change
[10:12:24] my delimter back to a semicolon, I can
[10:12:27] call sell on some particular ID like
[10:12:31] let's say I now want to sell the
[10:12:34] particular item. I could say maybe
[10:12:35] select star from collections to see what
[10:12:38] I have. And now I want to sell
[10:12:41] imaginative landscape which has the ID
[10:12:43] of two. Well, I could try call cell. And
[10:12:48] now pass in that value two. Call cell
[10:12:52] two. And if I now hit enter, I should
[10:12:56] see some rows were affected. This
[10:12:58] procedure worked. Let me check. I'll say
[10:13:00] select star from collections semicolon.
[10:13:04] And I'll see that that piece now has
[10:13:06] been updated. This value was zero, but
[10:13:09] now it's one for the deleted column. Now
[10:13:12] if I say select star from transactions
[10:13:15] semicolon I'll then see imaginative
[10:13:18] landscape being sold here as well. So
[10:13:22] good check here. Let me actually just
[10:13:25] check on this. So I think this was the
[10:13:27] ID was two and that actually makes sense
[10:13:30] here. So the ID we're thinking about and
[10:13:33] it is different here. So this is the ID
[10:13:34] of the transaction which is different
[10:13:37] than the ID of the painting which is two
[10:13:40] just to clarify that.
[10:13:42] Okay. So what other questions then do we
[10:13:45] have on stored procedures? We've seen
[10:13:48] some without inputs now some with
[10:13:51] inputs. What else are you wondering?
[10:13:54] >> Is it possible to pass in multiple
[10:13:56] inputs to a store procedure?
[10:13:58] >> Yeah, could it have multiple inputs? It
[10:14:00] absolutely could. separated by some
[10:14:02] commas inside of those parentheses. So
[10:14:04] you could imagine in sold ID int, some
[10:14:08] other input as well. And a procedure can
[10:14:11] also um output some value. You could say
[10:14:14] I want to store the result in some
[10:14:17] variable I could keep track of in the
[10:14:19] server too. Let's keep going then and
[10:14:22] we'll f we'll kind of end store
[10:14:23] procedures on this note here which is I
[10:14:27] seem to if I go back to what I um had
[10:14:29] discussed before I was able to update
[10:14:32] some item in my collections table and
[10:14:35] then add it to the uh transactions table
[10:14:38] too. So if I say select star from
[10:14:40] collections, there is some danger here.
[10:14:43] Like if I try to sell something that has
[10:14:45] already been sold, I might run the
[10:14:48] procedure and mark something as being
[10:14:51] sold twice. Now I'll actually leave this
[10:14:54] up to you as your own exercise, but I
[10:14:56] want to give you a few tools to think
[10:14:58] about for writing your own procedures.
[10:15:00] Among them are some constructs you might
[10:15:02] be familiar with if you've programmed
[10:15:04] before. So here you might notice a
[10:15:06] stored procedure can actually uh be
[10:15:08] compatible with some familiar
[10:15:10] programming syntax like conditions for
[10:15:12] example if else if and else and also
[10:15:15] loops like the ability to do something
[10:15:17] more than once or to repeat something
[10:15:19] over and over and over again. So you can
[10:15:22] use these to really build up your own
[10:15:24] store procedures to combine statements
[10:15:27] and automate processes that you're going
[10:15:28] to do very frequently on your database
[10:15:31] at large scale. So we've seen here some
[10:15:35] options for stored procedures. What
[10:15:37] we'll do is come back and talk next
[10:15:39] about Postgress. See you in a few. And
[10:15:42] we're back. So we've seen so far MySQL
[10:15:45] which is a new DBMS that allows you to
[10:15:48] do just a bit more than SQLite at a
[10:15:50] larger scale. It's worth also taking a
[10:15:53] brief detour into Postgress just to get
[10:15:55] a taste for what it looks like and get
[10:15:57] an understanding for how it can
[10:15:58] represent some of these same tables in a
[10:16:01] different environment. So we'll talk
[10:16:03] here about Postgress and our goal will
[10:16:05] be to do the same thing we did with
[10:16:07] MySQL converting our tables from SQLite
[10:16:10] over to Postgress taking advantage of
[10:16:13] some new types and some new affordances
[10:16:16] it might offer that are particular to
[10:16:18] Postgress itself. So here then is our
[10:16:22] table we used for cards in SQLite just
[10:16:25] to remind you again we had an ID column
[10:16:28] of type integer and that was our primary
[10:16:31] key. Well, we saw in MySQL we had a
[10:16:34] variety of integers and here we actually
[10:16:36] have the same thing in Postgress but
[10:16:38] they just look a little bit slightly
[10:16:40] different. So here I have a table of
[10:16:44] integers in Postgress the signed and
[10:16:47] signed values over here going from
[10:16:49] negative to positive. So unlike MySQL
[10:16:52] which had tiny int, uh medium int and so
[10:16:55] on, in Postgress we only have small int,
[10:16:59] int and big int. Just a little bit fewer
[10:17:01] options because the developers thought
[10:17:03] you might not need a tiny int or a
[10:17:05] medium int just give you three
[10:17:07] particular options. Now although there
[10:17:10] are fewer integer options, we also get
[10:17:13] something a little bit different. I can
[10:17:16] also use a serial type, small serial,
[10:17:20] serial or big serial. Now a serial is
[10:17:25] still an integer, a whole number, but it
[10:17:28] actually does what we try to do in MySQL
[10:17:32] for me, which was try to include an auto
[10:17:34] increment attribute. A serial will
[10:17:37] automatically increment for me, making
[10:17:39] it good for primary keys. So here, if I
[10:17:43] go back to my cars table and I had this
[10:17:46] ID column of type integer, I could
[10:17:49] update that to now be a serial where a
[10:17:52] serial means some whole integer number
[10:17:55] that will increase as I add more and
[10:17:57] more data to my table. Now what else do
[10:18:01] you notice here? Well, it seems like
[10:18:03] these double quotes are back in
[10:18:05] Postgress. So in MySQL, you had back
[10:18:08] ticks. In SQLite, you had double quotes.
[10:18:11] Well, in Postgress, you have double
[10:18:13] quotes for your identifiers here. So,
[10:18:16] this then is how we've changed our cards
[10:18:18] table. And now, let's actually do this
[10:18:21] inside of Postgress. I'll log in and
[10:18:24] create my very own database and my own
[10:18:27] table. So, I'll come back to my computer
[10:18:30] here. And now, let me do this. I will
[10:18:34] log into Postgress using this command
[10:18:37] right here. I'm going to open PSQL which
[10:18:41] is essentially the command line
[10:18:43] interface like MySQL but now just for
[10:18:46] Postgress. I'll hit enter here and I'll
[10:18:49] log in as the default Postgress user.
[10:18:52] This is the admin for Postgress. Now
[10:18:55] I'll type in my password and I'll see a
[10:18:58] prompt look just a little bit different
[10:19:00] but the same kind of spirit here. If I
[10:19:02] want to list all databases I don't type
[10:19:05] show databases. I just type back slashl
[10:19:09] for list and now I'll hit enter here and
[10:19:12] now I'll see a collection of default
[10:19:13] databases that come with the Postgress
[10:19:16] installation. Similar to MySQL, these
[10:19:19] are databases that contain configuration
[10:19:21] information metadata on this
[10:19:23] installation of Postgress. But now I
[10:19:26] want to create my own database one
[10:19:28] called MBTA. So I'll say create database
[10:19:32] same as before and call it MBTA. now
[10:19:36] using double quotes. If I hit enter now,
[10:19:39] I should see create database. It's
[10:19:41] confirming this statement. And if I type
[10:19:44] back slashl, I'll now see MBTA is
[10:19:48] included in my list of databases.
[10:19:51] So if I want to connect to a database in
[10:19:55] MySQL, I used use in Postgress, I'll use
[10:19:59] back slash C. So I'll say back slash C
[10:20:03] and then MBTA. Hit enter. And now I'm
[10:20:07] connected to the database MBTA as this
[10:20:10] user whose name is Postgress.
[10:20:14] And now if I want to see what tables I
[10:20:16] already have, I could type back slashdt,
[10:20:20] hit enter, and I'll see no relations, no
[10:20:24] tables, but just another way of figuring
[10:20:26] out this is an empty database.
[10:20:29] So we've seen so far how to log in to
[10:20:32] Postgress and some basic navigational
[10:20:35] statements we can use to work our way
[10:20:37] around this database. But it turns out
[10:20:40] there is some stuff that's familiar
[10:20:41] here. Like if I want to create a new
[10:20:43] table, I can do it the very same way I
[10:20:46] did it before. I could use create table.
[10:20:49] I could say create table. Let's say
[10:20:52] cards. And then let me include in this
[10:20:55] case an ID column of type serial which
[10:21:00] means an integer that auto increments
[10:21:03] for me. Then I'll apply the primary key
[10:21:07] constraint. Familiar old friend here.
[10:21:10] Then I'll close out cards like this. Hit
[10:21:13] enter. And I should see it confirms I
[10:21:16] created this table. If I now type
[10:21:20] slashdt to list my tables, I'll see I
[10:21:24] have a table called cards. And if I want
[10:21:28] to look at this table in particular to
[10:21:30] understand its schema, I could type
[10:21:33] slashd and then the name of that table
[10:21:36] cards like this. Hit enter. And now I
[10:21:39] should see some more information on this
[10:21:42] cards table. It has a column called ID,
[10:21:46] a type called integer, and some more
[10:21:48] information like we saw in MySQL, but
[10:21:51] now just in a different format.
[10:21:54] So, not to worry if these commands come
[10:21:57] uh a little bit seem maybe arcane to you
[10:22:00] at first glance. You'll get used to it
[10:22:01] with some practice if you choose to
[10:22:03] learn either MySQL or Postgress here. So
[10:22:07] let me pause before we go any further
[10:22:09] and just ask what questions so far do we
[10:22:12] have on Postgress if any?
[10:22:14] >> What's the sort of thing that indicates
[10:22:16] it's an error?
[10:22:18] >> Um a good question. So similar to SQLite
[10:22:21] or MySQL, you'll know you have an error
[10:22:24] when you hit enter and it doesn't say
[10:22:26] either query okay or repeat to you that
[10:22:29] um command you just used. It might give
[10:22:31] you a particular error like maybe you
[10:22:33] forgot a comma, maybe you forgot a quote
[10:22:35] somewhere. It should kind of give you an
[10:22:37] idea of what you didn't do correctly
[10:22:39] with the syntax. The best way to see it
[10:22:41] is just to try it and figure out what it
[10:22:44] tells you as you go.
[10:22:46] Okay, let's keep going then and we'll
[10:22:48] see a few differences between Postgress
[10:22:50] and MySQL 2. So, we have our cards
[10:22:54] table, but our other goal was to create
[10:22:56] a stations table. So, let me pull up
[10:22:59] what we did for this one. Let me find
[10:23:02] stations here. So this was our stations
[10:23:06] table with Postgress or sorry with
[10:23:08] SQLite we had an ID a name and a line
[10:23:12] column integer text and text for those
[10:23:15] types. Now we've seen in Postgress I
[10:23:18] could change this integer for my primary
[10:23:20] key to be a serial that's a little more
[10:23:22] apt for this use case here. And it turns
[10:23:24] out that in Postgress I also have
[10:23:27] varchars I could use inside of this
[10:23:30] station's table. I could make name a
[10:23:32] varchchar here up to size 32 characters.
[10:23:35] And for simplicity though we used an
[10:23:38] enum earlier. I'll now use a varchchar
[10:23:40] for line as well just to keep things
[10:23:43] simple. So here we've updated our
[10:23:45] stations table using what postgress
[10:23:48] might offer us. The real differences
[10:23:50] though come not in our stations table
[10:23:53] but actually inside of our other table.
[10:23:55] This one called swipes. So this here was
[10:23:59] our swipe table or some section of it.
[10:24:01] We had ids up top and primary key and
[10:24:04] foreign key constraints down below. Now
[10:24:07] remember we had type of text, date time
[10:24:10] of numeric and amount of numeric as
[10:24:13] well. Well, Postgress offers some other
[10:24:15] types we could use to update these as
[10:24:17] well. Among them are enum, our old
[10:24:20] friend again, but we use enum a little
[10:24:24] bit differently. So instead of including
[10:24:27] enum inside of our column definition, we
[10:24:31] actually create our very own type.
[10:24:34] Postgress supports something like this.
[10:24:37] Create a type and give it some name. And
[10:24:40] then I could say what that type actually
[10:24:43] is. So here I've created some type and
[10:24:47] called it swipe type and then said this
[10:24:50] type can have the following values enter
[10:24:53] exit or deposit and I can then use this
[10:24:56] name swipe type as my very own type in
[10:25:00] future create table statement. So
[10:25:03] something that Postgress has that my SQL
[10:25:05] might not in this form let's consider
[10:25:08] then dates and times. So dates and times
[10:25:11] largely similar. I have timestamp, date,
[10:25:14] time, and interval. A particular type
[10:25:17] representing the distance between times.
[10:25:19] How long did something take? But we
[10:25:22] still have our old friends date and time
[10:25:24] for dates and times respectively. And
[10:25:26] also time stamp to combine these two
[10:25:29] into one. And then we also have
[10:25:32] precision with these. I could say I want
[10:25:35] to represent to the hundreds place, the
[10:25:37] thousand's place or so on for each of
[10:25:39] time stamp, time and interval.
[10:25:42] Continuing on, we could also work with
[10:25:45] real numbers which are largely the same
[10:25:47] amenities between MySQL and Postgress
[10:25:50] with a few differences. One is that at
[10:25:53] least in Postgress we call decimal
[10:25:56] numeric. So numeric in this case can
[10:25:58] specify some precision that is the
[10:26:01] number of digits and the scale that is
[10:26:03] the number that come after the decimal
[10:26:04] point and new word to postgress is a
[10:26:08] type particularly for money which
[10:26:11] depending on your settings in your
[10:26:13] database will put to you either a
[10:26:15] certain number of decimal points and
[10:26:17] include perhaps a dollar sign or a euro
[10:26:20] sign or a pound sign whatever it is
[10:26:22] you're using and whatever it is you've
[10:26:24] configured in your database. So let's
[10:26:26] update now. Let's go ahead and improve
[10:26:29] this statement in swipes from SQLite to
[10:26:32] Postgress. Here I had type well that
[10:26:35] could now be our very own swipe type.
[10:26:38] Notice here I defined up above as an
[10:26:40] enum. Now I'm going to use it down below
[10:26:43] in my swipes table. This type column has
[10:26:47] the type swipe type and it cannot be
[10:26:50] null. Then I'll keep going and I'll make
[10:26:53] datetime just timestamp. timestamp is
[10:26:56] the newer version in Postgress of what
[10:26:59] um MySQL had called datetime and what
[10:27:02] SQLite called numeric and then instead
[10:27:05] of let's say current time stamp
[10:27:07] postgress just uses this function called
[10:27:09] now the current time stamp it will get
[10:27:11] for you as you add some new row and then
[10:27:15] finally amount we could use money we
[10:27:18] could use uh numeric we'll stick in this
[10:27:20] case to just numeric like we did for
[10:27:22] mysql and say numeric IC up to five
[10:27:25] digits, two of which come after the
[10:27:27] decimal point. So a whirlwind tour of
[10:27:31] some differences in types between MySQL
[10:27:34] and Postgress. What questions do we have
[10:27:37] on these? Not seeing too many here. Let
[10:27:41] me keep going. Come back to my computer
[10:27:44] here. So it's worth um showing that
[10:27:47] we're able to create a table. We can
[10:27:49] then show it and describe it like this.
[10:27:52] But then the question remains how do you
[10:27:54] get out of Postgress? Well, for that you
[10:27:56] can use let me clear my screen simply
[10:27:58] slash Q whereas in MySQL you could use
[10:28:02] quit in Postgress it's slash Q. So I'll
[10:28:05] hit enter on this and we'll say goodbye
[10:28:08] to Postgress for now but after the break
[10:28:10] we'll come back and keep working with
[10:28:11] MySQL and focus on actually what
[10:28:14] features we can use to scale up our
[10:28:16] applications. What does MySQL and
[10:28:18] Postgress offer to serve more users more
[10:28:21] frequently? Back in a few.
[10:28:24] And we're back. So, we've gotten a taste
[10:28:27] so far of both MySQL and Postgress, but
[10:28:31] now it's time to think through the
[10:28:32] features each offers up to scale up our
[10:28:35] application. So, let's envision a sample
[10:28:39] application here, one that starts off
[10:28:42] pretty small. We have users trying to
[10:28:44] read from this database about a hundred
[10:28:47] times per minute, but they're also
[10:28:50] writing to the databases, adding new
[10:28:52] data about 50 times per minute. And
[10:28:56] maybe this application over time, it
[10:28:58] grows a little bit. Maybe instead of a
[10:29:01] 100 reads, it goes up to a thousand. It
[10:29:03] multiplies by 10. And same thing for our
[10:29:06] rights, they also multiply on average by
[10:29:09] about 10. And this application, it gets
[10:29:12] even more popular, increases by tenfold
[10:29:14] again. Now we have 10,000 reads per
[10:29:17] minute, 5,000 writes per minute, and
[10:29:19] then finally it keeps growing another
[10:29:22] tenfold. And now we're at a 100,000
[10:29:25] reads per minute and 50,000 writes per
[10:29:28] minute. What might be the problem? If I
[10:29:32] had a single server like this, why might
[10:29:36] my application start to slow down?
[10:29:41] Uh so yeah, I would like to say that
[10:29:44] whenever the requests are increasing
[10:29:46] with that the time to which the server
[10:29:49] would reply would also increase and the
[10:29:52] list would seem to grow on and on. So
[10:29:54] yeah.
[10:29:55] >> Yeah, I like your thinking there. So you
[10:29:56] can think of the time that each query
[10:29:58] takes. As we saw in our optimizing
[10:30:00] lecture, we could time our queries. And
[10:30:02] if I have many, many, many of those
[10:30:05] queries running all at one time. I mean,
[10:30:07] that could add up substantially. So it's
[10:30:09] worth thinking about whether one
[10:30:12] computer can really handle all of these
[10:30:14] reads and all of these writes. So if you
[10:30:18] find yourself writing some application
[10:30:20] and it per behaves a little bit slower
[10:30:22] than you want it to at particularly at
[10:30:25] scale, you have a few options. And I
[10:30:29] want to ask you just to use your own
[10:30:30] intuition here. Like if you encounter
[10:30:33] this problem of your application slowing
[10:30:36] down, what might you try to do to solve
[10:30:40] that problem? Uh, you could try to you
[10:30:44] could try to optimize your queries.
[10:30:48] >> Yeah, try to optimize your queries. Make
[10:30:50] sure they take a little less time than
[10:30:51] they did before. Or you could even try
[10:30:54] to throw more hardware at the problem.
[10:30:56] Like maybe you have optimized your
[10:30:58] queries to the maximum you think you can
[10:31:00] and it's just still not fast enough.
[10:31:02] Well, one approach might be what's
[10:31:04] called vertical scaling. trying to make
[10:31:08] this single server all the more um
[10:31:11] quicker at replying to your queries. So
[10:31:14] vertical scaling is about increasing
[10:31:16] your application's capacity by
[10:31:18] increasing the capacity of a single
[10:31:21] server, the computing power of that
[10:31:23] server. So whereas this was our regular
[10:31:26] old server, you could imagine trying to
[10:31:29] vertically scale this server, just make
[10:31:31] it more powerful, optimize your queries
[10:31:33] and have them run on this server faster
[10:31:36] than they did before. But there's also
[10:31:40] another approach you could take. Here we
[10:31:42] focused on one server, but what else
[10:31:46] could you logically do to just have more
[10:31:49] resources at your disposal? Actually, we
[10:31:52] can horizontally scale up our server. We
[10:31:56] can add two or three more servers so we
[10:31:58] can manage it.
[10:31:59] >> Yeah, I like your thinking. So, maybe we
[10:32:02] buy a fancier server like this. But if
[10:32:05] we ever run out of this server's
[10:32:08] capacity, well, the only logical thing
[10:32:10] is to buy more servers. Like, let's have
[10:32:12] not just one but three, for instance.
[10:32:14] And this is an example of horizontal
[10:32:17] scaling. So horizontal scaling is
[10:32:20] increasing your application's capacity
[10:32:22] not by increasing a single server's
[10:32:24] computing power but by spreading it out
[10:32:27] buying more servers to handle that load
[10:32:29] across more in this case individual
[10:32:32] people who can do work on those queries.
[10:32:35] So horizontal scaling might look a bit
[10:32:37] more like this. We have not just one
[10:32:40] server but now three overall. So this
[10:32:44] process of having not just one server
[10:32:47] but multiple. It's a process called
[10:32:49] replication. So replication is keeping
[10:32:53] copies of your database not just on one
[10:32:56] server but on multiple. And this seems
[10:33:00] like a good idea. Like wouldn't it be
[10:33:02] great to have a copy of your data not
[10:33:04] just in one place but in multiple. Maybe
[10:33:07] you yourself have made a backup of your
[10:33:09] own data on your computer. This is not a
[10:33:11] dissimilar idea, but it turns out there
[10:33:15] are some challenges with this. Like it's
[10:33:17] very complicated to have servers
[10:33:19] communicate with themselves to keep
[10:33:21] track of who has the most recent
[10:33:23] updates. Uh who should I follow, who
[10:33:25] should lead and so on. And so for that
[10:33:28] reason, there are a few models of
[10:33:31] replication that you should at least
[10:33:33] know about. Among them are single leader
[10:33:36] replication, multiler replication and
[10:33:40] leaderless replication. So single leader
[10:33:43] means that there is a single database
[10:33:46] server out there that takes in the
[10:33:49] incoming rights to an application, the
[10:33:51] updates to some data and that single
[10:33:53] server passes them on to some copy to
[10:33:56] take care of making sure it's redundant
[10:33:59] that this data is stored not just in one
[10:34:02] place but multiple places too.
[10:34:05] Multile means there's not just one
[10:34:07] server listening for updates. There are
[10:34:09] multiple. And suffice to say, it gets a
[10:34:12] lot more complicated when there are more
[10:34:14] than one leader trying to listen for
[10:34:15] updates and process them. And finally,
[10:34:18] there are some other ones like leader
[10:34:20] lists and some more that actually just
[10:34:21] do away with leaders altogether and do
[10:34:23] something totally different. But today,
[10:34:25] we'll focus on single leader. One of the
[10:34:27] most basic replication strategies you
[10:34:29] could try and one that is built into
[10:34:32] MySQL. So let's focus on this one here.
[10:34:36] You could imagine in this case that you
[10:34:39] have a computer and you're trying to
[10:34:41] connect to some social network. Well,
[10:34:44] here are two databases. One is a leader
[10:34:48] and one is a follower. And just to check
[10:34:52] for understanding here, let's say I want
[10:34:54] to upload a profile photo. I'm updating
[10:34:57] some data to which server would I send
[10:35:01] that data? If I want to change something
[10:35:03] on the server, who's listening for that
[10:35:06] request?
[10:35:07] >> I think that we will send to the leader
[10:35:10] because the other data servers would get
[10:35:12] data from the leader. They will get
[10:35:13] updated from the leader, but the I will
[10:35:15] send to the leader because it will have
[10:35:18] the latest data for other servers and
[10:35:20] other users.
[10:35:21] >> Yeah, exactly right. So if I want to
[10:35:23] change some piece of data, I know by
[10:35:26] definition the leader has the most
[10:35:28] recent copy of that data and is also the
[10:35:31] designated server to process updates to
[10:35:34] my database, changes to its data like
[10:35:37] insertions or updates or deletions. So
[10:35:40] if I'm uploading some profile photo,
[10:35:42] I'll send this photo of of me right here
[10:35:45] to my leader and that leader will then
[10:35:47] take that profile photo and store it on
[10:35:50] the database. But before long the leader
[10:35:53] will also talk to communicate with the
[10:35:56] follower make sure that the follower has
[10:35:58] a copy of this data elsewhere. So it
[10:36:01] will forward on this update to the
[10:36:03] follower who will then process it in
[10:36:06] turn. And now that both the leader and
[10:36:09] the follower have this data. Well, who
[10:36:12] could I ask to see the latest profile
[10:36:14] photo for Carter Zeni? Which server
[10:36:18] might have that? Both the server also
[10:36:20] has the data.
[10:36:21] >> So I could ask either server for
[10:36:23] information on this profile photo. I
[10:36:26] could ask either the leader or the
[10:36:28] follower because each is storing a copy
[10:36:31] of this photo or rather a copy of its
[10:36:34] location on the server itself. Now let's
[10:36:38] say here I ask the follower for this
[10:36:40] profile photo so I can see it on my own
[10:36:42] browser. Here I'll ask the follower and
[10:36:45] get back that image inside of my own
[10:36:48] browser. But I could have asked either
[10:36:51] one to distribute that load across both
[10:36:54] of these servers. Now this follower is
[10:36:57] what's known as a read replica. A read
[10:37:01] replica is a server from which we would
[10:37:03] only ever read data. If I ever wanted to
[10:37:07] update some photo or insert some new
[10:37:10] rows, I would never ask the follower. I
[10:37:13] would always ask the leader who's in
[10:37:15] charge so to speak of handling these
[10:37:17] updates and these rights to that
[10:37:20] database. So the next step is to think
[10:37:22] about um not just the types of leaders
[10:37:26] that we have but also how they
[10:37:28] communicate. And in general there are
[10:37:31] two options for communication both
[10:37:34] synchronous and asynchronous. So
[10:37:36] synchronous means that the leader will
[10:37:39] wait for the follower to get the data
[10:37:42] and process it before doing anything
[10:37:44] else. It synchronizes with that
[10:37:47] follower. Asynchronous though means the
[10:37:50] leader sends that data to the follower
[10:37:52] and doesn't wait for the follower to
[10:37:53] finish processing. It just keeps going
[10:37:55] and going hoping the follower is keeping
[10:37:58] up. So let's focus first on a few of
[10:38:01] these in particular on synchronous. Now
[10:38:04] in this diagram I have a client and a
[10:38:08] server. My client is my computer. The
[10:38:11] server is some database. And on this
[10:38:14] xaxis here left to right. I have time.
[10:38:18] Well, if I want to make a request to
[10:38:21] this server, I might denote that with a
[10:38:23] line like this. My client sends some
[10:38:26] requests to my server. Maybe it asks for
[10:38:28] data or tries to update some photo. then
[10:38:32] that takes some time to get the request
[10:38:34] from my client to the server down here.
[10:38:38] And the response itself also takes some
[10:38:40] time. Maybe the server responds, hey,
[10:38:43] everything's okay. I got your photo,
[10:38:45] here's your data, etc. It'll take some
[10:38:47] time for that to get back to me. So,
[10:38:50] between here and here, that's how long
[10:38:52] it took for me to receive some data from
[10:38:55] this server. Now let's focus on
[10:38:58] synchronous replication here where the
[10:39:01] leader and the follower are always in
[10:39:04] sync. So this might look a bit like
[10:39:06] this. If I add in the follower and I
[10:39:08] have a leader and a follower, I might
[10:39:11] send that profile photo to the leader a
[10:39:14] bit like this. The leader then sends it
[10:39:16] to the follower down below and waits. It
[10:39:20] waits until the follower has confirmed
[10:39:23] they have received that photo. they have
[10:39:25] added to the database and now they send
[10:39:27] back a request saying look I got it
[10:39:30] everything is okay and now only at this
[10:39:33] point once the leader has received the
[10:39:36] okay from the follower does it then
[10:39:38] communicate with me it then says
[10:39:40] everything's okay we got your photo this
[10:39:44] is great because it's redundant like I
[10:39:46] know for sure that my photo is on both
[10:39:49] the leader and the follower but there is
[10:39:52] a downside and looking at this diagram
[10:39:55] here. What do you think that downside
[10:39:58] might be?
[10:39:59] >> Maybe it's too slow.
[10:40:00] >> Yeah, exactly. It could be just too
[10:40:02] slow. Like if I have to wait for the
[10:40:05] follower to get the okay back to the
[10:40:07] leader and then back to me, that's just
[10:40:09] more time for me to wait. And maybe my
[10:40:12] application shouldn't wait around that
[10:40:15] long. You might use this though if
[10:40:17] you're working in finance or healthcare
[10:40:20] where you have to be doubly sure you
[10:40:22] have data stored exactly as you want it
[10:40:25] to be. But if you're like a social media
[10:40:28] site like a Facebook or a Twitter, I
[10:40:30] mean maybe you don't care if you lose a
[10:40:31] tweet every once in a while. It's okay.
[10:40:34] So maybe synchronous isn't the best most
[10:40:36] ideal scenario for that as well. So
[10:40:40] let's think through now asynchronous. So
[10:40:42] we'll go back to asynchronous here and
[10:40:44] think through our diagram again. Well,
[10:40:46] in asynchronous, the leader doesn't wait
[10:40:49] around for the follower to get the data.
[10:40:51] So to visualize, my client could send
[10:40:53] this to the leader. Maybe a photo
[10:40:56] update, for example. Then
[10:40:58] simultaneously, the leader tells me, I
[10:41:00] got your photo, everything's okay. And
[10:41:03] then send the photo to the follower. The
[10:41:06] follower might later on tell the leader
[10:41:08] that everything's okay, but the leader
[10:41:11] already told me, "Look, all good. We got
[10:41:13] your photo." So, there's nothing more to
[10:41:15] do after this. Now, this admittedly is
[10:41:19] faster. Like, this amount of time is
[10:41:21] much shorter. But again, there is some
[10:41:24] downside here. Why might I not want to
[10:41:27] use asynchronous replication? At least
[10:41:30] in some cases,
[10:41:32] >> I would guess that it's um an issue with
[10:41:35] data being corrupted possibly.
[10:41:37] >> So, you're right. There could be some
[10:41:38] data corruption here where let's say the
[10:41:41] leader sends some data to the follower
[10:41:43] and they confirm for me that that data
[10:41:45] has been received across all instances
[10:41:47] of these servers. Well, I mean later on
[10:41:50] maybe the follower encounters some
[10:41:52] problem and they don't actually follow
[10:41:54] through. Well, at that point I have had
[10:41:56] a bad contract with my leader. It told
[10:41:58] me that everything was okay, but
[10:42:00] actually it wasn't. So, there are all
[10:42:02] kinds of trade-offs here. Um, whether in
[10:42:04] terms of the time that things take or
[10:42:06] redundancy, but it's up to you to decide
[10:42:09] which one might work best for your own
[10:42:11] use case, synchronous replication or
[10:42:13] asynchronous.
[10:42:15] Now, in addition to replication, there
[10:42:17] is some other strategy for scaling you
[10:42:20] should be at least familiar with, and
[10:42:21] this is a process known as sharding.
[10:42:24] Now, sharding is great for really large
[10:42:27] data sets on the order of many, many,
[10:42:29] many gigabytes or terabytes of data that
[10:42:32] you just can't fit on a single server or
[10:42:34] a single computer. Sharding involves
[10:42:37] taking some data set like that and
[10:42:40] essentially splitting it up in some
[10:42:41] logical way across multiple servers like
[10:42:44] this. Maybe for simplicity, you have
[10:42:47] some database of names, and you decide
[10:42:49] that all of those names that begin with,
[10:42:52] let's say, A to I end up on this server
[10:42:55] here, this first one. But then all those
[10:42:58] names J through R, well, they get stored
[10:43:00] on this server here. And S through Z,
[10:43:03] they get stored on this third server
[10:43:05] here. So our data has been split or
[10:43:08] sharded across multiple instances of
[10:43:10] some database server. And this is
[10:43:13] helpful because if I had a really large
[10:43:15] data set, it now is smaller on every
[10:43:18] individual database server. You could
[10:43:21] also organize your data by, let's say,
[10:43:23] primary key. Maybe you have 3,000 rows
[10:43:26] or 3,000 records. And the first one
[10:43:29] through a,000, those go on this first
[10:43:31] server. The second, 101 to 2,000
[10:43:34] inclusive, those go on the second
[10:43:36] server. And 2001 to 30,000 also
[10:43:38] inclusive, those go on that third
[10:43:41] server. Now, there's a lot of thought
[10:43:43] that goes behind the best way to shard
[10:43:46] your data. The goal is to really to
[10:43:48] avoid what we call um a hot spot wherein
[10:43:52] one database server becomes more
[10:43:54] frequently accessed or requested than
[10:43:57] others. Like let's say for some reason
[10:43:59] the data in 101 to 2000 gets um accessed
[10:44:04] quite a lot. Well, now we're actually uh
[10:44:06] trying to um run into a problem here
[10:44:09] wherein one server gets overload. The
[10:44:12] same problem we're trying to guard
[10:44:13] against using sharding. So, it's
[10:44:16] important then to think about what's the
[10:44:18] best most logical way to distribute
[10:44:20] data. So, you don't have one server
[10:44:23] being accessed much more than another.
[10:44:27] There's another problem here too, which
[10:44:29] is if I'm not using replication, I'm
[10:44:32] only using sharding. Well, let's say
[10:44:35] that one server goes down. What do we
[10:44:38] have now? Maybe we're missing all the
[10:44:41] names that went in the middle of um our
[10:44:43] partition. Or maybe we're missing all of
[10:44:45] those rows. Uh let's see, 101 to 2,00
[10:44:49] for instance. And that would be what we
[10:44:51] call a single point of failure. If one
[10:44:54] system goes down, our entire system is
[10:44:57] now not usable. So something to keep in
[10:44:59] mind as you work on sharding is also you
[10:45:02] could combine it with some strategies
[10:45:04] from replication to keep copies of your
[10:45:06] data across servers too.
[10:45:10] So these are some features built into
[10:45:12] MySQL and Postgress for scaling but they
[10:45:16] also give user accounts and we can
[10:45:18] perhaps enhance our security by taking
[10:45:21] advantage of some of those user
[10:45:22] accounts. So let's talk now about this
[10:45:25] idea of access control trying to have
[10:45:28] users and only grant some of them
[10:45:30] certain permissions. So here we saw
[10:45:33] before I was logging into MySQL using
[10:45:36] the root user. The root user is the
[10:45:39] admin. But I could just as easily create
[10:45:42] a new user perhaps one called Carter for
[10:45:45] myself. So I will open up MySQL again.
[10:45:49] And in this case I will create a new
[10:45:52] user one named Carter. So to do so I can
[10:45:56] use this command here this statement
[10:45:58] here create a user whose name is Carter
[10:46:03] in single quotes. Now I can say they are
[10:46:07] identified by the password and this
[10:46:10] password is literally password P A S W
[10:46:14] D. It is one of unfortunately the most
[10:46:16] popular passwords. do not use his
[10:46:18] password. So I will hit enter here and
[10:46:22] now I have created some new user named
[10:46:24] Carter and I can log in using that
[10:46:27] Carter username. So I'll create myself a
[10:46:30] new terminal here and I will try to log
[10:46:33] in to my SQL again. I will run this
[10:46:38] statement here. I'll say MySQL which is
[10:46:41] the command line interface for the MySQL
[10:46:43] server and I will say I want to connect
[10:46:46] using this user carter before we used
[10:46:50] root but now I'll use Carter the host
[10:46:53] the place the server is located is
[10:46:55] 127.0.0.1
[10:46:57] 0.1 my own computer here. This is the IP
[10:47:00] for this very computer. I can then say
[10:47:03] dash P capital P for the port number
[10:47:06] 3306 by default. And finally P means
[10:47:10] prompt me for my password. I'll type it
[10:47:12] in here. So I'll hit enter. And now I
[10:47:15] get prompted for the password. I'll type
[10:47:17] that in here. And now oh wait, I typed
[10:47:21] in my password. So let me try this
[10:47:22] again. So, I'll go back up and I will
[10:47:24] type in my password, which was password.
[10:47:27] Hit enter. And now I'm logged in as
[10:47:30] Carter. So, by default, if I try
[10:47:34] something like this, show databases.
[10:47:36] Enter. I'll only see a few. Like, I'm
[10:47:40] pretty sure I had MBTA, MFA in here, and
[10:47:44] a few others, but I just can't see them.
[10:47:47] So when I create this new user, by
[10:47:50] default it has very few privileges, very
[10:47:52] few ways of accessing this database, but
[10:47:56] I could decide to grant some privileges.
[10:47:59] And just to show you, let me be root
[10:48:01] again for a second. Here I'm the admin.
[10:48:04] I can do most anything I want. And
[10:48:06] notice how in here I have a new
[10:48:08] database. I can type show databases.
[10:48:11] Enter. And I'll see I have a new
[10:48:14] database called ride share which is
[10:48:16] similar from a prior week on viewing and
[10:48:19] security. So if I say use ride share
[10:48:24] semicolon enter I could say select star
[10:48:28] from ride share semicolon. Now whoops
[10:48:31] sorry the table isn't rid share. Se star
[10:48:33] from rides then I'll hit enter here. And
[10:48:37] now I'll see all of the rides in the
[10:48:40] rides table which is part of the ride
[10:48:42] share database. And if I look at this
[10:48:45] table in our week on viewing, we talked
[10:48:48] about eliminating some PII, personally
[10:48:53] identifiable information.
[10:48:55] What was that PII here?
[10:48:59] Seems it was the rider column, like the
[10:49:01] names of those riders. We know where
[10:49:03] each rider is going. But ideally, we
[10:49:05] should make a new view. One that allows
[10:49:08] us to see not the riders, but only their
[10:49:11] origins and destinations. Removing this
[10:49:14] pi of individuals names.
[10:49:18] So, by default, Carter can't see this
[10:49:21] data, but neither can Carter see the
[10:49:24] view I made called analysis. If I go
[10:49:27] back to my computer here, I could type
[10:49:31] select star from analysis. Hit semicolon
[10:49:35] enter. And now I'll see the view I had
[10:49:38] made the virtual table that removes that
[10:49:41] PII. But here I'm logged in as root. If
[10:49:44] Carter wants to see this, I go over
[10:49:46] here, show databases. I can't even see
[10:49:49] the ride share database. So the root
[10:49:52] user needs to grant access to Carter to
[10:49:55] see this particular view. Now for that I
[10:49:58] can use some syntax looks a bit like
[10:50:01] this here. I can use both grant and
[10:50:05] revoke. Grant means to give some
[10:50:08] privilege like select or update or
[10:50:10] delete on some table to a particular
[10:50:14] user. Revoke means simply to remove that
[10:50:17] permission. If I gave you select before,
[10:50:19] I'll now revoke it down below like this.
[10:50:22] And there are many privileges you can
[10:50:23] use. You could use all like everything.
[10:50:26] Allow Carter to do literally everything
[10:50:28] he could do. There's create to create
[10:50:31] tables and views and so on. There's
[10:50:33] insert to add data, select to read, and
[10:50:36] all the way down this list. Look at
[10:50:38] documentation to figure out what you can
[10:50:40] use here.
[10:50:42] So I want to give Carter, it seems like
[10:50:44] a select privilege on the view I created
[10:50:47] for analysis in this database. So I'll
[10:50:50] come back over here and I'll try that. I
[10:50:53] will log in as root here and I will try
[10:50:58] to grant the um let's see grant the
[10:51:03] select permission privilege on the ride
[10:51:07] share database in particular the
[10:51:11] analysis table inside of it and I'll
[10:51:14] grant that to Carter like this semicolon
[10:51:18] and enter now I'll see the query is okay
[10:51:22] If I log back in as Carter down here and
[10:51:25] now type show databases, enter, I should
[10:51:29] see I can now see the ride share
[10:51:31] database. So I'll type use ride share
[10:51:35] semicolon database changed. I could say
[10:51:38] show tables and what do I see but that
[10:51:41] virtual table that view called analysis.
[10:51:45] So now as Carter I can select I can uh
[10:51:49] select star from analysis semicolon and
[10:51:54] see that same data but I can't see the
[10:51:57] ride data. If I say select star from
[10:52:00] rides that table that's currently hidden
[10:52:02] to me I get back you don't have
[10:52:05] permission.
[10:52:07] So this is the benefit of MySQL's users
[10:52:11] and privileges to make sure I could have
[10:52:13] multiple users accessing this database
[10:52:16] and then only allowing some to access
[10:52:19] confidential data. So let me ask now
[10:52:23] what questions we have on access control
[10:52:26] in MySQL and Postgress. uh if we have to
[10:52:30] like ask for everything, do we grant uh
[10:52:34] is there any like particular syntax for
[10:52:36] that or should we type on all the uh
[10:52:39] like select right and everything?
[10:52:41] >> Yeah, a great question here. Like if you
[10:52:43] want to give somebody multiple
[10:52:44] privileges, what could you do? One
[10:52:47] approach is you could say grant and then
[10:52:50] say the privilege and then have a comma
[10:52:52] afterwards. I could grant select, comma,
[10:52:55] insert, comma, etc. including the tables
[10:52:58] that I this user can insert, update,
[10:53:00] delete on, etc. You could also use all
[10:53:03] like if I say grant all on star.star to
[10:53:07] Carter, that means grant all permissions
[10:53:10] on everything to this user named Carter.
[10:53:13] So you can absolutely do either of those
[10:53:16] approaches, but best to be more fine
[10:53:18] grained, particularly in a production
[10:53:20] environment.
[10:53:23] Okay, great questions here. So let's
[10:53:25] keep going. So this then was how to uh
[10:53:29] use access controls. Um but it's also
[10:53:33] worth thinking about ways we can prevent
[10:53:36] other kinds of attacks and harden the
[10:53:38] security of our database. Like here I
[10:53:42] have users and passwords which works
[10:53:45] well. But if I were to expose my
[10:53:48] application to the outside world, I
[10:53:50] should also be concerned about a few
[10:53:52] other attacks here. Now, one of these
[10:53:55] attacks is a SQL injection attack. SQL
[10:54:00] injection means I have some query and
[10:54:03] somebody else adds in some malicious
[10:54:06] code to finish that query for me. So,
[10:54:10] for example, maybe I have a query like
[10:54:12] this select ID from the users table
[10:54:16] where the username equals someone's
[10:54:19] username and the password equals
[10:54:21] somebody's password. And if I find a
[10:54:25] user matching this username and
[10:54:27] password, if I get back an ID, I'll log
[10:54:30] that user in. Now, in a regular website,
[10:54:35] if someone was actually behaving nicely,
[10:54:37] they could type in their username like
[10:54:39] this, and they could type in their
[10:54:40] password a bit like this. This is kind
[10:54:42] of what I did before. I logged in as
[10:54:44] Carter and gave the password of
[10:54:46] password. And when you are entering your
[10:54:49] own username and your own password on
[10:54:51] some website, something similar to this
[10:54:54] is likely happening. There might be some
[10:54:56] SQL query that takes your username and
[10:54:58] takes your password and inserts them
[10:55:01] into a SQL query to figure out are you
[10:55:04] who you say you are. But let's think a
[10:55:07] bit more maliciously about this. Like
[10:55:09] here, if I gave you permission to add
[10:55:12] anything to this dot dot dot here,
[10:55:16] anything at all, what could you do to
[10:55:20] try to hack this database to log in as
[10:55:23] Carter? Keep in mind that this is
[10:55:26] selecting an ID from users where some
[10:55:29] condition is true. What might you be
[10:55:32] able to add to this dot dot dot to log
[10:55:35] in as me? Yes, you could use some u kind
[10:55:39] of statements like
[10:55:42] union or with or delete something, etc.
[10:55:47] >> Yeah, I could really put most anything I
[10:55:49] want in here. But the SQL injection
[10:55:52] attack comes about when I deliberately
[10:55:54] put some SQL statement that I think will
[10:55:56] give me access to some data I shouldn't
[10:55:58] have access to. So you could imagine
[10:56:01] maybe I type in my password but then I
[10:56:03] type you know a single quote followed by
[10:56:06] or 1 equals 1. Now what would that do?
[10:56:10] Well notice that 1 equals 1 that
[10:56:13] condition will always be true. And so
[10:56:16] this condition where username equals
[10:56:18] Carter and password equals password.
[10:56:20] Well, in that case, I have access to
[10:56:23] Carter's account because I modified the
[10:56:25] condition to just always be true whether
[10:56:28] or not the password is correct. Let's
[10:56:31] see one more example here. Maybe I'm
[10:56:34] logging into my bank account and I want
[10:56:36] to check my balance. We could maybe
[10:56:38] assume that the bank has some table of
[10:56:41] balances or has some people of accounts
[10:56:43] that have balances. And I could type in
[10:56:46] my account number like this. you know, 1
[10:56:47] 2 3 4 all the way up to number nine
[10:56:50] here. And that will give me access to my
[10:56:53] accounts balance. But now let's take a
[10:56:56] look at this query here. Select balance
[10:56:59] from accounts where ID equals the
[10:57:01] account number. What kinds of SQL
[10:57:04] statements could you include in this ID
[10:57:07] value here to get access to everyone's
[10:57:12] account balances? So we basically have a
[10:57:15] where which does some ID. If we just
[10:57:18] commented that part out then
[10:57:22] it would be a sort of a problem. Or if
[10:57:25] we just did the similar example to the
[10:57:28] last time like putter or one is equal to
[10:57:31] one that could also trigger it. So there
[10:57:34] are multiple options.
[10:57:35] >> Yeah I like your thinking here. There's
[10:57:37] definitely more than one option. I like
[10:57:39] your thinking of maybe we include some
[10:57:41] comment that kind of messes up this
[10:57:44] query. Maybe it removes the condition.
[10:57:46] So I just get select balance from
[10:57:48] accounts. That could be one strategy. I
[10:57:51] could maybe include um an or that maybe
[10:57:55] makes sure that this wear is just always
[10:57:57] true. Give me back all balances from
[10:57:59] this account. I could also use as well a
[10:58:03] union like this. I could say make sure I
[10:58:06] add my own account ID. But then union
[10:58:09] some other query like this union select
[10:58:12] ID from accounts. Now I have all the
[10:58:15] account ids from this table and I could
[10:58:18] then query them one at a time for their
[10:58:21] balance. So let's try this out in MySQL
[10:58:24] to see some of the dangers of these
[10:58:26] injection attacks. Go back to my
[10:58:29] computer here and I'll show you how I
[10:58:32] already have a database set up for this.
[10:58:35] If I type show databases, hit enter. I
[10:58:40] see bank is one database here. Well, I
[10:58:43] want to use that database. I'll say use
[10:58:46] bank and then hit enter semicolon. Um,
[10:58:50] and now I can say show tables where I
[10:58:53] see an accounts table and I'll select
[10:58:56] star from accounts. Enter semicolon here
[10:59:00] to see some familiar users and some
[10:59:03] familiar balances.
[10:59:05] So let's actually complete this
[10:59:08] injection attack we just saw on the
[10:59:10] slides. Maybe this bank has some feature
[10:59:14] where I can choose some ID. I can enter
[10:59:16] in my own account ID to see my balance.
[10:59:20] So on the website they complete this
[10:59:22] query for me. I give them let's say the
[10:59:25] ID one. I am Alice in this case. They
[10:59:28] might finish this. They might say select
[10:59:30] star from accounts where the ID equals
[10:59:34] 1. And they might automatically run this
[10:59:37] SQL query. I'll hit enter. And now I'll
[10:59:40] see the balance for this account. Well,
[10:59:45] now what else could I do? I could try to
[10:59:48] deliberately mess up this query to run
[10:59:51] my own SQL injection attack. I could
[10:59:54] select let's say star from accounts and
[10:59:58] then let me try where the id equals 1. I
[11:00:02] give them one but I also give them some
[11:00:05] SQL statements they unwittingly execute.
[11:00:07] I say union and then select uh star from
[11:00:13] accounts bit like this. Now I'll hit
[11:00:16] enter. And if I complete this query, I
[11:00:19] see not just my own, I see everyone's
[11:00:22] balances and their names, too. So, this
[11:00:26] is one demo of how SQL injection attacks
[11:00:29] can show and leak data that isn't
[11:00:32] intended to be leaked. And sadly, these
[11:00:34] are fairly common today among people who
[11:00:36] just aren't familiar with how to prevent
[11:00:38] them.
[11:00:39] So let me ask now what questions we have
[11:00:42] on these attacks before we get to how to
[11:00:46] guard against them.
[11:00:48] >> Can we use some regular expressions
[11:00:51] also?
[11:00:52] >> Ah could you use regular expressions? So
[11:00:54] if you're familiar a regular expression
[11:00:56] is some pattern of characters that can
[11:00:58] match some text and find values within
[11:01:01] some text. I personally haven't seen
[11:01:04] regular expressions being used for
[11:01:06] injection attacks but that doesn't mean
[11:01:08] they can't be. So always do your
[11:01:09] research on what you can and can't use
[11:01:11] for an injection attack. But a good
[11:01:14] question here.
[11:01:16] Okay. So we've seen now SQL injection
[11:01:18] attacks, but how do we prevent them?
[11:01:21] Well, one strategy is using what we call
[11:01:23] a prepared statement. A prepared
[11:01:26] statement is kind of what it sounds
[11:01:28] like. A prepared statement is a
[11:01:30] pre-prepared statement. Is a statement
[11:01:31] that we will later on insert some values
[11:01:35] into. We might treat it like a fill-in-
[11:01:37] thelank, like here is my select and I'll
[11:01:40] let you fill in what you want me to
[11:01:43] select, but I'll make sure to clean your
[11:01:46] input before actually adding it in. So,
[11:01:49] let's think through a few of these here.
[11:01:51] Here I have prepare name from statement.
[11:01:56] This is a SQL statement I can use to
[11:02:00] prepare some statement to take some user
[11:02:03] input to make sure that when I add in
[11:02:06] that user input nothing malicious will
[11:02:09] happen. And in particular I can make
[11:02:12] sure the statement looks something a bit
[11:02:13] like this. Select balance from accounts
[11:02:16] where ID equals question mark. This
[11:02:20] question mark is just a question mark,
[11:02:23] but syntactically it stands for the
[11:02:26] ability of this statement to clean
[11:02:29] whatever I put inside of it to make sure
[11:02:32] it doesn't inadvertently run SQL code. I
[11:02:35] don't want it to run. So, let's try
[11:02:39] making our very own prepared statement
[11:02:41] to guard against these kinds of
[11:02:43] insertions here. I'll go back to my
[11:02:46] computer and let's try this one out. I
[11:02:50] could go back to MySQL
[11:02:52] and let me prepare some statement. I
[11:02:56] could say let's prepare a statement
[11:02:58] called balance check like we had before.
[11:03:02] And now if I try to prepare this
[11:03:06] statement from the following select star
[11:03:10] from accounts
[11:03:12] where the ID equals question mark end
[11:03:16] quote semicolon. So in single quotes I
[11:03:20] have the query I'm trying to prepare to
[11:03:23] take user input and I'm giving it some
[11:03:25] name like balance check. So I'll hit
[11:03:28] enter now and I'll see the query is
[11:03:30] okay. Statement prepared. Now if I want
[11:03:33] to run this statement to check on
[11:03:37] somebody's balance, I can go through a
[11:03:39] few steps. I could first set my own
[11:03:43] variable. Like let's say I get some user
[11:03:45] input from the user. They type in one
[11:03:48] underneath the hood in SQL. I could say
[11:03:51] set this variable called ID equal to
[11:03:55] one. this at symbol. It's just a uh
[11:03:57] convention for variables in MySQL.
[11:04:01] Now I'll hit enter. So the user input is
[11:04:04] stored separately in some variable, not
[11:04:07] inside of my SQL query like we saw
[11:04:09] before. Now I can execute I can say
[11:04:13] execute in this case the balance check
[11:04:17] statement
[11:04:18] using that same variable at id. So that
[11:04:24] question mark I had before, I will then
[11:04:26] take whatever the user typed in and
[11:04:29] clean it and then substitute in that
[11:04:32] value into this. So I'll say using ID
[11:04:36] and now I get back Alice's balance.
[11:04:41] And just to be clear here, let me try to
[11:04:43] make this deliberately malicious. I want
[11:04:45] to see everyone's accounts. Well, we saw
[11:04:48] before that I completed this query by
[11:04:51] typing in let's see set at id equal to
[11:04:55] one, but then union select star from
[11:04:59] accounts. This was what I added to that
[11:05:01] query to show me everyone's account
[11:05:04] balances. And I'll try to do the same
[11:05:06] here. I'll say this is what I'm trying
[11:05:09] to substitute into this prepared
[11:05:11] statement. I'll hit enter. Now execute
[11:05:15] again. I'll say execute balance check
[11:05:17] using at id which has an ID but also
[11:05:21] some malicious SQL statements. Now if I
[11:05:24] hit enter, what do I see? Only Alice's
[11:05:29] balance. So it seems that the prepared
[11:05:31] statement cleans up my input, ensures
[11:05:34] that if I have SQL statements, they
[11:05:36] don't get run. So we've seen now SQL
[11:05:41] injection attacks and how to guard
[11:05:43] against them. What questions do we have?
[11:05:47] >> So for this previous example you shown
[11:05:49] us, does the prepare statement only take
[11:05:51] into account the first uh the first
[11:05:54] acceptable condition or how does it
[11:05:56] work?
[11:05:57] >> Yeah, good question. So here, let me
[11:05:58] show you again the ID that I had um put
[11:06:02] inside of here. So if I say select at ID
[11:06:05] like that, I'll see this is the value of
[11:06:08] ID one union select star from accounts.
[11:06:12] And what happens is this paired
[11:06:14] statement does a process called
[11:06:16] escaping. It finds all of the SQL
[11:06:19] keywords, all of the values that could
[11:06:21] be malicious and escapes them. So they
[11:06:23] don't actually get executed. So it seems
[11:06:26] like in this case what actually happened
[11:06:28] was type in the query again. Balance
[11:06:30] check was select star from accounts
[11:06:34] where id equals 1. It seems like it just
[11:06:37] did the equals one part to give me back
[11:06:40] in this case the account balance while
[11:06:43] cleaning up the rest of it overall.
[11:06:46] Okay, let's take one more question here.
[11:06:49] >> So, uh is this the same reason why we
[11:06:52] shouldn't use a formatted string in
[11:06:55] Python to execute a SQL query?
[11:06:58] >> Yeah. So if you're familiar with Python
[11:07:00] format strings, it's a similar kind of
[11:07:02] pitfall which is you can add in any
[11:07:05] possible value for this variable you're
[11:07:08] substituting into and that can lead to
[11:07:10] some unintended consequences. So
[11:07:12] similarly, should we create um prepared
[11:07:14] statements that can actually clean and
[11:07:17] um escape the data that we might want to
[11:07:19] insert into our queries or our
[11:07:21] statements over there too? Good
[11:07:23] question.
[11:07:26] Okay, so we've seen here SQL injection
[11:07:28] attacks and also how to guard against
[11:07:32] them. And actually by now you're pretty
[11:07:35] well equipped to go off into the world
[11:07:37] of databases. And even though this is
[11:07:39] our last week, I hope you think back on
[11:07:42] how far you have come. So you began by
[11:07:45] querying a single table, a table of
[11:07:48] books in this case. You then graduated
[11:07:51] into tables that were related of books
[11:07:54] and authors and publishers and so on and
[11:07:56] querying those as well. Afterwards, you
[11:08:00] saw how to design your own databases,
[11:08:02] learn about types and create table
[11:08:04] statements to build something up from
[11:08:06] scratch. Finally, you saw how to write,
[11:08:09] how to add data to those databases you
[11:08:12] had designed. And then you kept going.
[11:08:14] You saw how to view databases, how to
[11:08:17] see them in a more simplified light, how
[11:08:19] to optimize those queries, and finally
[11:08:22] today, how to scale up all of this so we
[11:08:25] can serve more and more users. So, I
[11:08:28] hope after all these weeks that you are
[11:08:30] proud of how much you've grown. We are
[11:08:32] certainly proud of you all, too. Now, go
[11:08:34] off and continue your learning. We'll
[11:08:36] see you later.
