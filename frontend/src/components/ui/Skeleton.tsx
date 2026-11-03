import React from 'react';
import { cn } from '../../lib/utils';

export const Skeleton: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({
  className,
  ...props
}) => (
  <div
    className={cn('animate-pulse rounded-xl bg-slate-800/60', className)}
    {...props}
  />
);

export const CardSkeleton: React.FC = () => (
  <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-4">
    <div className="flex items-center space-x-3">
      <Skeleton className="w-10 h-10 rounded-xl" />
      <div className="space-y-2 flex-1">
        <Skeleton className="h-4 w-1/3" />
        <Skeleton className="h-3 w-1/2" />
      </div>
    </div>
    <Skeleton className="h-20 w-full rounded-xl" />
    <div className="flex justify-between pt-2">
      <Skeleton className="h-8 w-24 rounded-lg" />
      <Skeleton className="h-8 w-24 rounded-lg" />
    </div>
  </div>
);
