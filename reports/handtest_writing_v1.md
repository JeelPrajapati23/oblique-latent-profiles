# Prompt hand-test: writing

- Variant: `writing-33adcf__Qwen2.5-7B-Instruct-AWQ` (prompts: doc=`writing_style`, query=`writing_style`)
- Model: `Qwen/Qwen2.5-7B-Instruct-AWQ`, greedy decoding
- Words per profile: min 1, median 25, max 145 (target 60-120); in range: 0/20
- Profiles with copied content words: 19/20

| Cosine (Qwen3-0.6B) | same group | different group | gap |
|---|---|---|---|
| raw text | 0.260 | 0.214 | +0.046 |
| profile | 0.741 | 0.723 | +0.018 |

A bigger gap means profiles separate the hidden property better than raw text does.

## Group 1

**query `49`** (25 words)

> Part of me feels bad not to have written for weeks about quantum error-correction or BQP or QMA or even the new Austin-based startup that launched a “quantum computing dating app” (which, before anyone asks, is 100% as gimmicky and pointless as it sounds).  But the truth is that, even if you cared narrowly about quantum computing, there would be no bigger story right now than the fate of American ...

Profile: Short sentences, rapid rhythm, ellipsis, second-person, critical, sarcastic, exclamation marks, fear-mongering, informal vocabulary, personal anecdotes, rhetorical questions, conspiracy theories, hyperbole, appeals to authority, frustration, urgency

Copied words: fear

**doc `45`** (23 words)

> Here’s my favorite analogy. Suppose I spent a decade publishing books and papers arguing that, contrary to theoretical computer science’s dogma, the Church-Turing Thesis fails to capture all of computation, because Turing machines can’t toast bread. Therefore, you need my revolutionary new model, the Toaster-Enhanced Turing Machine (TETM), which allows bread as a possible input and includes toasti...

Profile: Short sentences, rhythmic, semi-formal, uses "you", serious tone, minimal humour, rhetorical questions, technical vocabulary, complex sentences, updates for additional points, clarifications, academic discussion

Copied words: -

**doc `48`** (20 words)

> In my last post, I came down pretty hard on the blankfaces: people who relish their power to persist in easily-correctable errors, to the detriment of those subject to their authority. The sad truth, though, is that I don’t obviously do better than your average blankface in my ability to resist falsehoods on early encounter with them. As one of many examples that readers of this blog might know, I...

Profile: short sentences, rhythmic, uses commas, third-person limited, self-deprecating, explains errors, technical vocabulary, detailed explanations, uses mathematical notation, speculative, cautious optimism

Copied words: errors, explains, self

**doc `42`** (29 words)

> I was at Epsilon Camp to accompany my son Daniel, who attended a different course there, for the 7- and 8-year-olds. So they got me to teach while I was there.  Teaching at Epsilon was some of the hardest work I’ve done in years: I taught two classes, held office hours, and interacted with or supervised students for 6-7 hours per day (compared to ~4 hours per week as a professor), on top of being ...

Profile: Short sentences, rapid rhythm, ellipsis, I, reflective, serious with moments of humor, "I felt certain," "But enough about the future," Informal to academic vocabulary, Stream-of-consciousness, fragmented thoughts, occasional digressions

Copied words: certain, enough, felt, future

## Group 2

**query `1061`** (145 words)

> Please steal my AI research ideas. This is a list of research questions and concrete experiments I would like to see done. If you are looking to break into AI research (e.g. as an undergraduate, or a software engineer in industry), these are low hanging fruit. Shoot me a line with experimental results if you want to collaborate. Starting from scratch vs checkpoints in pretraining  When should you ...

Profile: Short sentences, varied rhythm, uses ellipses, second person, informative, serious, questions, experimental, technical, detailed, speculative, hypothetical, data-driven, computational, theoretical, analytical, complex vocabulary, long sentences, technical terms, uses brackets, informal tone, practical advice, open-ended questions, explores possibilities, uses abbreviations, technical jargon, uses acronyms, uses placeholders, uses ellipsis for thought, uses question marks for uncertainty, uses colons for lists, uses semicolons for complex ideas, uses dashes for emphasis, uses parentheses for additional information, uses brackets for specific examples, uses ellipses for trailing thoughts, uses colons for definitions, uses semicolons for contrast, uses dashes for transitions, uses commas for separation, uses periods for clarity, uses exclamation marks for emphasis, uses question marks for inquiry, uses colons for explanations, uses semicolons for complexity, uses dashes for emphasis, uses commas for detail, uses periods for finality, uses exclamation marks for excitement, uses question marks for uncertainty, uses colons for definitions,

Copied words: data, detailed, examples, experimental, ideas, long, question, questions

**doc `1068`** (22 words)

> In this sense, I no longer see startups as outlets for scientists to out-innovate each other, but what they are: businesses. And the ability to run a startup is just a long way of saying you know how to do business. In other words, you're a good businessman.  This is an important realization for me because this word, "businessman", in particular, was one that would have had me see someone as "brai...

