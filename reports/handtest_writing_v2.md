# Prompt hand-test: writing

- Variant: `writing-86bf72__Qwen2.5-7B-Instruct-AWQ` (prompts: doc=`writing_style`, query=`writing_style`)
- Model: `Qwen/Qwen2.5-7B-Instruct-AWQ`, greedy decoding
- Words per profile: min 83, median 135, max 164 (target 60-120); in range: 6/20
- Format compliant (6 fields): 20/20
- Profiles containing formula symbols ($ \ ^ _ { } =): 0/20
- Profiles with copied content words: 20/20

| Cosine (Qwen3-0.6B) | same group | different group | gap |
|---|---|---|---|
| raw text | 0.260 | 0.214 | +0.046 |
| profile | 0.653 | 0.634 | +0.019 |

A bigger gap means profiles separate the hidden property better than raw text does.

## Group 1

**query `49`** (95 words)

> Part of me feels bad not to have written for weeks about quantum error-correction or BQP or QMA or even the new Austin-based startup that launched a “quantum computing dating app” (which, before anyone asks, is 100% as gimmicky and pointless as it sounds).  But the truth is that, even if you cared narrowly about quantum computing, there would be no bigger story right now than the fate of American ...

Profile: Voice: We, informal and direct, addressing the reader as an ally
Sentences: Short and punchy, with a rapid rhythm; sentences often begin with intensifiers or hedges
Punctuation: Frequent use of ellipses, colons, and parentheses; quotation marks around specific phrases
Tone and humour: Sarcastic, with a touch of dry humor
Signature phrases: "No, these funding cuts are not permanent," "If you aren’t woke or a communist," "I of course have no hope"
Other habits: Contractions are common, especially in informal expressions; frequent use of exclamation points for emphasis; paragraphs are short and to the point

Copied words: aren, communist, course, cuts, funding, hope, permanent, point, woke

**doc `45`** (121 words)

> Here’s my favorite analogy. Suppose I spent a decade publishing books and papers arguing that, contrary to theoretical computer science’s dogma, the Church-Turing Thesis fails to capture all of computation, because Turing machines can’t toast bread. Therefore, you need my revolutionary new model, the Toaster-Enhanced Turing Machine (TETM), which allows bread as a possible input and includes toasti...

Profile: Voice: We/I, informal and conversational, stance toward the reader is friendly and engaging
Sentences: Medium length, with a mix of short and longer sentences; rhythm is varied but often starts with a clause that introduces a thought and ends with a punchline or conclusion
Punctuation: Uses ellipses (...), colons (:), and semicolons (;) frequently; also uses multiple exclamation points (!!) for emphasis
Tone and humour: Informal, humorous, with a touch of sarcasm
Signature phrases: "Here’s my favorite analogy," "You might say," "So, I’d say," "To the people who keep banging the drum about"
Other habits: Uses contractions (e.g., "you’re," "it’s"), informal language ("awesome comment"), and includes updates at the end of the passage to add context or address criticism

Copied words: analogy, awesome, banging, comment, drum, favorite, includes, keep, language, people

**doc `48`** (161 words)

> In my last post, I came down pretty hard on the blankfaces: people who relish their power to persist in easily-correctable errors, to the detriment of those subject to their authority. The sad truth, though, is that I don’t obviously do better than your average blankface in my ability to resist falsehoods on early encounter with them. As one of many examples that readers of this blog might know, I...

Profile: Voice: I/we, informal and conversational, stance toward the reader is friendly and engaging
Sentences: Medium length, with a mix of short and longer sentences, creating a natural flow
Punctuation: Uses commas extensively to separate clauses, often employs dashes for emphasis
Tone and humour: Slightly self-deprecating, with a touch of academic humor
Signature phrases: "In my last post", "If I have any tool", "Adding my own name"
Other habits: Uses contractions ("I've", "you'll"), informal language ("doofosity"), and includes parenthetical remarks

