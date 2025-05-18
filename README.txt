Codebase Function Documentation

Page 1: Creating a user profile and signing in as an existing user

    Functions

Page 2: Submitting the Daily stress questionnaire

    Functions

Page 3: Application home page

    Functions

        + make_recommendation_table() from structure_recommendation_table.py

            + get_time() from structure_recommendation_table.py

Page 4: User profile alterations + Recommendation history

    Functions

        + change_recommendation_preference_for_user() from user_information.py

        + update_user() from user_information.py

Page 5: User record page

    Functions

Page 6: Recommendation page

    Functions

        + add_points() from user_information.py

            + get_limits() from generate_items.py

        + change_recommendation_preference_for_user() from user_information.py

Page 7: Tutorial page

    + Run streamlit_app.py file

        + page from st.session_state

        + error from st.session_state

        + error_status from st.session_state

        + insert_data() from mongo_connection.py

            + User from mongo_connection.py

                + db from mongo_connection.py

                     + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

            + Recommendation from mongo_connection.py

                + db from mongo_connection.py

                     + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

            + Tag from mongo_connection.py

                + db from mongo_connection.py

                     + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

        + menu_layout() from menu.py

            + current_passcode from st.session_state

            + open_recommendation from st.session_state

            + error from st.session_state

            + error_status from st.session_state

        + layout_7() from page_7.py

            + current_passcode from st.session_state

            + open_recommendation from st.session_state

            + error from st.session_state

            + error_status from st.session_state

            + initialize_variables() from initialise_variables.py

                + User from mongo_connection.py

                    + db from mongo_connection.py

                         + client from mongo_connection.py

                            + init_connection() from mongo_connection.py

                + Recommendation from mongo_connection.py

                    + db from mongo_connection.py

                         + client from mongo_connection.py

                            + init_connection() from mongo_connection.py

                + get_status() from check_and_balance.py

                    + Status from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

            + signing_in()

            + answering_the_questionnaire()

            + recommendations()

            + score()

            + score_history()

            + preferencies()

            + record()

            + confessions()

Page 8: Confession page

    + Run streamlit_app.py file

        + page from st.session_state

        + error from st.session_state

        + error_status from st.session_state

        + insert_data() from mongo_connection.py

            + User from mongo_connection.py

                + db from mongo_connection.py

                     + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

            + Recommendation from mongo_connection.py

                + db from mongo_connection.py

                     + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

            + Tag from mongo_connection.py

                + db from mongo_connection.py

                     + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

        + menu_layout() from menu.py

            + current_passcode from st.session_state

            + open_recommendation from st.session_state

            + error from st.session_state

            + error_status from st.session_state

        + layout_8() from page_8.py

            + current_passcode from st.session_state

            + open_recommendation from st.session_state

            + error from st.session_state

            + error_status from st.session_state

            + initialize_variables() from initialise_variables.py

                + User from mongo_connection.py

                    + db from mongo_connection.py

                         + client from mongo_connection.py

                            + init_connection() from mongo_connection.py

                + Recommendation from mongo_connection.py

                    + db from mongo_connection.py

                         + client from mongo_connection.py

                            + init_connection() from mongo_connection.py

                + get_status() from check_and_balance.py

                    + Status from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

            + confession_form_layout() from page_8.py

                + con_question from initialise_variables.py

                + record_question() from check_and_balance.py

                    + User from mongo_connection.py

                        + db from mongo_connection.py

                             + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                    + Status from mongo_connection.py

                        + db from mongo_connection.py

                             + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

            + confession_list_layout() from page_8.py

                + delete_entry() from make_record.py

                    + User from mongo_connection.py

                        + db from mongo_connection.py

                             + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                    + new_entry_in_record_collection() from check_and_balance.py

                        + Record from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

Page 9: Datapage management page

   + Run streamlit_app.py file

       + page from st.session_state

       + error from st.session_state

       + error_status from st.session_state

       + insert_data() from mongo_connection.py

            + User from mongo_connection.py

                + db from mongo_connection.py

                     + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

            + Recommendation from mongo_connection.py

                + db from mongo_connection.py

                     + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

            + Tag from mongo_connection.py

                + db from mongo_connection.py

                     + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

       + menu_layout() from menu.py

            + current_passcode from st.session_state

            + open_recommendation from st.session_state

            + error from st.session_state

            + error_status from st.session_state

       + layout_9() from page_9.py

            + current_passcode from st.session_state

            + open_recommendation from st.session_state

            + error from st.session_state

            + error_status from st.session_state

            + initialize_variables() from initialise_variables.py

                + User from mongo_connection.py

                    + db from mongo_connection.py

                         + client from mongo_connection.py

                            + init_connection() from mongo_connection.py

                + Recommendation from mongo_connection.py

                    + db from mongo_connection.py

                         + client from mongo_connection.py

                            + init_connection() from mongo_connection.py

                + get_status() from check_and_balance.py

                    + Status from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

            + add_a_recommendation_layout() from page_9.py

                + question_about_passcode from initialise_variables.py

                + question_about_recommendation_id from initialise_variables.py

                + question_about_points from initialise_variables.py

                + question_about_title from initialise_variables.py

                + question_about_link from initialise_variables.py

                + generate_recommendation_id() from generate_items.py

                    + Recommendation from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                + add_recommendation_here() from page_9.py

                    + error from st.session_state

                        + add_recommendation() from add_data_in_collection.py

                            + User from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                            + Recommendation from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                    + error_status from st.session_state

                        + add_recommendation() from add_data_in_collection.py

                            + User from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                            + Recommendation from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                    + record_question() from check_and_balance.py

                        + User from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                        + Status from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                        + Question from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                    + change_page() from change_page.py

                        + page from st.session_state

            + add_tags_layout() from page_9.py

                + question_about_passcode from initialise_variables.py

                + question_about_recommendation_id from initialise_variables.py

                + min_limit from initialise_variables.py

                + stress_max_limit from initialise_variables.py

                + max_limit from initialise_variables.py

                + question_age from initialise_variables.py

                + error from st.session_state

                + error_status from st.session_state

                + add_tag_here() from page_9.py

                    + error from st.session_state

                        + add_tag() from add_data_in_collection.py

                            + User from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                            + Recommendation from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                            + Tag from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                    + error_status from st.session_state

                        + add_tag() from add_data_in_collection.py

                            + User from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                            + Recommendation from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                            + Tag from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                    + record_question() from check_and_balance.py

                        + User from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                        + Status from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                    + change_page() from change_page.py

                        + page from st.session_state

            + add_a_question_layout() from page_9.py

                + question_about_passcode from initialise_variables.py

                + question_input from initialise_variables.py

                + Question_ID from initialise_variables.py

                + generate_question_id() from page_9.py

                    + Question_Questionnaire from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                + add_question() from page_9.py

                    + error from st.session_state

                        + add_question_to_Questionnaire() from add_data_in_collection.py

                            + User from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                            + Question_Questionnaire from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                    + error_status from st.session_state

                        + add_question_to_Questionnaire() from add_data_in_collection.py

                            + User from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                            + Question_Questionnaire from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                    + record_question() from check_and_balance.py

                        + User from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                        + Status from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                    + change_page() from change_page.py

                        + page from st.session_state