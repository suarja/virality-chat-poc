[Music]
Well, um, welcome everyone. Um, happy to
be here, uh, today. I'm very excited.
It's a very hot topic. Um so I am Cedric
Vidal uh principal AI advocate at
Microsoft and today we are going to talk
about how to evaluate agents. Uh so for
those of you who were in this very room
the session just before my uh colleagues
uh presented red teaming uh which is how
you create uh data uh that tries to put
your AI in a bad situation and generate
bad uh content and try to verify that it
behaves correctly. Today in this uh
session we are going to uh look at more
a traditional normal types of uh
evaluations when you have a data set
that you want to evaluate on your AI
agents. Um so we're going to see uh look
at a bunch of things uh on how to make
safe your AIS are safe.
So I see that people are still coming in
the room. Uh it's okay come in don't be
afraid. Um so
we don't want that, right? Uh
uh it's uh AI agents are all the rage.
Uh to be honest, every single day like
even as I was preparing this very
presentation and I was trying the latest
models and the latest uh uh SDKs, uh I'm
always uh amazed at the progress that
those agents are making. Um and u but of
course the more um agency we give to
them the more independent they become uh
the more the risk of uh creating havoc
uh increases. So let's uh see how we can
make sure that your AI agents behave
correctly and uh do not create that kind
of mess. Um, so how do you um No, sorry.
Um, how do you go about um uh evaluating
your AI agent? Do you submit like a
couple prompts to validate that the
models um respond correctly and go yeah
well that checks that should go and put
it uh in production or do you go about a
more methodical approach? Uh if you are
doing the former then I have some news
for you. You are uh in the right place.
um you need to change something uh it's
not going to uh work. If you're in the
uh ladder then um today I have some uh
frameworks to share to you on how to
which might help you improve uh your
evaluation process.
So when should you start doing
evaluations?
Um you may wondering what's the uh
evaluation um when does it occur? Um,
and I mean if you have already built an
app and you're asking yourself, should I
evaluate now? Well, uh, good news, I
mean, or bad news, uh, you're a bit
late. You should have started way
earlier. Evaluation starts, uh, at the
very beginning of your, uh, AI
development, uh, project. Um, the sooner
the better. So to get a bit a sense of
how to approach the uh subject of a
agent evaluation, we distinguish four uh
layers. Um uh we first you have the
model and the safety system which are
platform specific uh level protections
and this is built in Azure. You don't
have to do uh anything about that when
using Azure models on Azure. Uh and then
you have system message and grounding.
So for that part and user experience and
for that part that's where your app
design matters the most. Um the key
takeaway the financial model is just one
part. Um real safety comes from layering
uh smart mitigations at the application
layer and we're going to see how to do
that.
The first thing you should do is man
manual model evaluation. So which model
do you want to use for your AI agent? Um
uh you want to get a clear sense of how
different models would respond to a
given prompt. Uh something automatic
metrics can sometimes miss when you uh
launch a batch uh of metrics of
evaluations on a data set. you sometimes
you have a big average score and you
might be left wondering okay but uh I'm
not sure exactly how it works
specifically for a very specific example
before evaluating at scale you need
first to um cherry pick and look at
specific examples
so now I'm going to demo to you how to
do that in VS
So um the first thing here I'm going to
look at my history
um is that you can uh so in VS code
there is a new freshly recent relatively
new plug-in uh called AI toolkit which
was released uh at build I believe and
oh my god I love that plugin. Uh before
I used to go to uh different websites
all over the web to evaluate models and
compare I mean you had you had uh GitHub
models uh but now you can do it right
from your development environment and if
you're like me and you like to code
that's where I like to do things um
AI
toolkit yes um and so you can ask I did
ask it that question already what's a
good panakata recipe with salted caramel
butter which is my favorite uh and then
you get a pretty good response with 4.1.
But what if you want to compare with 40
for example? So
what
what's a good recipe for uh pana kota uh
with salted caramel
butter
and then you can see uh side to side how
the two moes will respond. uh 4.1 on the
left and four 40 4 on the right. And as
you can see, 4.1 uh is a major
improvement in terms of uh throughput.
Uh you're going to get the answer much
faster. Uh when it comes to the quality
uh of the answer, um so I looked at it
ahead of the conference and to be
honest, I prefer the 4.1 answer. 4.0 is
not too bad, but I mean 4.1 is so much
faster that usually that's what you're
going to use. Um so that's for
spot checking uh the answer of a
foundation model um without any
customization. We we don't have an AI
agent yet. Um then
uh you want to evaluate the whole
system. So that's where uh we are going
to actually build an AI agent and
evaluate the the agent uh from a
systematic system systemic approach as a
whole.
Um once you have selected the model it's
time to evaluate it end to end. Uh and
um so let's jump in and let me show you
how that works in VS code. So same that
same AI toolkit extension for VS code.
Uh wow I mean to be honest I love it. Uh
because now you can build an AI agent
like super fast and evaluate it super
fast too. So here I created ahead um I
prepared an agent to extract agenda uh
and event information from web pages. Um
uh for me as an advocate I do that kind
of talks pretty often and I need to know
uh uh I created a basically an agent
that helps me easily fetch information
from the web and pull um the the names
list of of talks of speakers and number
of attendees that kind of thing and um
it's super easy to do. So I'm going to
show you how to create a new agent
really quick. Uh and you have an example
here with a web scrapper. Um, and it
automatically generates a system prompt
saying, "Hey, you are a web exploration
assistant that can navigate to
websites." Uh, it's going to configure
an MCP server um ready to use. And um if
I run it,
uh it's going to
start uh the playright MCP server. um uh
the by default the uh it uses an example
domain
and we'll extract you can see the
background will extract information
about um the website. Now I'm going to
switch back to the agent that I created
because the one I just showed you is the
the built-in. So this one um I created
and I'm going to use GPT41.
Um and this one is more focused. What I
want is to extract the name, date,
location and number of attendees uh in a
specific format um and uh for that
website which is a lumar event page. So
run. So what I did is that I took the
the automatically generated one of the
sample AI agent that was created by AI
toolkit and I customized it for my use
case.
And here you can see the AI uh agent uh
working with uh and piloting um
playright going to the web page
extracting the information and giving me
the response. So the um the event is AI
agents and startup talks at GitHub
location is GitHub headquarter in San
Francisco uh on June 11th. Uh, and for
now we have 269 uh, people that
registered and I hope that after doing
the demo we're going to have more
uh, because that's an event that I
co-organized um, uh, in San Francisco.
Um, and um, so now that we have uh, spot
checked our we have built we have
customized we have spot checked what our
agent does for a specific input. Let's
see how we can evaluate it on multiple
uh inputs.
So you have uh um a tab here called uh
evaluation uh which allows you to uh
take uh that AI agent previously
configured and to execute it for uh on a
data set. So here I uh so I can type run
all
and in the background it's going to run
uh the agent of those inputs and give us
the answer in the response column. As
you can see I had executed it uh before.
So you can see uh what was the previous
answer. Uh but what's cool here is that
you can take that answer have a look at
it and as you can see we can see the uh
the information correctly um extracted.
Uh what's interesting is that the web
page here by the way does not contain
the number of attendees. Still we can
see here that we have an answer here
that's very interesting because it
actually went well it went to the um
reactor uh page to that event page found
the link to the luma page navigated to
the luma page and on the luma page we
have the number of attendees. So it
pulled in it mixed the information from
the reactor event page and the luma page
uh to collect everything I needed to in
order to get my answer. Okay. That's
that was a side note. Um and I mean I
love it. In both cases those are good
answers. So we can um manually evaluate
whether it's a thumbs up or thumbs down.
And then we can do a few things. We can
uh export the data set to a JSON file.
Uh, so I'm not going to do it, but it's
basically a JSON line file with uh the
result of the evaluation that you can
then reinject
um into um a more automated system. And
then once you have your your agent like
this, you can type view code generate uh
using whichever framework you prefer. Uh
OpenAI agents is usually the one people
want to use those days. Um and then you
have all configured uh an agent with uh
the MCP uh server and uh boiler plate
code to evaluate uh uh to run sorry your
agent. So let me close that. Let me move
on. Okay. So we've seen how to build and
um manually evaluate our AI agent uh on
the spot example and uh how to run it on
a batch of example locally. So a small
batch. Then how do you scale beyond a
few samples?
Uh let me move on to the next slide.
How
do you get the PowerPoint presentation?
Sorry, what
do you get? Did we get the
PowerPoint presentation?
Yeah, sure. I
can share it before. Excuse me. I have
five minutes left. Uh we Yes, I will
share it. Um so um
okay, so we've seen AI toolkit. Okay. So
how do we scale uh beyond what I just
showed? Uh because okay uh eyeballing uh
is great to get a sense of how it works
but what you want to do is uh go through
more thorough more wide range of checks
uh and you want to automate this. Um so
um well Azure foundry gives a wide set
of built-in evaluators to automate and
scale those evaluations. We've got AI
assisted quality checks like
roundedness, fluency, coherence, perfect
for measuring how well your agent
performs in realistic conversations. You
also find classic NLP metrics. Uh F1
blow rouge for benchmark comparisons as
well as um uh a suit of AI assisted risk
and safety evaluators. And you can also
customize and build your own.
Um
once you've spot checked uh the next the
next step is to scale uh and for that
you uh you need automated evaluation um
to measure quality either scale uh you
can do it either in Azure foundry portal
or via code and I'm going to show you
how to do it via code. Um it's important
because um we can define we want to
measure based on our apps uh use and
goal. Um so now demo Crazy
how 20 minutes goes fast. Uh so here's a
notebook and given the time we have I'm
not going to execute it because it takes
a bit of time. Uh but here you have the
the Python code to um and I'm going to
share at the end of the presentation the
link to the notebook. Uh you have the
notebook that allows you to um
programmatically
uh use connect to the Azure AI foundry
uh project uh and run those evaluation.
So the key function here is that you can
define so those are quality uh
evaluators to evaluate relevance,
coherence, groundedness, fluency and
similarity. And you have an evaluate
function code that takes those
evaluators takes the data set that you
want to evaluate uh and um bulk evaluate
um the AI agent on all those um metrics
and the result is uh here. So uh on that
data set here uh which is about camping
uh like what is the capital of France,
which tent is the most waterproof, what
camping table, whatever. Um you can see
for each um question here you can see um
the result of the evolution which also
you can configure a threshold. So it's
going to get um give you an answer
between one and five. And depending on
which threshold you configure because
depending on your application, you might
uh want your AI agent to be more or less
strict. Depending whether you're in the
gaming industry where usually they
accept more like um violent content or
whether you are doing an application for
kids, obviously the threshold is not
going to be the same. Um and so I'm
going to move on to the next. Um so in
this case, this this was passing. I I
want just want to show the next uh
evaluator that we have.
Um
also very cool now you can evaluate
multimodel models mixing text and
images. Uh this is very um important and
for multi-turn conversations.
So here
um I have an image on purpose. Uh so I
tried to find a violent image and it's
hard to find something violent that you
can show at a conference publicly.
Right? So uh I I did what I could and I
spent a lot of time looking and believe
me when you search for something violent
on the web you see things you don't want
to see. Uh and so I found that um and
let's go straight to the end and see
what it tells us. So um the systems
response uh blah blah blah. The image
actually depicts a character with
numerate pins or nails protruding from
their head which is a graphic and
violent depictions. Uh but what's
interesting the score is four. It's not
like five. It's not the max. So it's
failing. Um but it um like for example
if you were doing like like I said a
video game with violent content you
could increase to four and say hey four
I'm fine with it. uh and so in order to
be able to generate that kind of image
uh and at the end uh what's interesting
uh and I'm going to show you on another
uh okay I'm going to move on
um
I showed you that
um okay I don't have
I wanted to show you something Yes.
Okay. You also have an evaluation
evaluator to uh Oh, I think I'm on time
sadly. Okay. So, here's um some links to
more information. Uh we have um uh on
GitHub Azeri Foundry discussions uh
where you can come and ask questions
about uh that evaluation SDK and how to
build age AI gen and how to evaluate
them. uh you have the Azeri foundry
discord too where you can come and
discuss if you prefer discord and then
at the very end you have my uh contact
uh information uh if you want to reach
out for more uh questions
um so yeah very packed uh sorry a lot to
say and very little time so thank you
very much uh I'm here if you have more
questions
how are you sharing the slides
Uh,
that's a good question. Uh, I'm going to
put them on the Discord.
The Discord
and on the middle you have our Discord
server. So, you can come on the Discord
server and I will post it there.
Thank you very much.
[Music]
