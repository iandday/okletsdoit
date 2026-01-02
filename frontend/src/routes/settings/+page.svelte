<script lang="ts">
    import Icon from "$lib/components/Icon.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";

    const sections = [
        {
            title: "Wedding Configuration",
            description: "Manage your wedding details, RSVP settings, and site preferences",
            icon: "settings",
            href: "/settings/config",
            color: "primary",
            items: ["Wedding date and venue", "RSVP periods and labels", "Guest group settings", "Feature toggles"],
        },
        {
            title: "FAQ Management",
            description: "Create and organize frequently asked questions for your guests",
            icon: "help-circle",
            href: "/settings/faq",
            color: "secondary",
            items: ["Questions and answers", "Helpful tips", "Category organization", "Preview and publish"],
        },
        {
            title: "Deadline Tracking",
            description: "Stay on top of wedding planning tasks with deadline lists",
            icon: "calendar-check",
            href: "/settings/deadline",
            color: "accent",
            items: ["Create deadline lists", "Track task progress", "Set due dates", "Mark completions"],
        },
        {
            title: "Preview Pages",
            description: "Preview how your wedding pages will appear to guests",
            icon: "eye",
            href: "/settings/preview/faq",
            color: "info",
            items: ["FAQ page preview", "RSVP flow preview", "Guest experience view"],
        },
    ];
</script>

<ProtectedPageShell relativeCrumbs={[]}>
    <div class="max-w-6xl mx-auto">
        <!-- Header -->
        <div class="text-center mb-12">
            <h1 class="text-4xl font-bold text-base-content mb-4">Wedding Settings</h1>
            <p class="text-lg text-base-content/70 max-w-2xl mx-auto">
                Manage all aspects of your wedding website from this central hub. Configure settings, organize content,
                and track your planning progress.
            </p>
        </div>

        <!-- Settings Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            {#each sections as section (section.title)}
                <a
                    href={section.href}
                    class="card bg-base-100 border border-base-300 shadow-md hover:shadow-xl transition-all hover:-translate-y-1">
                    <div class="card-body">
                        <!-- Header -->
                        <div class="flex items-start gap-4 mb-4">
                            <div class="rounded-full bg-{section.color}/10 p-3 flex-shrink-0">
                                <Icon name={section.icon} class="size-8 text-{section.color}" />
                            </div>
                            <div class="flex-1">
                                <h2 class="card-title text-xl font-bold text-base-content mb-2">
                                    {section.title}
                                </h2>
                                <p class="text-base-content/70 text-sm">
                                    {section.description}
                                </p>
                            </div>
                        </div>

                        <!-- Features List -->
                        <div class="space-y-2">
                            {#each section.items as item, index (index)}
                                <div class="flex items-center gap-2 text-sm text-base-content/70">
                                    <Icon name="check" class="size-4 text-{section.color} flex-shrink-0" />
                                    <span>{item}</span>
                                </div>
                            {/each}
                        </div>

                        <!-- Action -->
                        <div class="card-actions justify-end mt-4 pt-4 border-t border-base-300">
                            <span class="text-sm font-semibold text-{section.color} flex items-center gap-2">
                                Manage
                                <Icon name="arrow-right" class="size-4" />
                            </span>
                        </div>
                    </div>
                </a>
            {/each}
        </div>

        <!-- Quick Stats -->
        <div class="card bg-gradient-to-r from-primary/10 to-secondary/10 border border-base-300">
            <div class="card-body">
                <h3 class="text-lg font-semibold text-base-content mb-4">Quick Tips</h3>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div class="flex items-start gap-3">
                        <Icon name="lightbulb" class="size-5 text-warning flex-shrink-0 mt-0.5" />
                        <div>
                            <p class="font-semibold text-base-content text-sm">Start with Configuration</p>
                            <p class="text-xs text-base-content/70">Set up your wedding date and RSVP settings first</p>
                        </div>
                    </div>
                    <div class="flex items-start gap-3">
                        <Icon name="lightbulb" class="size-5 text-warning flex-shrink-0 mt-0.5" />
                        <div>
                            <p class="font-semibold text-base-content text-sm">Preview Before Publishing</p>
                            <p class="text-xs text-base-content/70">Use preview pages to see guest experience</p>
                        </div>
                    </div>
                    <div class="flex items-start gap-3">
                        <Icon name="lightbulb" class="size-5 text-warning flex-shrink-0 mt-0.5" />
                        <div>
                            <p class="font-semibold text-base-content text-sm">Stay Organized</p>
                            <p class="text-xs text-base-content/70">Use deadlines to track all planning tasks</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</ProtectedPageShell>
