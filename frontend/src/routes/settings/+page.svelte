<script lang="ts">
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";

    const sections = [
        {
            title: "Wedding Configuration",
            description: "Manage your wedding details, RSVP settings, and site preferences",
            icon: "settings",
            href: "/settings/config",
            items: ["Wedding date and venue", "RSVP periods and labels", "Guest group settings", "Feature toggles"],
        },
        {
            title: "FAQ Management",
            description: "Create and organize frequently asked questions for your guests",
            icon: "help-circle",
            href: "/settings/faq",
            items: ["Questions and answers", "Helpful tips", "Category organization", "Preview and publish"],
        },
        {
            title: "Deadline Tracking",
            description: "Stay on top of wedding planning tasks with deadline lists",
            icon: "calendar-check",
            href: "/settings/deadline",
            items: ["Create deadline lists", "Track task progress", "Set due dates", "Mark completions"],
        },
        {
            title: "Preview Pages",
            description: "Preview how your wedding pages will appear to guests",
            icon: "eye",
            href: "/settings/preview/faq",
            items: ["FAQ page preview", "RSVP flow preview"],
        },
    ];
</script>

<ProtectedPageShell relativeCrumbs={[]}>
    <div class="max-w-6xl mx-auto">
        <!-- Header -->
        <div class="text-center mb-12">
            <h1 class="text-4xl font-bold text-base-content mb-4">Wedding Settings</h1>
            <p class="text-lg text-base-content max-w-2xl mx-auto">
                Manage all aspects of your wedding website from this central hub. Configure settings, organize content,
                and track your planning progress.
            </p>
        </div>

        <!-- Settings Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            {#each sections as section (section.title)}
                <a href={section.href} class="detail-card">
                    <div class="detail-card-body">
                        <div class="flex items-start gap-4 mb-4">
                            <div class="rounded-full p-3 flex-shrink-0">
                                <span class="icon-[lucide--{section.icon}] size-6 text-accent"></span>
                            </div>
                            <div class="flex-1">
                                <h2 class="detail-card-title">
                                    {section.title}
                                </h2>
                                <p>{section.description}</p>
                            </div>
                        </div>

                        <!-- Features List -->
                        <div class="space-y-2">
                            {#each section.items as item, index (index)}
                                <div class="flex items-center gap-2 text-sm">
                                    <span class="icon-[lucide--check] size-4 flex-shrink-0"></span>
                                    <span>{item}</span>
                                </div>
                            {/each}
                        </div>

                        <!-- Action -->
                        <div class="card-actions justify-end mt-4 pt-4 border-t border-base-300">
                            <span class="text-sm font-semibold text-accent flex items-center gap-2">
                                Manage
                                <span class="icon-[lucide--arrow-right] size-4"></span>
                            </span>
                        </div>
                    </div>
                </a>
            {/each}
        </div>
    </div>
</ProtectedPageShell>
