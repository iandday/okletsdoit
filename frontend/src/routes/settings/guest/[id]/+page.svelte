<script lang="ts">
    import ObjectDetail from "$lib/components/object/ObjectDetail.svelte";
    import type { PageData } from "./$types";

    const { data }: { data: PageData } = $props();

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
    ]);

    const displayName = $derived(
        data.guest.plusOne
            ? `${data.guest.firstName} ${data.guest.lastName} +1`
            : `${data.guest.firstName} ${data.guest.lastName}`,
    );
</script>

<ObjectDetail
    {relativeCrumbs}
    title={displayName}
    editLink={`/settings/guest/${data.guest.id}/edit`}
    deleteAction="?/delete"
    object={data.guest}>
    {#snippet mainSnippet()}
        <div class="space-y-6">
            <!-- Basic Information -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <div class="detail-card-field-name">First Name</div>
                    <div class="detail-card-field-value">{data.guest.firstName}</div>
                </div>

                <div>
                    <div class="detail-card-field-name">Last Name</div>
                    <div class="detail-card-field-value">{data.guest.lastName}</div>
                </div>

                {#if data.guestGroup}
                    <div>
                        <div class="detail-card-field-name">Guest Group</div>
                        <div class="detail-card-field-value">
                            <a href="/settings/guest_list/{data.guestGroup.id}" class="link">
                                {data.guestGroup.name}
                            </a>
                        </div>
                    </div>
                {/if}

                <div>
                    <div class="detail-card-field-name">Plus One</div>
                    <div class="detail-card-field-value">
                        {#if data.guest.plusOne}
                            <span class="badge badge-success">Yes</span>
                        {:else}
                            <span class="badge badge-error">No</span>
                        {/if}
                    </div>
                </div>
            </div>

            <!-- Invitation & RSVP Status -->
            <div>
                <h3 class="text-lg font-semibold mb-3">Status</h3>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                        <div class="detail-card-field-name">Invited</div>
                        <div class="detail-card-field-value">
                            {#if data.guest.isInvited}
                                <span class="badge badge-info">Yes</span>
                            {:else}
                                <span class="badge badge-ghost">No</span>
                            {/if}
                        </div>
                    </div>

                    <div>
                        <div class="detail-card-field-name">RSVP Status</div>
                        <div class="detail-card-field-value">
                            {#if data.guest.responded}
                                {#if data.guest.isAttending}
                                    <span class="badge badge-success">Attending</span>
                                {:else}
                                    <span class="badge badge-error">Declined</span>
                                {/if}
                            {:else}
                                <span class="badge badge-warning">No Response</span>
                            {/if}
                        </div>
                    </div>

                    <div>
                        <div class="detail-card-field-name">Response Date</div>
                        <div class="detail-card-field-value">
                            {#if data.guest.responded}
                                {new Date(data.guest.updatedAt).toLocaleDateString()}
                            {:else}
                                -
                            {/if}
                        </div>
                    </div>
                </div>
            </div>

            <!-- Special Requirements -->
            <div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {#if data.configData?.rsvpShowVipIntro}
                        <div>
                            <div class="detail-card-field-name">{data.configData?.vipGroupLabel} Guest</div>
                            <div class="detail-card-field-value">
                                {#if data.guest.vip}
                                    <span class="badge badge-success">Yes</span>
                                {:else}
                                    <span class="badge badge-error">No</span>
                                {/if}
                            </div>
                        </div>
                    {/if}

                    {#if data.configData?.rsvpShowAccommodationIntro}
                        <div>
                            <div class="detail-card-field-name">Accommodation</div>
                            <div class="detail-card-field-value">
                                {#if data.guest.accommodation}
                                    <span class="badge badge-success">Yes</span>
                                {:else}
                                    <span class="badge badge-error">No</span>
                                {/if}
                            </div>
                        </div>
                    {/if}

                    {#if data.guest.responded && data.guest.isAttending}
                        {#if data.configData?.rsvpShowVipIntro}
                            <div>
                                <div class="detail-card-field-name">
                                    Accepted {data.configData?.vipGroupLabel} Offer
                                </div>
                                <div class="detail-card-field-value">
                                    {#if data.guest.acceptVip}
                                        <span class="badge badge-success">Yes</span>
                                    {:else}
                                        <span class="badge badge-error">No</span>
                                    {/if}
                                </div>
                            </div>
                        {/if}

                        {#if data.configData?.rsvpShowAccommodationIntro}
                            <div>
                                <div class="detail-card-field-name">
                                    Accepted {data.configData?.accommodationGroupLabel} Offer
                                </div>
                                <div class="detail-card-field-value">
                                    {#if data.guest.acceptAccommodation}
                                        <span class="badge badge-success">Yes</span>
                                    {:else}
                                        <span class="badge badge-error">No</span>
                                    {/if}
                                </div>
                            </div>
                        {/if}
                    {/if}
                </div>
            </div>
            <!-- Notes -->
            {#if data.guest.notes}
                <div>
                    <h3 class="text-lg font-semibold mb-3">Notes</h3>
                    <div class="detail-card-field-value whitespace-pre-wrap bg-base-200 p-4 rounded-lg">
                        {data.guest.notes}
                    </div>
                </div>
            {/if}
        </div>
    {/snippet}
</ObjectDetail>
