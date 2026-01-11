<script lang="ts">
    import CreateObject from "$lib/components/buttons/CreateObject.svelte";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import type { PageData } from "./$types";

    const { data }: { data: PageData } = $props();
    const relativeCrumbs = [{ title: "Contacts", href: "/settings/contact" }];

    let searchQuery = $state("");

    // Client-side filtering
    const filteredContacts = $derived(
        searchQuery.trim()
            ? data.contacts.filter((contact) => {
                  const query = searchQuery.toLowerCase();
                  return (
                      contact.name?.toLowerCase().includes(query) ||
                      contact.company?.toLowerCase().includes(query) ||
                      contact.email?.toLowerCase().includes(query) ||
                      contact.category?.toLowerCase().includes(query)
                  );
              })
            : data.contacts,
    );
</script>

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader title="Contacts" description="Manage your wedding contacts and vendors">
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-8">
            <!-- Search Input -->
            <div class="flex-1 max-w-md">
                <div class="join w-full">
                    <input
                        type="search"
                        placeholder="Search contacts..."
                        class="edit-card-field-input join-item flex-1"
                        bind:value={searchQuery} />
                    {#if searchQuery}
                        <button type="button" onclick={() => (searchQuery = "")} class="btn btn-ghost join-item">
                            <span class="icon-[lucide--x] size-5"></span>
                        </button>
                    {/if}
                </div>
            </div>
            <CreateObject href="/settings/contact/new" label="New Contact" />
        </div>
    </ProtectedPageHeader>

    {#if data.contacts.length === 0}
        <!-- Empty State -->
        <div class="card bg-base-100 border border-base-300 shadow-lg">
            <div class="card-body items-center text-center py-16">
                <span class="icon-[lucide--users] size-16 text-base-content/30 mb-4"></span>
                <h3 class="text-xl font-semibold text-base-content mb-2">No contacts yet</h3>
                <p class="text-base-content/70 mb-6 max-w-md">
                    Create your first contact to start organizing vendors, guests, and other important people for your
                    wedding.
                </p>
                <a href="/settings/contact/new" class="btn btn-primary gap-2">
                    <span class="icon-[lucide--plus] size-5"></span>
                    Create First Contact
                </a>
            </div>
        </div>
    {:else}
        <!-- Contacts List -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {#each filteredContacts as contact (contact.id)}
                <div class="list-card">
                    <div class="list-card-body">
                        <div class="list-card-title flex items-start justify-between mb-4">
                            <div class="flex-1">
                                <h3 class="text-xl font-semibold mb-1">
                                    <a href="/settings/contact/{contact.id}" class="link link-hover">
                                        {#if contact.name}
                                            {contact.name}
                                            {#if contact.company}
                                                <span>({contact.company})</span>
                                            {/if}
                                        {:else if contact.company}
                                            {contact.company}
                                        {/if}
                                    </a>
                                </h3>
                                {#if contact.category}
                                    <div class="badge badge-accent mb-2">{contact.category}</div>
                                {/if}
                            </div>
                            <div class="flex gap-2">
                                <a href="/settings/contact/{contact.id}/edit" class="btn btn-sm btn-ghost">
                                    <span class="icon-[lucide--pencil] size-4"></span>
                                </a>
                            </div>
                        </div>

                        <div class="grid grid-cols-1 gap-4 mb-4">
                            {#if contact.email}
                                <div class="flex items-center gap-2 text-sm">
                                    <span class="icon-[lucide--mail] size-4 list-card-item"></span>
                                    <a href="mailto:{contact.email}" class="link link-hover">{contact.email}</a>
                                </div>
                            {/if}
                            {#if contact.phone}
                                <div class="flex items-center gap-2 text-sm">
                                    <span class="icon-[lucide--phone] size-4 list-card-item"></span>
                                    <a href="tel:{contact.phone}" class="link link-hover">{contact.phone}</a>
                                </div>
                            {/if}
                            {#if contact.website}
                                <div class="flex items-center gap-2 text-sm">
                                    <span class="icon-[lucide--globe] size-4 list-card-item"></span>
                                    <a
                                        href={contact.website}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        class="link link-hover">
                                        {contact.website}
                                    </a>
                                </div>
                            {/if}
                        </div>

                        {#if contact.notes}
                            <div class="text-sm list-card-item mb-4">
                                <p class="whitespace-pre-wrap">{contact.notes}</p>
                            </div>
                        {/if}

                        <!-- Attachments Section -->
                        {#if contact.attachments && contact.attachments.length > 0}
                            <div class="divider my-4">Attachments ({contact.attachments.length})</div>
                            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
                                {#each contact.attachments as attachment (attachment.id)}
                                    <div class="flex items-center gap-2 p-3 bg-base-200 rounded-lg">
                                        <span class="icon-[lucide--file] size-5 list-card-item"></span>
                                        <div class="flex-1 min-w-0">
                                            <p class="text-sm font-medium truncate">
                                                {attachment.name || attachment.filename}
                                            </p>
                                            {#if attachment.description}
                                                <p class="text-xs text-base-content/60 truncate">
                                                    {attachment.description}
                                                </p>
                                            {/if}
                                        </div>
                                        <a
                                            href={attachment.fileUrl}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            class="btn btn-xs"
                                            title="View attachment">
                                            <span class="icon-[lucide--eye] size-4 list-card-item"></span>
                                        </a>
                                    </div>
                                {/each}
                            </div>
                        {/if}
                    </div>
                </div>
            {/each}
        </div>
    {/if}
</ProtectedPageShell>
