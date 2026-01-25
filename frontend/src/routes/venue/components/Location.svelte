<script lang="ts">
    const { data } = $props();
</script>

<div class="card bg-base-300 shadow-lg p-8">
    <div class="card-body p-0 text-secondary-content">
        <h2
            class="card-body-title text-accent text-2xl mb-2 font-bold text-center gap-4 flex items-center justify-center">
            <span class="icon-[lucide--map-pin] size-6"></span>Location & Directions
        </h2>

        <div class="space-y-3">
            <div>
                <p class="mb-1"><strong>Address:</strong></p>
                <p class="mb-1">
                    {data.configData.venueName} <br />
                    {data.configData.venueAddressLineOne}
                    {#if data.configData.venueAddressLineTwo}<br />{data.configData.venueAddressLineTwo}{/if}
                    <br />
                    {data.configData.venueCity}, {data.configData.venueState}
                    {data.configData.venueZip}
                </p>
            </div>
            <div>
                <p class="mb-1"><strong>Parking:</strong></p>
                <p class="mb-1">{data.configData.venueParking}</p>
            </div>
            <div>
                <p><strong>Directions:</strong></p>
                <p class="mb-1">{data.configData.venueDirections}</p>
            </div>

            <div class="flex flex-wrap justify-center gap-4">
                <a
                    href="https://maps.google.com/?q={data.configData.venueAddressLineOne},{data.configData
                        .venueCity},{data.configData.venueState},{data.configData.venueZip}"
                    target="_blank"
                    rel="noopener noreferrer">
                    <img src="images/googleMaps.svg" alt="Google Maps" class="h-10 w-10 mr-2" />
                </a>
                <a
                    href="https://maps.apple.com/?address={data.configData.venueAddressLineOne},{data.configData
                        .venueCity},{data.configData.venueState},{data.configData.venueZip}"
                    target="_blank"
                    rel="noopener noreferrer">
                    <img src="images/appleMaps.png" alt="Apple Maps" class="h-10 w-10 mr-2" />
                </a>
            </div>
        </div>
    </div>
</div>
