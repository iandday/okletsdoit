<script lang="ts">
    const storyParts = [
        {
            title: "The Match",
            icon: "lucide--smartphone",
            content: [
                "It all started with a swipe right on Hinge. Two people on opposite sides of Columbus, both more than a little skeptical of online dating but still hoping to find something real. Neither of us expected much, but here we are.",
            ],
            color: "primary",
        },
        {
            title: "Let's Set The Scene",
            icon: "lucide--plane-takeoff",
            content: [
                "Ian had just sold his house and was getting ready to spend a month in Delaware, the state for all you Ohioans, before moving into a new place in Columbus.",
                "Steph debated saying yes to the date; she was convinced she’d catch feelings and then Ian would decide to stay in Delaware permanently. But she said yes anyway",
            ],
            color: "secondary",
        },
        {
            title: "The First Date Blunder",
            icon: "lucide--shield-alert",
            content: [
                "Steph picked the place, a bar in Easton called The Beeline, not knowing that Ian lived across town, all the way in Galloway. Obviously she beat him there! So, she waited and waited and waited.",
                'When Ian finally strolled up, he skipped the small talk and opened with, "Huh. I thought your hair would be brighter."',
                "The audacity of this man, we hadn’t even walked inside yet! Surprisingly, Steph laughed it off and didn’t toss a drink in his face later. And that’s when Ian knew he’d said something dumb, but maybe to the right person.",
            ],
            color: "primary",
        },
        {
            title: "The Rest is History",
            icon: "lucide--hand-heart",
            content: [
                "From that slightly awkward start to the first date, our love story unfolded. Believe it or not, Ian didn’t ghost Steph and came back to Columbus! And they continued seeing each other and definitely caught feelings.",
                "After countless dates and memories, tons of laughs, adventures, and concerts, and of course, lots of sarcastic comments and jests along the way, we discovered that sometimes the best relationships start with somewhat cringe-worthy moments.",
                "Who knew that insulting someone's hair on a first date could be the foundation of forever? Ian certainly didn't! Yet here we are, planning our wedding and proving that love truly does find a way, even when you start with the world's worst opening line.",
            ],
            color: "secondary",
        },
    ];
</script>

<div class="pb-8 lg:pb-16 xl:pb-24 2xl:pb-28">
    <div class="container mt-8 md:mt-12 lg:mt-16 2xl:mt-24">
        <!-- Timeline -->
        <div class="relative max-w-5xl mx-auto">
            <!-- Timeline line -->
            <div
                class="hidden md:block absolute left-1/2 top-0 bottom-0 w-0.5 bg-gradient-to-b from-primary via-secondary to-accent transform -translate-x-1/2">
            </div>

            <!-- Story Parts -->
            {#each storyParts as part, index}
                <div class="relative mb-16 md:mb-24 last:mb-0">
                    <!-- Mobile/Tablet Layout -->
                    <div class="md:hidden">
                        <div
                            class="card bg-gradient-to-br from-{part.color}/10 via-{part.color}/5 to-transparent shadow-xl border border-{part.color}/20 transition-all duration-1000 starting:scale-95 starting:opacity-0 starting:blur-sm">
                            <div class="card-body">
                                <div class="flex items-start gap-4">
                                    <div
                                        class="bg-{part.color}/20 rounded-full p-4 flex-shrink-0 border-2 border-{part.color}/30">
                                        <span class="iconify {part.icon} size-8 text-{part.color}"></span>
                                    </div>
                                    <div class="flex-1">
                                        <h2 class="card-title text-2xl badge badge-{part.color} mb-3">{part.title}</h2>
                                        {#each part.content as p}
                                            <p class="text-base-content/80 leading-relaxed pb-2">{p}</p>
                                        {/each}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Desktop Layout -->
                    <div class="hidden md:block">
                        {#if index % 2 === 0}
                            <!-- Left side -->
                            <div class="flex items-center gap-8">
                                <div class="w-1/2 text-right pr-8">
                                    <div
                                        class="card bg-gradient-to-br from-{part.color}/10 via-{part.color}/5 to-transparent shadow-xl border border-{part.color}/20 inline-block text-left transition-all duration-1000 starting:scale-95 starting:opacity-0 starting:blur-sm">
                                        <div class="card-body">
                                            <h2 class="card-title text-2xl badge badge-{part.color} mb-3">
                                                {part.title}
                                            </h2>
                                            {#each part.content as p}
                                                <p class="text-base-content/80 leading-relaxed pb-2">{p}</p>
                                            {/each}
                                        </div>
                                    </div>
                                </div>
                                <div class="relative z-10 flex-shrink-0 mr-14">
                                    <div class="bg-{part.color}/20 rounded-full p-4 border-4 border-base-100 shadow-lg">
                                        <span class="iconify {part.icon} size-10 text-{part.color}"></span>
                                    </div>
                                </div>
                                <div class="w-1/2"></div>
                            </div>
                        {:else}
                            <!-- Right side -->
                            <div class="flex items-center gap-8">
                                <div class="w-1/2"></div>
                                <div class="relative z-10 flex-shrink-0 ml-14">
                                    <div class="bg-{part.color}/20 rounded-full p-4 border-4 border-base-100 shadow-lg">
                                        <span class="iconify {part.icon} size-10 text-{part.color}"></span>
                                    </div>
                                </div>
                                <div class="w-1/2 pl-8">
                                    <div
                                        class="card bg-gradient-to-br from-{part.color}/10 via-{part.color}/5 to-transparent shadow-xl border border-{part.color}/20 inline-block transition-all duration-1000 starting:scale-95 starting:opacity-0 starting:blur-sm">
                                        <div class="card-body">
                                            <h2 class="card-title text-2xl badge badge-{part.color} mb-3">
                                                {part.title}
                                            </h2>
                                            {#each part.content as p}
                                                <p class="text-base-content/80 leading-relaxed pb-2">{p}</p>
                                            {/each}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        {/if}
                    </div>
                </div>
            {/each}
        </div>
    </div>
</div>
