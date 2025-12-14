<script lang="ts">
    import PageShell from "$lib/components/layouts/PageShell.svelte";

    type iURL = {
        url: string;
        url_text: string;
    };
    type iFAQ = {
        question: string;
        answer: string;
        icon: string;
        urls?: iURL[];
    };

    type iFaqTips = {
        category: string;
        faqs: iFAQ[];
        tips: string[];
    };

    const faqs: iFaqTips[] = [
        {
            category: "Event Details",
            faqs: [
                {
                    question: "When should I show up for the wedding?",
                    answer: "The wedding will take place on November 7, 2026, at 4:00 PM.",
                    icon: "lucide--calendar",
                },
            ],
            tips: [],
        },
        {
            category: "Event Details",
            faqs: [
                {
                    question: "Where is the venue located?",
                    answer: "The venue is located at Timberframe Lodge in Hocking Hills, Ohio. The address is 16187 Kreashbaum Rd, Rockbridge, OH 43149.",
                    icon: "lucide--map-pin",
                },
                {
                    question: "Will the ceremony be indoors or outdoors?",
                    answer: "We will be outside, Ohio weather can be unpredictable. It might be 80º and sunny or 60º and chilly. We’ll do our best to be prepared with essentials (heaters, sunscreen, bug spray, etc.) but we ask that you be open to the adventure of an outdoor wedding in November in Ohio!",

                    icon: "lucide--cloud-sun",
                },
            ],
            tips: [],
        },
        {
            category: "Attire",
            faqs: [
                {
                    question: "Is there a dress code?",
                    answer: "Our venue, Timberframe Lodge, is nestled right in the heart of Hocking Hills, a very hilly and fairly remote region in SE Ohio. The ceremony and reception will be taking place outside, rain or shine. Most of the outdoor area is gravel and grass and we’ll have outdoor heaters for when it gets a bit chilly. With these things in mind, please make wise choices regarding shoes and clothing. Dressy casual attire is requested.",
                    urls: [
                        {
                            url: "https://www.theknot.com/content/what-to-wear-dressy-casual",
                            url_text: "What to Wear: Dressy Casual",
                        },
                    ],
                    icon: "lucide--shirt",
                },
            ],
            tips: [
                "If you get cold easily, please bring a light jacket or sweater.",
                "For our mobility challenged guests, please wear flat soled shoes. We will have a mobility assistance golf cart available to shuttle guests from the parking area to the ceremony and reception areas if requuired.",
            ],
        },
        {
            category: "Logistics",
            faqs: [
                {
                    question: "Is parking available at the venue?",
                    answer: "Yes, there is a gravel parking lot on-site. When driving down the driveway, be prepared for a small peninsula that splits the driveway towards the parking lot - it comes quickly and will take you by surprise!",
                    icon: "lucide--car",
                },
            ],
            tips: [
                "Upon approaching the venue, keep your eyes open for the street address sign on the electric pole. There is no venue sign by the road and can be easy to miss.",
                "Portions of Hocking Hills can be remote and cell service might be inconsistent. Please be prepared and download driving directions - or, gasp, print them out!",
            ],
        },
        {
            category: "Accommodations",
            faqs: [
                {
                    question: "Will there be accommodations nearby?",
                    answer: "If you’d like to make a whole evening or spend the weekend in the area and are in need of accommodations, we included a list of options in the area on the Venue page",
                    icon: "lucide--hotel",
                },
            ],
            tips: [
                "Want to spend a little time exploring the area before the wedding? Check out our list of recommended area attractions on the Venue page.",
            ],
        },
        {
            category: "Guest Info",
            faqs: [
                {
                    question: "Can I bring a plus-one or children?",
                    answer: "Please be mindful of who your invitation is addressed to when making plans. We have made intentional choices to keep our wedding day small and intimate so we can maximize our time with our closest friends and family. Due to keeping a smaller guest list, some of our guests may not be able to bring a plus one and we kindly ask that children stay home. Our niece (the flower girl) and our two parking lot assistants, are the only exceptions. We really appreciate your understanding on this decision!",
                    icon: "lucide--users",
                },
                {
                    question: "Can I be your photographer?",
                    answer: "Please keep phones tucked away during the ceremony; our photographer, Brian, is amazing! However, after we say “I Do,” take as many photos as you’d like! This website will allow you to upload photos to share with everyone starting on the big day. Please leave traditional cameras at home and let our magical photographer make magic.",
                    icon: "lucide--camera",
                },
                {
                    question: "Can I bring a gift?",
                    answer: "Gifts are 100% unnecessary and not required. If you’d like to bring a card with thoughtful, witty, or sarcastic sentiments, we will have a box ready at the reception. If you REALLY would like to gift us something, we ask that you make a donation to the organizations below that are close to our hearts.",
                    icon: "lucide--gift",
                    urls: [
                        {
                            url: "https://www.aspca.org/",
                            url_text: "ASPCA",
                        },
                        {
                            url: "https://www.humanesociety.org/",
                            url_text: "Humane Society",
                        },
                    ],
                },
            ],
            tips: [],
        },
        {
            category: "Food & Drink",
            faqs: [
                {
                    question: "What food will be served?",
                    answer: "You'll have your choice of dishes from multiple food stations.  Please let us know of any allergies or dietary needs when you RSVP.",
                    icon: "lucide--utensils",
                },
                {
                    question: "Is there an open bar?",
                    answer: "Yes! We'll have a selection of beer, wine, and signature cocktails available throughout the reception.",
                    icon: "lucide--wine",
                },
                {
                    question: "What if I have dietary restrictions?",
                    answer: "Please let us know about any dietary restrictions or allergies when you RSVP, and we'll make sure you're taken care of!",
                    icon: "lucide--apple",
                },
            ],
            tips: ["Open Bar 🙂(we’re paying gratuity, just drink and enjoy, on us!)"],
        },
        {
            category: "RSVP",
            faqs: [
                {
                    question: "When is the RSVP deadline?",
                    answer: "Please RSVP by September 1, 2026, so we can finalize our guest count with the venue and caterer.",
                    icon: "lucide--check-circle",
                },
            ],
            tips: [],
        },
    ];

    const showFaqs = false;
