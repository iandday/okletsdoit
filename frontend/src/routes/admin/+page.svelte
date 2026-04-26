<script lang="ts">
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
</script>

<ProtectedPageShell relativeCrumbs={[]}>
    <ProtectedPageHeader
        title="Administrator Tools"
        description="These tools provide powerful administrative capabilities for managing your wedding planning
                        platform. Use caution when making changes to system configuration or performing bulk data
                        operations." />

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <!-- Admin Information -->
        <div class="mt-12">
            <div class="detail-card">
                <div class="detail-card-body">
                    <div class="detail-card-title">
                        <span class="icon-[lucide--shield-check] size-6"></span>
                        Administrator Tools
                    </div>
                    <p class="mb-4"></p>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div class="card bg-base-200 border border-base-300">
                            <div class="card-body">
                                <div class="flex items-center gap-2 mb-2">
                                    <span class="icon-[lucide--settings] size-5 text-accent"></span>
                                    <a href="/admin/config"><h3 class="font-semibold">Configuration</h3></a>
                                </div>
                                <p class="text-sm opacity-80">
                                    Manage application settings, feature flags, and system preferences.
                                </p>
                            </div>
                        </div>

                        <div class="card bg-base-200 border border-base-300">
                            <div class="card-body">
                                <a href="/admin/import"
                                    ><div class="card-title flex items-center gap-2 mb-2">
                                        <span class="icon-[lucide--upload] size-5 text-info"></span>
                                        <h3 class="font-semibold">Import Data</h3>
                                    </div></a>
                                <p class="text-sm opacity-80">
                                    Bulk import guests, contacts, and other data from spreadsheets.
                                </p>
                            </div>
                        </div>

                        <div class="card bg-base-200 border border-base-300">
                            <div class="card-body">
                                <div class="flex items-center gap-2 mb-2">
                                    <span class="icon-[lucide--download] size-5 text-success"></span>
                                    <a href="/admin/export"><h3 class="font-semibold">Export Data</h3></a>
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
