Codebase Function Documentation

Page 1: Creating a user profile and signing in as an existing user

    Functions

Page 2: Submitting the Daily stress questionnaire

    Functions

Page 3: Application home page

    + Run streamlit_app.py file

        + page from st.session_state

        + error from st.session_state

        + error_status from st.session_state

        + insert_data() from mongo_connection.py

            + User from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Recommendation from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Tag from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

        + menu_layout() from menu.py

            + current_passcode from st.session_state

            + open_recommendation from st.session_state

            + error from st.session_state

            + error_status from st.session_state

        + layout_3() from page_3.py

            + error from st.session_state

            + error_status from st.session_state

            + initialize_variables() from initialise_variables.py

                + User from mongo_connection.py

                    + db from mongo_connection.py

                        + client from mongo_connection.py

                            + init_connection() from mongo_connection.py

                                + Database_Connection from st.secrets

                + Recommendation from mongo_connection.py

                    + db from mongo_connection.py

                        + client from mongo_connection.py

                            + init_connection() from mongo_connection.py

                                + Database_Connection from st.secrets

                + get_status() from check_and_balance.py

                    + Status from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

            + section_1() from page_3.py

            + section_2() from page_3.py

                + determine_level_change(passcode)

                    + User from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

                    + new_entry_in_record_collection() from check_and_balance.py

                        + Record from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                    + new_entry_in_score_history_collection() from check_and_balance.py

                        + User from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                + get_limits() from generate_items.py

                + create_custom_slider() from page_3.py

                + get_time() from page_3.py

                + create_store_history_graph() from page_3.py

                    + Score_History from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

                    + get_limits() from generate_items.py

        + section_2_5() from page_3.py

        + section_3() from page_3.py

            + get_recommendations(passcode) from generate_recommendations_main.py

                + User from mongo_connection.py

                    + db from mongo_connection.py

                        + client from mongo_connection.py

                            + init_connection() from mongo_connection.py

                                + Database_Connection from st.secrets

                + Recommendation from mongo_connection.py

                    + db from mongo_connection.py

                        + client from mongo_connection.py

                            + init_connection() from mongo_connection.py

                                + Database_Connection from st.secrets

                + get_status() from check_and_balance.py

                    + Status from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

                + Status from mongo_connection.py

                    + db from mongo_connection.py

                        + client from mongo_connection.py

                            + init_connection() from mongo_connection.py

                                + Database_Connection from st.secrets

                + Recommendation_Per_Person from mongo_connection.py

                    + db from mongo_connection.py

                        + client from mongo_connection.py

                            + init_connection() from mongo_connection.py

                                + Database_Connection from st.secrets

                + calculate_entries(passcode)

                    + User from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

                    + Recommendation from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

                    + add_category()

                + generate_recommendations_by_AI() from create_prompt_by_AI.py

                    + return_prompt() from create_prompt_by_AI.py

                        + active_model from st.secrets

                        + groqkey from st.secrets

                        + geminikey from st.secrets

                        + create_prompt() from create_prompt_by_AI.py

                            + generate_user_profile(passcode) from create_prompt_by_AI.py

                                + User from mongo_connection.py

                                    + db from mongo_connection.py

                                        + client from mongo_connection.py

                                            + init_connection() from mongo_connection.py

                                                + Database_Connection from st.secrets

                                + Recommendation from mongo_connection.py

                                    + db from mongo_connection.py

                                        + client from mongo_connection.py

                                            + init_connection() from mongo_connection.py

                                                + Database_Connection from st.secrets

                                + Status from mongo_connection.py

                                    + db from mongo_connection.py

                                        + client from mongo_connection.py

                                            + init_connection() from mongo_connection.py

                                                + Database_Connection from st.secrets

                                + Recommendation_Per_Person from mongo_connection.py

                                    + db from mongo_connection.py

                                        + client from mongo_connection.py

                                            + init_connection() from mongo_connection.py

                                                + Database_Connection from st.secrets

                                + Question_Questionnaire from mongo_connection.py

                                    + db from mongo_connection.py

                                        + client from mongo_connection.py

                                            + init_connection() from mongo_connection.py

                                                + Database_Connection from st.secrets

                                + Question from mongo_connection.py

                                    + db from mongo_connection.py

                                        + client from mongo_connection.py

                                            + init_connection() from mongo_connection.py

                                                + Database_Connection from st.secrets

                                + Favorite_Recommendation from mongo_connection.py

                                    + db from mongo_connection.py

                                        + client from mongo_connection.py

                                            + init_connection() from mongo_connection.py

                                                + Database_Connection from st.secrets

                                + Removed_Recommendation from mongo_connection.py

                                    + db from mongo_connection.py

                                        + client from mongo_connection.py

                                            + init_connection() from mongo_connection.py

                                                + Database_Connection from st.secrets

                        + call_gemini_api(passcode, api_key)

                            + generate_user_profile(passcode) from create_prompt_by_AI.py

                                + User from mongo_connection.py

                                    + db from mongo_connection.py

                                        + client from mongo_connection.py

                                            + init_connection() from mongo_connection.py

                                                + Database_Connection from st.secrets

                                + Recommendation from mongo_connection.py

                                    + db from mongo_connection.py

                                        + client from mongo_connection.py

                                            + init_connection() from mongo_connection.py

                                                + Database_Connection from st.secrets

                                + Status from mongo_connection.py

                                    + db from mongo_connection.py

                                        + client from mongo_connection.py

                                            + init_connection() from mongo_connection.py

                                                + Database_Connection from st.secrets

                                + Recommendation_Per_Person from mongo_connection.py

                                    + db from mongo_connection.py

                                        + client from mongo_connection.py

                                            + init_connection() from mongo_connection.py

                                                + Database_Connection from st.secrets

                                + Question_Questionnaire from mongo_connection.py

                                    + db from mongo_connection.py

                                        + client from mongo_connection.py

                                            + init_connection() from mongo_connection.py

                                                + Database_Connection from st.secrets

                                + Question from mongo_connection.py

                                    + db from mongo_connection.py

                                        + client from mongo_connection.py

                                            + init_connection() from mongo_connection.py

                                                + Database_Connection from st.secrets

                                + Favorite_Recommendation from mongo_connection.py

                                    + db from mongo_connection.py

                                        + client from mongo_connection.py

                                            + init_connection() from mongo_connection.py

                                                + Database_Connection from st.secrets

                                + Removed_Recommendation from mongo_connection.py

                                    + db from mongo_connection.py

                                        + client from mongo_connection.py

                                            + init_connection() from mongo_connection.py

                                                + Database_Connection from st.secrets

                    + evaluate_output(prompt, model_output) from evaluation.py

                    + extract_json(new_recommendation, prompt)

                    + generate_recommendation_id() from generate_items.py

                        + Recommendation from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + Recommendation_Per_Person from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + Tag from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + Favorite_Recommendation from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + Removed_Recommendation from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                    + add_recommendation() from add_data_in_collection.py

                        + User from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + Recommendation from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + Tag from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + Recommendation_Per_Person from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + add_tag() from add_data_in_collection.py

                            + User from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                            + Recommendation from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                            + Tag from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                    + enter_recommendation_for_user() from generate_recommendations_functions.py

                        + User from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + get_status() from check_and_balance.py

                            + Status from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                        + Status from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + Recommendation_Per_Person from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                + generate_recommendations_chosen_by_tags() from generate_by_tags.py

                    + User from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

                    + get_status() from check_and_balance.py

                        + Status from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                    + Status from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

                    + Recommendation_Per_Person from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

                    + Recommendation from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

                    + Tag from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

                    + pass_filter() from generate_recommendations_functions.py

                    + enter_recommendation_for_user() from generate_recommendations_functions.py

                        + User from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + get_status() from check_and_balance.py

                            + Status from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                        + Status from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + Recommendation_Per_Person from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                    + generate_valid_index() from generate_recommendations_functions.py

                        + Recommendation from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                    + validate_recommendation_pick() from generate_by_tags.py

                        + enter_recommendation_for_user() from generate_recommendations_functions.py

                            + User from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                            + get_status() from check_and_balance.py

                                + Status from mongo_connection.py

                                    + db from mongo_connection.py

                                        + client from mongo_connection.py

                                            + init_connection() from mongo_connection.py

                                                + Database_Connection from st.secrets

                            + Status from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                            + Recommendation_Per_Person from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                        + generate_valid_index() from generate_recommendations_functions.py

                            + Recommendation from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                + generate_recommendations_by_algorithm() from generate_by_algorithm.py

                    + generate_recommendation() from generate_by_algorithm.py

                        + get_status() from check_and_balance.py

                            + Status from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                        + Recommendation_Per_Person from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + generate_valid_index() from generate_recommendations_functions.py

                            + Recommendation from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                        + has_the_user_seen_this_recommendation_before() from generate_by_algorithm.py

                            + User from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                            + Recommendation_Per_Person from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                        + do_the_tags_match() from generate_by_algorithm.py

                            + User from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                            + Tag from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                            + Status from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                            + pass_filter() from generate_recommendations_functions.py

                        + Removed_Recommendation from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + enter_recommendation_for_user() from generate_recommendations_functions.py

                            + User from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                            + get_status() from check_and_balance.py

                                + Status from mongo_connection.py

                                    + db from mongo_connection.py

                                        + client from mongo_connection.py

                                            + init_connection() from mongo_connection.py

                                                + Database_Connection from st.secrets

                            + Status from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                            + Recommendation_Per_Person from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                    + generate_valid_index() from generate_recommendations_functions.py

                        + Recommendation from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                    + enter_recommendation_for_user() from generate_recommendations_functions.py

                        + User from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + get_status() from check_and_balance.py

                            + Status from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                        + Status from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + Recommendation_Per_Person from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                + make_recommendation_table() from structure_recommendation_table.py

                    + User from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

                    + Recommendation from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

                    + get_time() from structure_recommendation_table.py

                    + Favorite_Recommendation from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

                    + Removed_Recommendation from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

