<script lang="ts">
    type iAddress = {
        name: string;
        event: string | null;
        addressLine1: string;
        addressLine2?: string | null;
        city: string;
        state: string;
        zip: string;
        parking: string;
        directions: string;
    };

    const Addresses: iAddress[] = [
        {
            name: "Timberframe Lodge",
            event: null,
            addressLine1: "16187 Kreashbaum Road",
            addressLine2: null,
            city: "Rockbridge",
            state: "OH",
            zip: "43149",
            parking: "Ample on-site parking available for all guests",
            directions:
                "Look for the sign once you're on Kreashbaum Road, follow the gravel drive down to the venue entrance.",
        },
    ];
</script>

<div class="card bg-base-300 shadow-lg p-8">
    <div class="card-body p-0 text-secondary-content">
        <h2
            class="card-body-title text-accent text-2xl mb-2 font-bold text-center gap-4 flex items-center justify-center">
            <span class="iconify lucide--map-pin size-6"></span>Location & Directions
        </h2>
        {#each Addresses as address}
            {#if Addresses.length > 1}
                <h3 class="text-xl font-semibold mb-4">{address.event}</h3>
            {/if}
            <div class="space-y-3">
                <div>
                    <p class="mb-1"><strong>Address:</strong></p>
                    <p class="mb-1">
                        {address.name} <br />
                        {address.addressLine1}
                        {#if address.addressLine2}<br />{address.addressLine2}{/if}
                        <br />
                        {address.city}, {address.state}
                        {address.zip}
                    </p>
                </div>
                <div>
                    <p class="mb-1"><strong>Parking:</strong></p>
                    <p class="mb-1">{address.parking}</p>
                </div>
                <div>
                    <p><strong>Directions:</strong></p>
                    <p class="mb-1">{address.directions}</p>
                </div>

                <div class="flex flex-wrap justify-center gap-4">
                    <a
                        href="https://maps.google.com/?q={address.addressLine1},{address.city},{address.state},{address.zip}"
                        target="_blank"
                        rel="noopener noreferrer">
                        <img src="images/googleMaps.svg" alt="Google Maps" class="h-10 w-10 mr-2" />
                    </a>
                    <a
                        href="https://maps.apple.com/?address={address.addressLine1},{address.city},{address.state},{address.zip}"
                        target="_blank"
                        rel="noopener noreferrer">
                        <img src="images/appleMaps.png" alt="Apple Maps" class="h-10 w-10 mr-2" />
                    </a>
                </div>
            </div>
        {/each}
    </div>
</div>