Passage:
In my last post, I came down pretty hard on the blankfaces: people who relish their power to persist in easily-correctable errors, to the detriment of those subject to their authority. The sad truth, though, is that I don’t obviously do better than your average blankface in my ability to resist falsehoods on early encounter with them. As one of many examples that readers of this blog might know, I didn’t think covid seemed like a

Copied words: ability, adding, authority, average, better, blankface, blankfaces, blog, came, correctable, covid, detriment, didn, doofosity, down, early, easily, encounter, errors, examples, falsehoods, hard, know, last, like, obviously, people, persist, post, power, pretty, readers, relish, resist, seemed, self, subject, think, though, tool, truth

**doc `42`** (103 words)

> I was at Epsilon Camp to accompany my son Daniel, who attended a different course there, for the 7- and 8-year-olds. So they got me to teach while I was there.  Teaching at Epsilon was some of the hardest work I’ve done in years: I taught two classes, held office hours, and interacted with or supervised students for 6-7 hours per day (compared to ~4 hours per week as a professor), on top of being ...

Profile: Voice: First-person singular, direct stance, informal
Sentences: Medium length, varied rhythm, often starts with "I" or "So"
Punctuation: Frequent use of commas, occasional exclamation marks
Tone and humour: Slightly wry, self-deprecating
Signature phrases: "I was at Epsilon Camp", "But then", "But enough about the future"
Other habits: Use of contractions ("wasn't", "hadn't"), informal language ("world-leading"), frequent use of parentheticals ("(!)", "~4 hours"), emphasis with bolding or italics

Passage:
I was at Epsilon Camp to accompany my son Daniel, who attended a different course there, for the 7- and 8-year-olds. So they got me to teach while I was there.

Copied words: accompany, attended, camp, course, daniel, different, enough, epsilon, first, future, hadn, hours, leading, often, olds, teach, world, year

## Group 2

**query `1061`** (157 words)

> Please steal my AI research ideas. This is a list of research questions and concrete experiments I would like to see done. If you are looking to break into AI research (e.g. as an undergraduate, or a software engineer in industry), these are low hanging fruit. Shoot me a line with experimental results if you want to collaborate. Starting from scratch vs checkpoints in pretraining  When should you ...

Profile: Voice: You/We, informal and direct
Sentences: Medium length, rhythmic, often starting with a question or transition
Punctuation: Uses ellipses (...), colons (:), and brackets ([d]) for emphasis and structure
Tone and humour: Casual, slightly humorous
Signature phrases: "starting from scratch vs checkpoints", "logit-matching against", "anneal into"
Other habits: Frequent use of contractions ("you'll", "it's"), informal language ("shoot me a line"), technical jargon mixed with everyday language

Passage:
Please steal my AI research ideas. This is a list of research questions and concrete experiments I would like to see done. If you are looking to break into AI research (e.g. as an undergraduate, or a software engineer in industry), these are low hanging fruit. Shoot me a line with experimental results if you want to collaborate.

Starting from scratch vs checkpoints in pretraining

When should you start a pretraining run from scratch vs from a past checkpoint? Should you lean toward the former over the latter as

Copied words: against, anneal, break, checkpoint, checkpoints, collaborate, concrete, done, engineer, experimental, experiments, former, fruit, hanging, ideas, industry, latter, lean, like, line, list, logit, looking, matching, past, please, pretraining, question, questions, research, results, scratch, shoot, software, start, starting, steal, toward, undergraduate, want

**doc `1068`** (93 words)

> In this sense, I no longer see startups as outlets for scientists to out-innovate each other, but what they are: businesses. And the ability to run a startup is just a long way of saying you know how to do business. In other words, you're a good businessman.  This is an important realization for me because this word, "businessman", in particular, was one that would have had me see someone as "brai...

