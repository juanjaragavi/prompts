# Prompt

For this iteration, I am attaching several files and images of Figma designs. The `.tsx` files are the ones I feel are necessary to give you all the context you need to complete your task.

Your task is to help me create an initial walkthrough tutorial for **TalentAssisto**. This component is a kind of overlay layer that sits on top of the main chat window in our application, ONLY for new users on their very first visit. The overlay has a 15% opacity and a slightly blurred background, and above it are animated `<motion.div>` container popup windows, with `<image />` components, titles, text and `<button>` elements for navigation.

Please investigate where I should `import' the component we have created and help me brainstorm the handling of edge cases, such as when the user clicks on the corresponding element (it could be a positive feedback additional window between the main steps windows, leading to the next step when closed), or how to handle when the user clicks on the overlay background.

If you need me to upload any additional component files or pages to help you complete your task, please let me know.

Below, I will attach the TalentAssisto logo and the `.webp` files of the character images.

- <https://storage.googleapis.com/media.juanjaramillo.tech/TalentAssisto-Logo-SplashScreen.png>
- <https://storage.googleapis.com/media.juanjaramillo.tech/talent-assisto-walkthrough/onboarding-1.webp>
- <https://storage.googleapis.com/media.juanjaramillo.tech/talent-assisto-walkthrough/onboarding-2.webp>
- <https://storage.googleapis.com/media.juanjaramillo.tech/talent-assisto-walkthrough/onboarding-3.webp>
- <https://storage.googleapis.com/media.juanjaramillo.tech/talent-assisto-walkthrough/onboarding-4.webp>
- <https://storage.googleapis.com/media.juanjaramillo.tech/talent-assisto-walkthrough/onboarding-process-1.jpg>
- <https://storage.googleapis.com/media.juanjaramillo.tech/talent-assisto-walkthrough/onboarding-process-2.jpg>
- <https://storage.googleapis.com/media.juanjaramillo.tech/talent-assisto-walkthrough/onboarding-process-3.jpg>
- <https://storage.googleapis.com/media.juanjaramillo.tech/talent-assisto-walkthrough/onboarding-process-4.jpg>

Here is the `page.tsx` into which the component will be imported and with which components it will interact.

```typescript
// page.tsx   `/app/[locale]/[workspaceid]/chat/page.tsx`

'use client';

import Link from 'next/link';
import Image from 'next/image';
import { ChatHelp } from '@/components/chat/chat-help';
import { useChatHandler } from '@/components/chat/chat-hooks/use-chat-handler';
import { ChatInput } from '@/components/chat/chat-input';
import { ChatSettings } from '@/components/chat/chat-settings';
import { ChatUI } from '@/components/chat/chat-ui';
import { QuickSettings } from '@/components/chat/quick-settings';
import { ChatbotUIContext } from '@/context/context';
import useHotkey from '@/lib/hooks/use-hotkey';
import { useTheme } from 'next-themes';
import { useContext } from 'react';
import { useTranslation } from 'react-i18next';

export default function ChatPage() {
  useHotkey('o', () => handleNewChat());
  useHotkey('l', () => {
    handleFocusChatInput();
  });

  const { t } = useTranslation();

  const { chatMessages } = useContext(ChatbotUIContext);

  const { handleNewChat, handleFocusChatInput } = useChatHandler();

  const { theme } = useTheme();

  return (
    <>
      {chatMessages.length === 0 ? (
        <div className="relative flex h-full flex-col items-center justify-center">
          <div className="top-50% left-50% -translate-x-50% -translate-y-50% absolute mb-20">
            <Link
              className="flex cursor-pointer flex-col items-center transition-all duration-300 ease-in-out hover:opacity-70"
              href="https://www.talentassisto.com"
              target="_blank"
              rel="noopener noreferrer"
            >
              <div className="mb-2">
                <Image
                  style={{ width: '300px', height: '100px' }}
                  className="rounded"
                  src="/images/TalentAssisto-Logo-SplashScreen.png"
                  alt="TalentAssisto | All-purpose HR Assistant powered by AI"
                  width={300}
                  height={100}
                />
              </div>
            </Link>
          </div>

          <div className="absolute right-2 top-2">
            <QuickSettings />
          </div>

          <div className="absolute right-2 top-2 hidden">
            <ChatSettings />
          </div>

          <div className="flex grow flex-col items-center justify-center" />

          <div className="w-full min-w-[300px] items-end px-2 pb-3 pt-0 sm:w-[600px] sm:pb-8 sm:pt-5 md:w-[700px] lg:w-[700px] xl:w-[800px]">
            <ChatInput />
          </div>

          <div className="absolute bottom-2 right-2 hidden md:block lg:bottom-4 lg:right-4">
            <ChatHelp />
          </div>
        </div>
      ) : (
        <ChatUI />
      )}
    </>
  );
}
```
