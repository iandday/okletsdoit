<script lang="ts">
    import { enhance } from "$app/forms";
    import { goto } from "$app/navigation";
    import Stats from "$lib/components/Stats.svelte";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import { previewMenu, protectedMenu } from "$lib/components/layouts/Topbar.svelte";
    import { formatCurrency } from "$lib/utils/formatters";
    import type { ActionData, PageData } from "./$types";

    const { data, form }: { data: PageData; form: ActionData } = $props();

    let activeTab = $state(0);
    let isSendingEmail = $state(false);
</script>

<ProtectedPageShell relativeCrumbs={[]}>
    <ProtectedPageHeader
        title="Wedding Planning Hub"
        description="Your central command center for managing every aspect of your special day." />

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <!-- Tabs Navigation -->
        <div class="bg-base-300 py-2 px-4 mb-6">
            <div class="flex gap-2 flex-col lg:flex-row min-w-max justify-between">
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
                                {item.description || `Manage your ${item.title.toLowerCase()} for your wedding.`}
                            </p>
                            {#if item.href == "/planning/budget"}
                                <div class="flex justify-around items-center">
                                    <Stats
                                        size="sm"
                                        class="justify-center flex flex-col sm:flex-row gap-4"
                                        align="center"
                                        objects={[
                                            {
                                                title: "Estimated",
                                                value: formatCurrency(data.budgetEstimated),
                                                description: "Total Budget",
                                            },
                                            {
                                                title: "Spent",
                                                value: formatCurrency(data.budgetActual),
                                                description: "Total Spent",
                                            },
                                        ]} />
                                </div>
                            {/if}
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
        <div class="mt-12">
            <div class="detail-card">
                <div class="detail-card-body">
                    <div class="detail-card-title">
                        <span class="icon-[lucide--bell] size-6"></span>
                        Actions
                    </div>
                    <p></p>
                    <form
                        method="POST"
                        action="?/sendUpdateEmail"
                        use:enhance={() => {
                            isSendingEmail = true;
                            return async ({ update }) => {
                                await update();
                                isSendingEmail = false;
                            };
                        }}>
                        <button type="submit" disabled={isSendingEmail} class="btn btn-accent gap-2">
                            <span class="icon-[lucide--send] size-5"></span>
                            {isSendingEmail ? "Sending..." : "Send Update Email"}
                        </button>
                    </form>

                    {#if form?.success}
                        <div class="alert alert-success mt-4">
                            <span class="icon-[lucide--check-circle] size-5"></span>
                            <span>{form.message} (Task ID: {form.taskId})</span>
                        </div>
                    {:else if form?.error}
                        <div class="alert alert-error mt-4">
                            <span class="icon-[lucide--alert-circle] size-5"></span>
                            <span>{form.error}</span>
                        </div>
                    {/if}
                </div>
            </div>
        </div>
    </div>
</ProtectedPageShell>
