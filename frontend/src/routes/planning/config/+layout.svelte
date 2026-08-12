<script lang="ts">
    import { page } from "$app/stores";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";

    const { children } = $props();

    const relativeCrumbs = [{ title: "Configuration" }];

    const sections = [
        { title: "General", href: "/planning/config/general", icon: "icon-[lucide--settings]" },
        { title: "Guest List", href: "/planning/config/guest-list", icon: "icon-[lucide--users]" },
        { title: "RSVP", href: "/planning/config/rsvp", icon: "icon-[lucide--calendar-check]" },
        {
            title: "RSVP Questions",
            href: "/planning/config/rsvp-questions",
            icon: "icon-[lucide--circle-help]",
        },
        { title: "Venue", href: "/planning/config/venue", icon: "icon-[lucide--map-pin]" },
        { title: "Maintenance", href: "/planning/config/maintenance", icon: "icon-[lucide--wrench]" },
        { title: "Edit All", href: "/planning/config/edit", icon: "icon-[lucide--square-pen]" },
    ];
</script>

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader
        title="Configuration"
        description="Configure all settings for the wedding platform not found in the planning section" />

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-4">
        <aside class="lg:col-span-3">
            <nav class="menu bg-base-200 text-primary-content border border-base-300 rounded-box p-2 w-full">
                {#each sections as section (section.href)}
                    {@const isActive = $page.url.pathname === section.href}
                    <li>
                        <a href={section.href} class={isActive ? "menu-active" : ""}>
                            <span class={section.icon + " size-4"}></span>
                            {section.title}
                        </a>
                    </li>
                {/each}
            </nav>
        </aside>

        <section class="lg:col-span-9">
            {@render children()}
        </section>
    </div>
</ProtectedPageShell>
