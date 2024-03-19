/*
   IGraph library.
   Copyright (C) 2024  The igraph development team

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
   02110-1301 USA
*/

#include <igraph.h>
#include <cstdlib>

inline void check_err(igraph_error_t err) {
    if (err != IGRAPH_SUCCESS)
        abort();
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
    igraph_t graph;
    igraph_vector_int_t edges;

    igraph_set_warning_handler(igraph_warning_handler_ignore);

    if (Size % 2 == 0 || Size > 512+1 || Size < 1) {
        return 0;
    }

    check_err(igraph_vector_int_init(&edges, Size-1));
    for (size_t i=0; i < Size-1; ++i) {
        VECTOR(edges)[i] = Data[i+1];
    }

    /* Directed */
    if (igraph_create(&graph, &edges, Data[0], IGRAPH_DIRECTED) == IGRAPH_SUCCESS) {
        igraph_vector_int_list_t ivl1, ivl2;
        igraph_vector_int_t iv1, iv2, iv3, iv4, iv5;
        igraph_graph_list_t gl;
        igraph_vector_bool_t bv;
        igraph_matrix_t m;
        igraph_integer_t i, i2;
        igraph_bool_t b, b2;
        igraph_real_t r;

        check_err(igraph_vector_int_list_init(&ivl1, 0));
        check_err(igraph_vector_int_list_init(&ivl2, 0));
        check_err(igraph_vector_int_init(&iv1, 0));
        check_err(igraph_vector_int_init(&iv2, 0));
        check_err(igraph_vector_int_init(&iv3, 0));
        check_err(igraph_vector_int_init(&iv4, 0));
        check_err(igraph_vector_int_init(&iv5, 0));
        check_err(igraph_vector_bool_init(&bv, 0));
        check_err(igraph_matrix_init(&m, 0, 0));

        igraph_connected_components(&graph, &iv1, &iv2, &i, IGRAPH_STRONG);
        igraph_coreness(&graph, &iv1, IGRAPH_OUT);
        igraph_assortativity_degree(&graph, &r, IGRAPH_DIRECTED);
        igraph_count_multiple(&graph, &iv1, igraph_ess_all(IGRAPH_EDGEORDER_ID));
        igraph_is_loop(&graph, &bv, igraph_ess_all(IGRAPH_EDGEORDER_FROM));
        igraph_is_multiple(&graph, &bv, igraph_ess_all(IGRAPH_EDGEORDER_TO));
        igraph_maxdegree(&graph, &i, igraph_vss_all(), IGRAPH_IN, true);

        // These algorithms require a starting vertex,
        // so we require the graph to have at least one vertex.
        if (igraph_vcount(&graph) >= 1) {
            igraph_distances(&graph, &m, igraph_vss_1(0), igraph_vss_all(), IGRAPH_OUT);
            igraph_get_shortest_paths(&graph, &ivl1, &ivl2, 0, igraph_vss_all(), IGRAPH_OUT, &iv1, &iv2);
            igraph_pseudo_diameter(&graph, &r, 0, &i, &i2, IGRAPH_DIRECTED, true);
            igraph_bfs(&graph, 0, NULL, IGRAPH_OUT, true, NULL, &iv1, &iv2, &iv3, &iv4, NULL, &iv5, NULL, NULL);
            igraph_dfs(&graph, 0, IGRAPH_OUT, true, &iv1, &iv2, &iv3, &iv4, NULL, NULL, NULL);
            igraph_bfs_simple(&graph, 0, IGRAPH_OUT, &iv1, &iv2, &iv3);
            igraph_dominator_tree(&graph, 0, &iv1, NULL, &iv2, IGRAPH_OUT);
            igraph_subcomponent(&graph, &iv1, 0, IGRAPH_OUT);
            igraph_degree_1(&graph, &i, 0, IGRAPH_OUT, true);
            igraph_degree_1(&graph, &i, 0, IGRAPH_OUT, false);
        }

        igraph_is_dag(&graph, &b);
        if (b) {
            igraph_topological_sorting(&graph, &iv1, IGRAPH_OUT);
        }

        igraph_is_eulerian(&graph, &b, &b2);
        if (b) igraph_eulerian_path(&graph, &iv1, &iv2);
        if (b2) igraph_eulerian_cycle(&graph, &iv1, &iv2);

        igraph_graph_list_init(&gl, 0);
        igraph_decompose(&graph, &gl, IGRAPH_STRONG, 10, 5);
        igraph_graph_list_destroy(&gl);

        igraph_simplify(&graph, true, true, NULL);

        if (igraph_vcount(&graph) >=1) {
            // Run only on the simplified graph to avoid a very large number of
            // shortest paths due to multi-edges.
            igraph_get_all_shortest_paths(&graph, &ivl1, &ivl2, &iv1, 0, igraph_vss_all(), IGRAPH_ALL);
        }

        igraph_add_vertices(&graph, 3, NULL);
        igraph_degree_1(&graph, &i, 0, IGRAPH_IN, IGRAPH_NO_LOOPS);
        igraph_delete_vertices(&graph, igraph_vss_1(0));
        igraph_add_edge(&graph, 0, 1);
        igraph_count_multiple_1(&graph, &i, 0);
        igraph_delete_edges(&graph, igraph_ess_1(0));

        igraph_matrix_destroy(&m);
        igraph_vector_bool_destroy(&bv);
        igraph_vector_int_destroy(&iv5);
        igraph_vector_int_destroy(&iv4);
        igraph_vector_int_destroy(&iv3);
        igraph_vector_int_destroy(&iv2);
        igraph_vector_int_destroy(&iv1);
        igraph_vector_int_list_destroy(&ivl2);
        igraph_vector_int_list_destroy(&ivl1);

        igraph_destroy(&graph);
    }

    igraph_vector_int_destroy(&edges);

    IGRAPH_ASSERT(IGRAPH_FINALLY_STACK_EMPTY);

    return 0;  // Non-zero return values are reserved for future use.
}
