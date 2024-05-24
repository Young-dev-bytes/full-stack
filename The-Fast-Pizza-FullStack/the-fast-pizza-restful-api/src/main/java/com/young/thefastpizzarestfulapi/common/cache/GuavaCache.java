package com.young.thefastpizzarestfulapi.common.cache;

import com.google.common.cache.CacheBuilder;
import com.google.common.cache.CacheLoader;
import com.google.common.cache.LoadingCache;
import com.google.common.util.concurrent.ListeningExecutorService;
import com.google.common.util.concurrent.MoreExecutors;

import java.util.concurrent.ExecutionException;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public abstract class GuavaCache<K, V> {
    private static final long DEFAULT_MAXIMUM_SIZE = 1000L;
    private static final long DEFAULT_EXPIRE_AFTER_WRITE_DURATION = 60L;
    private static final int REFRESH_POOL_SIZE = 5;
    private static final ListeningExecutorService REFRESH_POOLS = MoreExecutors.listeningDecorator(Executors.newFixedThreadPool(5));
    private LoadingCache<K, V> cache;
    private final long maximumSize;
    private final long expireDuration;
    private long refreshDuration;
    private final GuavaRefreshEnum guavaFreshEnum;

    public GuavaCache() {
        this.maximumSize = 1000L;
        this.expireDuration = 5L;
        this.guavaFreshEnum = GuavaRefreshEnum.EXPIRE_AFTER_WRITE;

    }

    public V getValue(K key) throws ExecutionException {
        return this.getCache().get(key);
    }

    private LoadingCache<K, V> getCache() {
        if (this.cache == null) {
            synchronized (this) {
                if (this.cache == null) {

                    CacheBuilder cacheBuilder = CacheBuilder.newBuilder().maximumSize(this.maximumSize);
                    switch (this.guavaFreshEnum) {
                        case EXPIRE_AFTER_WRITE:
                            cacheBuilder.expireAfterWrite(this.expireDuration, TimeUnit.SECONDS);
                            break;
                        case EXPIRE_AFTER_ACCESS:
                            cacheBuilder.expireAfterAccess(this.expireDuration, TimeUnit.SECONDS);
                            break;
                        default:

                    }

                    cacheBuilder.removalListener(notification -> {
                        System.out.println(notification.getKey() + " - " + notification.getValue() + " - " + notification.getCause());
                    });

                    this.cache = cacheBuilder.build(new CacheLoader<K, V>() {
                        @Override
                        public V load(K key) throws Exception {
                            return GuavaCache.this.fetchData(key);
                        }
                        /*public ListenableFuture<V> reload(final K key, V oldValue) throws Exception {

                        }*/
                    });
                }
            }

        }
        return this.cache;
    }

    /**
     * fetch data
     *
     * @param key key
     * @return v
     */
    protected abstract V fetchData(K key);
}