</script>

<div>
    <PageShell title="Frequently Asked Questions">
        {#if !showFaqs}
            <div class="pb-8 lg:pb-12 xl:pb-16">
                <div class="container mx-auto px-4 md:px-6 lg:px-8 max-w-4xl">
                    <!-- Coming Soon Announcement -->
                    <div class="flex justify-center items-center min-h-[400px]">
                        <div class="card bg-base-200 shadow-2xl border border-primary/20 w-full max-w-2xl pb-2">
                            <div class="card-body items-center text-center">
                                <div class="mb-6">
                                    <span class="iconify lucide--help-circle size-20 text-accent animate-pulse"></span>
                                </div>
                                <div class="badge badge-primary badge-lg mb-4 gap-2 px-4 py-3">
                                    <span class="iconify lucide--clock size-4"></span>
                                    Coming Soon
                                </div>

                                <p class="text-primary-content text-lg leading-relaxed mb-6 max-w-lg">
                                    We're preparing a comprehensive FAQ section to answer all your questions about our
                                    special day! Check back soon for helpful information.
                                </p>

                                <div class="text-left w-full max-w-md">
                                    <h3 class="font-bold text-primary-content text-lg mb-3 flex items-center gap-2">
                                        <span class="iconify lucide--sparkles size-5 text-primary-content"></span>
                                        What to Expect:
                                    </h3>
                                    <ul class="space-y-3">
                                        <li class="flex items-start gap-3">
                                            <span
                                                class="iconify lucide--calendar size-5 text-accent mt-0.5 flex-shrink-0"
                                            ></span>
                                            <span class="text-primary-content">Event date and time details</span>
                                        </li>
                                        <li class="flex items-start gap-3">
                                            <span
                                                class="iconify lucide--map-pin size-5 text-accent mt-0.5 flex-shrink-0"
                                            ></span>
                                            <span class="text-primary-content">Venue location and directions</span>
                                        </li>
                                        <li class="flex items-start gap-3">
                                            <span class="iconify lucide--shirt size-5 text-accent mt-0.5 flex-shrink-0"
                                            ></span>
                                            <span class="text-primary-content">Dress code and attire guidance</span>
                                        </li>
                                        <li class="flex items-start gap-3">
                                            <span
                                                class="iconify lucide--utensils size-5 text-accent mt-0.5 flex-shrink-0"
                                            ></span>
                                            <span class="text-primary-content">Food, drinks, and dietary options</span>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        {/if}
        {#if showFaqs}
            <div class="pb-8 lg:pb-12 xl:pb-16">
                <div class="container mx-auto px-4 md:px-6 lg:px-8 max-w-5xl">
                    <!-- Header -->
                    <div class="text-center mb-8 md:mb-12">
                        <p class="text-base-content/70 text-lg max-w-2xl mx-auto">
                            Have questions about our big day? We've got answers! If you don't see your question here,
                            feel free to reach out to us directly.
                        </p>
                    </div>

                    <!-- FAQs by Category -->
                    {#each faqs as entry}
                        <div class="mb-8">
                            <!-- Category Header -->
                            <div class="flex items-center gap-3 mb-4">
                                <div
                                    class="h-px flex-grow bg-gradient-to-r from-transparent via-primary to-transparent">
                                </div>
                                <h3 class="text-xl font-bold text-primary">{entry.category}</h3>
                                <div
                                    class="h-px flex-grow bg-gradient-to-r from-primary via-transparent to-transparent">
                                </div>
                            </div>

                            <!-- FAQ Items -->
                            <div class="space-y-3">
                                {#each entry.faqs as faq, index}
                                    <div
                                        class="collapse collapse-plus bg-secondary text-secondary-content border border-base-300 shadow-md hover:shadow-lg transition-shadow">
                                        <input type="radio" name="faq-accordion-{index}" />
                                        <div class="collapse-title text-lg font-medium flex items-center gap-3">
                                            <div class="bg-primary/10 rounded-full p-2 flex-shrink-0">
                                                <span class="iconify {faq.icon} size-7 font-strong text-primary-content"
                                                ></span>
                                            </div>
                                            <span>{faq.question}</span>
                                        </div>
                                        <div class="collapse-content">
                                            <div class="pt-2 pl-14">
                                                <p class="leading-relaxed">{faq.answer}</p>
                                                {#if faq.urls}
                                                    <div class="flex flex-row flex-wrap gap-3 mt-4">
                                                        {#each faq.urls as url}
                                                            <a
                                                                href={url.url}
                                                                target="_blank"
                                                                rel="noopener noreferrer"
                                                                class="badge badge-primary gap-2">
                                                                {url.url_text}
                                                            </a>
                                                        {/each}
                                                    </div>
                                                {/if}
                                            </div>
                                        </div>
                                    </div>
                                {/each}
                            </div>

                            <!-- Tips Section -->
                            {#if entry.tips && entry.tips.length > 0}
                                <div class="mt-4 alert bg-base-100 text-neutral-content border-accent/30 shadow-md">
                                    <div class="flex items-start gap-3 w-full">
                                        <span class="iconify lucide--lightbulb size-6 text-accent flex-shrink-0"></span>
                                        <div class="flex-1">
                                            <h4 class="font-bold text-accent mb-2">Helpful Tips</h4>
                                            <ul class="space-y-2">
                                                {#each entry.tips as tip}
                                                    <li class="text-sm text-secondary-content flex items-start gap-2">
                                                        <span
                                                            class="iconify lucide--check size-4 text-accent mt-0.5 flex-shrink-0"
                                                        ></span>
                                                        <span>{tip}</span>
                                                    </li>
                                                {/each}
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            {/if}
                        </div>
                    {/each}

                    <!-- Contact Section -->
                    <div class="mt-12">
                        <div
                            class="card bg-gradient-to-br from-primary/10 via-secondary/10 to-accent/10 shadow-xl border border-primary/20">
                            <div class="card-body items-center text-center">
                                <span class="iconify lucide--mail size-12 text-primary mb-4"></span>
                                <h3 class="text-2xl font-bold mb-2">Still Have Questions?</h3>
                                <p class="text-base-content/70 mb-6 max-w-md">
                                    Don't hesitate to reach out! We're here to help make sure you have all the
                                    information you need.
                                </p>
                                <a href="mailto:wedding@example.com" class="btn btn-primary gap-2">
                                    <span class="iconify lucide--send size-5"></span>
                                    Contact Us
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        {/if}
    </PageShell>
</div>