Profile: Voice: We, conversational and slightly informal, stance toward the reader is friendly and engaging.
Sentences: Typically long, with a rhythmic flow that builds momentum before concluding with a punchline or insight.
Punctuation: Frequent use of commas to separate clauses, and en dashes to link related ideas.
Tone and humour: Slightly dry, with a touch of irony and self-deprecating humor.
Signature phrases: "In other words", "I believe", "That is what"
Other habits: Use of contractions ("I've", "it's"), informal language ("kettle on to boil"), and occasional run-on sentences that build to a climax.

Copied words: believe, boil, kettle, long, words

**doc `1065`** (132 words)

> This isn't building up to a criticism of the academy. On the contrary: mathematicians and physicists have falsifiability, too. If your proof of a proposition is incorrect, it will be clear to everyone and unambiguous that you have failed at proving the proposition. If your theory of gravitation yields bad predictions for how a projectile or planet will behave, one can simply conduct an experiment ...

Profile: Voice: We, conversational and slightly informal, balanced stance
Sentences: Medium length, rhythmic, often starting with a transition or intensifier
Punctuation: Frequent use of commas, occasional em dashes for emphasis
Tone and humour: Slightly dry, with a touch of sarcasm
Signature phrases: "It's not just the presence of clear right and wrong", "It's the rare field where studying measure theory and reading Hamlet can both be reasonably argued to be relevant to your job"
Other habits: Use of contractions ("it's", "you're"), informal language ("middle-schooler"), occasional rhetorical questions

My problem with economics is that such examples of falsifiability are far and few between. It's not just the presence of clear right and wrong or lack of ambiguity, it is also the ownership of risk and coupling of cause and effect in one's job.

Copied words: ambiguity, argued, between, cause, clear, coupling, economics, effect, examples, falsifiability, field, hamlet, lack, measure, middle, often, ownership, presence, rare, reading, reasonably, relevant, right, risk, schooler, studying, theory, wrong

**doc `1066`** (83 words)

> The difficult moral quanderies philosphers toyed with decades ago as mere hypotheticals are now coming to pass. We are living in the future.  We send goods created locally 10,000 miles across the world because it is cheaper to have them refined there and transported all the way back than to process them locally. And we still get those goods on our doorstep, exactly when we want them. It has been m...

Profile: Voice: We, critical and slightly sarcastic, informal
Sentences: Medium length, rhythmic, often starting with a transition or intensifier
Punctuation: Frequent use of commas, occasional em dashes for emphasis
Tone and humour: Slightly dry, with hints of irony
Signature phrases: "For such an advanced civilisation," "Despite living in a vastly more connected and globalized world than ever before," "And they're overweight"
Other habits: Use of contractions ("we're," "they're"), informal spelling ("color" instead of "colour"), occasional run-on sentences, paragraphs often structured around contrasting ideas

Copied words: advanced, civilisation, connected, despite, ever, globalized, living, overweight, vastly, world

## Group 3

**query `2022`** (164 words)

> Chat models sometimes are too eager to refuse answering at all, specifically on innocuous questions about a sometimes-hot topic.  Here's a recent example of this, DeepSeek refusing to answer any question whatsoever about Xi Jinping:  Here's what many people seem to not get: if you don’t really want to do safety tuning, but for one reason or another, you have to, this is the result. It’s very simpl...

Profile: Voice: We/I, informal, direct
Sentences: Short to medium length, rhythmic, often starts with a transition or intensifier
Punctuation: Uses commas, ellipses, and quotation marks for emphasis
Tone and humour: Casual, slightly sarcastic
Signature phrases: "Would you like to discuss the trade-offs of capitalism instead?", "Fun fact:"
Other habits: Contractions, informal language, explanatory examples

Passage:
Chat models sometimes are too eager to refuse answering at all, specifically on innocuous questions about a sometimes-hot topic.

Here's a recent example of this, DeepSeek refusing to answer any question whatsoever about Xi Jinping:

