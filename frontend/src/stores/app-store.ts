import { create } from "zustand";

export type ActiveModule =
  | "dashboard"
  | "chat"
  | "voice"
  | "browser"
  | "agents"
  | "repos"
  | "memory"
  | "terminal";

export type ThemeMode = "light" | "dark" | "system";

interface SystemStatus {
  cpu: number;
  memory: number;
  uptime: string;
  online: boolean;
}

interface AppState {
  sidebarOpen: boolean;
  activeModule: ActiveModule;
  themeMode: ThemeMode;
  systemStatus: SystemStatus;
  toggleSidebar: () => void;
  setActiveModule: (module: ActiveModule) => void;
  setThemeMode: (mode: ThemeMode) => void;
  setSystemStatus: (status: Partial<SystemStatus>) => void;
}

export const useAppStore = create<AppState>((set) => ({
  sidebarOpen: true,
  activeModule: "dashboard",
  themeMode: "light",
  systemStatus: {
    cpu: 0,
    memory: 0,
    uptime: "0h 0m",
    online: false,
  },
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  setActiveModule: (module) => set({ activeModule: module }),
  setThemeMode: (mode) => set({ themeMode: mode }),
  setSystemStatus: (status) =>
    set((state) => ({
      systemStatus: { ...state.systemStatus, ...status },
    })),
}));
