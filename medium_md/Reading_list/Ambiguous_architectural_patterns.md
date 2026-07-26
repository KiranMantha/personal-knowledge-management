---
title: "Ambiguous architectural patterns"
url: https://medium.com/p/7733c1225422
---

# Ambiguous architectural patterns

[Original](https://medium.com/p/7733c1225422)

# Ambiguous architectural patterns

[![Denys Poltorak](https://miro.medium.com/v2/resize:fill:64:64/1*h7aQtRSEV2EBK5hMwsvVXA.png)](https://denyspoltorak.medium.com/?source=post_page---byline--7733c1225422---------------------------------------)

[Denys Poltorak](https://denyspoltorak.medium.com/?source=post_page---byline--7733c1225422---------------------------------------)

6 min read

·

Oct 23, 2024

--

6

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D7733c1225422&operation=register&redirect=https%3A%2F%2Fitnext.io%2Fambiguous-architectural-patterns-7733c1225422&source=---header_actions--7733c1225422---------------------post_audio_button------------------)

Share

> This is an outdated version of a chapter from my book [Architectural Metapatterns: the Pattern Language of Software Architecture](https://medium.com/itnext/the-list-of-architectural-metapatterns-ed64d8ba125d) which you can [read online](https://metapatterns.io/analytics/ambiguous-patterns/) or download for free from [Leanpub](https://leanpub.com/metapatterns) or [GitHub](https://github.com/denyspoltorak/publications/tree/main/ArchitecturalMetapatterns).

We’ve seen a single pattern come under many names, as it happens with [*Orchestrator*](https://medium.com/itnext/orchestrator-0708881ffdb1), and also one name used for multiple topologies, as with *services*, which may [orchestrate each other](https://medium.com/itnext/services-ab8a45878621), make a [*pipeline*](https://medium.com/itnext/pipeline-88e24688b5ec) or be components of a [*SOA*](https://medium.com/itnext/service-oriented-architecture-soa-5d0cd2b8464c). On top of that, there are several pattern names that are often believed to be unambiguous while each of them sees conflicting definitions in the books or over the web. Let’s explore the last kind, which is the most dangerous both for your understanding of other people and for your time wasted on arguments.

## [Monolith](https://medium.com/itnext/monolith-e84e8454106b)

Press enter or click to view image in full size

![]()

The old books, namely [GoF] and [POSA1], described a tightly coupled unstructured system, where anything depends on everything, as *monolithic*, which matched the meaning of the word in Latin — “single stone”.

Then something evil happened — I believe that the proponents of *SOA*, backed by the hype and money they had earned from corporations, started labeling any *non-distributed* system as *monolithic*, obviously to contrast the negative connotation of the word to their most progressive design.

It took only a decade for the karma to strike back — when the new generation behind *Microservices* redefined *monolithic* as a single unit of deployment — to call the now obsolescent *SOA* systems *distributed monoliths* [MP] because their services often grew so coupled that they had to be deployed together.

The novel misnomers, [*Layered Monolith*](https://medium.com/itnext/layers-138e793adf51) [FSA] and [*Modular Monolith*](https://medium.com/itnext/services-ab8a45878621) [FSA], which denote an application partitioned by abstractness or subdomain, correspondingly, add to the confusion.

## [Microkernel](https://medium.com/itnext/microkernel-abb60773e469)

Press enter or click to view image in full size

![]()

*Microkernel* is another notable case. The mess goes all the way back to [POSA1] which used operating systems for examples of *Plugin Architecture*. I believe that it was a mismatch:

* An operating system is mainly about [sharing resources of producers among consumers](https://medium.com/itnext/microkernel-abb60773e469), where both producers and consumers may be written by external teams. The *kernel* itself does not feature much logic — its role is to connect the other components together.
* [*Plugins*](https://medium.com/itnext/plugins-a70bd06bd36f), on the other hand, extend or modify the business logic of the *core* — which alone is the reason for the system to exist and is in no way “*micro-*” as it got the bulk of the system’s code. In many such systems *plugins* are utterly optional — which cannot be said of *OS drivers*.

Thus, here we have two architectural patterns of arguably (*Microkernel/Plugins* of [SAP, FSA] omit 3 of 5 components of the original *Microkernel* of [POSA1, POSA4]) similar structure but very different intent and action known under the same name.

## [Domain Services](https://medium.com/itnext/services-ab8a45878621)

Press enter or click to view image in full size

![]()

I was told that [*Domain Services*](https://medium.com/itnext/services-ab8a45878621) of [FSA] are incorrect — because a *domain service* is always limited to the *domain* layer of [DDD] while those of [FSA] also cover the *application* and, maybe, *infrastructure*.

I believe that both definitions are technically correct, if the difference of the meaning of *domain* is accounted for. In [FSA] *domain* is synonymous to a *bounded context* of [DDD], while [DDD] more often uses that word for the name of its middle layer that contains business rules.

## Cells

Press enter or click to view image in full size

![]()

The fresh *Cell-Based Architecture* also got multiple definitions.

* WSO2 [wrote](https://github.com/wso2/reference-architecture/blob/master/reference-architecture-cell-based.md) about a *cell* as a group of services which is encapsulated from the remaining system by a *gateway* and *adapters* and often uses a dedicated *middleware* — letting each *cell*, though internally distributed, be treated by other components as a single service. That makes designing and managing a large system a bit simpler by introducing a [*hierarchy*](https://medium.com/itnext/hierarchy-7352e21f301f).
* Amazon [promotes](https://docs.aws.amazon.com/wellarchitected/latest/reducing-scope-of-impact-with-cell-based-architecture/what-is-a-cell-based-architecture.html) its *cells* as [*shards*](https://medium.com/itnext/shards-2637f1ae7771) of the whole system which run in multiple regions. That grants fault tolerance and improves performance as each client has an instance of the system deployed to a nearby datacenter, but does not have much impact on organization and complexity of the code.

The case looks like Amazon’s hijacking and redefining a popular emerging technology, though I may be wrong about that as I did not investigate the history of the term.

## [Nanoservices](https://medium.com/itnext/services-ab8a45878621)

Press enter or click to view image in full size

![]()

*Nanoservices* is another emerging technology, and it seems to have never been strictly defined. Most sources agree that a *nanoservice* is a cloud-based function ([*FaaS*](https://en.wikipedia.org/wiki/Function_as_a_service)), similar to a *service* with a single API method but, just as with the old good [*services*](https://medium.com/itnext/services-ab8a45878621), they differ in the ways they use the technology:

* Diego Zanon in *Building Serverless Web Applications* proposes a single layer of nanoservices, each implementing a method of the system’s public API, to be used as a thin backend.
* [Here](https://increment.com/software-architecture/the-rise-of-nanoservices/) we have *nanoservices* built into a [*pipeline*](https://medium.com/itnext/pipeline-88e24688b5ec), similar to *Choreographed Event-Driven Architecture* [FSA].
* [Another article](https://medium.com/@ido.vapner/unlocking-the-power-of-nano-services-a-new-era-in-microservices-architecture-22647ea36f22) proposes to (re)use them in [*SOA*](https://medium.com/itnext/service-oriented-architecture-soa-5d0cd2b8464c) style.

Nonetheless, there are a couple of sources which call a *nanoservice* something totally different:

* [There is a concept](https://nanoservices.io/docs/docs/building/introduction/) of *nanoservice* as a module that can run both as a separate service and as a part of a binary — allowing for the team to choose if they want their system to execute as a single process or become distributed. *Nano-* is because an in-process module is more lightweight than a *microservice*. This idea resembles [*Modular Monolith*](https://medium.com/itnext/services-ab8a45878621) [FSA] and [actor frameworks](https://en.wikipedia.org/wiki/Actor_model).
* And [here we got](https://dev.to/siy/nanoservices-or-alternative-to-monoliths-and-microservices-12bb) something akin to [*Space-Based Architecture*](https://medium.com/itnext/combined-component-51c3205c94de) but it is also called *Nanoservices* — as the proposed framework makes them so easy to create that programmers tend to write many smaller *nanoservices* instead of a single *microservice*.

In my opinion, the disarray happened because the notion of “making *smaller* microservices” got hyped but was never adopted widely enough to become an industry standard, therefore everybody follows their own vision about what *smaller* means.

## Summary

A few names of architectural patterns cause confusion as the meaning of each of them changes from source to source. The [current book](https://medium.com/itnext/the-list-of-architectural-metapatterns-ed64d8ba125d) aims at identifying such issues and building a cohesive understanding of software and system architecture.

## References

[DDD] Domain-Driven Design: Tackling Complexity in the Heart of Software. *Eric Evans. Addison-Wesley (2003).*

[GoF] Design Patterns: Elements of Reusable Object-Oriented Software. *Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides. Addison-Wesley (1994).*

[FSA] Fundamentals of Software Architecture: An Engineering Approach. *Mark Richards and Neal Ford. O’Reilly Media, Inc. (2020).*

[MP] Microservices Patterns: With Examples in Java. *Chris Richardson.* *Manning Publications (2018)*.

[POSA1] Pattern-Oriented Software Architecture Volume 1: A System of Patterns. *Frank Buschmann, Regine Meunier, Hans Rohnert, Peter Sommerlad and Michael Stal. John Wiley & Sons, Inc. (1996).*

[POSA4] Pattern-Oriented Software Architecture Volume 4: A Pattern Language for Distributed Computing. *Frank Buschmann, Kevlin Henney, Douglas C. Schmidt. John Wiley & Sons, Ltd. (2007).*

[SAP] Software Architecture Patterns. *Mark Richards. O’Reilly Media, Inc. (2015).*