Page 4: User profile alterations + Recommendation history

    + Run streamlit_app.py file

        + page from st.session_state

        + error from st.session_state

        + error_status from st.session_state

        + insert_data() from mongo_connection.py

            + User from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Recommendation from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Tag from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

        + menu_layout() from menu.py

            + current_passcode from st.session_state

            + open_recommendation from st.session_state

            + error from st.session_state

            + error_status from st.session_state

    + layout_4() from page_4.py

        + current_passcode from st.session_state

        + open_recommendation from st.session_state

        + error from st.session_state

        + error_status from st.session_state

        + initialize_variables() from initialise_variables.py

            + User from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Recommendation from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + get_status() from check_and_balance.py

                + Status from mongo_connection.py

                    + db from mongo_connection.py

                        + client from mongo_connection.py

                            + init_connection() from mongo_connection.py

                                + Database_Connection from st.secrets

            + update_user_layout(user)

            + question_username from initialise_variables.py

            + question_age from initialise_variables.py

            + ages from initialise_variables.py

            + question_gender from initialise_variables.py

            + genders from initialise_variables.py

            + question_focus_area from initialise_variables.py

            + focus_areas from initialise_variables.py

            + question_time_available from initialise_variables.py

            + min_time_limit from initialise_variables.py

            + max_limit from initialise_variables.py

            + question_suggestions from initialise_variables.py

            + min_limit from initialise_variables.py

            + max_recommendation_limit from initialise_variables.py

                + get_maximum_entries() from generate_items.py

                    + Recommendation from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

            + update_user_here() from page_4.py

                + update_user() from user_information.py

                    + User from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

                    + new_entry_in_record_collection() from check_and_balance.py

                        + Record from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                + question_username from initialise_variables.py

                + question_age from initialise_variables.py

                + question_gender from initialise_variables.py

                + question_focus_area from initialise_variables.py

                + question_time_available from initialise_variables.py

                + question_suggestions from initialise_variables.py

                + record_question() from check_and_balance.py

                    + User from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

                    + Status from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

                    + Question from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

                    + get_now() from generate_items.py

                + change_page() from change_page.py

                    + page from st.session_state

                    + error_status from st.session_state

            + make_record() from page_4.py

                + create_recommendation_history() from make_record_recommendations.py

                    + Recommendation_Per_Person from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

                    + Favorite_Recommendation from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

                    + Removed_Recommendation from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

                    + add_collection() from make_record_recommendations.py

                        + create_entry() from make_record_recommendations.py

                            + Recommendation from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                    + sort_by_created_by() from make_record_recommendations.py

