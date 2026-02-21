/**
 * Export Registry
 * Maps resource types to their corresponding api-client export methods
 * Add new export types here to make them available to ExportData component
 */
import { api } from "$lib/server/api-client";

export type ExportFormat = "csv" | "xlsx";
export type ExportResourceType = "guest" | "guest_group";

type ExportConfig = {
    exportFn: (format: ExportFormat) => Promise<Blob>;
    defaultFileName: string;
    contentType: {
        csv: string;
        xlsx: string;
    };
};

export const exportRegistry: Record<ExportResourceType, ExportConfig> = {
    guest: {
        exportFn: (format) => api.guestlist.guestlistApiExportGuestData({ format }),
        defaultFileName: "guests_export",
        contentType: {
            csv: "text/csv",
            xlsx: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        },
    },
    guest_group: {
        exportFn: (format) => api.guestlist.guestlistApiExportGuestGroupData({ format }),
        defaultFileName: "guest_groups_export",
        contentType: {
            csv: "text/csv",
            xlsx: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        },
    },
};
