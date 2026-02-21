<script lang="ts">
    import { goto } from "$app/navigation";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";

    let activeTab = $state(0);

    const adminSections = [
        {
            title: "Configuration",
            icon: "icon-[lucide--settings]",
            href: "/admin/config",
            description:
                "Manage system settings, application configuration, and site preferences. Control how your wedding planning platform behaves.",
        },
        {
            title: "Data Import",
            icon: "icon-[lucide--upload]",
            href: "/admin/import",
            description:
                "Import guest lists, vendor information, and other data from external sources. Supports CSV, Excel, and other common formats.",
        },
        {
            title: "Data Export",
            icon: "icon-[lucide--download]",
            href: "/admin/export",
            description:
                "Export your guest lists, contacts, and other data for backup or external use. Generate reports and download data in various formats.",
        },
    ];
</script>

<ProtectedPageShell relativeCrumbs={[]}>
    <ProtectedPageHeader
        title="Administration"
        description="System administration tools for managing configuration, data import, and data export." />

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <!-- Tabs Navigation -->
        <div class="bg-base-300 py-2 px-4 mb-6 overflow-x-auto">
            <div class="flex gap-2 min-w-max justify-between">
                {#each adminSections as section, index (section.title)}
                    <button
                        onclick={() => (activeTab = index)}
                        class="btn btn-sm rounded-lg transition-all duration-200 {activeTab === index
                            ? 'btn-accent'
                            : 'btn-secondary'}"
                        class:scale-105={activeTab === index}>
                        <span class="{section.icon} size-5"></span>
                        {section.title}
                    </button>
                {/each}
            </div>
        </div>

        <!-- Tab Content -->
        <div class="grid grid-cols-1 gap-6">
            {#each adminSections as section, index (section.title)}
                {#if activeTab === index}
                    <div class="config-card animate-fade-in">
                        <div class="config-card-body">
                            <div class="config-card-title">{section.title}</div>
                            <p>{section.description}</p>
                        </div>
                        <div class="config-card-actions">
                            <button onclick={() => goto(section.href)} class="btn btn-accent btn-lg gap-2">
                                <span class="{section.icon} size-5"></span>
                                Open {section.title}
                                <span class="icon-[lucide--arrow-right] size-5"></span>
                            </button>
                        </div>
                    </div>
                {/if}
            {/each}
        </div>

        <!-- Admin Information -->
        <div class="mt-12">
            <div class="detail-card">
                <div class="detail-card-body">
                    <div class="detail-card-title">
                        <span class="icon-[lucide--shield-check] size-6"></span>
                        Administrator Tools
                    </div>
                    <p class="mb-4">
                        These tools provide powerful administrative capabilities for managing your wedding planning
                        platform. Use caution when making changes to system configuration or performing bulk data
                        operations.
                    </p>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div class="card bg-base-200 border border-base-300">
                            <div class="card-body">
                                <div class="flex items-center gap-2 mb-2">
                                    <span class="icon-[lucide--settings] size-5 text-accent"></span>
                                    <h3 class="font-semibold">Configuration</h3>
                                </div>
                                <p class="text-sm opacity-80">
                                    Manage application settings, feature flags, and system preferences.
                                </p>
                            </div>
                        </div>
                        <div class="card bg-base-200 border border-base-300">
                            <div class="card-body">
                                <div class="flex items-center gap-2 mb-2">
                                    <span class="icon-[lucide--upload] size-5 text-info"></span>
                                    <h3 class="font-semibold">Import Data</h3>
                                </div>
                                <p class="text-sm opacity-80">
                                    Bulk import guests, contacts, and other data from spreadsheets.
                                </p>
                            </div>
                        </div>
                        <div class="card bg-base-200 border border-base-300">
                            <div class="card-body">
                                <div class="flex items-center gap-2 mb-2">
                                    <span class="icon-[lucide--download] size-5 text-success"></span>
                                    <h3 class="font-semibold">Export Data</h3>
                                </div>
                                <p class="text-sm opacity-80">
                                    Generate reports and export data for backup or external analysis.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</ProtectedPageShell>