Page 5: User record page

    + Run streamlit_app.py file

        + page from st.session_state

        + error from st.session_state

        + error_status from st.session_state

        + insert_data() from mongo_connection.py

            + User from mongo_connection.py

                + db from mongo_connection.py

                     + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Recommendation from mongo_connection.py

                + db from mongo_connection.py

                     + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Tag from mongo_connection.py

                + db from mongo_connection.py

                     + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

        + menu_layout() from menu.py

            + current_passcode from st.session_state

            + open_recommendation from st.session_state

            + error from st.session_state

            + error_status from st.session_state

    + layout_5() from page_5.py

        + current_passcode from st.session_state

        + open_recommendation from st.session_state

        + error from st.session_state

        + error_status from st.session_state

        + initialize_variables() from initialise_variables.py

            + User from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Recommendation from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + get_status() from check_and_balance.py

                + Status from mongo_connection.py

                    + db from mongo_connection.py

                        + client from mongo_connection.py

                            + init_connection() from mongo_connection.py

                                + Database_Connection from st.secrets

        + create_history() from make_record.py

            + User from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Question from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Record from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Status from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Recommendation from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Tag from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Favorite_Recommendation from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Removed_Recommendation from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Recommendation_Per_Person from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Question_Questionnaire from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Score_History from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + add_history_entries() from make_record.py

            + sort_by_time() from make_record.py

            + sort_by_message() from make_record.py

            + sort_by_type() from make_record.py

            + new_entry_in_record_collection() from check_and_balance.py

                + Record from mongo_connection.py

                    + db from mongo_connection.py

                        + client from mongo_connection.py

                            + init_connection() from mongo_connection.py

                                + Database_Connection from st.secrets

        + delete_entry() from make_record.py

            + User from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Question from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Record from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Status from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Recommendation from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Tag from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Favorite_Recommendation from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Removed_Recommendation from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Recommendation_Per_Person from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Question_Questionnaire from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Score_History from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + User from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + new_entry_in_record_collection() from check_and_balance.py

                + Record from mongo_connection.py

                    + db from mongo_connection.py

                        + client from mongo_connection.py

                            + init_connection() from mongo_connection.py

                                + Database_Connection from st.secrets