Here's what many people seem to not get: if you don’t really want to do safety tuning, but for one reason or another, you have to, this is the result. It’s very simple, let me explain. I'll use the example of Xi Jinping, but the same applies to anything someone might want to regulate the LLM's speech on, usually either for legal or social reasons.

The easiest place to safely

Copied words: another, answer, answering, anything, applies, capitalism, chat, deepseek, discuss, eager, easiest, either, example, examples, explain, fact, innocuous, jinping, legal, like, models, offs, people, place, question, questions, really, reason, reasons, recent, refuse, refusing, regulate, result, safely, safety, seem, simple, social, someone, sometimes, specifically, speech, topic, trade, tuning, usually, want, whatsoever

**doc `2024`** (164 words)

> There are generally two different and incompatible perspectives on pixels:  One school of thought considers a pixel to be an infinitesimally small point, and thus an image is a grid of points sparsely sampling the color information of the captured scene. The other school of thought considers a pixel to be a tiny square (sometimes rectangular) area, whose color is the summary of all light in that a...

Profile: Voice: We/I, informal and conversational, stance toward the reader is friendly and explanatory
Sentences: Medium length, rhythmic, often start with a transition or intensifier
Punctuation: Uses colons and ellipses for emphasis and flow, occasional use of dashes
Tone and humour: Informal, slightly humorous, uses playful language
Signature phrases: "It sounds like", "Except that", "That's a mouthful"
Other habits: Uses technical terms but explains them in simple terms, occasional use of contractions

Passage:
There are generally two different and incompatible perspectives on pixels:

One school of thought considers a pixel to be an infinitesimally small point, and thus an image is a grid of points sparsely sampling the color information of the captured scene. The other school of thought considers a pixel to be a tiny square (sometimes rectangular) area, whose color is the summary of all light in that area; think of a screen pixel or a camera's receptor.

Both of these are valid, depending on the context they are used in. However

Copied words: area, camera, captured, color, considers, context, depending, different, except, generally, grid, however, image, incompatible, infinitesimally, information, light, like, mouthful, often, perspectives, pixel, pixels, point, points, receptor, rectangular, sampling, scene, school, screen, small, sometimes, sounds, sparsely, square, summary, think, thought, thus, tiny, used, valid, whose

**doc `2025`** (125 words)

> Use Python's completely undocumented ThreadPool to parallelize non-bytecode work on shared memory! Like so:  from multiprocessing.pool import ThreadPool  pool = ThreadPool() pool.map(io_heavy_work, data_in_shared_memory)  In contrast to multiprocessing.Pool, where each process gets a copy of the second argument of map and the main process is responsible for collecting results as returned by map, t...

Profile: Voice: We, informative and slightly critical, formal
Sentences: Medium length, rhythmic, often starting with a transition or intensifier
Punctuation: Frequent use of ellipses, colons, and semicolons; occasional use of parentheses
Tone and humour: Slightly dry, with a touch of sarcasm
Signature phrases: "Beautiful, isn't it?" "Well, beautiful! ", "In contrast to"
Other habits: Use of technical terms without explanation; frequent use of colons to introduce lists; informal contractions like "ain't"; occasional spelling errors like "fashing" instead of "fashioning"

Example:
Voice: We, informative and slightly critical, formal
Sentences: Medium length, rhythmic, often starting with a transition or intensifier
Punctuation: Frequent use of ellipses, colons, and semicolons; occasional use of parentheses
Tone and humour: Slightly dry, with a touch of sarcasm
Signature phrases: "Beautiful, isn't it?" "Well, beautiful! ", "

Copied words: beautiful, contrast, fashing, instead, like, well

**doc `2021`** (141 words)

> Here's a post claiming that only Gemini 2.5 Flash can create a Galton Board, and no other thinking model can. This intuitively sounds wrong to me. What's worse, is that they then go and provide a big-ass prompt with waaaay too much yap.  That's not the future we're aiming for, so I did some test across models. I want a reasonably good starting point with a very simple prompt:      Can you write a ...

