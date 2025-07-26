import React from 'react';

interface RankCrownProps {
    rank: number;
    size?: number;
}

const RankCrown: React.FC<RankCrownProps> = ({ rank, size = 24 }) => {
    const getCrownColor = (rank: number) => {
        switch (rank) {
            case 1:
                return '#FFD700';
            case 2:
                return '#C0C0C0';
            case 3:
                return '#CD7F32';
            default:
                return '#9CA3AF';
        }
    };

    const crownColor = getCrownColor(rank);

    return (
        <div className="flex items-center gap-1">
            <svg
                width={size}
                height={size}
                viewBox={`0 0 ${size} ${size}`}
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                role="img"
                aria-labelledby={`crown-${rank}`}
            >
                <title id={`crown-${rank}`}>{rank}位の王冠</title>
                <path
                    d="M5 16L3 7L7.5 10L12 4L16.5 10L21 7L19 16H5Z"
                    fill={crownColor}
                    stroke={crownColor}
                    strokeWidth="1"
                    strokeLinejoin="round"
                />
                <path
                    d="M5 16H19V18C19 18.5523 18.5523 19 18 19H6C5.44772 19 5 18.5523 5 18V16Z"
                    fill={crownColor}
                />
                <circle cx="12" cy="10" r="1" fill="#FF6B6B" />
                <circle cx="8.5" cy="11" r="0.5" fill="#4ECDC4" />
                <circle cx="15.5" cy="11" r="0.5" fill="#45B7D1" />
            </svg>
            <span className="text-md sm:text-lg font-bold">マッチ度 {rank}位 の求人</span>
        </div>
    );
};

export default RankCrown; 