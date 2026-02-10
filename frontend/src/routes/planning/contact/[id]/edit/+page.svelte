<script lang="ts">
    import { enhance } from "$app/forms";
    import Icon from "$lib/components/Icon.svelte";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import type { ActionData, PageData } from "./$types";

    const { data, form }: { data: PageData; form: ActionData } = $props();

    const relativeCrumbs = [
        { title: "Contacts", href: "/planning/contact" },
        {
            title: data.contact.name || data.contact.company || "Contact",
            href: `/planning/contact/${data.contact.id}`,
        },
        { title: "Edit", href: `/planning/contact/${data.contact.id}/edit` },
    ];
</script>

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader title="Edit Contact" description="Update the details of your contact" />
    <div class="container mx-auto p-4 max-w-6xl">
        {#if form?.error}
            <div class="alert alert-error mb-4">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="stroke-current shrink-0 h-6 w-6"
                    fill="none"
                    viewBox="0 0 24 24">
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>{form.error}</span>
            </div>
        {/if}

        <form method="POST" use:enhance>
            <div class="config-card">
                <div class="config-card-body">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="name">
                                <span>Name</span>
                            </label>
                            <input
                                type="text"
                                id="name"
                                name="name"
                                class="edit-card-field-input"
                                value={data.contact.name || ""}
                                autofocus />
                            <span class="text-sm text-base-content/70 mt-1">Either name or company is required</span>
                        </div>

                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="company">
                                <span>Company</span>
                            </label>
                            <input
                                type="text"
                                id="company"
                                name="company"
                                class="edit-card-field-input"
                                value={data.contact.company || ""} />
                        </div>

                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="category">
                                <span>Category</span>
                            </label>
                            <input
                                type="text"
                                id="category"
                                name="category"
                                class="edit-card-field-input"
                                value={data.contact.category || ""}
                                placeholder="e.g., Vendor, Guest, Venue" />
                        </div>

                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="email">
                                <span>Email</span>
                            </label>
                            <input
                                type="email"
                                id="email"
                                name="email"
                                class="edit-card-field-input"
                                value={data.contact.email || ""} />
                        </div>

                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="phone">
                                <span>Phone</span>
                            </label>
                            <input
                                type="tel"
                                id="phone"
                                name="phone"
                                class="edit-card-field-input"
                                value={data.contact.phone || ""} />
                        </div>

                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="website">
                                <span>Website</span>
                            </label>
                            <input
                                type="url"
                                id="website"
                                name="website"
                                class="edit-card-field-input"
                                value={data.contact.website || ""}
                                placeholder="https://" />
                        </div>
                    </div>

                    <div class="form-control w-full mt-4">
                        <label class="edit-card-field-name" for="notes">
                            <span>Notes</span>
                        </label>
                        <textarea id="notes" name="notes" class="edit-card-field-textarea" rows="4"
                            >{data.contact.notes || ""}</textarea>
                    </div>
                </div>
            </div>

            <div class="flex gap-4 mt-6 justify-end">
                <a href="/planning/contact/{data.contact.id}" class="btn btn-error">Cancel</a>
                <button type="submit" class="btn btn-primary gap-2">
                    <Icon name="save" class="size-5" />
                    Save Changes
                </button>
            </div>
        </form>
    </div>
</ProtectedPageShell>