Profile: Voice: I/we, informal, direct
Sentences: Short, rhythmic, often starting with "That's" or "What's"
Punctuation: Uses colons and ellipses for lists and explanations
Tone and humour: Casual, slightly sarcastic
Signature phrases: "intuitively sounds wrong", "waaaay too much yap", "click on the videos"
Other habits: Frequent use of contractions, informal spelling (e.g., "shitfluencers"), lists with colons, informal capitalisation (e.g., "LLM"), emphasis with bold or italics

Passage:
Here's a post claiming that only Gemini 2.5 Flash can create a Galton Board, and no other thinking model can. This intuitively sounds wrong to me. What's worse, is that they then go and provide a big-ass prompt with waaaay too much yap.

That's not the future we're aiming for, so I did some test across models. I want a reasonably good starting point with a very simple prompt:

    Can you write

Copied words: across, aiming, board, claiming, click, create, flash, future, galton, gemini, good, intuitively, model, models, often, point, post, prompt, provide, reasonably, shitfluencers, simple, sounds, starting, test, thinking, videos, waaaay, want, worse, write, wrong

## Group 4

**query `1909`** (139 words)

> While Quickstrom proved its worth, finding bugs in more than half of the TodoMVC apps, Bombadil aims to improve on its shortcomings while also envisioning a more ambitious future for generative testing of web apps: faster and smarter state space exploration, a modern and usable specification language, better tools for reproducing and debugging test failures, and a better distribution story.  I con...

Profile: Voice: I/we, informal and conversational, stance toward the reader is friendly and engaging
Sentences: Medium length, rhythmic with a mix of complex and simple sentences; often starts with a phrase or concept before diving into details
Punctuation: Uses colons and semicolons to list items, and ellipses for trailing off; sparing use of commas to connect clauses
Tone and humour: Informal, slightly humorous, with a touch of sarcasm
Signature phrases: "Right now," "Isn’t that the holy grail of testing?" "That gives you perfect reproductions"
Other habits: Frequent use of technical jargon mixed with everyday language; emphasis on accessibility and user-friendliness; mentions of open-source projects and commercial offerings

Example phrases:
- "Right now, I’m working on a specification DSL in TypeScript."
- "Isn’t that the holy grail of testing?"
- "That gives you perfect reproductions of failed tests."

Copied words: accessibility, commercial, example, failed, gives, grail, holy, language, open, perfect, reproductions, right, specification, testing, tests, typescript, working

**doc `1902`** (86 words)

> Why? Building a programming language, even a small one as Oden where I can piggy-back on the success and engineering efforts of Go, takes a lot of time. A lot of time. I currently work professionally at a startup called Empear where we develop products for analyzing and understanding large software projects based on their history. The work is a lot of fun, but also takes much of my time and energy...

Profile: Voice: I, confiding and introspective, informal
Sentences: Medium length, rhythmic, often starting with a transition or intensifier
Punctuation: Uses ellipses (...), colons (:), and semicolons (;) frequently
Tone and humour: Reflective, sometimes self-deprecating, occasionally dramatic
Signature phrases: "I have wrestled with these thoughts for some time now", "I think it is reasonable for me to be clear why I am doing this"
Other habits: Uses contractions (e.g., "I've", "it's"), informal language ("hell of a ride"), and a mix of British and American spellings (e.g., "colour", "color").

Copied words: clear, hell, language, reasonable, ride, think, thoughts, time, wrestled

**doc `1905`** (145 words)

> or the last six months I’ve been working on a screencast video editor called Komposition, and it’s now released and open source. This is an experience report, based on a talk from Lambda World Cádiz 2018, that’ll give an overview of Komposition’s design, implementation, testing, and planned future work. Background  It all began with Haskell at Work, the series of screencasts focused on practical H...

