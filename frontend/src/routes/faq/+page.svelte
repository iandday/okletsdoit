<!-- frontend/src/routes/faq/+page.svelte -->
<script lang="ts">
    import ComingSoon from "$lib/components/ComingSoon.svelte";
    import PageShell from "$lib/components/layouts/PageShell.svelte";
    import type { IComingSoon } from "../../types";

    // const faqs: iFaqTips[] = [
    //     {
    //         category: "Event Details",
    //         faqs: [
    //             {
    //                 question: "When should I show up for the wedding?",
    //                 answer: "The wedding will take place on November 7, 2026, at 4:00 PM.",
    //                 icon: "lucide--calendar",
    //                 id: "event-date",
    //             },
    //         ],
    //         tips: [],
    //         id: "event-details",
    //     },
    //     {
    //         category: "Event Details",
    //         faqs: [
    //             {
    //                 question: "Where is the venue located?",
    //                 answer: "The venue is located at Timberframe Lodge in Hocking Hills, Ohio. The address is 16187 Kreashbaum Rd, Rockbridge, OH 43149.",
    //                 icon: "lucide--map-pin",
    //                 id: "venue-address",
    //             },
    //             {
    //                 question: "Will the ceremony be indoors or outdoors?",
    //                 answer: "We will be outside, Ohio weather can be unpredictable. It might be 80º and sunny or 60º and chilly. We’ll do our best to be prepared with essentials (heaters, sunscreen, bug spray, etc.) but we ask that you be open to the adventure of an outdoor wedding in November in Ohio!",
    //                 id: "ceremony-location",
    //                 icon: "lucide--cloud-sun",
    //             },
    //         ],
    //         tips: [],
    //         id: "venue-location",
    //     },
    //     {
    //         category: "Attire",
    //         faqs: [
    //             {
    //                 question: "Is there a dress code?",
    //                 answer: "Our venue, Timberframe Lodge, is nestled right in the heart of Hocking Hills, a very hilly and fairly remote region in SE Ohio. The ceremony and reception will be taking place outside, rain or shine. Most of the outdoor area is gravel and grass and we’ll have outdoor heaters for when it gets a bit chilly. With these things in mind, please make wise choices regarding shoes and clothing. Dressy casual attire is requested.",
    //                 urls: [
    //                     {
    //                         url: "https://www.theknot.com/content/what-to-wear-dressy-casual",
    //                         url_text: "What to Wear: Dressy Casual",
    //                     },
    //                 ],
    //                 id: "dress-code",
    //                 icon: "lucide--shirt",
    //             },
    //         ],
    //         tips: [
    //             "If you get cold easily, please bring a light jacket or sweater.",
    //             "For our mobility challenged guests, please wear flat soled shoes. We will have a mobility assistance golf cart available to shuttle guests from the parking area to the ceremony and reception areas if requuired.",
    //         ],
    //         id: "attire-info",
    //     },
    //     {
    //         category: "Logistics",
    //         faqs: [
    //             {
    //                 question: "Is parking available at the venue?",
    //                 answer: "Yes, there is a gravel parking lot on-site. When driving down the driveway, be prepared for a small peninsula that splits the driveway towards the parking lot - it comes quickly and will take you by surprise!",
    //                 icon: "lucide--car",
    //                 id: "parking-info",
    //             },
    //         ],
    //         tips: [
    //             "Upon approaching the venue, keep your eyes open for the street address sign on the electric pole. There is no venue sign by the road and can be easy to miss.",
    //             "Portions of Hocking Hills can be remote and cell service might be inconsistent. Please be prepared and download driving directions - or, gasp, print them out!",
    //         ],
    //         id: "logistics-info",
    //     },
    //     {
    //         category: "Accommodations",
    //         faqs: [
    //             {
    //                 question: "Will there be accommodations nearby?",
    //                 answer: "If you’d like to make a whole evening or spend the weekend in the area and are in need of accommodations, we included a list of options in the area on the Venue page",
    //                 icon: "lucide--hotel",
    //                 id: "accommodations-info",
    //             },
    //         ],
    //         tips: [
    //             "Want to spend a little time exploring the area before the wedding? Check out our list of recommended area attractions on the Venue page.",
    //         ],
    //         id: "accommodations-tips",
    //     },
    //     {
    //         category: "Guest Info",
    //         faqs: [
    //             {
    //                 question: "Can I bring a plus-one or children?",
    //                 answer: "Please be mindful of who your invitation is addressed to when making plans. We have made intentional choices to keep our wedding day small and intimate so we can maximize our time with our closest friends and family. Due to keeping a smaller guest list, some of our guests may not be able to bring a plus one and we kindly ask that children stay home. Our niece (the flower girl) and our two parking lot assistants, are the only exceptions. We really appreciate your understanding on this decision!",
    //                 icon: "lucide--users",
    //                 id: "plus-one-children",
    //             },
    //             {
    //                 question: "Can I be your photographer?",
    //                 answer: "Please keep phones tucked away during the ceremony; our photographer, Brian, is amazing! However, after we say “I Do,” take as many photos as you’d like! This website will allow you to upload photos to share with everyone starting on the big day. Please leave traditional cameras at home and let our magical photographer make magic.",
    //                 icon: "lucide--camera",
    //                 id: "photographer-info",
    //             },
    //             {
    //                 question: "Can I bring a gift?",
    //                 answer: "Gifts are 100% unnecessary and not required. If you’d like to bring a card with thoughtful, witty, or sarcastic sentiments, we will have a box ready at the reception. If you REALLY would like to gift us something, we ask that you make a donation to the organizations below that are close to our hearts.",
    //                 icon: "lucide--gift",
    //                 id: "gift-info",
    //                 urls: [
    //                     {
    //                         url: "https://www.aspca.org/",
    //                         url_text: "ASPCA",
    //                     },
    //                     {
    //                         url: "https://www.humanesociety.org/",
    //                         url_text: "Humane Society",
    //                     },
    //                 ],
    //             },
    //         ],
    //         tips: [],
    //         id: "guest-info",
    //     },
    //     {
    //         category: "Food & Drink",
    //         faqs: [
    //             {
    //                 question: "What food will be served?",
    //                 answer: "You'll have your choice of dishes from multiple food stations.  Please let us know of any allergies or dietary needs when you RSVP.",
    //                 icon: "lucide--utensils",
    //                 id: "food-info",
    //             },
    //             {
    //                 question: "Is there an open bar?",
    //                 answer: "Yes! We'll have a selection of beer, wine, and signature cocktails available throughout the reception.",
    //                 icon: "lucide--wine",
    //                 id: "bar-info",
    //             },
    //             {
    //                 question: "What if I have dietary restrictions?",
    //                 answer: "Please let us know about any dietary restrictions or allergies when you RSVP, and we'll make sure you're taken care of!",
    //                 icon: "lucide--apple",
    //                 id: "dietary-restrictions",
    //             },
    //         ],
    //         tips: ["Open Bar 🙂(we’re paying gratuity, just drink and enjoy, on us!)"],
    //         id: "food-drink-info",
    //     },
    //     {
    //         category: "RSVP",
    //         faqs: [
    //             {
    //                 question: "When is the RSVP deadline?",
    //                 answer: "Please RSVP by September 1, 2026, so we can finalize our guest count with the venue and caterer.",
    //                 icon: "lucide--check-circle",
    //                 id: "rsvp-deadline",
    //             },
    //         ],
    //         tips: [],
    //         id: "rsvp-info",
    //     },
    // ];

    const comingSoon: IComingSoon = {
        icon: "help-circle",
        alert: "Coming Soon",
        intro: "We're preparing a comprehensive FAQ section to answer all your questions about our special day! Check back soon for helpful information.",
        expectations: [
            { text: "Event date and time details", icon: "calendar" },
            { text: "Venue location and directions", icon: "map-pin" },
            { text: "Dress code and attire guidance", icon: "shirt" },
            { text: "Food, drinks, and dietary options", icon: "utensils" },
        ],
    };

    const { data } = $props();