Profile: short sentences, rhythmic, uses commas, third person, matter-of-fact, no humour, uses "I", "you", "we", formal vocabulary, complex sentences, lists, contrasts, draws parallels

Copied words: person

**doc `1065`** (36 words)

> This isn't building up to a criticism of the academy. On the contrary: mathematicians and physicists have falsifiability, too. If your proof of a proposition is incorrect, it will be clear to everyone and unambiguous that you have failed at proving the proposition. If your theory of gravitation yields bad predictions for how a projectile or planet will behave, one can simply conduct an experiment ...

Profile: Short sentences, varied rhythm, uses commas, third person, serious tone, some sarcasm, mentions of diverse fields, technical vocabulary, complex sentences, critical analysis, lack of humor, use of "falsifiability", contrasts, examples, explanations, criticism of lack of accountability

Copied words: criticism, examples, falsifiability, fields, lack

**doc `1066`** (23 words)

> The difficult moral quanderies philosphers toyed with decades ago as mere hypotheticals are now coming to pass. We are living in the future.  We send goods created locally 10,000 miles across the world because it is cheaper to have them refined there and transported all the way back than to process them locally. And we still get those goods on our doorstep, exactly when we want them. It has been m...

Profile: Short sentences, rapid rhythm, semi-colons, third person, reflective tone, minimal humour, rhetorical questions, mix of formal and informal vocabulary, fragmented paragraphs, personal musings

Copied words: short

## Group 3

**query `2022`** (15 words)

> Chat models sometimes are too eager to refuse answering at all, specifically on innocuous questions about a sometimes-hot topic.  Here's a recent example of this, DeepSeek refusing to answer any question whatsoever about Xi Jinping:  Here's what many people seem to not get: if you don’t really want to do safety tuning, but for one reason or another, you have to, this is the result. It’s very simpl...

Profile: short sentences, rapid rhythm, ellipsis, third person, matter-of-fact tone, no humour, technical vocabulary, concise paragraphs

Copied words: fact

**doc `2024`** (1 words)

> There are generally two different and incompatible perspectives on pixels:  One school of thought considers a pixel to be an infinitesimally small point, and thus an image is a grid of points sparsely sampling the color information of the captured scene. The other school of thought considers a pixel to be a tiny square (sometimes rectangular) area, whose color is the summary of all light in that a...

Profile: short_sentences,consistent_rhythm,uses_we,informal_tone,explanatory,technical_vocabulary,clear_paragraph_structure

Copied words: consistent

**doc `2025`** (25 words)

> Use Python's completely undocumented ThreadPool to parallelize non-bytecode work on shared memory! Like so:  from multiprocessing.pool import ThreadPool  pool = ThreadPool() pool.map(io_heavy_work, data_in_shared_memory)  In contrast to multiprocessing.Pool, where each process gets a copy of the second argument of map and the main process is responsible for collecting results as returned by map, t...

Profile: Short sentences, rapid rhythm, exclamation marks, second person, enthusiastic, no humour, technical jargon, concise explanations, inline code snippets, ellipsis for thought, abrupt shifts in tone

Copied words: code, second

**doc `2021`** (12 words)

> Here's a post claiming that only Gemini 2.5 Flash can create a Galton Board, and no other thinking model can. This intuitively sounds wrong to me. What's worse, is that they then go and provide a big-ass prompt with waaaay too much yap.  That's not the future we're aiming for, so I did some test across models. I want a reasonably good starting point with a very simple prompt:      Can you write a ...

Profile: short_sentences, rhythmic, exclamation_marks, second_person, critical, no_humour, technical_terms, detailed_explanations, lists, comparisons, speculative, analytical

Copied words: detailed

## Group 4

**query `1909`** (20 words)

> While Quickstrom proved its worth, finding bugs in more than half of the TodoMVC apps, Bombadil aims to improve on its shortcomings while also envisioning a more ambitious future for generative testing of web apps: faster and smarter state space exploration, a modern and usable specification language, better tools for reproducing and debugging test failures, and a better distribution story.  I con...

Profile: short sentences, rhythmic, uses commas, third person, enthusiastic, technical, jargon, detailed explanations, future-oriented, open-source, commercial, Rust, TypeScript, linear temporal logic

Copied words: commercial, future, linear, logic, open, rust, temporal, typescript

**doc `1902`** (34 words)

> Why? Building a programming language, even a small one as Oden where I can piggy-back on the success and engineering efforts of Go, takes a lot of time. A lot of time. I currently work professionally at a startup called Empear where we develop products for analyzing and understanding large software projects based on their history. The work is a lot of fun, but also takes much of my time and energy...

Profile: Short sentences, varied rhythm, uses "I", serious tone, minimal humour, uses "I have wrestled", "I think", "I have learned", technical vocabulary, direct statements, focuses on personal challenges and achievements, ends with a reflective conclusion

Copied words: learned, think, wrestled

**doc `1905`** (43 words)

