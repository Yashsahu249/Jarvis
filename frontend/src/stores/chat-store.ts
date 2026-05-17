import { create } from "zustand";

interface Message {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  timestamp: number;
}

interface Conversation {
  id: string;
  title: string;
  messages: Message[];
  createdAt: number;
  updatedAt: number;
}

interface ChatState {
  messages: Message[];
  isStreaming: boolean;
  inputText: string;
  conversations: Conversation[];
  activeConversationId: string | null;
  addMessage: (message: Message) => void;
  setStreaming: (streaming: boolean) => void;
  setInputText: (text: string) => void;
  setConversations: (conversations: Conversation[]) => void;
  setActiveConversation: (id: string | null) => void;
  createConversation: () => string;
  clearMessages: () => void;
}

export const useChatStore = create<ChatState>((set, get) => ({
  messages: [],
  isStreaming: false,
  inputText: "",
  conversations: [],
  activeConversationId: null,
  addMessage: (message) =>
    set((state) => ({ messages: [...state.messages, message] })),
  setStreaming: (streaming) => set({ isStreaming: streaming }),
  setInputText: (text) => set({ inputText: text }),
  setConversations: (conversations) => set({ conversations }),
  setActiveConversation: (id) => set({ activeConversationId: id }),
  createConversation: () => {
    const id = crypto.randomUUID();
    const now = Date.now();
    const conversation: Conversation = {
      id,
      title: "New Conversation",
      messages: [],
      createdAt: now,
      updatedAt: now,
    };
    set((state) => ({
      conversations: [conversation, ...state.conversations],
      activeConversationId: id,
      messages: [],
    }));
    return id;
  },
  clearMessages: () => set({ messages: [] }),
}));
