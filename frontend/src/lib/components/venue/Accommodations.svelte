<script lang="ts">
    import Icon from "$lib/components/Icon.svelte";
    import type { AccommodationSchema } from "../../../../api-client";

    interface iAccommodationsProps {
        accommodations?: AccommodationSchema[];
    }

    const { accommodations = [] }: iAccommodationsProps = $props();

    function getAccommodationTypeIcon(type: string) {
        switch (type) {
            case "hotel":
                return { icon: "hotel", label: "Hotel" };
            case "rental":
                return { icon: "home", label: "Rental" };
            case "campground":
                return { icon: "tent", label: "Camping" };
            default:
                return { icon: "hotel", label: "Hotel" };
        }
    }

    function formatAddress(accommodation: AccommodationSchema): string {
        const parts = [
            accommodation.addressLineOne,
            accommodation.addressLineTwo,
            accommodation.city && accommodation.state
                ? `${accommodation.city}, ${accommodation.state}`
                : accommodation.city || accommodation.state,
            accommodation.zipcode,
        ].filter(Boolean);
        return parts.join(", ");
    }
</script>

<div class="mx-auto my-16 max-w-7xl px-4 sm:px-6 lg:px-8">
    <h2
        class="text-center text-2xl leading-tight font-bold sm:text-3xl md:text-4xl lg:text-4xl xl:text-5xl bg-gradient-to-r from-primary via-secondary to-accent bg-clip-text text-transparent mb-4">
        Need a Place to Stay?
    </h2>
    <p class="text-base-content/70 text-lg text-center mb-12 max-w-3xl mx-auto">
        We've compiled a list of nearby accommodations to make your stay comfortable. Whether you prefer a hotel, cabin
        rental, or camping under the stars, there's something for everyone!
    </p>

    <!-- Accommodations Grid -->
    {#if accommodations.length > 0}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-7xl mx-auto px-4">
            {#each accommodations as accommodation (accommodation.id)}
                {@const typeInfo = getAccommodationTypeIcon(accommodation.accommodationType)}
                {@const address = formatAddress(accommodation)}
                <div
                    class="card bg-base-200 shadow-xl border border-base-300 hover:shadow-2xl transition-all duration-300 hover:-translate-y-1">
                    <div class="card-body">
                        <div class="flex items-start justify-between mb-2">
                            <div class="badge badge-accent badge-sm rounded-full p-4 m-3">
                                <Icon name={typeInfo.icon} class="size-6 text-accent-content" />
                                {typeInfo.label}
                            </div>
                        </div>

                        <h3 class="card-title text-primary-content text-lg mb-2">{accommodation.name}</h3>
                        {#if accommodation.description}
                            <p class="text-primary-content text-sm mb-4 line-clamp-3">{accommodation.description}</p>
                        {/if}

                        <div class="space-y-2 mb-4">
                            {#if accommodation.phoneNumber}
                                <div class="flex items-center gap-2 text-sm text-primary-content">
                                    <span class="icon-[lucide--phone] size-4"></span>
                                    <a
                                        href="tel:{accommodation.phoneNumber}"
                                        class="hover:text-primary transition-colors">
                                        {accommodation.phoneNumber}
                                    </a>
                                </div>
                            {/if}
                            {#if address}
                                <div class="flex items-start gap-2 text-sm text-primary-content">
                                    <span class="icon-[lucide--map-pin] size-4 mt-0.5 flex-shrink-0"></span>
                                    <span class="line-clamp-2">{address}</span>
                                </div>
                            {/if}
                        </div>

                        {#if accommodation.url}
                            <div class="card-actions justify-end mt-auto">
                                <a
                                    href={accommodation.url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    class="btn btn-primary btn-sm gap-2">
                                    <span>View Details</span>
                                    <span class="icon-[lucide--external-link] size-4"></span>
                                </a>
                            </div>
                        {/if}
                    </div>
                </div>
            {/each}
        </div>
    {:else}
        <div class="text-center py-8 max-w-md mx-auto">
            <Icon name="hotel" class="size-12 text-base-content mx-auto block mb-2" />
            <p class="text-base-content/70">No accommodations listed yet.</p>
            <p class="text-sm text-base-content/50">Check back soon for lodging options near the venue.</p>
        </div>
    {/if}
</div>
