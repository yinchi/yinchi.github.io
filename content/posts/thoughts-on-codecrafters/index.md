---
title: "Thoughts on CodeCrafters"
date: 2026-04-04
categories: ["ramblings", "Python", "Rust"]
---

[CodeCrafters](https://app.codecrafters.io/catalog) is a site where one can complete a number of
programming challenges. Challenges include:

- Build your own HTTP server
- Build your own Interpreter
- Build your own Shell
- Build your own Claude Code (still in beta)

Each challenge is broken into a number of steps, with an extensive test suite triggered by the
command `codecrafters submit` which:

- Pushes your submission to a Git repo on the CodeCrafters server
- Runs the tests for the given step
- Reports results back to the user in the terminal

Supposedly, this is made possible by Git's `post-receive` hook, which runs the test suite and
reports the results back to the user via Git's side-channel communication capabilities (as well
as updating the user status in Codecrafter's database if the step was cleared sucessfully).

## Challenges

### Complete your own shell

The first challenge I tried was "Complete your own shell", which I chose to do in Rust, which I
am learning. Not too hard &mdash; I quickly completed the base stages and the directory
navigation, quoting (' and "), and redirection (1> and 2> and their >> forms) extensions. I later
noticed that I've only handled standalone ~ and not `cd ~/subdir` or `cd ~otheruser`, for
example, but that's fine for now &mdash; the tests pass.

Then came autocomplete. Now, instead of reading user input line by line, I'd have to process raw
keyboard events, not something I know how to do in Rust or am interested in learning at the
moment. The challenge step states the following:

> We recommend using a library like [`rustyline`](https://crates.io/crates/rustyline) for your
> implementation.

Note that this recommendation came after already completing 22 stages and there are no
instructions on how to use the crate. Eventually, I found some AI-written documentation on
[deepwiki.com](https://deepwiki.com/kkawakam/rustyline/1-overview) which I suppose I could use as
a starting point, and it seems most of the existing code I wrote can be re-used eventually once I
have the rustyline loop set up. But, since my autocompletion implementation will have to figure
out "Am I expecting a command, file path, or something else for the current token?", I figured
that I might benefit from completing another challenge first...

### Complete your own interpreter

Hey, a shell is basically an interpreter, right? Let's complete this challenge first!

Now, the "Complete your own interpreter" challenge is special on CodeCrafters because it follows
an existing, freely available textbook:
[Crafting Interpreters](https://craftinginterpreters.com/contents.html) by Robert Nystrom.
Specifically, it tracks Part II of the book, "A Tree-Walk Interpreter", which walks through the
steps of scanning, parsing, and evaluation.

Unfortunately, once you understand the basics of token scanning and recursive-descent parsing, as
taught in the book, implementing the challenge stages does start to become an exercise in tedium,
and I did rely on AI a little bit to expand the language grammar step-by-step. I paused in the
middle of implementing logical operators as I needed to finish my actual work at the time (and
now, to handle a intercontinental move), but I think the rest of the challenge will be pretty
simple once I get back to it. Hopefully implementing functions and classes will pose more of a
challenge.

Reliance on an existing book for this challenge highlighted for me the main feature of most of
the other challenges: you are handed a set of tests to pass for each stage and are pretty much
left to **figure it out by yourself** given whatever internet resources you can find. Which
possibly includes code written by others *specifically* for the exact challenge you are
completing. There really isn't any formal teaching system, or anti-cheat system; what you get out
of the system is fully up to you.

That being said, having a sequential to-do list of features and tests to pass definitely makes
things easier than trying to write a piece of software from scratch, and is a good way to show
others "Yes, this little toy project of mine actually *works*." Or, at least the parts I have
implemented so far.

### Complete your own Claude Code

The title of this (new, still in beta) challenge is a bit of a stretch: yes, you will communicate
with an LLM via the command line, but the functionality you will write for this challenge is only
a tiny percentage of what Claude Code provides. Nevertheless, this challenge, which I chose to
complete in Python, introduced me to the [OpenAI API](https://github.com/openai/openai-python)
and how to implement a basic client with a few advertised tools (file I/O and bash access). No
permissions system yet, so I quickly learned to wrap my local testing environment in a Docker
container.

One thing that surprised me is that using the OpenAI API, I have to feed the LLM the entire
session history **from scratch every time** my client sends a response, e.g. for a tool call. As
it turned out, session persistence is a proposed extension for the challenge, and seemingly
[not too hard](https://openai.github.io/openai-agents-python/sessions/), although I might hold
off on extending my code in any way until CodeCrafters implements the challenge steps and tests
for them &mdash; not like I'd ever use my own toy implementation over a professionally-made LLM
client anyway. Another thing is the absolute monstrosity that is the OpenAI's type system: here
is an excerpt from my code:

```py
from openai import OpenAI
from openai.types.chat.chat_completion_assistant_message_param import (
    ChatCompletionAssistantMessageParam,
)
from openai.types.chat.chat_completion_message import ChatCompletionMessage
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
)
from openai.types.chat.chat_completion_message_tool_call_param import (
    ChatCompletionMessageToolCallParam,
    Function,
)
from openai.types.chat.chat_completion_system_message_param import (
    ChatCompletionSystemMessageParam,
)
from openai.types.chat.chat_completion_tool_message_param import (
    ChatCompletionToolMessageParam,
)
from openai.types.chat.chat_completion_user_message_param import (
    ChatCompletionUserMessageParam,
)
```

**Note**: I later found out that I can import the types directly from `openai.types.chat` instead
of using `from` on each individual submodule. Oh, well.

Notably, messages to be sent to the LLM are typed dicts (since we control their creation), and
their type names end with `_param`. On the other hand, messages received are Pydantic models (so
that Pydantic can validate whether the LLM sent back messages in the expected format or not).
Anyhow, a lot of time was spent on clearing away `mypy` errors for this challenge and navigating
the insane `openai.types.chat` module hierarchy, but I think it was worth it.

#### Wasted efforts?

As it turns out, instead of messing with the various message classes in the OpenAI API directly,
I probably could have just used the `agents` module. In fact, what I wrote for the challenge
seems mostly covered by a
[single quickstart page](https://openai.github.io/openai-agents-python/quickstart/) that I
failed to read before attempting this challenge.

Guess this is what happens when you poke around blindly instead of actually learning something
in a structured environment. Oh, well. Maybe, by exploring how OpenAI's messages system actually
works instead of just invoking the `openai.agents` module, one gains a deeper understanding of
the OpenAI platform itself.

#### Roadmap for the "Complete your own Claude Code" challenge

[Proposed extensions for the challenge](https://app.codecrafters.io/roadmap/challenge-extensions?course=claude-code)
that I've upvoted include:

- **[Skills](https://code.claude.com/docs/en/skills)**. I understand that skills are basically
  Markdown files that teach the LLM how to do things. I guess these get tacked onto the OpenAI
  API request? If so, no wonder requests burn through tokens so quickly, if **each** API call,
  even in the same session, embeds the entire `skills/` directory.
- **Web search**: seems like an important tool to have. Probably using something like the
  Beautiful Soup HTML parser, or even a mini-browser that can handle dynamic web content.
- **Command permissions**: "Allow MyClaudeClone to run `sudo rm -rf /` (Y/n)?"
- **Sessions and an REPL loop**. As mentioned above, the current implementation just throws the
  whole conversation history into each API call. Implementing sessions should fix this.

### Build your own HTTP server

This challenge introduced me to the `threadpool` (for concurrency) and `flate2` Rust crates, as
well as the `move` keyword for closures. I'll probably have to revisit these concepts to truly
master them, though. I could really get a feel of both the power and verbosity of Rust's Result
and Option types in this challenge, but otherwise, not much else to say. TLS and HTTP2 are listed
as possible future extensions one can vote for, as well as Basic Authentication.

## Final thoughts

The [available challenges](https://app.codecrafters.io/catalog) on CodeCrafters are fairly
limited for now, with the HTTP server and (in beta) Claude Code challenges containing 14 and just
6 stages, respectively, while the interpreter, shell, and Redis challenges have 84, 59, and 97 (!)
stages. The challenges also very wildly in difficulty. In particular, "Build your own SQLite" has
only 9 stages at the moment, almost all rated Hard (3/3), and apparently only implements the read
part of CRUD so far. Hopefully, these challenges will get more attention soon. Note that for
April 2026, the newly implemented challenge extension was background jobs for the shell
challenge.

The CodeCrafters team is also very small and geographically disperse, and it is unclear how they
create or collect contributions for challenges
([this link](https://docs.codecrafters.io/contributors/authoring-challenges/planning-your-challenge)
describes an invite-based system but doesn't really talk about the approval process). It also
seems they are not hiring developers at the moment; the single job posting I can find is for a
marketing position (interesting since they already have someone in this role). All this means new
challenge stages are few and far between, and with the uneven development problem I mentioned
above.

There is also no prerequisite system in place, meaning a future "Build your own compiler" likely
wouldn't be able to check if the user had previously completed "Build your own interpreter",
which would give them the tokenizer and parser they'd need for both (assuming, of course, the
interpreter and compiler target the same language). Indeed, understanding how these two tools
work will make some of the other challenges (e.g. shell, grep) a lot easier. I therefore recommend
anyone trying out CodeCrafters to attempt the **interpreter challenge first**, using (of course)
the associated third-party book as a guide. Unfortunately, this means paying for a subscription as
the current free offering appears to be "Build your own Redis" (sounds interesting but wow, are
there a lot of stages for this one).

### CodeCrafters and generative AI

Due to the breakdown of each challenge into small steps, each with an extensive test suite, and
the fact that each challenge has already been completed by others many times, with publicly
accessible code, it seems that it wouldn't be too difficult to let loose an LLM on a challenge and
have it complete it all by itself. But... you wouldn't learn much from doing so. I think that even
in the era of AI code, there is still value in learning how things actually work.

That being said, there are some aspects of some challenges that are quite repetitive and where AI
helps a lot. For example, completing the interpreter challenge quickly falls into a rhythm of:

1. Update the grammar.
2. Update the tokenizer if necessary.
3. Update the parser, taking care to maintain the correct hierarchy for the
   [recursive descent](https://en.wikipedia.org/wiki/Recursive_descent_parser).
4. Update the evaluator to handle the new node type in the abstract syntax tree.

Thus, if you can handle `+` and `*`, you can handle `||` and `&&` and so on. This is where AI code
assistance shines in my opinion, since you don't really learn much by repeating the same "add an
operator" loop over and over. A balance is to be made between doing everything by hand and letting
the AI take over.

AI code completion is also much better at figuring out Rust's ownership system than I ever will
be. I do hope I get better at it eventually. However, this is something that more formal
instruction would be good at, I think, so hopefully I'll find (or make) the time for that too.
