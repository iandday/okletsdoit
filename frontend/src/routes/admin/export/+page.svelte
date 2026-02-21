<script lang="ts">
    import ExportData from "$lib/components/buttons/ExportData.svelte";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
</script>

<ProtectedPageShell relativeCrumbs={[{ label: "Administration", href: "/admin" }]}>
    <ProtectedPageHeader title="Data Export" description="Export your data for backup, analysis, or external use." />

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="detail-card">
            <div class="detail-card-body">
                <div class="detail-card-title">
                    <span class="icon-[lucide--download] size-6"></span>
                    Export Tools
                </div>
                <p class="mb-6">
                    Export your data in CSV or Excel format for backup, analysis, or use in external applications. All
                    exports include data from non-deleted records only.
                </p>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <!-- Guest Export -->
                    <div class="card bg-base-200 border border-base-300">
                        <div class="card-body">
                            <div class="flex items-center gap-2 mb-2">
                                <span class="icon-[lucide--users] size-5 text-accent"></span>
                                <h3 class="font-semibold text-lg">Export Guests</h3>
                            </div>
                            <p class="text-sm opacity-80 mb-4">
                                Export all guest information including names, RSVP status, dietary preferences, and
                                associated group details.
                            </p>
                            <div class="flex gap-2">
                                <ExportData
                                    resourceType="guest"
                                    format="csv"
                                    label="Export CSV"
                                    fileName="guests_export.csv" />
                                <ExportData
                                    resourceType="guest"
                                    format="xlsx"
                                    label="Export Excel"
                                    fileName="guests_export.xlsx" />
                            </div>
                        </div>
                    </div>

                    <!-- Guest Group Export -->
                    <div class="card bg-base-200 border border-base-300">
                        <div class="card-body">
                            <div class="flex items-center gap-2 mb-2">
                                <span class="icon-[lucide--users-round] size-5 text-info"></span>
                                <h3 class="font-semibold text-lg">Export Guest Groups</h3>
                            </div>
                            <p class="text-sm opacity-80 mb-4">
                                Export guest group information including addresses, RSVP codes, and group statistics
                                (invited, attending, declined counts).
                            </p>
                            <div class="flex gap-2">
                                <ExportData
                                    resourceType="guest_group"
                                    format="csv"
                                    label="Export CSV"
                                    fileName="guest_groups_export.csv" />
                                <ExportData
                                    resourceType="guest_group"
                                    format="xlsx"
                                    label="Export Excel"
                                    fileName="guest_groups_export.xlsx" />
                            </div>
                        </div>
                    </div>

                    <!-- Future Export Options -->
                    <div class="card bg-base-200 border border-base-300">
                        <div class="card-body">
                            <div class="flex items-center gap-2 mb-2">
                                <span class="icon-[lucide--contact] size-5 text-success"></span>
                                <h3 class="font-semibold text-lg">Export Contacts</h3>
                            </div>
                            <p class="text-sm opacity-80 mb-4">
                                Export vendor and contact information including addresses and communication details.
                            </p>
                            <button class="btn btn-success btn-sm gap-2" disabled>
                                <span class="icon-[lucide--download] size-4"></span>
                                Coming Soon
                            </button>
                        </div>
                    </div>

                    <div class="card bg-base-200 border border-base-300">
                        <div class="card-body">
                            <div class="flex items-center gap-2 mb-2">
                                <span class="icon-[lucide--file-text] size-5 text-warning"></span>
                                <h3 class="font-semibold text-lg">Export Reports</h3>
                            </div>
                            <p class="text-sm opacity-80 mb-4">
                                Generate comprehensive reports with custom fields and filtering options.
                            </p>
                            <button class="btn btn-warning btn-sm gap-2" disabled>
                                <span class="icon-[lucide--download] size-4"></span>
                                Coming Soon
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Export Information -->
        <div class="mt-6">
            <div class="alert alert-info">
                <span class="icon-[lucide--info] size-5"></span>
                <div>
                    <h4 class="font-semibold">Export Information</h4>
                    <ul class="text-sm list-disc list-inside mt-1">
                        <li>CSV exports are compatible with most spreadsheet applications</li>
                        <li>Excel exports preserve formatting and include all data types</li>
                        <li>Boolean values are displayed as "Yes" or "No" for readability</li>
                        <li>Only non-deleted records are included in exports</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</ProtectedPageShell>
