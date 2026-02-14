<script lang="ts">
    import { enhance } from "$app/forms";
    import Icon from "$lib/components/Icon.svelte";
    import DeleteObject from "$lib/components/buttons/DeleteObject.svelte";
    import ViewDetails from "$lib/components/buttons/ViewDetails.svelte";
    import ObjectChildItems from "$lib/components/object/ObjectChildItems.svelte";
    import ObjectDetail from "$lib/components/object/ObjectDetail.svelte";
    import type { PageData } from "./$types";

    const { data }: { data: PageData } = $props();

    const relativeCrumbs = $derived([
        { title: "Guest List", href: "/planning/guest_list" },
        { title: data.guestGroup.name || "Guest Group", href: `/planning/guest_list/${data.guestGroup.id}` },
    ]);

    const displayName = $derived(data.guestGroup.name || "Guest Group");

    let showAddForm = $state(false);
    let submitting = $state(false);
</script>

<ObjectDetail
    {relativeCrumbs}
    title={displayName}
    editLink={`/planning/guest_list/${data.guestGroup.id}/edit`}
    deleteAction="?/delete"
    object={data.guestGroup}>
    {#snippet mainSnippet()}
        <div class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <div class="detail-card-field-name">Name</div>
                    <div class="detail-card-field-value">{data.guestGroup.name}</div>
                </div>
                <div>
                    <div class="detail-card-field-name">Relationship</div>
                    <div class="detail-card-field-value">
                        {data.guestGroup.associatedWithFirstName}'s {data.guestGroup.relationshipDisplay}
                    </div>
                </div>
                <div>
                    <div class="detail-card-field-name">Priority</div>
                    <div class="detail-card-field-value">
                        <span class="badge badge-secondary">{data.guestGroup.priorityDisplay}</span>
                    </div>
                </div>

                <div>
                    <div class="detail-card-field-name">RSVP Code</div>
                    <div class="detail-card-field-value font-mono">{data.guestGroup.rsvpCode}</div>
                </div>

                <div>
                    <div class="detail-card-field-name">Email</div>
                    <div class="detail-card-field-value flex items-center gap-2">
                        <span class="icon-[lucide--mail] size-4"></span>
                        {#if data.guestGroup.email}
                            <a href="mailto:{data.guestGroup.email}" class="link link-accent"
                                >{data.guestGroup.email}</a>
                        {:else}
                            Not Provided
                        {/if}
                    </div>
                </div>

                <div>
                    <div class="detail-card-field-name">Phone</div>
                    <div class="detail-card-field-value flex items-center gap-2">
                        <span class="icon-[lucide--phone] size-4"></span>
                        {#if data.guestGroup.phone}
                            <a href="tel:{data.guestGroup.phone}" class="link link-accent">{data.guestGroup.phone}</a>
                        {:else}
                            <span>Not Provided</span>
                        {/if}
                    </div>
                </div>

                {#if data.guestGroup.address || data.guestGroup.city || data.guestGroup.state || data.guestGroup.zipCode || data.guestGroup.addressName}
                    <div>
                        <div class="detail-card-field-name">Address</div>

                        <div class="detail-card-field-value">{data.guestGroup.addressName || "Undefined"}</div>
                        <div class="detail-card-field-value">{data.guestGroup.address}</div>
                        {#if data.guestGroup.addressTwo}
                            <div class="detail-card-field-value">{data.guestGroup.addressTwo}</div>
                        {/if}
                        <div class="detail-card-field-value">
                            {data.guestGroup.city}, {data.guestGroup.state}
                            {data.guestGroup.zipCode}
                        </div>
                    </div>
                {/if}
                <div>
                    <div class="detail-card-field-name">RSVP URL</div>
                    <div class="detail-card-field-value">
                        <a
                            href={data.guestGroup.rsvpUrl}
                            class="link link-accent"
                            target="_blank"
                            rel="noopener noreferrer">
                            {data.guestGroup.rsvpUrl}
                        </a>
                    </div>

                    <img src={data.guestGroup.qrCodeUrl} alt="RSVP QR Code" class="mt-4 w-48 h-48 object-contain" />
                </div>
            </div>
            {#if data.guestGroup.notes}
                <div>
                    <h3 class="text-lg font-semibold mb-3">Notes</h3>
                    <div class="detail-card-field-value whitespace-pre-wrap bg-base-200 p-4 rounded-lg">
                        {data.guestGroup.notes}
                    </div>
                </div>
            {/if}
        </div>
    {/snippet}
    {#snippet mainActionsSnippet()}
        <div>
            <div class="flex items-center justify-between mb-4">
                <button type="button" onclick={() => (showAddForm = !showAddForm)} class="btn btn-sm btn-accent gap-2">
                    <span class="{showAddForm ? 'icon-[lucide--x]' : 'icon-[lucide--plus]'} size-4"></span>
                    {showAddForm ? "Cancel" : "Add Guest"}
                </button>
            </div>

            {#if showAddForm}
                <form
                    method="POST"
                    action="?/addGuest"
                    class="edit-card p-6 mb-6"
                    use:enhance={() => {
                        submitting = true;
                        return async ({ update }) => {
                            await update(); // Automatically invalidates load function after successful action
                            submitting = false;
                            showAddForm = false;
                        };
                    }}>
                    <div class="edit-card-body">
                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="guest-first-name">
                                <span>First Name</span>
                            </label>
                            <input
                                type="text"
                                id="guest-first-name"
                                name="firstName"
                                class="edit-card-field-input"
                                placeholder="Guest first name"
                                disabled={submitting} />
                        </div>
                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="guest-last-name">
                                <span>Last Name</span>
                            </label>
                            <input
                                type="text"
                                id="guest-last-name"
                                name="lastName"
                                class="edit-card-field-input"
                                placeholder="Guest last name"
                                disabled={submitting} />
                        </div>

                        <div class="form-control">
                            <label class="cursor-pointer label">
                                <span class="edit-card-field-name">+1 for {data.guestGroup.name}</span>
                                <input
                                    type="checkbox"
                                    name="plusOne"
                                    class="edit-card-field-toggle"
                                    disabled={submitting} />
                            </label>
                        </div>
                        {#if data.configData?.rsvpShowAccommodationIntro}
                            <div class="form-control">
                                <label class="cursor-pointer label">
                                    <span class="edit-card-field-name">
                                        ({data.configData?.accommodationGroupLabel}) Guest
                                    </span>
                                    <input
                                        type="checkbox"
                                        name="accommodation"
                                        class="edit-card-field-toggle"
                                        disabled={submitting} />
                                </label>
                            </div>
                        {/if}
                        {#if data.configData?.rsvpShowVipIntro}
                            <div class="form-control">
                                <label class="cursor-pointer label">
                                    <span class="edit-card-field-name">
                                        {data.configData?.vipGroupLabel} Guest
                                    </span>
                                    <input
                                        type="checkbox"
                                        name="vip"
                                        class="edit-card-field-toggle"
                                        disabled={submitting} />
                                </label>
                            </div>
                        {/if}
                        <div class="form-control">
                            <label class="cursor-pointer label">
                                <span class="edit-card-field-name"> Invited Guest </span>
                                <input
                                    type="checkbox"
                                    name="invited"
                                    class="edit-card-field-toggle"
                                    disabled={submitting} />
                            </label>
                        </div>
                        <div class="flex gap-2 justify-end">
                            <button
                                type="button"
                                class="btn btn-error"
                                onclick={() => (showAddForm = false)}
                                disabled={submitting}>
                                Cancel
                            </button>
                            <button type="submit" class="btn btn-success gap-2" disabled={submitting}>
                                {#if submitting}
                                    <span class="loading loading-spinner loading-sm"></span>
                                    Adding...
                                {:else}
                                    <span class="icon-[lucide--plus] size-4"></span>
                                    Add
                                {/if}
                            </button>
                        </div>
                    </div>
                </form>
            {/if}
        </div>
    {/snippet}
    {#snippet extraCardsSnippet()}
        <div>
            <ObjectChildItems showTitle={false}>
                {#if data.guests.length === 0}
                    {#if !showAddForm}
                        <p class="text-sm italic">No guests yet</p>
                    {/if}
                {:else}
                    <div class="detail-card mt-4">
                        <div class="detail-card-body">
                            <div class="detail-card-title">Guest Statistics</div>
                            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                                <div>
                                    <div class="detail-card-field-name">Total Guests</div>
                                    <div class="detail-card-field-value text-2xl font-bold">
                                        {data.guestGroup.groupCount}
                                    </div>
                                </div>
                                {#if data.guestGroup.groupStandard > 0}
                                    <div>
                                        <div class="detail-card-field-name">{data.configData?.standardGroupLabel}</div>
                                        <div class="detail-card-field-value text-xl">
                                            {data.guestGroup.groupStandard}
                                        </div>
                                    </div>
                                {/if}

                                {#if data.guestGroup.groupVip > 0}
                                    <div>
                                        <div class="detail-card-field-name">{data.configData?.vipGroupLabel}</div>
                                        <div class="detail-card-field-value text-xl">{data.guestGroup.groupVip}</div>
                                    </div>
                                {/if}

                                {#if data.guestGroup.groupOvernight > 0}
                                    <div>
                                        <div class="detail-card-field-name">
                                            {data.configData?.accommodationGroupLabel}
                                        </div>
                                        <div class="detail-card-field-value text-xl">
                                            {data.guestGroup.groupOvernight}
                                        </div>
                                    </div>
                                {/if}
                            </div>
                            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                                <div>
                                    <div class="detail-card-field-name">Invited</div>
                                    <div class="detail-card-field-value text-2xl font-bold text-info">
                                        {data.guestGroup.groupInvitedCount}
                                    </div>
                                </div>

                                <div>
                                    <div class="detail-card-field-name">Attending</div>
                                    <div class="detail-card-field-value text-2xl font-bold text-success">
                                        {data.guestGroup.groupAttendingCount}
                                    </div>
                                </div>

                                <div>
                                    <div class="detail-card-field-name">Declined</div>
                                    <div class="detail-card-field-value text-2xl font-bold text-error">
                                        {data.guestGroup.groupDeclinedCount}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 mt-4">
                        {#each data.guests as guest (guest.id)}
                            <div class="list-card">
                                <div class="list-card-body">
                                    <div class="list-card-title">
                                        {guest.firstName}
                                        {guest.lastName}{guest.plusOne ? " +1" : ""}
                                    </div>

                                    <div class="flex flex-wrap gap-2 my-2">
                                        {#if guest.isInvited}
                                            <span class="badge badge-info badge-sm">Invited</span>
                                        {/if}
                                        {#if guest.responded}
                                            {#if guest.isAttending}
                                                <span class="badge badge-success badge-sm">Attending</span>
                                            {:else}
                                                <span class="badge badge-error badge-sm">Declined</span>
                                            {/if}
                                        {:else}
                                            <span class="badge badge-warning badge-sm">No Response</span>
                                        {/if}
                                        {#if guest.vip}
                                            <span class="badge badge-secondary badge-sm"
                                                >{data.configData?.vipGroupLabel}</span>
                                        {/if}
                                        {#if guest.accommodation}
                                            <span class="badge badge-accent badge-sm"
                                                >{data.configData?.accommodationGroupLabel}</span>
                                        {/if}
                                    </div>

                                    {#if guest.notes}
                                        <div class="list-card-item">{guest.notes}</div>
                                    {/if}
                                </div>
                                <div class="list-card-actions flex gap-2">
                                    <ViewDetails href={`/planning/guest/${guest.id}`} label="View Details" size="sm" />
                                    <DeleteObject
                                        action="?/deleteGuest"
                                        href="#"
                                        label="Remove Guest"
                                        value={guest.id}
                                        confirmMessage="Are you sure you want to remove this guest?" />
                                </div>
                            </div>
                        {/each}
                    </div>
                {/if}
            </ObjectChildItems>
        </div>
    {/snippet}
</ObjectDetail>