Profile: Voice: I/we, informal and direct, stance toward the reader is friendly and engaging
Sentences: Medium length, rhythmic, often starting with a verb or a phrase
Punctuation: Uses commas to separate clauses, occasional use of dashes for emphasis
Tone and humour: Casual, with a touch of self-deprecating humour
Signature phrases: "I’ve found this workflow beneficial," "Having to redo the recording phase is very time-consuming," "What does a programmer do when faced with a repetitive task?"
Other habits: Uses contractions (e.g., "I’ve," "you’re"), informal spelling (e.g., "screencast"), occasional use of technical terms but explained in simple language

Example:
"I’ve found this workflow beneficial for me, partly because of being a non-native English speaker and not being keen on coding and talking simultaneously, but also because I think it helps with organizing the content into a cohesive narrative."

Copied words: beneficial, coding, cohesive, consuming, content, english, faced, found, having, helps, keen, narrative, native, organizing, partly, phase, programmer, recording, redo, repetitive, screencast, self, simultaneously, speaker, starting, talking, task, think, time, voice, workflow

**doc `1901`** (108 words)

> Having tried a lot of color schemes for editors, especially for Vim, I have gotten quite picky. All right, very picky. Most of the time Vim has been configured to use Tomorrow Night or Gruvbox. Although they’re great, they have felt a bit over the top. Also, depending on where I’m sitting at the moment I use both dark and light backgrounds for best contrast.  The last couple of days I’ve tried off...

Profile: Voice: First-person singular, direct to the reader, informal
Sentences: Short to medium length, rhythmic, often starting with "I" or "My"
Punctuation: Frequent use of commas, occasional semicolons
Tone and humour: Casual, slightly humorous
Signature phrases: "All right", "e.g.", "Thanks for the great work"
Other habits: Use of contractions ("I've", "it's"), informal spelling ("off" instead of "on"), mentions of specific Vim configurations and color schemes

Example:
Voice: I, casual and direct
Sentences: Short and rhythmic, often starting with "I"
Punctuation: Frequent commas, some semicolons
Tone and humour: Casual, slightly humorous
Signature phrases: "All right", "e.g."
Other habits: Contractions ("I've"), informal spelling ("off"), mentions of Vim configurations

Copied words: color, great, right, schemes, thanks, work

## Group 5

**query `486`** (144 words)

> I thought it would be fun to analyze the activity on one of my favorite sources of interesting links and information, Hacker News. My source of data is a script I’ve set up some time in August that downloads HN (the Front page and the New stories page) every minute. We will be interested in visualizing the stories as they get upvoted during the day, figuring out which domains/users are most popula...

Profile: Voice: We, informative and slightly casual, moderately formal
Sentences: Medium to long, rhythmic, often starting with a verb or a transition
Punctuation: Uses colons and commas extensively, occasional ellipses for flow
Tone and humour: Informal, slightly humorous
Signature phrases: "I thought it would be fun", "We will be interested in", "A single day of data"
Other habits: Uses contractions (e.g., "had to"), informal language ("ugliest-parsing-function-ever"), multiple spaces between words (likely intentional for readability), occasional use of all-caps for emphasis

