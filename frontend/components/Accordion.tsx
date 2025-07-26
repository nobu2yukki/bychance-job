import { ChevronDown, ChevronUp } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';

const AccordionItem = ({ title, children, isOpen, onToggle }: { title: string, children: React.ReactNode, isOpen: boolean, onToggle: () => void }) => {
    const contentRef = useRef<HTMLDivElement>(null)
    const [maxHeight, setMaxHeight] = useState('0px');

    useEffect(() => {
        if (contentRef.current) {
            setMaxHeight(isOpen ? `${contentRef.current.scrollHeight}px` : '0px');
        }
    }, [isOpen]);

    return (
        <div className="border border-gray-200 rounded-lg mb-2 overflow-hidden">
            <button
                className="w-full px-4 py-3 text-left bg-gray-50 hover:bg-gray-100 transition-colors duration-200 flex justify-between items-center focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-inset"
                onClick={onToggle}
                type="button"
            >
                <span className="font-medium text-gray-900">{title}</span>
                {isOpen ? (
                    <ChevronUp />
                ) : (
                    <ChevronDown />
                )}
            </button>
            <div
                ref={contentRef}
                style={{ maxHeight }}
                className={`transition-all duration-300 ease-in-out overflow-hidden ${isOpen ? 'opacity-100' : 'opacity-0'
                    }`}
            >
                <div className="px-4 py-3 bg-white text-gray-700">
                    {children}
                </div>
            </div>
        </div>
    );
};

export const Accordion = ({ items, allowMultiple = false }: { items: { title: string, content: React.ReactNode }[], allowMultiple: boolean }) => {
    const [openItems, setOpenItems] = useState(new Set());

    const toggleItem = (index: number) => {
        const newOpenItems = new Set(openItems);

        if (allowMultiple) {
            if (newOpenItems.has(index)) {
                newOpenItems.delete(index);
            } else {
                newOpenItems.add(index);
            }
        } else {
            if (newOpenItems.has(index)) {
                newOpenItems.clear();
            } else {
                newOpenItems.clear();
                newOpenItems.add(index);
            }
        }

        setOpenItems(newOpenItems);
    };

    return (
        <div className="w-full max-w-2xl mx-auto">
            {items.map((item, index) => (
                <AccordionItem
                    key={item.title}
                    title={item.title}
                    isOpen={openItems.has(index)}
                    onToggle={() => toggleItem(index)}
                >
                    {item.content}
                </AccordionItem>
            ))}
        </div>
    );
};