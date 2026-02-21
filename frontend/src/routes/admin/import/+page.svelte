<script lang="ts">
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
</script>

<ProtectedPageShell relativeCrumbs={[{ label: "Administration", href: "/admin" }]}>
    <ProtectedPageHeader
        title="Data Import"
        description="Import guest lists, contacts, and other data from external sources." />

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="detail-card">
            <div class="detail-card-body">
                <div class="detail-card-title">
                    <span class="icon-[lucide--upload] size-6"></span>
                    Import Tools
                </div>
                <p class="mb-6">
                    Use these tools to import data from spreadsheets and other external sources. Supported formats
                    include CSV and Excel (XLSX).
                </p>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="card bg-base-200 border border-base-300">
                        <div class="card-body">
                            <div class="flex items-center gap-2 mb-2">
                                <span class="icon-[lucide--users] size-5 text-accent"></span>
                                <h3 class="font-semibold">Import Guests</h3>
                            </div>
                            <p class="text-sm opacity-80 mb-4">
                                Import guest information including names, contact details, and preferences.
                            </p>
                            <button class="btn btn-accent btn-sm gap-2" disabled>
                                <span class="icon-[lucide--upload] size-4"></span>
                                Coming Soon
                            </button>
                        </div>
                    </div>

                    <div class="card bg-base-200 border border-base-300">
                        <div class="card-body">
                            <div class="flex items-center gap-2 mb-2">
                                <span class="icon-[lucide--users-round] size-5 text-info"></span>
                                <h3 class="font-semibold">Import Guest Groups</h3>
                            </div>
                            <p class="text-sm opacity-80 mb-4">
                                Import guest groups with addresses and RSVP information.
                            </p>
                            <button class="btn btn-info btn-sm gap-2" disabled>
                                <span class="icon-[lucide--upload] size-4"></span>
                                Coming Soon
                            </button>
                        </div>
                    </div>

                    <div class="card bg-base-200 border border-base-300">
                        <div class="card-body">
                            <div class="flex items-center gap-2 mb-2">
                                <span class="icon-[lucide--contact] size-5 text-success"></span>
                                <h3 class="font-semibold">Import Contacts</h3>
                            </div>
                            <p class="text-sm opacity-80 mb-4">Import vendor and contact information.</p>
                            <button class="btn btn-success btn-sm gap-2" disabled>
                                <span class="icon-[lucide--upload] size-4"></span>
                                Coming Soon
                            </button>
                        </div>
                    </div>

                    <div class="card bg-base-200 border border-base-300">
                        <div class="card-body">
                            <div class="flex items-center gap-2 mb-2">
                                <span class="icon-[lucide--file-spreadsheet] size-5 text-warning"></span>
                                <h3 class="font-semibold">Template Downloads</h3>
                            </div>
                            <p class="text-sm opacity-80 mb-4">Download CSV/Excel templates for data import.</p>
                            <button class="btn btn-warning btn-sm gap-2" disabled>
                                <span class="icon-[lucide--download] size-4"></span>
                                Coming Soon
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</ProtectedPageShell>
