<script lang="ts">
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import { previewMenu, protectedMenu } from "$lib/components/layouts/Topbar.svelte";

    const sections = [
        {
            title: "Wedding Configuration",
            icon: "settings",
            href: "/planning/config",
        },
        {
            title: "FAQ Management",
            icon: "help-circle",
            href: "/planning/faq",
        },
        {
            title: "Deadline Tracking",
            icon: "calendar-check",
            href: "/planning/deadline",
        },
        {
            title: "Lists Management",
            icon: "check-square",
            href: "/planning/list",
        },
        {
            title: "Guest List Management",
            icon: "users",
            href: "/planning/guest_list",
        },
        {
            title: "Preview Pages",
            icon: "eye",
            href: "/planning/preview/faq",
        },
        {
            title: "Contacts Management",
            icon: "book-user",
            href: "/planning/contact",
        },
        {
            title: "Timeline",
            icon: "timeline",
            href: "/planning/timeline",
        },
        {
            title: "Inspiration",
            icon: "lightbulb",
            href: "/planning/inspiration",
        },
        {
            title: "Budget",
            icon: "dollar-sign",
            href: "/planning/expense",
        },
    ];
</script>

<ProtectedPageShell relativeCrumbs={[]}>
    <ProtectedPageHeader
        title="Wedding Planning"
        description="Manage all aspects of your wedding from this central hub. Configure settings, organize content, and track your planning progress." />
    <div class="max-w-6xl mx-auto">
        <div class="join gap-2">
            {#each protectedMenu as section (section.title)}
                <a href={section.href} class="btn btn-accent join-item"
                    ><span class="{section.icon} size-6"></span>{section.title}</a>
            {/each}
        </div>
    </div>
</ProtectedPageShell>