> or the last six months I’ve been working on a screencast video editor called Komposition, and it’s now released and open source. This is an experience report, based on a talk from Lambda World Cádiz 2018, that’ll give an overview of Komposition’s design, implementation, testing, and planned future work. Background  It all began with Haskell at Work, the series of screencasts focused on practical H...

Profile: short sentences, rhythmic, uses commas, past tense, objective, detailed, technical, explains processes, lists steps, uses "I", no humour, focuses on tools, mentions software names, describes workflows, uses "thus", mentions challenges, explains solutions, uses "what does a programmer do", describes projects, mentions programming languages

Copied words: detailed, programmer, software, thus, tools

**doc `1901`** (45 words)

> Having tried a lot of color schemes for editors, especially for Vim, I have gotten quite picky. All right, very picky. Most of the time Vim has been configured to use Tomorrow Night or Gruvbox. Although they’re great, they have felt a bit over the top. Also, depending on where I’m sitting at the moment I use both dark and light backgrounds for best contrast.  The last couple of days I’ve tried off...

Profile: Short sentences, varied rhythm, uses ellipses, switches between first and third person, informal tone, slight self-deprecating humor, mentions "got quite picky", "feels a bit over the top", "fit my taste very well", limited vocabulary register, brief paragraphs, includes technical terms, mentions color schemes, uses "e.g."

Copied words: color, picky, quite, schemes, taste, uses, well

## Group 5

**query `486`** (27 words)

> I thought it would be fun to analyze the activity on one of my favorite sources of interesting links and information, Hacker News. My source of data is a script I’ve set up some time in August that downloads HN (the Front page and the New stories page) every minute. We will be interested in visualizing the stories as they get upvoted during the day, figuring out which domains/users are most popula...

Profile: Short sentences, rapid rhythm, uses commas, third-person, informative, technical, detailed descriptions, uses "we", "I", "you", straightforward, no humour, uses technical jargon, structured paragraphs, transitions smoothly between topics

Copied words: between, detailed, structured, topics, uses

**doc `482`** (28 words)

> This guide is patterned after my “Doing well in your courses”, a post I wrote a long time ago on some of the tips/tricks I’ve developed during my undergrad. I’ve received nice comments about that guide, so in the same spirit, now that my PhD has come to an end I wanted to compile a similar retrospective document in hopes that it might be helpful to some. Unlike the undergraduate guide, this one wa...

Profile: Short sentences, varied rhythm, uses commas, avoids first-person, informative tone, minimal humour, uses bullet points, moderate vocabulary, uses lists, transitions to longer sentences, shifts to more technical vocabulary

Copied words: first, points

**doc `489`** (20 words)

> My summer internship work at Google has turned into a CVPR 2014 Oral titled “Large-scale Video Classification with Convolutional Neural Networks” (project page). Politically correct, professional, and carefully crafted scientific exposition in the paper and during my oral presentation at CVPR last week is one thing, but I thought this blog might be a nice medium to also give a more informal and pe...

Profile: Short sentences, rhythmic, semi-formal, uses "I", professional tone, few humorous elements, technical vocabulary, detailed descriptions, lists, explains complex ideas clearly

Copied words: professional

**doc `488`** (133 words)

> Throughout my life I never paid too much attention to health, exercise, diet or nutrition. I knew that you’re supposed to get some exercise and eat vegetables or something, but it stopped at that (“mom said”-) level of abstraction. I also knew that I can probably get away with some ignorance while I am young, but at some point I was messing with my health-adjusted life expectancy. So about halfway...

Profile: Short sentences, dashes, first-person singular, casual, self-deprecating, mentions of experiments, technical vocabulary, explanatory, detailed descriptions, scientific references, abbreviations, ellipses, lists, analogies, parenthetical remarks, technical terms, chemical symbols, molecular structures, biochemistry explanations, energy metabolism descriptions, weight loss focus, health and wellness discussions, scientific curiosity, biohacking, metabolic processes, ATP synthesis, metabolic pathways, macronutrients, metabolic rate, metabolic flexibility, metabolic health, metabolic syndrome, metabolic disorders, metabolic testing, metabolic markers, metabolic biomarkers, metabolic profiling, metabolic fingerprinting, metabolic signatures, metabolic signatures, metabolic signatures, metabolic signatures, metabolic signatures, metabolic signatures, metabolic signatures, metabolic signatures, metabolic signatures, metabolic signatures, metabolic signatures, metabolic signatures, metabolic signatures, metabolic signatures, metabolic signatures, metabolic signatures, metabolic signatures, metabolic signatures, metabolic signatures, metabolic signatures, metabolic signatures, metabolic signatures, metabolic signatures, metabolic signatures, metabolic signatures, metabolic signatures, metabolic signatures, metabolic signatures, metabolic signatures, metabolic signatures, metabolic signatures,

Copied words: biochemistry, biohacking, energy, experiments, focus, health, loss, macronutrients, metabolism, molecular, rate, synthesis, weight
