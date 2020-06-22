#!/usr/bin/env bash

kubectl port-forward --address localhost,${LOCKSS_IPADDR} service/lockss-configuration-service ${CFG_REST_PORT}:${CFG_DEFAULT_REST_PORT}  ${CFG_UI_PORT}:${CFG_DEFAULT_UI_PORT} ${LOCKSS_UI_PORT}:${CFG_DEFAULT_UI_PORT}

kubectl port-forward --address localhost,${LOCKSS_IPADDR} service/lockss-metadata-extraction-service ${MDX_REST_PORT}:${MDX_DEFAULT_REST_PORT} ${MDX_UI_PORT}:${MDX_DEFAULT_UI_PORT}

kubectl port-forward --address localhost,${LOCKSS_IPADDR} service/lockss-metadata-extraction-service ${MDQ_REST_PORT}:${MDQ_DEFAULT_REST_PORT} ${MDQ_UI_PORT}:${MDQ_DEFAULT_UI_PORT}

kubectl port-forward --address localhost,${LOCKSS_IPADDR} service/lockss-metadata-extraction-service ${POL_REST_PORT}:${POL_DEFAULT_REST_PORT} ${POL_UI_PORT}:${POL_DEFAULT_UI_PORT} ${POL_LCAP_PORT}:${POL_DEFAULT_LCAP_PORT} ${SERV_PORT}:${SERV_DEFAULT_PORT} ${LOCKSS_PROXY_PORT}:${LOCKSS_DEFAULT_PROXY_PORT} ${LOCKSS_AUDIT_PORT}:${LOCKSS_DEFAULT_AUDIT_PORT} ${LOCKSS_ICP_PORT}:${LOCKSS_DEFAULT_ICP_PORT}

kubectl port-forward --address localhost,${LOCKSS_IPADDR} service/lockss-metadata-extraction-service ${POSTGRES_PORT}:${POSTGRES_DEFAULT_PORT}

kubectl port-forward --address localhost,${LOCKSS_IPADDR} service/lockss-metadata-extraction-service ${PYWB_PORT}:${PYWB_DEFAULT_PORT}

kubectl port-forward --address localhost,${LOCKSS_IPADDR} service/lockss-metadata-extraction-service ${REPO_REST_PORT}:${REPO_DEFAULT_REST_PORT}

kubectl port-forward --address localhost,${LOCKSS_IPADDR} service/lockss-metadata-extraction-service ${SOLR_PORT}:${SOLR_DEFAULT_PORT}