Page 6: Recommendation page

    + Run streamlit_app.py file

        + page from st.session_state

        + error from st.session_state

        + error_status from st.session_state

        + insert_data() from mongo_connection.py

            + User from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Recommendation from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Tag from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

        + menu_layout() from menu.py

            + current_passcode from st.session_state

            + open_recommendation from st.session_state

            + error from st.session_state

            + error_status from st.session_state

        + layout_6() from page_6.py

            + current_passcode from st.session_state

            + open_recommendation from st.session_state

            + error from st.session_state

            + error_status from st.session_state

            + initialize_variables() from initialise_variables.py

                + User from mongo_connection.py

                    + db from mongo_connection.py

                        + client from mongo_connection.py

                            + init_connection() from mongo_connection.py

                                + Database_Connection from st.secrets

                + Recommendation from mongo_connection.py

                    + db from mongo_connection.py

                        + client from mongo_connection.py

                            + init_connection() from mongo_connection.py

                                + Database_Connection from st.secrets

                + get_status() from check_and_balance.py

                    + Status from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

            + Recommendation_Per_Person from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Removed_Recommendation from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Favorite_Recommendation from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Tag from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + completed_recommendation() from page_6.py

                + error from st.session_state

                    + add_points() from user_information.py

                        + User from mongo_connection.py

                            + db from mongo_connection.py

                                 + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + Recommendation_Per_Person from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + Recommendation_Per_Person from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + new_entry_in_score_history_collection() from check_and_balance.py

                            + User from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                            + Score_History from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                        + new_entry_in_record_collection() from check_and_balance.py

                            + Record from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                + error_status from st.session_state

                    + add_points() from user_information.py

                        + User from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + Recommendation_Per_Person from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + Recommendation from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + new_entry_in_score_history_collection() from check_and_balance.py

                            + User from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                            + Score_History from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                        + new_entry_in_record_collection() from check_and_balance.py

                            + Record from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                    + change_page() from change_page.py

                        + page from st.session_state

                        + error_status from st.session_state

            + change_recommendation_status() from page_6.py

                + error from st.session_state

                    + change_recommendation_preference_for_user from user_information.py

                        + User from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + Recommendation from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + Removed_Recommendation from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + Favorite_Recommendation from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                + error_status from st.session_state

                    change_recommendation_preference_for_user from user_information.py

                        + User from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + Recommendation from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + Removed_Recommendation from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + Favorite_Recommendation from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                + change_page() from change_page.py

                    + page from st.session_state

                    + error_status from st.session_state

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

                            + Database_Connection from st.secrets

            + Recommendation from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Tag from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

        + menu_layout() from menu.py

            + current_passcode from st.session_state

            + open_recommendation from st.session_state

            + error from st.session_state

            + error_status from st.session_state

        + layout_7() from page_7.py

            + current_passcode from st.session_state

            + open_recommendation from st.session_state

            + initialize_variables() from initialise_variables.py

                + User from mongo_connection.py

                    + db from mongo_connection.py

                        + client from mongo_connection.py

                            + init_connection() from mongo_connection.py

                                + Database_Connection from st.secrets

                + Recommendation from mongo_connection.py

                    + db from mongo_connection.py

                        + client from mongo_connection.py

                            + init_connection() from mongo_connection.py

                                + Database_Connection from st.secrets

                + get_status() from check_and_balance.py

                    + Status from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

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

                            + Database_Connection from st.secrets

            + Recommendation from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Tag from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

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

                                + Database_Connection from st.secrets

                + Recommendation from mongo_connection.py

                    + db from mongo_connection.py

                        + client from mongo_connection.py

                            + init_connection() from mongo_connection.py

                                + Database_Connection from st.secrets

                + get_status() from check_and_balance.py

                    + Status from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

            + confession_form_layout() from page_8.py

                + con_question from initialise_variables.py

                + record_question() from check_and_balance.py

                    + User from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

                    + Status from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

                    + Question from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

                    + get_now() from generate_items.py

            + confession_list_layout() from page_8.py

                + delete_entry() from make_record.py

                    + User from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

                    + new_entry_in_record_collection() from check_and_balance.py

                        + Record from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

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

                            + Database_Connection from st.secrets

            + Recommendation from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

            + Tag from mongo_connection.py

                + db from mongo_connection.py

                    + client from mongo_connection.py

                        + init_connection() from mongo_connection.py

                            + Database_Connection from st.secrets

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

                                + Database_Connection from st.secrets

                + Recommendation from mongo_connection.py

                    + db from mongo_connection.py

                         + client from mongo_connection.py

                            + init_connection() from mongo_connection.py

                                + Database_Connection from st.secrets

                + get_status() from check_and_balance.py

                    + Status from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

            + add_a_recommendation_layout() from page_9.py

                + question_about_passcode from initialise_variables.py

                + question_about_recommendation_id from initialise_variables.py

                + question_about_points from initialise_variables.py

                + question_about_title from initialise_variables.py

                + question_about_link from initialise_variables.py

                + max_limit from initialise_variables.py

                + question_about_duration from initialise_variables.py

                + generate_recommendation_id() from generate_items.py

                    + Recommendation from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

                    + Recommendation_Per_Person from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

                    + Tag from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

                    + Favorite_Recommendation from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

                    + Removed_Recommendation from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

                + add_recommendation_here() from page_9.py

                    + error from st.session_state

                        + add_recommendation() from add_data_in_collection.py

                            + User from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                            + Recommendation from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                            + Tag from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                            + Recommendation_Per_Person from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                            + get_now() from generate_items.py

                            + add_tag() from add_data_in_collection.py

                                + User from mongo_connection.py

                                    + db from mongo_connection.py

                                        + client from mongo_connection.py

                                            + init_connection() from mongo_connection.py

                                                + Database_Connection from st.secrets

                                + Recommendation from mongo_connection.py

                                    + db from mongo_connection.py

                                        + client from mongo_connection.py

                                            + init_connection() from mongo_connection.py

                                                + Database_Connection from st.secrets

                                + Tag from mongo_connection.py

                                    + db from mongo_connection.py

                                        + client from mongo_connection.py

                                            + init_connection() from mongo_connection.py

                                                + Database_Connection from st.secrets

                                + get_now() from generate_items.py

                    + error_status from st.session_state

                        + add_recommendation() from add_data_in_collection.py

                            + User from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                            + Recommendation from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                            + Tag from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                            + Recommendation_Per_Person from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                            + get_now() from generate_items.py

                            + add_tag() from add_data_in_collection.py

                                + User from mongo_connection.py

                                    + db from mongo_connection.py

                                        + client from mongo_connection.py

                                            + init_connection() from mongo_connection.py

                                                + Database_Connection from st.secrets

                                + Recommendation from mongo_connection.py

                                    + db from mongo_connection.py

                                        + client from mongo_connection.py

                                            + init_connection() from mongo_connection.py

                                                + Database_Connection from st.secrets

                                + Tag from mongo_connection.py

                                    + db from mongo_connection.py

                                        + client from mongo_connection.py

                                            + init_connection() from mongo_connection.py

                                                + Database_Connection from st.secrets

                                + get_now() from generate_items.py

                    + record_question() from check_and_balance.py

                        + User from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + Status from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + Question from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + get_now() from generate_items.py

                    + change_page() from change_page.py

                        + page from st.session_state

                        + error_status from st.session_state

            + add_tags_layout() from page_9.py

                + question_about_passcode from initialise_variables.py

                + question_about_recommendation_id from initialise_variables.py

                + min_limit from initialise_variables.py

                + stress_max_limit from initialise_variables.py

                + max_limit from initialise_variables.py

                + question_age from initialise_variables.py

                + ages from initialise_variables.py

                + question_focus_area from initialise_variables.py

                + focus_areas from initialise_variables.py

                + question_gender from initialise_variables.py

                + genders from initialise_variables.py

                + error from st.session_state

                + error_status from st.session_state

                + add_tag_here() from page_9.py

                    + error from st.session_state

                        + add_tag() from add_data_in_collection.py

                            + User from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                            + Recommendation from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                            + Tag from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                            + get_now() from generate_items.py

                    + error_status from st.session_state

                        + add_tag() from add_data_in_collection.py

                            + User from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                            + Recommendation from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                            + Tag from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                            + get_now() from generate_items.py

                    + record_question() from check_and_balance.py

                        + User from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + Status from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + Question from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + get_now() from generate_items.py

                    + change_page() from change_page.py

                        + page from st.session_state

                        + error_status from st.session_state

            + add_a_question_layout() from page_9.py

                + question_about_passcode from initialise_variables.py

                + question_input from initialise_variables.py

                + Question_ID from initialise_variables.py

                + generate_question_id() from page_9.py

                    + Question_Questionnaire from mongo_connection.py

                        + db from mongo_connection.py

                            + client from mongo_connection.py

                                + init_connection() from mongo_connection.py

                                    + Database_Connection from st.secrets

                + add_question() from page_9.py

                    + error from st.session_state

                        + add_question_to_Questionnaire() from add_data_in_collection.py

                            + User from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                            + Question_Questionnaire from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                            + get_now() from generate_items.py

                    + error_status from st.session_state

                        + add_question_to_Questionnaire() from add_data_in_collection.py

                            + User from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                            + Question_Questionnaire from mongo_connection.py

                                + db from mongo_connection.py

                                    + client from mongo_connection.py

                                        + init_connection() from mongo_connection.py

                                            + Database_Connection from st.secrets

                            + get_now() from generate_items.py

                    + record_question() from check_and_balance.py

                        + User from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + Status from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + Question from mongo_connection.py

                            + db from mongo_connection.py

                                + client from mongo_connection.py

                                    + init_connection() from mongo_connection.py

                                        + Database_Connection from st.secrets

                        + get_now() from generate_items.py

                    + change_page() from change_page.py

                        + page from st.session_state

                        + error_status from st.session_state