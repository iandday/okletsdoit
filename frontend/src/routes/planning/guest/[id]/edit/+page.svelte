<script lang="ts">
    import { enhance } from "$app/forms";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import type { ActionData, PageData } from "./$types";

    const { data, form }: { data: PageData; form: ActionData } = $props();

    const relativeCrumbs = $derived([
        { title: "Guest List", href: "/settings/guest_list" },
        ...(data.guestGroup
            ? [
                  {
                      title: data.guestGroup.name || "Guest Group",
                      href: `/settings/guest_list/${data.guestGroup.id}`,
                  },
              ]
            : []),
        {
            title: `${data.guest.firstName} ${data.guest.lastName}`,
            href: `/settings/guest/${data.guest.id}`,
        },
        { title: "Edit", href: `/settings/guest/${data.guest.id}/edit` },
    ]);
</script>

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader title="Edit Guest" description="Update the details of this guest" />
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
                    <h3 class="text-lg font-semibold mb-4">Basic Information</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="firstName">
                                <span>First Name</span>
                            </label>
                            <input
                                type="text"
                                id="firstName"
                                name="firstName"
                                class="edit-card-field-input"
                                value={data.guest.firstName || ""}
                                autofocus />
                        </div>

                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="lastName">
                                <span>Last Name</span>
                            </label>
                            <input
                                type="text"
                                id="lastName"
                                name="lastName"
                                class="edit-card-field-input"
                                value={data.guest.lastName || ""} />
                        </div>

                        <div class="form-control w-full">
                            <label class="label cursor-pointer justify-start gap-4">
                                <input
                                    type="checkbox"
                                    name="plusOne"
                                    class="checkbox checkbox-primary"
                                    checked={data.guest.plusOne} />
                                <span class="edit-card-field-name">Plus One</span>
                            </label>
                            <span class="text-sm text-base-content/70 mt-1">
                                Check if this is a +1 guest (names optional)
                            </span>
                        </div>
                    </div>

                    <div class="divider"></div>

                    <h3 class="text-lg font-semibold mb-4">Status & Invitations</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="form-control w-full">
                            <label class="label cursor-pointer justify-start gap-4">
                                <input
                                    type="checkbox"
                                    name="isInvited"
                                    class="checkbox checkbox-info"
                                    checked={data.guest.isInvited} />
                                <span class="edit-card-field-name">Invited</span>
                            </label>
                        </div>
                    </div>

                    <div class="divider"></div>

                    <h3 class="text-lg font-semibold mb-4">Special Requirements</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="form-control w-full">
                            <label class="label cursor-pointer justify-start gap-4">
                                <input
                                    type="checkbox"
                                    name="vip"
                                    class="checkbox checkbox-secondary"
                                    checked={data.guest.vip} />
                                <span class="edit-card-field-name">VIP Guest</span>
                            </label>
                        </div>

                        <div class="form-control w-full">
                            <label class="label cursor-pointer justify-start gap-4">
                                <input
                                    type="checkbox"
                                    name="accommodation"
                                    class="checkbox checkbox-accent"
                                    checked={data.guest.accommodation} />
                                <span class="edit-card-field-name">Needs Accommodation</span>
                            </label>
                        </div>
                    </div>

                    <div class="divider"></div>

                    <h3 class="text-lg font-semibold mb-4">Notes</h3>
                    <div class="form-control w-full">
                        <label class="edit-card-field-name" for="notes">
                            <span>Notes</span>
                        </label>
                        <textarea
                            id="notes"
                            name="notes"
                            class="textarea textarea-bordered min-h-24"
                            placeholder="Any additional notes about this guest">{data.guest.notes || ""}</textarea>
                    </div>

                    <div class="divider"></div>

                    <div class="flex justify-end gap-4 mt-6">
                        <a href="/settings/guest/{data.guest.id}" class="btn btn-ghost">Cancel</a>
                        <button type="submit" class="btn btn-primary">
                            <span class="icon-[lucide--save] size-4"></span>
                            Save Changes
                        </button>
                    </div>
                </div>
            </div>
        </form>

        {#if data.guestGroup}
            <div class="mt-6 text-sm text-base-content/70">
                <p>
                    This guest belongs to:
                    <a href="/settings/guest_list/{data.guestGroup.id}" class="link link-primary link-hover">
                        {data.guestGroup.name}
                    </a>
                </p>
            </div>
        {/if}
    </div>
</ProtectedPageShell>
