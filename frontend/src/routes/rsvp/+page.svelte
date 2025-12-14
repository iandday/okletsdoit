<script lang="ts">
    import PageShell from "$lib/components/layouts/PageShell.svelte";
</script>

<div>
    <PageShell title="RSVP">
        <div class="pb-8 lg:pb-12 xl:pb-16">
            <div class="container mx-auto px-4 md:px-6 lg:px-8 max-w-4xl">
                <!-- Coming Soon Announcement -->
                <div class="flex justify-center items-center min-h-[400px]">
                    <div class="card bg-base-200 shadow-2xl border border-primary/20 w-full max-w-2xl pb-2">
                        <div class="card-body items-center text-center">
                            <div class="mb-6">
                                <span class="iconify lucide--calendar-check size-20 text-accent animate-pulse"></span>
                            </div>
                            <div class="badge badge-primary badge-lg mb-4 gap-2 px-4 py-3">
                                <span class="iconify lucide--clock size-4"></span>
                                Coming Soon
                            </div>

                            <p class="text-primary-content text-lg leading-relaxed mb-6 max-w-lg">
                                We're creating a simple RSVP system where you can let us know if you'll be joining us
                                for our special day! This feature will be available soon.
                            </p>
                            <div class="text-left w-full max-w-md">
                                <h3 class="font-bold text-primary-content text-lg mb-3 flex items-center gap-2">
                                    <span class="iconify lucide--sparkles size-5 text-primary-content"></span>
                                    What to Expect:
                                </h3>
                                <ul class="space-y-3">
                                    <li class="flex items-start gap-3">
                                        <span
                                            class="iconify lucide--check-circle size-5 text-accent mt-0.5 flex-shrink-0"
                                        ></span>
                                        <span class="text-primary-content">Quick and easy RSVP process</span>
                                    </li>
                                    <li class="flex items-start gap-3">
                                        <span class="iconify lucide--users size-5 text-accent mt-0.5 flex-shrink-0"
                                        ></span>
                                        <span class="text-primary-content">Manage your party's attendance</span>
                                    </li>
                                    <li class="flex items-start gap-3">
                                        <span class="iconify lucide--utensils size-5 text-accent mt-0.5 flex-shrink-0"
                                        ></span>
                                        <span class="text-primary-content"
                                            >Share dietary restrictions and preferences</span>
                                    </li>
                                    <li class="flex items-start gap-3">
                                        <span
                                            class="iconify lucide--message-square size-5 text-accent mt-0.5 flex-shrink-0"
                                        ></span>
                                        <span class="text-primary-content">Send us a personal message</span>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </PageShell>
</div>
