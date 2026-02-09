<script lang="ts">
    import { goto } from "$app/navigation";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import { previewMenu, protectedMenu } from "$lib/components/layouts/Topbar.svelte";

    let activeTab = $state(0);

    const descriptions: Record<string, string> = {
        Contacts: "Manage your wedding contacts, vendors, guests, and important people.",
        FAQ: "Create and organize frequently asked questions for your wedding website.",
        Deadlines: "Track important dates and milestones leading up to your big day.",
        Lists: "Organize tasks, checklists, and to-do items for your wedding planning.",
        Budget: "Monitor expenses, set budgets, and track spending across all wedding categories.",
        "Guest List": "Manage your guest list, RSVPs, meal preferences, and seating arrangements.",
        Inspiration: "Save and organize inspiration photos, ideas, and references for your wedding.",
        Ideas: "Brainstorm and capture creative ideas for your wedding celebration.",
        Timeline: "Create and visualize your wedding day timeline and schedule.",
        Settings: "Configure your wedding website settings, theme, and preferences.",
    };
</script>

<ProtectedPageShell relativeCrumbs={[]}>
    <ProtectedPageHeader
        title="Wedding Planning Hub"
        description="Your central command center for managing every aspect of your special day." />

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <!-- Tabs Navigation -->
        <div class="bg-base-300 py-2 px-4 mb-6 overflow-x-auto">
            <div class="flex gap-2 min-w-max justify-between">
                {#each protectedMenu as item, index (item.title)}
                    <button
                        onclick={() => (activeTab = index)}
                        class="btn btn-sm rounded-lg transition-all duration-200 {activeTab === index
                            ? 'btn-accent'
                            : 'btn-secondary'}"
                        class:scale-105={activeTab === index}>
                        <span class="{item.icon} size-5"></span>
                        {item.title}
                    </button>
                {/each}
            </div>
        </div>

        <!-- Tab Content -->
        <div class="grid grid-cols-1 gap-6">
            {#each protectedMenu as item, index (item.title)}
                {#if activeTab === index}
                    <div class="config-card animate-fade-in">
                        <div class="config-card-body">
                            <div class="config-card-title">{item.title}</div>
                            <p>
                                {descriptions[item.title] ||
                                    `Manage your ${item.title.toLowerCase()} for your wedding.`}
                            </p>
                        </div>
                        <div class="config-card-actions">
                            <button onclick={() => goto(item.href)} class="btn btn-accent btn-lg gap-2">
                                <span class="{item.icon} size-5"></span>
                                Open {item.title}
                                <span class="icon-[lucide--arrow-right] size-5"></span>
                            </button>
                        </div>
                    </div>
                {/if}
            {/each}
        </div>

        <!-- Preview Section -->
        {#if previewMenu && previewMenu.length > 0}
            <div class="mt-12">
                <div class="detail-card">
                    <div class="detail-card-body">
                        <div class="detail-card-title">
                            <span class="icon-[lucide--layout-template] size-6"></span>
                            Website Previews
                        </div>
                        <p>
                            See how your wedding website looks to your guests. Preview different pages and sections
                            before making them live.
                        </p>
                        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                            {#each previewMenu as preview, index (preview.title)}
                                <a href={preview.href} class="btn btn-secondary gap-2 justify-center" target="_blank">
                                    <span class="icon-[lucide--external-link] size-4"></span>
                                    {preview.title}
                                </a>
                            {/each}
                        </div>
                    </div>
                </div>
            </div>
        {/if}
    </div>
</ProtectedPageShell>

<style>
    @keyframes fade-in {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .animate-fade-in {
        animation: fade-in 0.3s ease-out;
    }
</style>