Example:
Voice: We, informative and slightly casual, moderately formal
Sentences: Medium to long, rhythmic, often starting with a verb or a transition
Punctuation: Uses colons and commas extensively, occasional ellipses for flow
Tone and humour: Informal, slightly humorous
Signature phrases: "I thought it would be fun", "We will be interested in", "A single day of data"
Other habits: Uses contractions (

Copied words: between, data, ever, function, interested, parsing, single, thought, ugliest, uses

**doc `482`** (164 words)

> This guide is patterned after my “Doing well in your courses”, a post I wrote a long time ago on some of the tips/tricks I’ve developed during my undergrad. I’ve received nice comments about that guide, so in the same spirit, now that my PhD has come to an end I wanted to compile a similar retrospective document in hopes that it might be helpful to some. Unlike the undergraduate guide, this one wa...

Profile: Voice: First-person singular, direct and engaging stance toward the reader, informal formality
Sentences: Short to medium length, rhythmic with a mix of complex and simple sentences, often starting with a question or a transition
Punctuation: Frequent use of commas, occasional use of dashes for emphasis
Tone and humour: Casual, slightly humorous, with self-deprecating remarks
Signature phrases: "First, I really liked school and learning things", "Freedom. A PhD will offer you a lot of freedom"
Other habits: Use of contractions ("you're", "it's"), informal language ("cog in a wheel"), occasional spelling errors ("there's" instead of "their"), no specific formatting or paragraph structure noted

Passage:
This guide is patterned after my “Doing well in your courses”, a post I wrote a long time ago on some of the tips/tricks I’ve developed during my undergrad. I’ve received nice comments about that guide, so in the same spirit, now that my PhD has come to an end I wanted to compile a similar retrospective

Copied words: come, comments, compile, courses, developed, during, first, freedom, guide, learning, liked, long, medium, nice, offer, patterned, post, really, received, retrospective, school, self, similar, specific, spirit, starting, things, time, tips, tricks, undergrad, wanted, well, wheel, wrote

**doc `489`** (156 words)

> My summer internship work at Google has turned into a CVPR 2014 Oral titled “Large-scale Video Classification with Convolutional Neural Networks” (project page). Politically correct, professional, and carefully crafted scientific exposition in the paper and during my oral presentation at CVPR last week is one thing, but I thought this blog might be a nice medium to also give a more informal and pe...

Profile: Voice: I, informal and conversational, stance toward the reader is friendly and engaging
Sentences: Medium length, with a mix of complex and simple structures; sentences often start with a casual phrase or thought experiment
Punctuation: Uses ellipses (... ) frequently to indicate pauses or trailing off; occasional use of quotation marks for direct speech or emphasis
Tone and humour: Casual, with a touch of self-deprecating humor
Signature phrases: "hanging out at Google", "it’s interesting to note", "it’s like"
Other habits: Uses contractions (e.g., "it’s", "wasn’t"), informal language ("gobble up all of internet data"), and occasional use of technical terms in a conversational manner

Example:
Voice: I, informal and conversational, stance toward the reader is friendly and engaging
Sentences: Medium length, with a mix of complex and simple structures; sentences often start with a casual phrase or thought experiment
Punctuation: Uses ellipses (... ) frequently to indicate pauses or trailing off; occasional use of quotation

Copied words: data, gobble, google, hanging, informal, interesting, internet, medium, note, thought

**doc `488`** (125 words)

> Throughout my life I never paid too much attention to health, exercise, diet or nutrition. I knew that you’re supposed to get some exercise and eat vegetables or something, but it stopped at that (“mom said”-) level of abstraction. I also knew that I can probably get away with some ignorance while I am young, but at some point I was messing with my health-adjusted life expectancy. So about halfway...

Profile: Voice: First-person singular, informal and conversational, stance toward the reader is friendly and engaging.
Sentences: Short to medium length, with a mix of simple and complex structures. Sentences often start with personal pronouns or phrases like "So" and "For this post."
Punctuation: Uses ellipses (...), quotation marks for direct speech or emphasis, and occasional dashes (—) for pauses or transitions.
Tone and humour: Casual, slightly humorous, with self-deprecating remarks.
Signature phrases: "I won’t lie," "full detail link," "I liked [book title]," "For this post I wanted to focus on."
Other habits: Frequent use of contractions ("I'm," "it's"), informal spelling ("color" instead of "colour"), and a mix of British and American English spellings ("colour," "color"). Uses informal capitalization (e.g., "ATP" as a common noun).

Copied words: detail, focus, full, like, liked, link, medium, post, wanted