</script>

<div>
    <PageShell title="Frequently Asked Questions">
        {#if !data?.configData?.showFaq}
            <ComingSoon {...comingSoon} />
        {:else}
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
                    {#each data.categories as cat (cat.categoryId)}
                        <div class="mb-8">
                            <!-- Category Header -->
                            <div class="flex items-center gap-3 mb-4">
                                <div
                                    class="h-px flex-grow bg-gradient-to-r from-transparent via-primary to-transparent">
                                </div>
                                <h3 class="text-xl font-bold text-primary">{cat.categoryName}</h3>
                                <div
                                    class="h-px flex-grow bg-gradient-to-r from-primary via-transparent to-transparent">
                                </div>
                            </div>

                            <!-- FAQ Items -->
                            <div class="space-y-3">
                                {#each cat.questions as question (question.id)}
                                    <div
                                        class="collapse collapse-plus bg-secondary text-secondary-content border border-base-300 shadow-md hover:shadow-lg transition-shadow">
                                        <input type="radio" name="faq-accordion-{question.id}" />
                                        <div class="collapse-title text-lg font-medium flex items-center gap-3">
                                            <div class="bg-primary/10 rounded-full p-2 flex-shrink-0">
                                                <span
                                                    class="iconify lucide--{question.icon} size-7 font-strong text-primary-content"
                                                ></span>
                                            </div>
                                            <span>{question.question}</span>
                                        </div>
                                        <div class="collapse-content">
                                            <div class="pt-2 pl-14">
                                                <p class="leading-relaxed">{question.answer}</p>
                                                {#if question.urls}
                                                    <div class="flex flex-row flex-wrap gap-3 mt-4">
                                                        {#each question.urls as url (url.id)}
                                                            <a
                                                                href={url.url}
                                                                target="_blank"
                                                                rel="noopener noreferrer"
                                                                class="badge badge-primary gap-2">
                                                                {url.text}
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
                            {#if cat.tips && cat.tips.length > 0}
                                <div class="mt-4 alert bg-base-100 text-neutral-content border-accent/30 shadow-md">
                                    <div class="flex items-start gap-3 w-full">
                                        <span class="iconify lucide--lightbulb size-6 text-accent flex-shrink-0"></span>
                                        <div class="flex-1">
                                            <h4 class="font-bold text-accent mb-2">Helpful Tips</h4>
                                            <ul class="space-y-2">
                                                {#each cat.tips as tip (tip.id)}
                                                    <li class="text-sm text-secondary-content flex items-start gap-2">
                                                        <span
                                                            class="iconify lucide--check size-4 text-accent mt-0.5 flex-shrink-0"
                                                        ></span>
                                                        <span>{tip.content}</span>
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
