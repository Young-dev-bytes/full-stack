// package com.young.thefastpizzarestfulapi.common.elasticsearch;
//
// import org.elasticsearch.action.search.SearchRequest;
// import org.elasticsearch.index.query.BoolQueryBuilder;
// import org.elasticsearch.index.query.QueryBuilders;
// import org.elasticsearch.search.builder.SearchSourceBuilder;
// import org.elasticsearch.search.sort.SortOrder;
// import org.springframework.util.ObjectUtils;
// import org.springframework.util.StringUtils;
//
// import com.young.thefastpizzarestfulapi.common.constants.SymbolConstants;
//
// /**
//  * desc:
//  *
//  * @author Young.
//  * @since 2024/5/26 18:59
//  */
// public class ElasticSearchDemo {
//
//     public static final String TIMESTAMP = "@timestamp";
//     public static final String NANOS = "nanos";
//     public static final String LOG_TIMESTAMP_TIME = "log,@timestamp,time";
//     private static final String POD_NAME_KW = "kubernetes.pod_name.keyword";
//     private static final String POD_NAME = "kubernetes.pod_name";
//     private static final String NAMESPACE = "kubernetes.namespace_name.keyword";
//     private static final String CONTAINER_NAME = "kubernetes.container_name.keyword";
//
//     public static void main(String[] args) {
//
//         SearchRequest searchRequest = new SearchRequest();
//         searchRequest.indices("ls-ml-scheduler-log-");
//
//         SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder();
//         searchSourceBuilder.size(1000);
//         searchSourceBuilder.sort(TIMESTAMP, SortOrder.ASC);
//         searchSourceBuilder.sort(NANOS, SortOrder.ASC);
//         String[] sourceField = LOG_TIMESTAMP_TIME.split(SymbolConstants.COMMA);
//         searchSourceBuilder.fetchSource(sourceField, new String[] {});
//
//         BoolQueryBuilder boolQueryBuilder = QueryBuilders.boolQuery();
//
//         String podNameKw = "job-judishy87yd6xgsukjddk98u";
//         if (StringUtils.hasLength(podNameKw)) {
//             boolQueryBuilder.filter(QueryBuilders.termQuery(POD_NAME_KW, podNameKw));
//         }
//
//         String k8sJobName = "job-judishy87yd6xgsukjddk98u";
//         if (StringUtils.hasLength(k8sJobName)) {
//             boolQueryBuilder.filter(QueryBuilders.matchQuery(POD_NAME, k8sJobName));
//         }
//
//         String namespace = "sft-test";
//         if (StringUtils.hasLength(namespace)) {
//             boolQueryBuilder.filter(QueryBuilders.termQuery(POD_NAME, namespace));
//         }
//
//         String containerName = "containerName";
//         if (StringUtils.hasLength(containerName)) {
//             boolQueryBuilder.filter(QueryBuilders.termQuery(CONTAINER_NAME, containerName));
//         }
//
//         String lastQueryTime = "";
//         String startTime = "";
//         if (ObjectUtils.isEmpty(lastQueryTime) && !ObjectUtils.isEmpty(startTime)) {
//             boolQueryBuilder.filter(QueryBuilders.rangeQuery(TIMESTAMP).gte(startTime));
//         }
//         if (!ObjectUtils.isEmpty(lastQueryTime) && !ObjectUtils.isEmpty(startTime)) {
//             boolQueryBuilder.filter(QueryBuilders.rangeQuery(TIMESTAMP).gte(lastQueryTime));
//         }
//
//         searchSourceBuilder.query(boolQueryBuilder);
//         SearchRequest searchRequestRes = searchRequest.source(searchSourceBuilder);
//     }
// }
