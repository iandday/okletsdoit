<script lang="ts">
    import { enhance } from "$app/forms";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import type { ActionData } from "./$types";

    const { form }: { form: ActionData } = $props();

    const relativeCrumbs = [
        { title: "Guest List", href: "/planning/guest_list" },
        { title: "New Group", href: "/planning/guest_list/new" },
    ];
</script>

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader title="New Guest Group" description="Create a new guest group for your wedding" />
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
            <!-- Basic Information -->
            <div class="edit-card mb-6">
                <div class="edit-card-body">
                    <div class="edit-card-title">Basic Information</div>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="form-control w-full md:col-span-2">
                            <label class="edit-card-field-name" for="name">
                                <span>Group Name</span>
                                <span class="text-error ml-1">*</span>
                            </label>
                            <input
                                type="text"
                                id="name"
                                name="name"
                                class="edit-card-field-input"
                                placeholder="The Smith Family"
                                required
                                autofocus />
                            <span class="text-sm text-base-content mt-1"
                                >Main name for this guest group (e.g., family name or couple)</span>
                        </div>

                        <div class="form-control w-full md:col-span-2">
                            <label class="edit-card-field-name" for="address_name">
                                <span>Address Name</span>
                            </label>
                            <input
                                type="text"
                                id="address_name"
                                name="address_name"
                                class="edit-card-field-input"
                                placeholder="Mr. and Mrs. John Smith" />
                            <span class="text-sm text-base-content mt-1"
                                >Name as it should appear on mailed invitations</span>
                        </div>

                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="relationship">
                                <span>Relationship</span>
                            </label>
                            <select id="relationship" name="relationship" class="edit-card-field-select">
                                <option value="Rel">Relative</option>
                                <option value="Fri">Friend</option>
                                <option value="Col">Colleague</option>
                            </select>
                        </div>

                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="priority">
                                <span>Priority</span>
                            </label>
                            <select id="priority" name="priority" class="edit-card-field-select">
                                <option value="1">Low</option>
                                <option value="2" selected>Medium</option>
                                <option value="3">High</option>
                            </select>
                            <span class="text-sm text-base-content mt-1">Priority level for invitation planning</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Contact Information -->
            <div class="edit-card mb-6">
                <div class="edit-card-body">
                    <h3 class="text-lg font-semibold mb-4">Contact Information</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="email">
                                <span>Email</span>
                            </label>
                            <input
                                type="email"
                                id="email"
                                name="email"
                                class="edit-card-field-input"
                                placeholder="smith@example.com" />
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
                                placeholder="(555) 123-4567" />
                        </div>
                    </div>
                </div>
            </div>

            <!-- Address Information -->
            <div class="edit-card mb-6">
                <div class="edit-card-body">
                    <h3 class="text-lg font-semibold mb-4">Mailing Address</h3>
                    <div class="grid grid-cols-1 gap-4">
                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="address">
                                <span>Address Line 1</span>
                            </label>
                            <input
                                type="text"
                                id="address"
                                name="address"
                                class="edit-card-field-input"
                                placeholder="123 Main Street" />
                        </div>

                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="address_two">
                                <span>Address Line 2</span>
                            </label>
                            <input
                                type="text"
                                id="address_two"
                                name="address_two"
                                class="edit-card-field-input"
                                placeholder="Apt 4B" />
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                            <div class="form-control w-full">
                                <label class="edit-card-field-name" for="city">
                                    <span>City</span>
                                </label>
                                <input
                                    type="text"
                                    id="city"
                                    name="city"
                                    class="edit-card-field-input"
                                    placeholder="Springfield" />
                            </div>

                            <div class="form-control w-full">
                                <label class="edit-card-field-name" for="state">
                                    <span>State</span>
                                </label>
                                <input
                                    type="text"
                                    id="state"
                                    name="state"
                                    class="edit-card-field-input"
                                    placeholder="OH" />
                            </div>

                            <div class="form-control w-full">
                                <label class="edit-card-field-name" for="zip_code">
                                    <span>Zip Code</span>
                                </label>
                                <input
                                    type="text"
                                    id="zip_code"
                                    name="zip_code"
                                    class="edit-card-field-input"
                                    placeholder="12345" />
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Notes -->
            <div class="edit-card mb-6">
                <div class="edit-card-body">
                    <h3 class="text-lg font-semibold mb-4">Additional Notes</h3>
                    <div class="form-control w-full">
                        <label class="edit-card-field-name" for="notes">
                            <span>Notes</span>
                        </label>
                        <textarea
                            id="notes"
                            name="notes"
                            class="edit-card-field-textarea"
                            rows="4"
                            placeholder="Any special notes about this guest group..."></textarea>
                    </div>
                </div>
            </div>

            <!-- Form Actions -->
            <div class="flex gap-4 mt-6 justify-end">
                <a href="/planning/guest_list" class="btn btn-error">Cancel</a>
                <button type="submit" class="btn btn-success gap-2">
                    <span class="icon-[lucide--plus] size-5"></span>
                    Create Guest Group
                </button>
            </div>
        </form>
    </div>
</ProtectedPageShell>
